"""room_cfd_numba.py: room_cfd.py with the time step compiled by Numba (test version).

Same model, same inputs and same results as room_cfd.py (to round-off), but each stage of a time
step (viscosity at the corners, momentum, energy, k-epsilon) is one compiled loop over the cells
instead of many NumPy array operations, and the pressure equation uses a faster ordering of the
LU factorisation. Needs the numba package (pip install numba). The first run
compiles the loops, which takes some seconds; the compiled code is cached in __pycache__.

room_cfd.py: a small 2D CFD model of a room section for teaching.

Solves the incompressible Navier-Stokes equations with the Boussinesq approximation
for buoyancy and an energy equation for temperature, on a uniform staggered (MAC) grid.
Time stepping is explicit (Chorin projection). It is for showing trends (high vs low opening,
cold vs warm supply, flow rate), not for design values.

Advection scheme (Case.advection), for momentum and temperature:
  "upwind" : first order. Robust, but adds numerical diffusion of about |u|*dx/2, which in a
             jet is larger than the eddy viscosity itself.
  "tvd"    : second-order upwind with the van Leer limiter (a TVD scheme). Same as upwind where
             the field has a peak or a step (no wiggles), second order where it is smooth.

Turbulence (eddy viscosity nu_t, turbulent Prandtl number 0.85), three options:
  "constant"  : one nu_t everywhere (Case.nu_t)
  "chen-xu"   : zero-equation indoor model nu_t = 0.03874 * V * l, with V the local mean
                speed and l the distance to the nearest wall
                (Chen, Q. & Xu, W. 1998, Energy and Buildings 28(2), 137-144)
  "k-epsilon" : standard k-epsilon model (Launder & Spalding 1974), nu_t = 0.09 k^2/eps,
                with log-law wall functions, buoyancy production of k, and inlet turbulence
                k = 1.5 (Tu_in U)^2, eps = k^1.5 / (0.1 h_inlet) as in the IEA Annex 20 test case

Boundary conditions
  walls   : no slip, adiabatic
  inlet   : velocity inlet, uniform normal speed U = q / (h_open * W_room), temperature T_in
  outlet  : pressure outlet, p = 0, zero-gradient velocity and temperature
Heat sources
  volumetric blocks (people, equipment): W per metre of room width spread over a rectangle
  floor heat flux patches (sun patch): W per metre of room width spread over a floor strip

Contact: Christian Hviid, cahv@dtu.dk

Disclaimer: use at own risk. This is a simplified 2D teaching model for comparing cases and seeing the
physics. It has been validated only against the isothermal IEA Annex 20 two-dimensional test room
(Nielsen 1990). It does not give design values, and it is provided as is, without warranty of any kind.

2D caveat: the section represents a room that is W_room wide with openings spanning the
full width. A 2D (line) jet decays as 1/sqrt(x), slower than a 3D jet (1/x), so speeds far
from the opening are overestimated compared with a real window.
"""
from dataclasses import dataclass, field
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import splu
from numba import njit

RHO, CP, G = 1.2, 1005.0, 9.81
NU_AIR = 1.5e-5                 # molecular kinematic viscosity (m²/s)
WALL, INLET, OUTLET = 0, 1, 2


@dataclass
class Opening:
    side: str            # "left", "right" or "top"
    start: float         # m, along the wall (height for side walls, x for the ceiling)
    end: float


@dataclass
class HeatBlock:
    x0: float; x1: float; y0: float; y1: float
    power: float         # W per metre of room width


@dataclass
class FloorFlux:
    x0: float; x1: float
    power: float         # W per metre of room width


@dataclass
class Case:
    L: float = 5.0              # room depth (m), x direction
    H: float = 2.5              # room height (m)
    W: float = 4.0              # room width (m), only used to turn q and Q into per-metre values
    nx: int = 100
    ny: int = 50
    ach: float = 6.0            # air changes per hour
    T_in: float = 18.0          # supply temperature (°C)
    T_room0: float = None       # initial room temperature (°C); None = well-mixed steady value
    inlet: Opening = field(default_factory=lambda: Opening("left", 0.10, 0.30))
    outlet: Opening = field(default_factory=lambda: Opening("right", 2.20, 2.40))
    heat: list = field(default_factory=list)
    floor_flux: list = field(default_factory=list)
    turbulence: str = "k-epsilon"  # "k-epsilon" (default), "chen-xu" or "constant"
    Tu_in: float = 0.04         # inlet turbulence intensity, used by "k-epsilon"
    nu_t: float = 2e-3          # eddy viscosity (m²/s) for "constant", about 130 x molecular
    Pr_t: float = 0.85
    advection: str = "tvd"      # "tvd" (van Leer, default) or "upwind"
    t_end: float = 900.0        # simulated time (s)
    t_avg: float = 300.0        # averaging window at the end (s)

    @property
    def q(self):                # m³/s for the whole room
        return self.ach * self.L * self.H * self.W / 3600.0


def _mask(case, side, opening, kind, n, h):
    """Boundary type per face along one wall."""
    m = np.full(n, WALL)
    if opening.side == side:
        s = (np.arange(n) + 0.5) * h
        m[(s > opening.start) & (s < opening.end)] = kind
    return m


