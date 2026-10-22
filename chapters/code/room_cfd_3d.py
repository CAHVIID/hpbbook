"""room_cfd_3d.py: a small 3D CFD model of a room for teaching (test version).

The 3D extension of room_cfd.py, with a multigrid pressure solver. Same physics,
same numerics and the same options, but the room has a width, the side walls are real walls, and
openings can be narrower than the room (a window 1.2 m wide in a 4 m wide room).

Coordinates: x along the depth L (facade at x = 0), y across the width W, z up the height H.

Solves the incompressible Navier-Stokes equations with the Boussinesq approximation for buoyancy
and an energy equation for temperature, on a uniform staggered (MAC) grid. Time stepping is
explicit (Chorin projection). It is for showing trends, not for design values.

Advection (Case.advection), for momentum and temperature:
  "upwind" : first order
  "tvd"    : second-order upwind with the van Leer limiter (default)
Turbulence (eddy viscosity nu_t, turbulent Prandtl number 0.85):
  "constant"  : one nu_t everywhere (Case.nu_t)
  "chen-xu"   : nu_t = 0.03874 * V * l, l = distance to the nearest wall (Chen & Xu 1998)
  "k-epsilon" : standard k-epsilon (Launder & Spalding 1974) with log-law wall functions on all
                six walls, buoyancy production of k, inlet k = 1.5 (Tu_in U)^2, eps = k^1.5/(0.1 h)
Pressure (Case.pressure):
  "multigrid" : conjugate gradients preconditioned by one multigrid V-cycle (default). The cells
                are grouped 2 x 2 x 2 into coarser grids (smoothed aggregation, A_c = P^T A P),
                with weighted Jacobi smoothing and a direct solve on the coarsest grid
  "direct"    : sparse LU, factorised once (only for small meshes: the factor fills in fast in 3D)

Boundary conditions
  walls   : no slip, adiabatic (floor, ceiling, facade, back wall and both side walls)
  inlet   : in the facade or back wall, uniform normal speed U = q / A_open, temperature T_in
  outlet  : in the facade, back wall or ceiling, p = 0, zero-gradient velocity and temperature
Heat sources
  HeatBlock: total power (W) spread over a box; FloorFlux: total power (W) over a floor rectangle

Contact: Christian Hviid, cahv@dtu.dk

Disclaimer: use at own risk. This is a simplified teaching model for comparing cases and seeing the
physics. It does not give design values, and it is provided as is, without warranty of any kind.
"""
from dataclasses import dataclass, field
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import splu, factorized
from room_cfd import draught_rate, pmv, ankle_draft_ppd, ankle_draft_limit   # comfort functions, as in 2D

RHO, CP, G = 1.2, 1005.0, 9.81
NU_AIR = 1.5e-5                 # molecular kinematic viscosity (m²/s)
WALL, INLET, OUTLET = 0, 1, 2
CMU, C1, C2, SK, SE, KAP, EWF = 0.09, 1.44, 1.92, 1.0, 1.3, 0.41, 9.0


@dataclass
class Opening:
    side: str            # "left" (facade, x = 0), "right" (back wall, x = L) or "top" (ceiling)
    start: float         # m: height for the walls, x for the ceiling
    end: float
    y0: float = None     # m across the width; None = the full width
    y1: float = None


@dataclass
class HeatBlock:
    x0: float; x1: float; y0: float; y1: float; z0: float; z1: float
    power: float         # W, spread over the box


@dataclass
class FloorFlux:
    x0: float; x1: float; y0: float; y1: float
    power: float         # W, spread over the floor rectangle


