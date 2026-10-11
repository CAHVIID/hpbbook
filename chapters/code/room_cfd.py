"""room_cfd.py: a small 2D CFD model of a room section for teaching.

Solves the incompressible Navier-Stokes equations with the Boussinesq approximation
for buoyancy and an energy equation for temperature, on a uniform staggered (MAC) grid.
Time stepping is explicit (Chorin projection). It is for showing trends (high vs low opening,
cold vs warm supply, flow rate), not for design values.

Advection scheme (Case.advection), for momentum and temperature:
  "upwind" : first order. Robust, but adds numerical diffusion of about |u|*dx/2, which in a
             jet is larger than the eddy viscosity itself.
  "tvd"    : second-order upwind with the van Leer limiter (a TVD scheme). Same as upwind where
             the field has a peak or a step (no wiggles), second order where it is smooth.

Turbulence (eddy viscosity nu_t, turbulent Prandtl number 0.85), two options:
  "constant" : one nu_t everywhere (Case.nu_t)
  "chen-xu"  : zero-equation indoor model nu_t = 0.03874 * V * l, with V the local mean
               speed and l the distance to the nearest wall
               (Chen, Q. & Xu, W. 1998, Energy and Buildings 28(2), 137-144)

Boundary conditions
  walls   : no slip, adiabatic
  inlet   : velocity inlet, uniform normal speed U = q / (h_open * W_room), temperature T_in
  outlet  : pressure outlet, p = 0, zero-gradient velocity and temperature
Heat sources
  volumetric blocks (people, equipment): W per metre of room width spread over a rectangle
  floor heat flux patches (sun patch): W per metre of room width spread over a floor strip

2D caveat: the section represents a room that is W_room wide with openings spanning the
full width. A 2D (line) jet decays as 1/sqrt(x), slower than a 3D jet (1/x), so speeds far
from the opening are overestimated compared with a real window.
"""
from dataclasses import dataclass, field
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import factorized

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
    turbulence: str = "chen-xu" # "chen-xu" or "constant"
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
            k = idx(i, j); diag = 0.0
            for di, dj, h2, bnd in ((-1, 0, dx * dx, bL[j] if i == 0 else None), (1, 0, dx * dx, bR[j] if i == nx - 1 else None),
                                    (0, -1, dy * dy, WALL if j == 0 else None), (0, 1, dy * dy, bT[i] if j == ny - 1 else None)):
                if bnd is None:
                    rows.append(k); cols.append(idx(i + di, j + dj)); vals.append(1.0 / h2); diag -= 1.0 / h2
                elif bnd == OUTLET:
                    diag -= 2.0 / h2
            rows.append(k); cols.append(k); vals.append(diag)
    solve = factorized(sp.csc_matrix((vals, (rows, cols)), shape=(N, N)))

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
    edge = lambda a, ax: np.pad(a, [(1, 1) if k == ax else (0, 0) for k in range(a.ndim)], mode="edge")

    hist = {k: [] for k in ("t", "du", "dv", "dT", "div", "imb", "v_floor", "T_exh")}
    i_mon, j_mon = min(int(1.0 / dx), nx - 1), min(int(0.1 / dy), ny - 1)
    outR, outL, outT = bR == OUTLET, bL == OUTLET, bT == OUTLET
    view = None
    if live:
        import matplotlib.pyplot as plt
        plt.ion(); view = plt.subplots(2, 2, figsize=(10, 6))

    while t < case.t_end:
        mon = n % monitor_every == 0
        if mon:
            u0, v0, T0 = u.copy(), v.copy(), T.copy()
        nu_c = eddy_viscosity(u, v)                                  # cell centres
        nup = np.pad(nu_c, 1, mode="edge")
        nu_k = 0.25 * (nup[:-1, :-1] + nup[1:, :-1] + nup[:-1, 1:] + nup[1:, 1:])   # cell corners
        alpha_c = nu_c / case.Pr_t
        umax = max(np.abs(u).max(), np.abs(v).max(), U_in, 0.05)
        dt = min(cfl * h / umax, 0.2 * h * h / nu_c.max(), 0.5)

        # ---- momentum, u faces (interior i = 1..nx-1), viscous term in conservative form ----
        ug = np.pad(u, ((0, 0), (1, 1))); ug[:, 0] = -u[:, 0]; ug[:, -1] = -u[:, -1]
        uc = u[1:-1]
        vavg = 0.25 * (v[:-1, :-1] + v[1:, :-1] + v[:-1, 1:] + v[1:, 1:])
        dudx = _ddx(edge(u, 0), uc, dx, tvd)
        dudy = _ddx(edge(ug[1:-1], 1).T, vavg.T, dy, tvd).T
        tx = nu_c * (u[1:] - u[:-1]) / dx                             # at cell centres
        ty = nu_k * (ug[:, 1:] - ug[:, :-1]) / dy                     # at corners
        visu = (tx[1:] - tx[:-1]) / dx + (ty[1:-1, 1:] - ty[1:-1, :-1]) / dy
        us = u.copy(); us[1:-1] = uc + dt * (-uc * dudx - vavg * dudy + visu)

        # ---- momentum, v faces (interior j = 1..ny-1) ----
        vg = np.pad(v, ((1, 1), (0, 0))); vg[0] = -v[0]; vg[-1] = -v[-1]
        vc = v[:, 1:-1]
        uavg = 0.25 * (u[:-1, :-1] + u[1:, :-1] + u[:-1, 1:] + u[1:, 1:])
        dvdy = _ddx(edge(v, 1).T, vc.T, dy, tvd).T
        dvdx = _ddx(edge(vg[:, 1:-1], 0), uavg, dx, tvd)
        sy = nu_c * (v[:, 1:] - v[:, :-1]) / dy                       # at cell centres
        sx = nu_k * (vg[1:] - vg[:-1]) / dx                           # at corners
        visv = (sy[:, 1:] - sy[:, :-1]) / dy + (sx[1:, 1:-1] - sx[:-1, 1:-1]) / dx
        buoy = G * beta * (0.5 * (T[:, :-1] + T[:, 1:]) - Tref)
        vs = v.copy(); vs[:, 1:-1] = vc + dt * (-uavg * dvdx - vc * dvdy + visv + buoy)

        # ---- projection ----
        apply_bc(us, vs)
        div = (us[1:] - us[:-1]) / dx + (vs[:, 1:] - vs[:, :-1]) / dy
        p = solve((div / dt).ravel()).reshape(nx, ny)
        us[1:-1] -= dt * (p[1:] - p[:-1]) / dx
        vs[:, 1:-1] -= dt * (p[:, 1:] - p[:, :-1]) / dy
        oL, oR, oT = bL == OUTLET, bR == OUTLET, bT == OUTLET
        us[0, oL] -= dt * (p[0, oL] - 0.0) / (dx / 2)
        us[nx, oR] -= dt * (0.0 - p[nx - 1, oR]) / (dx / 2)
        vs[oT, ny] -= dt * (0.0 - p[oT, ny - 1]) / (dy / 2)
        u, v = us, vs
        if mon:
            div_max = np.abs((u[1:] - u[:-1]) / dx + (v[:, 1:] - v[:, :-1]) / dy).max()

        # ---- energy (finite volume, upwind or TVD face values) ----
        Tin_L = np.where(bL == INLET, case.T_in, T[0]); Tin_R = np.where(bR == INLET, case.T_in, T[-1])
        Fx = u * _faces(np.vstack([Tin_L, Tin_L, T, Tin_R, Tin_R]), u, tvd)
        Ey = np.hstack([T[:, :1], T[:, :1], T, T[:, -1:], T[:, -1:]])
        Fy = v * _faces(Ey.T, v.T, tvd).T
        Fy[:, 0] = 0.0
        diffx = np.zeros_like(Fx); diffx[1:-1] = -0.5 * (alpha_c[1:] + alpha_c[:-1]) * (T[1:] - T[:-1]) / dx
        diffy = np.zeros_like(Fy); diffy[:, 1:-1] = -0.5 * (alpha_c[:, 1:] + alpha_c[:, :-1]) * (T[:, 1:] - T[:, :-1]) / dy
        Fx += diffx; Fy += diffy
        Fy[:, 0] -= qfloor / (RHO * CP)                                   # floor heat flux enters through bottom faces
        T = T - dt * ((Fx[1:] - Fx[:-1]) / dx + (Fy[:, 1:] - Fy[:, :-1]) / dy) + dt * S / (RHO * CP)

        if mon:
            rms = lambda a: float(np.sqrt(np.mean(a * a)))
            q_open = (Fx[-1].sum() - Fx[0].sum()) * dy + Fy[:, -1].sum() * dx       # K m²/s per metre width
            T_exh = np.concatenate([T[-1, outR], T[0, outL], T[outT, -1]]).mean()
            for k, val in (("t", t + dt), ("du", rms(u - u0) / dt), ("dv", rms(v - v0) / dt), ("dT", rms(T - T0) / dt),
                           ("div", div_max), ("imb", 100 * (RHO * CP * q_open - Q_tot) / max(Q_tot, 1.0)),
                           ("v_floor", float(np.hypot(0.5 * (u[i_mon, j_mon] + u[i_mon + 1, j_mon]),
                                                      0.5 * (v[i_mon, j_mon] + v[i_mon, j_mon + 1])))),
                           ("T_exh", float(T_exh))):
                hist[k].append(val)
            if view is not None and len(hist["t"]) % live_every == 0:
                draw_convergence(hist, case, *view)
                view[0].canvas.flush_events(); plt.pause(0.001)
        t += dt; n += 1
        if t >= t_avg0:                                               # time average, weighted by dt
            ua += dt * u; va += dt * v; Ta += dt * T; nua += dt * nu_c; wa += dt
            spa += dt * np.hypot(0.5 * (u[1:] + u[:-1]), 0.5 * (v[:, 1:] + v[:, :-1]))
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