def _lim(a, b):
    """van Leer limiter in product form, psi(a/b)*b: harmonic mean of two slopes, 0 if they differ in sign."""
    return (a * np.abs(b) + np.abs(a) * b) / (np.abs(a) + np.abs(b) + 1e-30)


def _ddx(P, vel, h, tvd):
    """Upwind-biased derivative along axis 0 at P[2:-2] (P has two ghost values each side).
    Written as the difference of two face values; tvd=False gives first-order upwind."""
    D = np.diff(P, axis=0)                                  # D[k] = P[k+1] - P[k]
    Lm = _lim(D[:-1], D[1:]) if tvd else np.zeros_like(D[1:])   # Lm[k-1] = lim(D[k-1], D[k])
    pos = D[1:-2] + 0.5 * Lm[1:-1] - 0.5 * Lm[:-2]          # face values from the left
    neg = D[2:-1] - 0.5 * Lm[2:] + 0.5 * Lm[1:-1]             # face values from the right
    return np.where(vel > 0, pos, neg) / h


def _faces(E, vel, tvd):
    """Upwind face values between E[1:-2] and E[2:-1] (E has two ghost values each side)."""
    if not tvd:
        return np.where(vel > 0, E[1:-2], E[2:-1])
    D = np.diff(E, axis=0)
    Lm = _lim(D[:-1], D[1:])                                # Lm[k-1] = lim(D[k-1], D[k])
    return np.where(vel > 0, E[1:-2] + 0.5 * Lm[:-1], E[2:-1] - 0.5 * Lm[1:])


# ---------------------------------------------------------------------------------------------
# Numba kernels: the same formulas as the NumPy expressions in room_cfd.py, written as loops over
# the cells so that each stage of a time step is one compiled call. The operations are done in
# the same order as in room_cfd.py, so the results agree to round-off.
# ---------------------------------------------------------------------------------------------
@njit(cache=True)
def _nlim(a, b):
    return (a * abs(b) + abs(a) * b) / (abs(a) + abs(b) + 1e-30)


@njit(cache=True)
def _nddx(pm2, pm1, p0, pp1, pp2, vel, h, tvd):
    """One value of _ddx: upwind-biased derivative at p0 from its four neighbours."""
    d0, d1, d2, d3 = pm1 - pm2, p0 - pm1, pp1 - p0, pp2 - pp1
    if tvd:
        l0, l1, l2 = _nlim(d0, d1), _nlim(d1, d2), _nlim(d2, d3)
    else:
        l0 = l1 = l2 = 0.0
    if vel > 0:
        return (d1 + 0.5 * l1 - 0.5 * l0) / h
    return (d2 - 0.5 * l2 + 0.5 * l1) / h


@njit(cache=True)
def _nface(em1, e0, e1, e2, vel, tvd):
    """One value of _faces: upwind face value between e0 and e1."""
    if not tvd:
        return e0 if vel > 0 else e1
    if vel > 0:
        return e0 + 0.5 * _nlim(e0 - em1, e1 - e0)
    return e1 - 0.5 * _nlim(e1 - e0, e2 - e1)


@njit(cache=True)
def _nu_wall1(kw, y, cmu25):
    ys = cmu25 * np.sqrt(kw) * y / NU_AIR
    if ys > 11.2:
        return 0.41 * ys * NU_AIR / np.log(9.0 * max(ys, 1.0))
    return NU_AIR


@njit(cache=True)
def _k_corner_viscosity(nu_c, k, ke, cT, cL, cR, dx, dy, cmu25):
    """Eddy viscosity at the cell corners (average of four cells), with log-law wall values for k-epsilon."""
    nx, ny = nu_c.shape
    nu_k = np.empty((nx + 1, ny + 1))
    for i in range(nx + 1):
        a0, a1 = max(i - 1, 0), min(i, nx - 1)
        for j in range(ny + 1):
            b0, b1 = max(j - 1, 0), min(j, ny - 1)
            nu_k[i, j] = 0.25 * (nu_c[a0, b0] + nu_c[a1, b0] + nu_c[a0, b1] + nu_c[a1, b1])
    if ke:
        kk = lambda i, j: 0.25 * (k[max(i - 1, 0), max(j - 1, 0)] + k[min(i, nx - 1), max(j - 1, 0)]
                                  + k[max(i - 1, 0), min(j, ny - 1)] + k[min(i, nx - 1), min(j, ny - 1)])
        for i in range(nx + 1):
            nu_k[i, 0] = _nu_wall1(kk(i, 0), dy / 2, cmu25)
            if cT[i]:
                nu_k[i, ny] = _nu_wall1(kk(i, ny), dy / 2, cmu25)
        for j in range(ny + 1):
            if cL[j]:
                nu_k[0, j] = _nu_wall1(kk(0, j), dx / 2, cmu25)
            if cR[j]:
                nu_k[nx, j] = _nu_wall1(kk(nx, j), dx / 2, cmu25)
    return nu_k