@dataclass
class Case:
    L: float = 5.0              # room depth (m), x
    W: float = 4.0              # room width (m), y
    H: float = 2.5              # room height (m), z
    nx: int = 50
    ny: int = 40
    nz: int = 25
    ach: float = 6.0            # air changes per hour
    T_in: float = 18.0          # supply temperature (°C)
    T_room0: float = None       # initial room temperature (°C); None = well-mixed steady value
    inlet: Opening = field(default_factory=lambda: Opening("left", 0.10, 0.30))
    outlet: Opening = field(default_factory=lambda: Opening("right", 2.20, 2.40))
    heat: list = field(default_factory=list)
    floor_flux: list = field(default_factory=list)
    turbulence: str = "k-epsilon"  # "k-epsilon" (default), "chen-xu" or "constant"
    Tu_in: float = 0.04         # inlet turbulence intensity, used by "k-epsilon"
    nu_t: float = 2e-3          # eddy viscosity (m²/s) for "constant"
    Pr_t: float = 0.85
    advection: str = "tvd"      # "tvd" (van Leer, default) or "upwind"
    pressure: str = "multigrid"  # "multigrid" (default) or "direct"
    p_tol: float = 1e-6         # relative residual of the multigrid pressure solve (1e-6 changes T by < 1e-4 K)
    t_end: float = 900.0        # simulated time (s)
    t_avg: float = 300.0        # averaging window at the end (s)

    @property
    def q(self):                # m³/s
        return self.ach * self.L * self.H * self.W / 3600.0


# ---------------------------------------------------------------------------------------------
# array helpers: the same schemes as room_cfd.py, along any axis of a 3D array
# ---------------------------------------------------------------------------------------------
def _sl(a, axis, start=None, stop=None):
    """a[..., start:stop, ...] along one axis."""
    idx = [slice(None)] * a.ndim; idx[axis] = slice(start, stop)
    return a[tuple(idx)]


def _edge(a, axis, n=1):
    """Pad with copies of the end values along one axis."""
    return np.pad(a, [(n, n) if k == axis else (0, 0) for k in range(a.ndim)], mode="edge")


def _mirror(a, axis):
    """Pad with one ghost value that is minus the end value (no slip at a wall between them)."""
    return np.concatenate([-_sl(a, axis, 0, 1), a, -_sl(a, axis, -1, None)], axis=axis)


def _lim(a, b):
    """van Leer limiter in product form, psi(a/b)*b."""
    return (a * np.abs(b) + np.abs(a) * b) / (np.abs(a) + np.abs(b) + 1e-30)


def _ddx(P, vel, h, tvd, axis):
    """Upwind-biased derivative along axis at P[2:-2] (two ghost values each side), as in room_cfd.py."""
    P = np.moveaxis(P, axis, 0); vel = np.moveaxis(vel, axis, 0)
    D = np.diff(P, axis=0)
    Lm = _lim(D[:-1], D[1:]) if tvd else np.zeros_like(D[1:])
    pos = D[1:-2] + 0.5 * Lm[1:-1] - 0.5 * Lm[:-2]
    neg = D[2:-1] - 0.5 * Lm[2:] + 0.5 * Lm[1:-1]
    return np.moveaxis(np.where(vel > 0, pos, neg) / h, 0, axis)


def _faces(E, vel, tvd, axis):
    """Upwind face values between E[1:-2] and E[2:-1] along axis (two ghost values each side)."""
    E = np.moveaxis(E, axis, 0); vel = np.moveaxis(vel, axis, 0)
    if not tvd:
        out = np.where(vel > 0, E[1:-2], E[2:-1])
    else:
        D = np.diff(E, axis=0)
        Lm = _lim(D[:-1], D[1:])
        out = np.where(vel > 0, E[1:-2] + 0.5 * Lm[:-1], E[2:-1] - 0.5 * Lm[1:])
    return np.moveaxis(out, 0, axis)