@njit(cache=True)
def _k_momentum(u, v, T, nu_c, nu_k, dx, dy, dt, tvd, gb, Tref):
    """Predictor step: advection (upwind or TVD), viscous terms and buoyancy, explicit in time."""
    nx, ny = T.shape
    us, vs = u.copy(), v.copy()

    def UG(i, g):                                   # u with mirrored ghost rows below the floor and above the ceiling
        if g == 0:
            return -u[i, 0]
        if g == ny + 1:
            return -u[i, ny - 1]
        return u[i, g - 1]

    def VG(g, j):                                   # v with mirrored ghost columns outside the side walls
        if g == 0:
            return -v[0, j]
        if g == nx + 1:
            return -v[nx - 1, j]
        return v[g - 1, j]

    for i in range(1, nx):
        for j in range(ny):
            uc = u[i, j]
            vavg = 0.25 * (v[i - 1, j] + v[i, j] + v[i - 1, j + 1] + v[i, j + 1])
            dudx = _nddx(u[max(i - 2, 0), j], u[i - 1, j], uc, u[i + 1, j], u[min(i + 2, nx), j], uc, dx, tvd)
            g = j + 1
            dudy = _nddx(UG(i, max(g - 2, 0)), UG(i, g - 1), UG(i, g), UG(i, g + 1), UG(i, min(g + 2, ny + 1)),
                         vavg, dy, tvd)
            tx1 = nu_c[i, j] * (u[i + 1, j] - u[i, j]) / dx
            tx0 = nu_c[i - 1, j] * (u[i, j] - u[i - 1, j]) / dx
            ty1 = nu_k[i, j + 1] * (UG(i, j + 2) - UG(i, j + 1)) / dy
            ty0 = nu_k[i, j] * (UG(i, j + 1) - UG(i, j)) / dy
            visu = (tx1 - tx0) / dx + (ty1 - ty0) / dy
            us[i, j] = uc + dt * (-uc * dudx - vavg * dudy + visu)

    for i in range(nx):
        for j in range(1, ny):
            vc = v[i, j]
            uavg = 0.25 * (u[i, j - 1] + u[i + 1, j - 1] + u[i, j] + u[i + 1, j])
            dvdy = _nddx(v[i, max(j - 2, 0)], v[i, j - 1], vc, v[i, j + 1], v[i, min(j + 2, ny)], vc, dy, tvd)
            g = i + 1
            dvdx = _nddx(VG(max(g - 2, 0), j), VG(g - 1, j), VG(g, j), VG(g + 1, j), VG(min(g + 2, nx + 1), j),
                         uavg, dx, tvd)
            sy1 = nu_c[i, j] * (v[i, j + 1] - v[i, j]) / dy
            sy0 = nu_c[i, j - 1] * (v[i, j] - v[i, j - 1]) / dy
            sx1 = nu_k[i + 1, j] * (VG(i + 2, j) - VG(i + 1, j)) / dx
            sx0 = nu_k[i, j] * (VG(i + 1, j) - VG(i, j)) / dx
            visv = (sy1 - sy0) / dy + (sx1 - sx0) / dx
            buoy = gb * (0.5 * (T[i, j - 1] + T[i, j]) - Tref)
            vs[i, j] = vc + dt * (-uavg * dvdx - vc * dvdy + visv + buoy)
    return us, vs


@njit(cache=True)
def _k_fluxes(phi, u, v, inL, inR, phi_in, D, dx, dy, tvd):
    """Face fluxes of a cell-centred scalar: advection (upwind or TVD) plus diffusion with coefficient D.
    Inlet faces carry phi_in, outlet faces zero gradient, walls zero flux (bottom faces set to 0)."""
    nx, ny = phi.shape
    Fx = np.empty((nx + 1, ny)); Fy = np.empty((nx, ny + 1))

    def EX(e, j):                                   # phi along x with two ghost cells at each end
        if e < 2:
            return phi_in if inL[j] else phi[0, j]
        if e > nx + 1:
            return phi_in if inR[j] else phi[nx - 1, j]
        return phi[e - 2, j]

    def EY(i, e):
        return phi[i, min(max(e - 2, 0), ny - 1)]

    for f in range(nx + 1):
        for j in range(ny):
            Fx[f, j] = u[f, j] * _nface(EX(f, j), EX(f + 1, j), EX(f + 2, j), EX(f + 3, j), u[f, j], tvd)
            if 0 < f < nx:
                Fx[f, j] = Fx[f, j] - 0.5 * (D[f, j] + D[f - 1, j]) * (phi[f, j] - phi[f - 1, j]) / dx
    for i in range(nx):
        Fy[i, 0] = 0.0
        for f in range(1, ny + 1):
            Fy[i, f] = v[i, f] * _nface(EY(i, f), EY(i, f + 1), EY(i, f + 2), EY(i, f + 3), v[i, f], tvd)
            if f < ny:
                Fy[i, f] = Fy[i, f] - 0.5 * (D[i, f] + D[i, f - 1]) * (phi[i, f] - phi[i, f - 1]) / dy
    return Fx, Fy


@njit(cache=True)
def _k_divergence(Fx, Fy, dx, dy):
    nx, ny = Fy.shape[0], Fx.shape[1]
    r = np.empty((nx, ny))
    for i in range(nx):
        for j in range(ny):
            r[i, j] = -((Fx[i + 1, j] - Fx[i, j]) / dx + (Fy[i, j + 1] - Fy[i, j]) / dy)
    return r


@njit(cache=True)
def _k_kepsilon(k, eps, u, v, T_old, nu_c, wall_cell, yp, inL, inR, k_in, e_in, dx, dy, dt, gneg, Pr_t, consts):
    """k and epsilon update: production by shear and buoyancy, upwind transport, implicit sinks."""
    CMU, C1, C2, SK, SE, KAP, cmu25, cmu75 = consts
    nx, ny = k.shape
    nut = np.empty((nx, ny)); Dk = np.empty((nx, ny)); De = np.empty((nx, ny))
    for i in range(nx):
        for j in range(ny):
            nut[i, j] = nu_c[i, j] - NU_AIR
            Dk[i, j] = NU_AIR + nut[i, j] / SK
            De[i, j] = NU_AIR + nut[i, j] / SE
    Fx, Fy = _k_fluxes(k, u, v, inL, inR, k_in, Dk, dx, dy, False)
    rk = _k_divergence(Fx, Fy, dx, dy)
    Fx, Fy = _k_fluxes(eps, u, v, inL, inR, e_in, De, dx, dy, False)
    re = _k_divergence(Fx, Fy, dx, dy)

    def UG(i, g):
        if g == 0:
            return -u[i, 0]
        if g == ny + 1:
            return -u[i, ny - 1]
        return u[i, g - 1]

    def VG(g, j):
        if g == 0:
            return -v[0, j]
        if g == nx + 1:
            return -v[nx - 1, j]
        return v[g - 1, j]

    sh = np.empty((nx + 1, ny + 1))                 # shear du/dy + dv/dx at the corners
    for i in range(nx + 1):
        for j in range(ny + 1):
            sh[i, j] = (UG(i, j + 1) - UG(i, j)) / dy + (VG(i + 1, j) - VG(i, j)) / dx
    kn = np.empty((nx, ny)); en = np.empty((nx, ny))
    for i in range(nx):
        for j in range(ny):
            kc, ec = k[i, j], eps[i, j]
            shc = 0.25 * (sh[i, j] + sh[i + 1, j] + sh[i, j + 1] + sh[i + 1, j + 1])
            ex = (u[i + 1, j] - u[i, j]) / dx; ey = (v[i, j + 1] - v[i, j]) / dy
            P = nut[i, j] * (2 * (ex * ex + ey * ey) + shc * shc)
            ypw = yp[i, j] if wall_cell[i, j] else 1.0
            if wall_cell[i, j]:
                Up = np.hypot(0.5 * (u[i + 1, j] + u[i, j]), 0.5 * (v[i, j + 1] + v[i, j]))
                tau = _nu_wall1(kc, ypw, cmu25) * Up / ypw
                P = tau * cmu25 * np.sqrt(kc) / (KAP * ypw)
            if j == 0:
                dT = (T_old[i, 1] - T_old[i, 0]) / dy
            elif j == ny - 1:
                dT = (T_old[i, ny - 1] - T_old[i, ny - 2]) / dy
            else:
                dT = (T_old[i, j + 1] - T_old[i, j - 1]) / (2.0 * dy)
            Gb = gneg * nut[i, j] / Pr_t * dT
            Gp, Gm = max(Gb, 0.0), max(-Gb, 0.0)
            k_new = (kc + dt * (rk[i, j] + P + Gp)) / (1 + dt * (ec + Gm) / kc)
            e_new = (ec + dt * (re[i, j] + C1 * ec / kc * (P + Gp))) / (1 + dt * C2 * ec / kc)
            kn[i, j] = max(k_new, 1e-10)
            en[i, j] = max(e_new, 1e-12)
            if wall_cell[i, j]:
                en[i, j] = cmu75 * kn[i, j] ** 1.5 / (KAP * ypw)
    return kn, en


@njit(cache=True)
def _k_bc_rhs(us, vs, bL, bR, bT, U_in, dx, dy, dt):
    """Boundary values of the predicted velocities, then the right-hand side div(u*)/dt of the pressure equation."""
    nx, ny = vs.shape[0], us.shape[1]
    for j in range(ny):
        us[0, j] = U_in if bL[j] == INLET else (us[1, j] if bL[j] == OUTLET else 0.0)
        us[nx, j] = -U_in if bR[j] == INLET else (us[nx - 1, j] if bR[j] == OUTLET else 0.0)
    for i in range(nx):
        vs[i, 0] = 0.0
        vs[i, ny] = vs[i, ny - 1] if bT[i] == OUTLET else 0.0
    rhs = np.empty(nx * ny)
    for i in range(nx):
        for j in range(ny):
            rhs[i * ny + j] = ((us[i + 1, j] - us[i, j]) / dx + (vs[i, j + 1] - vs[i, j]) / dy) / dt
    return rhs