# ---------------------------------------------------------------------------------------------
# multigrid pressure solver
# ---------------------------------------------------------------------------------------------
class Multigrid:
    """Solve M p = b for the SPD pressure matrix M on a grid of cells (C order).

    Conjugate gradients preconditioned by one symmetric V-cycle. Coarse grids group the cells
    2 x 2 x 2 (an odd last layer stays alone), the piecewise-constant prolongation is smoothed by
    one Jacobi step, and the coarse matrices are A_c = P^T A P."""

    def __init__(self, M, shape, n_coarse=400, omega=2 / 3, sweeps=2):
        self.omega, self.sweeps = omega, sweeps
        self.A, self.P, self.Dinv = [M.tocsr()], [], []
        shape = tuple(shape)
        while self.A[-1].shape[0] > n_coarse and max(shape) > 1:
            A = self.A[-1]
            cs = tuple((n + 1) // 2 for n in shape)
            idx = np.indices(shape) // 2
            agg = np.ravel_multi_index(tuple(idx), cs).ravel()
            n = int(np.prod(shape))
            P0 = sp.csr_matrix((np.ones(n), (np.arange(n), agg)), shape=(n, int(np.prod(cs))))
            Dinv = sp.diags(1.0 / A.diagonal())
            P = (P0 - (4 / 3 / 2.0) * (Dinv @ (A @ P0))).tocsr()   # spectral radius of D^-1 A <= 2
            self.Dinv.append(1.0 / A.diagonal()); self.P.append(P)
            self.A.append((P.T @ A @ P).tocsr())
            shape = cs
        self.Dinv.append(1.0 / self.A[-1].diagonal())
        self.coarse = factorized(self.A[-1].tocsc())
        self.iters = 0

    def vcycle(self, r, lev=0):
        if lev == len(self.P):
            return self.coarse(r)
        A, D, w = self.A[lev], self.Dinv[lev], self.omega
        x = w * D * r
        for _ in range(self.sweeps - 1):
            x += w * D * (r - A @ x)
        x += self.P[lev] @ self.vcycle(self.P[lev].T @ (r - A @ x), lev + 1)
        for _ in range(self.sweeps):
            x += w * D * (r - A @ x)
        return x

    def solve(self, b, x0, tol, maxit=200):
        A = self.A[0]
        x = x0.copy(); r = b - A @ x
        bnorm = max(np.linalg.norm(b), 1e-300)
        if np.linalg.norm(r) <= tol * bnorm:
            return x
        z = self.vcycle(r); d = z.copy(); rz = r @ z
        for _ in range(maxit):
            Ad = A @ d; a = rz / (d @ Ad)
            x += a * d; r -= a * Ad; self.iters += 1
            if np.linalg.norm(r) <= tol * bnorm:
                break
            z = self.vcycle(r); rz, rz_old = r @ z, rz
            d = z + (rz / rz_old) * d
        return x


def _lap1(n, h):
    """1D second difference with zero-gradient ends."""
    d = -2.0 * np.ones(n); d[0] = d[-1] = -1.0
    if n == 1:
        d[:] = 0.0
    return sp.diags([np.ones(n - 1), d, np.ones(n - 1)], [-1, 0, 1]) / h ** 2


# ---------------------------------------------------------------------------------------------
# the solver
# ---------------------------------------------------------------------------------------------
def boundaries(case):
    """Boundary type of every face of the six walls: dict (axis, side) -> array over the other two axes."""
    nx, ny, nz = case.nx, case.ny, case.nz
    xc = (np.arange(nx) + 0.5) * case.L / nx
    yc = (np.arange(ny) + 0.5) * case.W / ny
    zc = (np.arange(nz) + 0.5) * case.H / nz
    b = {(0, 0): np.zeros((ny, nz), int), (0, 1): np.zeros((ny, nz), int),
         (1, 0): np.zeros((nx, nz), int), (1, 1): np.zeros((nx, nz), int),
         (2, 0): np.zeros((nx, ny), int), (2, 1): np.zeros((nx, ny), int)}
    for op, kind in ((case.inlet, INLET), (case.outlet, OUTLET)):
        y0 = 0.0 if op.y0 is None else op.y0
        y1 = case.W if op.y1 is None else op.y1
        iy = (yc > y0) & (yc < y1)
        if op.side in ("left", "right"):
            m = iy[:, None] & ((zc > op.start) & (zc < op.end))[None, :]
            key = (0, 0) if op.side == "left" else (0, 1)
        elif op.side == "top":
            if kind == INLET:
                raise ValueError("inlets must be in the facade (left) or the back wall (right)")
            m = ((xc > op.start) & (xc < op.end))[:, None] & iy[None, :]
            key = (2, 1)
        else:
            raise ValueError(f"unknown side {op.side!r}")
        if not m.any():
            raise ValueError(f"the {op.side} opening covers no cell faces: refine the mesh")
        b[key][m] = kind
    return b


def run(case: Case, verbose=False, monitor_every=50):
    """Run the case and return time-averaged fields (u, v, w on the faces; T, speed, nu_t at the cell centres)."""
    n = (case.nx, case.ny, case.nz)
    d = (case.L / case.nx, case.W / case.ny, case.H / case.nz)
    nx, ny, nz = n; dx, dy, dz = d
    shp = [tuple(n[k] + (1 if k == c else 0) for k in range(3)) for c in range(3)]
    bnd = boundaries(case)
    bL, bR, bT = bnd[(0, 0)], bnd[(0, 1)], bnd[(2, 1)]
    A_in = ((bL == INLET).sum() + (bR == INLET).sum()) * dy * dz
    U_in = case.q / A_in
    h_in = A_in / case.W                                  # mean opening height (for the k-eps inlet length)

    U = [np.zeros(s) for s in shp]                        # u, v, w
    Q_tot = sum(b.power for b in case.heat) + sum(f.power for f in case.floor_flux)
    T_mix = case.T_in + Q_tot / (RHO * CP * case.q)
    T0 = T_mix if case.T_room0 is None else case.T_room0
    T = np.full(n, float(T0)); Tref = float(T0)
    beta = 1.0 / (273.15 + Tref)

    xc, yc, zc = [(np.arange(n[k]) + 0.5) * d[k] for k in range(3)]
    X, Y, Z = np.meshgrid(xc, yc, zc, indexing="ij")
    lwall = np.minimum.reduce([X, case.L - X, Y, case.W - Y, Z, case.H - Z])

    # heat sources (W/m³) and floor fluxes (W/m²)
    S = np.zeros(n)
    for b in case.heat:
        cells = (X > b.x0) & (X < b.x1) & (Y > b.y0) & (Y < b.y1) & (Z > b.z0) & (Z < b.z1)
        S[cells] += b.power / (cells.sum() * dx * dy * dz)
    qfloor = np.zeros((nx, ny))
    for f in case.floor_flux:
        sel = ((xc > f.x0) & (xc < f.x1))[:, None] & ((yc > f.y0) & (yc < f.y1))[None, :]
        qfloor[sel] += f.power / (sel.sum() * dx * dy)

    # k-epsilon: inlet values, wall cells and their distance to the wall
    ke = case.turbulence == "k-epsilon"
    k_in = 1.5 * (case.Tu_in * U_in) ** 2
    e_in = k_in ** 1.5 / (0.1 * h_in)
    k = np.full(n, k_in); eps = np.full(n, e_in)
    yp = np.full(n, np.inf)
    for (ax, side), m in bnd.items():
        idx = [slice(None)] * 3; idx[ax] = 0 if side == 0 else n[ax] - 1
        cur = yp[tuple(idx)]
        yp[tuple(idx)] = np.where(m == WALL, np.minimum(cur, d[ax] / 2), cur)
    wall_cell = np.isfinite(yp)
    ypw = np.where(wall_cell, yp, 1.0)

    def nu_wall(kw, y):
        ys = CMU ** 0.25 * np.sqrt(kw) * y / NU_AIR
        return np.where(ys > 11.2, KAP * ys * NU_AIR / np.log(EWF * np.maximum(ys, 1.0)), NU_AIR)

    def wall_edges(m, axis):
        """For a wall mask m, True at the edges along axis where the faces on both sides are wall."""
        e = _edge(m, axis)
        return (_sl(e, axis, 0, -1) == WALL) & (_sl(e, axis, 1, None) == WALL)

    def edge_viscosity(nu_c, p, q):
        """Viscosity on the cell edges between axes p < q (average of four cells), log law at the walls."""
        nup = _edge(_edge(nu_c, p), q)
        ne = 0.25 * (_sl(_sl(nup, p, 0, -1), q, 0, -1) + _sl(_sl(nup, p, 1, None), q, 0, -1)
                     + _sl(_sl(nup, p, 0, -1), q, 1, None) + _sl(_sl(nup, p, 1, None), q, 1, None))
        if ke:
            kp = _edge(_edge(k, p), q)
            kk = 0.25 * (_sl(_sl(kp, p, 0, -1), q, 0, -1) + _sl(_sl(kp, p, 1, None), q, 0, -1)
                         + _sl(_sl(kp, p, 0, -1), q, 1, None) + _sl(_sl(kp, p, 1, None), q, 1, None))
            for wa, other in ((q, p), (p, q)):            # walls normal to q first, then to p (as in 2D)
                for side, pos in ((0, 0), (1, n[wa])):
                    m = bnd[(wa, side)]
                    oth = other if other < wa else other - 1      # axis of `other` in the wall mask
                    sel = wall_edges(m, oth)
                    idx = [slice(None)] * 3; idx[wa] = pos
                    cur = ne[tuple(idx)]
                    ne[tuple(idx)] = np.where(sel, nu_wall(kk[tuple(idx)], d[wa] / 2), cur)
        return ne

    def eddy_viscosity():
        if ke:
            return NU_AIR + CMU * k * k / eps
        if case.turbulence == "constant":
            return np.full(n, NU_AIR + case.nu_t)
        uc = [0.5 * (_sl(U[c], c, 1, None) + _sl(U[c], c, 0, -1)) for c in range(3)]
        return NU_AIR + 0.03874 * np.sqrt(uc[0] ** 2 + uc[1] ** 2 + uc[2] ** 2) * lwall

    def fluxes(phi, phi_in, D, tvd):
        """Face fluxes (advection + diffusion) of a cell-centred scalar along x, y and z."""
        F = []
        for c in range(3):
            if c == 0:
                lo = np.where(bL == INLET, phi_in, phi[0])[None]
                hi = np.where(bR == INLET, phi_in, phi[-1])[None]
                E = np.concatenate([lo, lo, phi, hi, hi], axis=0)
            else:
                E = _edge(phi, c, 2)
            Fc = U[c] * _faces(E, U[c], tvd, c)
            inner = _sl(Fc, c, 1, -1)
            inner -= 0.5 * (_sl(D, c, 1, None) + _sl(D, c, 0, -1)) * np.diff(phi, axis=c) / d[c]
            F.append(Fc)
        F[2][:, :, 0] = 0.0
        return F

    def divergence(F):
        return sum(np.diff(F[c], axis=c) / d[c] for c in range(3))

    def apply_bc(V):
        u, v, w = V
        u[0] = np.where(bL == INLET, U_in, np.where(bL == OUTLET, u[1], 0.0))
        u[nx] = np.where(bR == INLET, -U_in, np.where(bR == OUTLET, u[nx - 1], 0.0))
        v[:, 0] = 0.0; v[:, ny] = 0.0
        w[:, :, 0] = 0.0
        w[:, :, nz] = np.where(bT == OUTLET, w[:, :, nz - 1], 0.0)

    # pressure Poisson matrix: zero gradient at walls and inlets, p = 0 at the outlet faces
    I = [sp.identity(m, format="csr") for m in n]
    Amat = (sp.kron(sp.kron(_lap1(nx, dx), I[1]), I[2]) + sp.kron(sp.kron(I[0], _lap1(ny, dy)), I[2])
            + sp.kron(sp.kron(I[0], I[1]), _lap1(nz, dz))).tolil()
    extra = np.zeros(n)
    extra[0][bL == OUTLET] -= 2.0 / dx ** 2
    extra[-1][bR == OUTLET] -= 2.0 / dx ** 2
    extra[:, :, -1][bT == OUTLET] -= 2.0 / dz ** 2
    Amat = (Amat.tocsr() + sp.diags(extra.ravel())).tocsc()
    if case.pressure == "multigrid":
        mgs = Multigrid(-Amat, n); p_last = np.zeros(Amat.shape[0])

        def solve(rhs):
            nonlocal p_last
            p_last = mgs.solve(-rhs, p_last, case.p_tol)     # A p = rhs  <=>  (-A) p = -rhs
            return p_last
    else:
        solve = splu(Amat, permc_spec="MMD_AT_PLUS_A").solve

    apply_bc(U)
    avg = dict(u=np.zeros(shp[0]), v=np.zeros(shp[1]), w=np.zeros(shp[2]), T=np.zeros(n), speed=np.zeros(n),
               nu_t=np.zeros(n), k=np.zeros(n))
    wa = 0.0
    t, step, t_avg0, h = 0.0, 0, case.t_end - case.t_avg, min(d)
    tvd = case.advection == "tvd"
    cfl = 0.25 if tvd else 0.4

    hist = {key: [] for key in ("t", "du", "dv", "dw", "dT", "div", "imb", "v_floor", "T_exh")}
    mon_pt = (min(int(1.0 / dx), nx - 1), ny // 2, min(int(0.1 / dz), nz - 1))
    outR, outL, outT = bR == OUTLET, bL == OUTLET, bT == OUTLET

    def cell_speed(V):
        uc = [0.5 * (_sl(V[c], c, 1, None) + _sl(V[c], c, 0, -1)) for c in range(3)]
        return np.sqrt(uc[0] ** 2 + uc[1] ** 2 + uc[2] ** 2)

    while t < case.t_end:
        mon = step % monitor_every == 0
        if mon:
            U0, T0_ = [a.copy() for a in U], T.copy()
        nu_c = eddy_viscosity()
        nu_e = {(p, q): edge_viscosity(nu_c, p, q) for p, q in ((0, 1), (0, 2), (1, 2))}
        alpha_c = nu_c / case.Pr_t
        umax = max(max(np.abs(a).max() for a in U), U_in, 0.05)
        dt = min(cfl * h / umax, 0.15 * h * h / nu_c.max(), 0.5)

        # ---- momentum: advection (non-conservative, upwind or TVD), viscous term in conservative form ----
        Us = [a.copy() for a in U]
        for c in range(3):
            Uc = U[c]
            inner = _sl(Uc, c, 1, -1)                     # interior faces normal to c
            rhs = np.zeros_like(inner)
            for a in range(3):
                if a == c:
                    vel = inner
                    deriv = _ddx(_edge(Uc, c), vel, d[c], tvd, c)
                    flux = nu_c * np.diff(Uc, axis=c) / d[c]                 # at cell centres
                    rhs += -vel * deriv + np.diff(flux, axis=c) / d[c]
                else:
                    Ua = U[a]                                                  # velocity a at the c faces
                    vel = 0.25 * (_sl(_sl(Ua, c, 0, -1), a, 0, -1) + _sl(_sl(Ua, c, 1, None), a, 0, -1)
                                  + _sl(_sl(Ua, c, 0, -1), a, 1, None) + _sl(_sl(Ua, c, 1, None), a, 1, None))
                    G_ = _mirror(inner, a)
                    deriv = _ddx(_edge(G_, a), vel, d[a], tvd, a)
                    ne = nu_e[(min(a, c), max(a, c))]                         # on the edges
                    flux = _sl(ne, c, 1, -1) * np.diff(G_, axis=a) / d[a]
                    rhs += -vel * deriv + np.diff(flux, axis=a) / d[a]
            if c == 2:
                rhs += G * beta * (0.5 * (T[:, :, :-1] + T[:, :, 1:]) - Tref)
            _sl(Us[c], c, 1, -1)[...] = inner + dt * rhs

        # ---- projection ----
        apply_bc(Us)
        div = sum(np.diff(Us[c], axis=c) / d[c] for c in range(3))
        p = solve((div / dt).ravel()).reshape(n)
        for c in range(3):
            _sl(Us[c], c, 1, -1)[...] -= dt * np.diff(p, axis=c) / d[c]
        Us[0][0][outL] -= dt * (p[0][outL] - 0.0) / (dx / 2)
        Us[0][nx][outR] -= dt * (0.0 - p[-1][outR]) / (dx / 2)
        Us[2][:, :, nz][outT] -= dt * (0.0 - p[:, :, -1][outT]) / (dz / 2)
        U = Us
        if mon:
            div_max = np.abs(sum(np.diff(U[c], axis=c) / d[c] for c in range(3))).max()

        # ---- energy (finite volume) ----
        F = fluxes(T, case.T_in, alpha_c, tvd)
        F[2][:, :, 0] -= qfloor / (RHO * CP)
        T_old = T
        T = T - dt * divergence(F) + dt * S / (RHO * CP)

        # ---- k and epsilon (sinks implicit) ----
        if ke:
            nut = nu_c - NU_AIR
            P = 2 * sum((np.diff(U[c], axis=c) / d[c]) ** 2 for c in range(3))
            for p_, q_ in ((0, 1), (0, 2), (1, 2)):
                s_ = (np.diff(_mirror(U[p_], q_), axis=q_) / d[q_]
                      + np.diff(_mirror(U[q_], p_), axis=p_) / d[p_])           # on the edges
                s_ = 0.25 * (_sl(_sl(s_, p_, 0, -1), q_, 0, -1) + _sl(_sl(s_, p_, 1, None), q_, 0, -1)
                             + _sl(_sl(s_, p_, 0, -1), q_, 1, None) + _sl(_sl(s_, p_, 1, None), q_, 1, None))
                P = P + s_ ** 2
            P = nut * P
            Up = cell_speed(U)
            tau = nu_wall(k, ypw) * Up / ypw
            P = np.where(wall_cell, tau * CMU ** 0.25 * np.sqrt(k) / (KAP * ypw), P)
            Gb = -G * beta * nut / case.Pr_t * np.gradient(T_old, dz, axis=2)
            rk = -divergence(fluxes(k, k_in, NU_AIR + nut / SK, False))
            re = -divergence(fluxes(eps, e_in, NU_AIR + nut / SE, False))
            k_new = (k + dt * (rk + P + np.maximum(Gb, 0))) / (1 + dt * (eps + np.maximum(-Gb, 0)) / k)
            e_new = (eps + dt * (re + C1 * eps / k * (P + np.maximum(Gb, 0)))) / (1 + dt * C2 * eps / k)
            k = np.maximum(k_new, 1e-10); eps = np.maximum(e_new, 1e-12)
            eps = np.where(wall_cell, CMU ** 0.75 * k ** 1.5 / (KAP * ypw), eps)

        if mon:
            rms = lambda a: float(np.sqrt(np.mean(a * a)))
            q_open = ((F[0][-1].sum() - F[0][0].sum()) * dy * dz + F[2][:, :, -1].sum() * dx * dy)   # K m³/s
            T_exh = np.concatenate([T[-1][outR], T[0][outL], T[:, :, -1][outT]]).mean()
            i_, j_, k_ = mon_pt
            for key, val in (("t", t + dt), ("du", rms(U[0] - U0[0]) / dt), ("dv", rms(U[1] - U0[1]) / dt),
                             ("dw", rms(U[2] - U0[2]) / dt), ("dT", rms(T - T0_) / dt), ("div", div_max),
                             ("imb", 100 * (RHO * CP * q_open - Q_tot) / max(Q_tot, 1.0)),
                             ("v_floor", float(cell_speed(U)[i_, j_, k_])), ("T_exh", float(T_exh))):
                hist[key].append(val)
        t += dt; step += 1
        if t >= t_avg0:
            for key, val in (("u", U[0]), ("v", U[1]), ("w", U[2]), ("T", T), ("speed", cell_speed(U)),
                             ("nu_t", nu_c), ("k", k)):
                avg[key] += dt * val
            wa += dt
        if verbose and step % 500 == 0:
            print(f"t = {t:6.0f} s  dt = {dt:.3f}  max|u| = {umax:.2f}  max nu_t = {nu_c.max():.4f}  "
                  f"T mean = {T.mean():.2f}", flush=True)

    for key in avg:
        avg[key] /= wa
    q_out = (avg["u"][nx][outR].sum() - avg["u"][0][outL].sum()) * dy * dz + avg["w"][:, :, nz][outT].sum() * dx * dy
    T_out = np.concatenate([avg["T"][-1][outR], avg["T"][0][outL], avg["T"][:, :, -1][outT]]).mean()
    res = dict(case=case, x=xc, y=yc, z=zc, dx=dx, dy=dy, dz=dz, U_in=U_in, h_in=h_in, steps=step,
               q_in=case.q, q_out=q_out, T_out=T_out, T_out_expected=T_mix,
               cg_iters=mgs.iters if case.pressure == "multigrid" else 0,
               history={key: np.array(a) for key, a in hist.items()})
    res.update(avg)
    return res


# ---------------------------------------------------------------------------------------------
# comfort at the ankles and simple plots
# ---------------------------------------------------------------------------------------------

def occupied_zone(res, x_min=0.6, y_min=0.6, h=0.1, h_max=1.8, rh=50.0, met=1.2, clo=0.5, ts=None):
    """Draught at the ankles in the occupied zone (EN 16798: 0.6 m from the facade, back and side walls).

    Returns the max mean speed at height h, where it is (x, y), the temperature there, the ISO 7730 DR,
    the whole-body thermal sensation TS (PMV from the occupied-zone mean temperature and speed, tr = ta,
    unless ts is given), the ASHRAE 55 ankle draft PPD_AD and its speed limit."""
    c = res["case"]
    kz = min(int(h / res["dz"]), c.nz - 1)
    sx = (res["x"] > x_min) & (res["x"] < c.L - x_min)
    sy = (res["y"] > y_min) & (res["y"] < c.W - y_min)
    sel = sx[:, None] & sy[None, :]
    s, t = res["speed"][:, :, kz], res["T"][:, :, kz]
    s_sel = np.where(sel, s, -1.0)
    i, j = np.unravel_index(np.argmax(s_sel), s.shape)
    oz = sel[:, :, None] & (res["z"] < h_max)[None, None, :]
    t_oz, v_oz = res["T"][oz].mean(), res["speed"][oz].mean()
    ts = pmv(t_oz, max(v_oz, 0.05), rh=rh, met=met, clo=clo) if ts is None else ts
    return dict(v_max=s[i, j], x_at=res["x"][i], y_at=res["y"][j], T=t[i, j], DR=draught_rate(t[i, j], s[i, j]),
                T_oz=t_oz, v_oz=v_oz, TS=ts, PPD_AD=ankle_draft_ppd(s[i, j], ts), v_limit_AD=ankle_draft_limit(ts))


def plot_slices(res, y=None, z=0.1, path=None, vmin=None, vmax=None):
    """Temperature and air speed in a vertical section at y (default mid-width) and a plan at height z."""
    import matplotlib.pyplot as plt
    c = res["case"]
    y = c.W / 2 if y is None else y
    j = min(int(y / res["dy"]), c.ny - 1); kz = min(int(z / res["dz"]), c.nz - 1)
    uc = 0.5 * (res["u"][1:] + res["u"][:-1]); vc = 0.5 * (res["v"][:, 1:] + res["v"][:, :-1])
    wc = 0.5 * (res["w"][:, :, 1:] + res["w"][:, :, :-1])
    fig, axs = plt.subplots(2, 2, figsize=(12, 7.5), gridspec_kw=dict(height_ratios=[c.H, c.W]))
    vmin = c.T_in if vmin is None else vmin
    vmax = res["T"].max() if vmax is None else vmax
    for col, (fld, cmap, lab, lo, hi) in enumerate((("T", "coolwarm", "Temperature (°C)", vmin, vmax),
                                                     ("speed", "viridis", "Air speed (m/s)", 0, None))):
        a = axs[0, col]
        im = a.pcolormesh(res["x"], res["z"], res[fld][:, j, :].T, cmap=cmap, vmin=lo, vmax=hi, shading="auto")
        a.streamplot(res["x"], res["z"], uc[:, j, :].T, wc[:, j, :].T, color="k", linewidth=0.5, density=1.0,
                     arrowsize=0.6)
        a.set_aspect("equal"); a.set_title(f"{lab}, section at y = {res['y'][j]:.2f} m")
        a.set_xlabel("x (m)"); a.set_ylabel("z (m)"); fig.colorbar(im, ax=a, shrink=0.8)
        a = axs[1, col]
        im = a.pcolormesh(res["x"], res["y"], res[fld][:, :, kz].T, cmap=cmap, vmin=lo, vmax=hi, shading="auto")
        a.streamplot(res["x"], res["y"], uc[:, :, kz].T, vc[:, :, kz].T, color="k", linewidth=0.5, density=1.0,
                     arrowsize=0.6)
        a.set_aspect("equal"); a.set_title(f"{lab}, plan at z = {res['z'][kz]:.2f} m")
        a.set_xlabel("x (m)"); a.set_ylabel("y (m)"); fig.colorbar(im, ax=a, shrink=0.8)
    fig.tight_layout()
    if path:
        fig.savefig(path, dpi=130)
        plt.close(fig)
    return fig