@njit(cache=True)
def _k_correct(us, vs, p, bL, bR, bT, dx, dy, dt):
    """Subtract the pressure gradient so that the velocity field is divergence free (p = 0 outside outlets)."""
    nx, ny = p.shape
    for i in range(1, nx):
        for j in range(ny):
            us[i, j] -= dt * (p[i, j] - p[i - 1, j]) / dx
    for i in range(nx):
        for j in range(1, ny):
            vs[i, j] -= dt * (p[i, j] - p[i, j - 1]) / dy
    for j in range(ny):
        if bL[j] == OUTLET:
            us[0, j] -= dt * (p[0, j] - 0.0) / (dx / 2)
        if bR[j] == OUTLET:
            us[nx, j] -= dt * (0.0 - p[nx - 1, j]) / (dx / 2)
    for i in range(nx):
        if bT[i] == OUTLET:
            vs[i, ny] -= dt * (0.0 - p[i, ny - 1]) / (dy / 2)


@njit(cache=True)
def _k_average(ua, va, Ta, nua, spa, u, v, T, nu_c, dt):
    """Add dt times the current fields to the time sums."""
    nx, ny = T.shape
    ua += dt * u; va += dt * v
    for i in range(nx):
        for j in range(ny):
            Ta[i, j] += dt * T[i, j]
            nua[i, j] += dt * nu_c[i, j]
            spa[i, j] += dt * np.hypot(0.5 * (u[i + 1, j] + u[i, j]), 0.5 * (v[i, j + 1] + v[i, j]))


def run(case: Case, verbose=False, live=False, monitor_every=50, live_every=20):
    """Run the case and return time-averaged fields.

    Convergence history is recorded every monitor_every steps in res["history"]:
      du, dv, dT  rate of change, RMS of (new - old)/dt  (the transient "residuals")
      div         continuity residual after projection, max |div u| (1/s)
      imb         energy imbalance through the openings vs the gains (%), 0 at steady state
      v_floor     monitor point: speed at x = 1.0 m, 0.1 m above the floor (m/s)
      T_exh       monitor point: mean exhaust temperature (°C)
    live=True draws them in a window while the run goes on (needs an interactive matplotlib
    backend, e.g. when run from Spyder or a terminal); see plots.convergence for the saved figure."""
    nx, ny, L, H = case.nx, case.ny, case.L, case.H
    dx, dy = L / nx, H / ny

    # boundary types per face
    bL = np.maximum(_mask(case, "left", case.inlet, INLET, ny, dy), _mask(case, "left", case.outlet, OUTLET, ny, dy))
    bR = np.maximum(_mask(case, "right", case.inlet, INLET, ny, dy), _mask(case, "right", case.outlet, OUTLET, ny, dy))
    bT = _mask(case, "top", case.outlet, OUTLET, nx, dx)
    h_in = (bL == INLET).sum() * dy + (bR == INLET).sum() * dy
    U_in = case.q / case.W / h_in                     # m/s normal to the opening
    sgn_in = 1.0 if case.inlet.side == "left" else -1.0

    # fields
    u = np.zeros((nx + 1, ny)); v = np.zeros((nx, ny + 1))
    Q_tot = sum(b.power for b in case.heat) + sum(f.power for f in case.floor_flux)
    T_mix = case.T_in + Q_tot / (RHO * CP * case.q / case.W)          # steady well-mixed temperature
    T0 = T_mix if case.T_room0 is None else case.T_room0
    T = np.full((nx, ny), float(T0)); Tref = float(T0)
    beta = 1.0 / (273.15 + Tref)

    # heat sources (W/m³ per cell, per metre of width) and floor fluxes (W/m² per bottom face)
    xc = (np.arange(nx) + 0.5) * dx; yc = (np.arange(ny) + 0.5) * dy
    Xc, Yc = np.meshgrid(xc, yc, indexing="ij")
    lwall = np.minimum.reduce([Xc, L - Xc, Yc, H - Yc])              # distance to nearest wall

    def eddy_viscosity(u, v):
        if case.turbulence == "constant":
            return np.full((nx, ny), NU_AIR + case.nu_t)
        V = np.hypot(0.5 * (u[1:] + u[:-1]), 0.5 * (v[:, 1:] + v[:, :-1]))
        return NU_AIR + 0.03874 * V * lwall
    # k-epsilon: constants, inlet values, wall-adjacent cells and their wall distance
    ke = case.turbulence == "k-epsilon"
    CMU, C1, C2, SK, SE, KAP, EWF = 0.09, 1.44, 1.92, 1.0, 1.3, 0.41, 9.0
    k_in = 1.5 * (case.Tu_in * U_in) ** 2
    e_in = k_in ** 1.5 / (0.1 * h_in)
    k = np.full((nx, ny), k_in); eps = np.full((nx, ny), e_in)
    wy = np.zeros((nx, ny), bool); wy[:, 0] = True; wy[:, -1] = bT == WALL
    wx = np.zeros((nx, ny), bool); wx[0, :] = bL == WALL; wx[-1, :] = bR == WALL
    wall_cell = wx | wy
    yp = np.where(wy, dy / 2, np.inf); yp = np.where(wx, np.minimum(yp, dx / 2), yp)
    walls_k = lambda b: (np.r_[b[0], b] == WALL) & (np.r_[b, b[-1]] == WALL)   # wall at each corner point
    cT, cL, cR = walls_k(bT), walls_k(bL), walls_k(bR)

    def nu_wall(kw, y):
        """Effective viscosity tau_w * y / U_p from the log law (laminar below y* = 11.2)."""
        ys = CMU ** 0.25 * np.sqrt(kw) * y / NU_AIR
        return np.where(ys > 11.2, KAP * ys * NU_AIR / np.log(EWF * np.maximum(ys, 1.0)), NU_AIR)

    def transport(phi, phi_in, D):
        """Upwind advection + diffusion of a cell-centred scalar (zero flux at walls, zero gradient at outlets)."""
        eL = np.where(bL == INLET, phi_in, phi[0]); eR = np.where(bR == INLET, phi_in, phi[-1])
        Fx = u * _faces(np.vstack([eL, eL, phi, eR, eR]), u, False)
        Fy = v * _faces(np.hstack([phi[:, :1], phi[:, :1], phi, phi[:, -1:], phi[:, -1:]]).T, v.T, False).T
        Fy[:, 0] = 0.0
        Fx[1:-1] -= 0.5 * (D[1:] + D[:-1]) * (phi[1:] - phi[:-1]) / dx
        Fy[:, 1:-1] -= 0.5 * (D[:, 1:] + D[:, :-1]) * (phi[:, 1:] - phi[:, :-1]) / dy
        return -((Fx[1:] - Fx[:-1]) / dx + (Fy[:, 1:] - Fy[:, :-1]) / dy)

    S = np.zeros((nx, ny))
    for b in case.heat:
        cells = np.outer((xc > b.x0) & (xc < b.x1), (yc > b.y0) & (yc < b.y1))
        S[cells] += b.power / (cells.sum() * dx * dy)
    qfloor = np.zeros(nx)
    for f in case.floor_flux:
        sel = (xc > f.x0) & (xc < f.x1)
        qfloor[sel] += f.power / (sel.sum() * dx)

    # pressure Poisson matrix: Neumann at walls and inlet, Dirichlet p = 0 at outlet faces
    N = nx * ny; idx = lambda i, j: i * ny + j
    rows, cols, vals = [], [], []
    for i in range(nx):
        for j in range(ny):
            kc = idx(i, j); diag = 0.0
            for di, dj, h2, bnd in ((-1, 0, dx * dx, bL[j] if i == 0 else None), (1, 0, dx * dx, bR[j] if i == nx - 1 else None),
                                    (0, -1, dy * dy, WALL if j == 0 else None), (0, 1, dy * dy, bT[i] if j == ny - 1 else None)):
                if bnd is None:
                    rows.append(kc); cols.append(idx(i + di, j + dj)); vals.append(1.0 / h2); diag -= 1.0 / h2
                elif bnd == OUTLET:
                    diag -= 2.0 / h2
            rows.append(kc); cols.append(kc); vals.append(diag)
    # LU factorisation once; the minimum-degree ordering for symmetric matrices makes each solve
    # about twice as fast as the default ordering used by room_cfd.py
    solve = splu(sp.csc_matrix((vals, (rows, cols)), shape=(N, N)), permc_spec="MMD_AT_PLUS_A").solve

    def apply_bc(u, v):
        u[0, :] = np.where(bL == INLET, U_in, np.where(bL == OUTLET, u[1, :], 0.0))
        u[nx, :] = np.where(bR == INLET, -U_in, np.where(bR == OUTLET, u[nx - 1, :], 0.0))
        v[:, 0] = 0.0
        v[:, ny] = np.where(bT == OUTLET, v[:, ny - 1], 0.0)

    apply_bc(u, v)
    ua = np.zeros_like(u); va = np.zeros_like(v); Ta = np.zeros_like(T); spa = np.zeros_like(T)
    nua = np.zeros_like(T); wa = 0.0
    t, n, t_avg0, h = 0.0, 0, case.t_end - case.t_avg, min(dx, dy)
    tvd = case.advection == "tvd"
    cfl = 0.25 if tvd else 0.4

    hist = {k: [] for k in ("t", "du", "dv", "dT", "div", "imb", "v_floor", "T_exh")}
    i_mon, j_mon = min(int(1.0 / dx), nx - 1), min(int(0.1 / dy), ny - 1)
    outR, outL, outT = bR == OUTLET, bL == OUTLET, bT == OUTLET
    inL, inR = bL == INLET, bR == INLET
    view = None
    if live:
        import matplotlib.pyplot as plt
        plt.ion(); view = plt.subplots(2, 2, figsize=(10, 6))

    while t < case.t_end:
        mon = n % monitor_every == 0
        if mon:
            u0, v0, T0 = u.copy(), v.copy(), T.copy()
        nu_c = NU_AIR + CMU * k * k / eps if ke else eddy_viscosity(u, v)   # cell centres
        nu_k = _k_corner_viscosity(nu_c, k, ke, cT, cL, cR, dx, dy, CMU ** 0.25)   # cell corners, wall functions
        alpha_c = nu_c / case.Pr_t
        umax = max(np.abs(u).max(), np.abs(v).max(), U_in, 0.05)
        dt = min(cfl * h / umax, 0.2 * h * h / nu_c.max(), 0.5)

        # ---- momentum (u and v faces), viscous term in conservative form, buoyancy ----
        us, vs = _k_momentum(u, v, T, nu_c, nu_k, dx, dy, dt, tvd, G * beta, Tref)

        # ---- projection ----
        p = solve(_k_bc_rhs(us, vs, bL, bR, bT, U_in, dx, dy, dt)).reshape(nx, ny)
        _k_correct(us, vs, p, bL, bR, bT, dx, dy, dt)
        u, v = us, vs
        if mon:
            div_max = np.abs((u[1:] - u[:-1]) / dx + (v[:, 1:] - v[:, :-1]) / dy).max()

        # ---- energy (finite volume, upwind or TVD face values) ----
        Fx, Fy = _k_fluxes(T, u, v, inL, inR, case.T_in, alpha_c, dx, dy, tvd)
        Fy[:, 0] -= qfloor / (RHO * CP)                                   # floor heat flux enters through bottom faces
        T_old = T
        T = T + dt * _k_divergence(Fx, Fy, dx, dy) + dt * S / (RHO * CP)

        # ---- k and epsilon (sink terms implicit, so k and eps stay positive) ----
        if ke:
            k, eps = _k_kepsilon(k, eps, u, v, T_old, nu_c, wall_cell, yp, inL, inR, k_in, e_in, dx, dy, dt,
                                 -G * beta, case.Pr_t, (CMU, C1, C2, SK, SE, KAP, CMU ** 0.25, CMU ** 0.75))

        if mon:
            rms = lambda a: float(np.sqrt(np.mean(a * a)))
            q_open = (Fx[-1].sum() - Fx[0].sum()) * dy + Fy[:, -1].sum() * dx       # K m²/s per metre width
            T_exh = np.concatenate([T[-1, outR], T[0, outL], T[outT, -1]]).mean()
            for key, val in (("t", t + dt), ("du", rms(u - u0) / dt), ("dv", rms(v - v0) / dt), ("dT", rms(T - T0) / dt),
                           ("div", div_max), ("imb", 100 * (RHO * CP * q_open - Q_tot) / max(Q_tot, 1.0)),
                           ("v_floor", float(np.hypot(0.5 * (u[i_mon, j_mon] + u[i_mon + 1, j_mon]),
                                                      0.5 * (v[i_mon, j_mon] + v[i_mon, j_mon + 1])))),
                           ("T_exh", float(T_exh))):
                hist[key].append(val)
            if view is not None and len(hist["t"]) % live_every == 0:
                draw_convergence(hist, case, *view)
                view[0].canvas.flush_events(); plt.pause(0.001)
        t += dt; n += 1
        if t >= t_avg0:                                               # time average, weighted by dt
            _k_average(ua, va, Ta, nua, spa, u, v, T, nu_c, dt); wa += dt
        if verbose and n % 2000 == 0:
            print(f"t = {t:6.0f} s  dt = {dt:.3f}  max|u| = {np.abs(u).max():.2f}  max nu_t = {nu_c.max():.4f}  T mean = {T.mean():.2f}")

    ua /= wa; va /= wa; Ta /= wa; spa /= wa; nua /= wa
    # energy check: outflow enthalpy vs inflow + sources
    q_out = (ua[nx, bR == OUTLET].sum() - ua[0, bL == OUTLET].sum()) * dy + va[bT == OUTLET, ny].sum() * dx
    T_out = (np.concatenate([Ta[-1, bR == OUTLET], Ta[0, bL == OUTLET], Ta[bT == OUTLET, -1]])).mean()
    return dict(case=case, x=xc, y=yc, dx=dx, dy=dy, u=ua, v=va, T=Ta, speed=spa, nu_t=nua, U_in=U_in, h_in=h_in, steps=n,
                q_in=case.q / case.W, q_out=q_out, T_out=T_out,
                T_out_expected=T_mix, history={k: np.array(a) for k, a in hist.items()})


def draw_convergence(hist, case, fig, ax):
    """Four-panel convergence monitor (used live by run() and by plots.convergence)."""
    t = np.asarray(hist["t"]) / 60
    for a in ax.flat: a.clear(); a.grid(alpha=0.25); a.spines[["top", "right"]].set_visible(False)
    for k, lab, c in (("du", "u", "#2a78d6"), ("dv", "v", "#1b9e77"), ("dT", "T", "#eb6834")):
        ax[0, 0].semilogy(t, hist[k], color=c, lw=1.2, label=lab)
    ax[0, 0].set_title("Rate of change, RMS of (new − old)/Δt", fontsize=9); ax[0, 0].legend(frameon=False, fontsize=8)
    ax[0, 1].semilogy(t, np.maximum(hist["div"], 1e-16), color="0.3", lw=1.2)
    ax[0, 1].set_title("Continuity residual, max |∇·u| (1/s)", fontsize=9)
    ax[1, 0].plot(t, hist["imb"], color="#7a1f4f", lw=1.2); ax[1, 0].axhline(0, color="k", lw=0.6)
    ax[1, 0].set_title("Energy imbalance, openings vs gains (%)", fontsize=9)
    ax[1, 0].set_ylim(-50, 50)
    a2 = ax[1, 1]; a2.plot(t, hist["v_floor"], color="#2a78d6", lw=1.2)
    a2.set_title("Monitor points", fontsize=9); a2.set_ylabel("Floor speed at x = 1 m (m/s)", color="#2a78d6", fontsize=8)
    if not hasattr(a2, "_twin"): a2._twin = a2.twinx()
    tw = a2._twin; tw.clear(); tw.yaxis.tick_right(); tw.yaxis.set_label_position("right")
    tw.plot(t, hist["T_exh"], color="#eb6834", lw=1.2)
    tw.set_ylabel("Exhaust temperature (°C)", color="#eb6834", fontsize=8)
    t0 = (case.t_end - case.t_avg) / 60
    for a in ax.flat: a.axvspan(t0, case.t_end / 60, color="0.9", zorder=0)
    for a in ax[1]: a.set_xlabel("Simulated time (min)  (grey: averaging window)")
    fig.tight_layout()


def draught_rate(ta, v, tu=40.0):
    """ISO 7730 draught rate (%), Fanger et al. (1988). Derived for the neck, so it is
    conservative at the ankles. No feet factor is applied (see ankle_draft_ppd)."""
    v = np.maximum(v, 0.05)
    return np.clip((34 - ta) * (v - 0.05) ** 0.62 * (0.37 * v * tu + 3.14), 0, 100)


def pmv(ta, v, tr=None, rh=50.0, met=1.2, clo=0.5, wme=0.0):
    """ISO 7730 PMV (scalar inputs). tr = ta if not given. Defaults: seated office, summer clothing."""
    tr = ta if tr is None else tr
    pa = rh * 10 * np.exp(16.6536 - 4030.183 / (ta + 235))
    icl, m, w = 0.155 * clo, met * 58.15, wme * 58.15
    mw = m - w
    fcl = 1.0 + 1.29 * icl if icl <= 0.078 else 1.05 + 0.645 * icl
    hcf = 12.1 * np.sqrt(v)
    taa, tra = ta + 273.0, tr + 273.0
    tcla = taa + (35.5 - ta) / (3.5 * icl + 0.1)
    p1 = icl * fcl; p2 = p1 * 3.96; p3 = p1 * 100; p4 = p1 * taa
    p5 = 308.7 - 0.028 * mw + p2 * (tra / 100) ** 4
    xn, xf = tcla / 100, tcla / 50
    for _ in range(150):
        if abs(xn - xf) < 1.5e-5: break
        xf = (xf + xn) / 2
        hcn = 2.38 * abs(100 * xf - taa) ** 0.25
        hc = max(hcf, hcn)
        xn = (p5 + p4 * hc - p2 * xf ** 4) / (100 + p3 * hc)
    tcl = 100 * xn - 273
    hl = (3.05e-3 * (5733 - 6.99 * mw - pa) + (0.42 * (mw - 58.15) if mw > 58.15 else 0)
          + 1.7e-5 * m * (5867 - pa) + 0.0014 * m * (34 - ta)
          + 3.96 * fcl * (xn ** 4 - (tra / 100) ** 4) + fcl * hc * (tcl - ta))
    return (0.303 * np.exp(-0.036 * m) + 0.028) * (mw - hl)


def ankle_draft_ppd(v_ankle, ts):
    """ASHRAE 55-2020 ankle draft model (Liu et al. 2017, Indoor Air 27(4), 852-862):
    percentage dissatisfied with draught at the ankles (%), from the mean air speed at 0.1 m
    (m/s) and the whole-body thermal sensation TS (use PMV). ASHRAE 55 limits PPD_AD to 20 %."""
    z = -2.58 + 3.05 * np.asarray(v_ankle) - 1.06 * np.asarray(ts)
    return 100 * np.exp(z) / (1 + np.exp(z))


def ankle_draft_limit(ts):
    """Mean air speed at 0.1 m (m/s) that gives PPD_AD = 20 % (ASHRAE 55: v < 0.35 TS + 0.39)."""
    return (np.log(0.25) + 2.58 + 1.06 * np.asarray(ts)) / 3.05


def occupied_zone(res, x_min=0.6, h=0.1, h_max=1.8, rh=50.0, met=1.2, clo=0.5, ts=None):
    """Draught at the ankles for x_min < x < L - x_min (EN 16798 occupied zone).

    Returns the max mean speed at height h, where it is, the temperature there, the ISO 7730 DR,
    the whole-body thermal sensation TS (PMV from the occupied-zone mean temperature and speed,
    tr = ta, unless ts is given), the ASHRAE 55 ankle draft PPD_AD and its speed limit."""
    L = res["case"].L
    j = int(h / res["dy"]); sel = (res["x"] > x_min) & (res["x"] < L - x_min)
    s, t = res["speed"][sel, j], res["T"][sel, j]
    k = np.argmax(s)
    oz = sel[:, None] & (res["y"] < h_max)[None, :]
    t_oz, v_oz = res["T"][oz].mean(), res["speed"][oz].mean()
    ts = pmv(t_oz, max(v_oz, 0.05), rh=rh, met=met, clo=clo) if ts is None else ts
    return dict(v_max=s[k], x_at=res["x"][sel][k], T=t[k], DR=draught_rate(t[k], s[k]),
                T_oz=t_oz, v_oz=v_oz, TS=ts, PPD_AD=ankle_draft_ppd(s[k], ts), v_limit_AD=ankle_draft_limit(ts))
