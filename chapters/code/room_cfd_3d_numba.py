"""room_cfd_3d_numba.py: room_cfd_3d.py with the time step compiled by Numba (test version).

Same model, same inputs (Case, Opening, HeatBlock, FloorFlux from room_cfd_3d.py) and the same results
to round-off, but each stage of a time step is one compiled loop over the cells, run in parallel on all
processor cores. The pressure equation uses the same multigrid solver as room_cfd_3d.py.
Needs the numba package (pip install numba). The first run compiles the loops (some tens of seconds);
the compiled code is cached in __pycache__.

Contact: Christian Hviid, cahv@dtu.dk. Use at own risk; see the disclaimer in room_cfd_3d.py.
"""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import splu
from numba import njit, prange
from room_cfd_3d import (Case, Opening, HeatBlock, FloorFlux, Multigrid, boundaries, occupied_zone, plot_slices,  # noqa: F401
                         _lap1, _edge, _sl, RHO, CP, G, NU_AIR, WALL, INLET, OUTLET, CMU, C1, C2, SK, SE, KAP, EWF)


# ---------------------------------------------------------------------------------------------
# small helpers (inlined by Numba)
# ---------------------------------------------------------------------------------------------
@njit(inline="always")
def _lim(a, b):
    return (a * abs(b) + abs(a) * b) / (abs(a) + abs(b) + 1e-30)


@njit(inline="always")
def _ddx(pm2, pm1, p0, pp1, pp2, vel, h, tvd):
    d0, d1, d2, d3 = pm1 - pm2, p0 - pm1, pp1 - p0, pp2 - pp1
    if tvd:
        l0, l1, l2 = _lim(d0, d1), _lim(d1, d2), _lim(d2, d3)
    else:
        l0 = l1 = l2 = 0.0
    if vel > 0:
        return (d1 + 0.5 * l1 - 0.5 * l0) / h
    return (d2 - 0.5 * l2 + 0.5 * l1) / h


@njit(inline="always")
def _face(em1, e0, e1, e2, vel, tvd):
    if not tvd:
        return e0 if vel > 0 else e1
    if vel > 0:
        return e0 + 0.5 * _lim(e0 - em1, e1 - e0)
    return e1 - 0.5 * _lim(e1 - e0, e2 - e1)


@njit(inline="always")
def _nu_wall(kw, y):
    ys = CMU ** 0.25 * np.sqrt(kw) * y / NU_AIR
    if ys > 11.2:
        return KAP * ys * NU_AIR / np.log(EWF * max(ys, 1.0))
    return NU_AIR


@njit(inline="always")
def _gv(U, c, a, i, j, k, s):
    """U_c at (i, j, k) shifted s along axis a: zero-gradient ends along its own axis, mirrored (no slip) across walls."""
    n0, n1, n2 = U.shape
    if a == 0:
        i += s
    elif a == 1:
        j += s
    else:
        k += s
    if a == c:
        return U[min(max(i, 0), n0 - 1), min(max(j, 0), n1 - 1), min(max(k, 0), n2 - 1)]
    sign = 1.0
    if i < 0 or j < 0 or k < 0 or i > n0 - 1 or j > n1 - 1 or k > n2 - 1:
        sign = -1.0
    return sign * U[min(max(i, 0), n0 - 1), min(max(j, 0), n1 - 1), min(max(k, 0), n2 - 1)]


@njit(inline="always")
def _at(A, a, i, j, k, s):
    """A at (i, j, k) shifted s along axis a (no bounds handling)."""
    if a == 0:
        return A[i + s, j, k]
    if a == 1:
        return A[i, j + s, k]
    return A[i, j, k + s]


@njit(inline="always")
def _at2(A, a, sa, b, sb, i, j, k):
    """A at (i, j, k) shifted sa along axis a and sb along axis b."""
    if a == 0:
        i += sa
    elif a == 1:
        j += sa
    else:
        k += sa
    if b == 0:
        i += sb
    elif b == 1:
        j += sb
    else:
        k += sb
    return A[i, j, k]


# ---------------------------------------------------------------------------------------------
# kernels: one per stage of a time step
# ---------------------------------------------------------------------------------------------
@njit(inline="always")
def _edge_visc(nu_c, k, ke, p, q, wd, out):
    """Viscosity on the edges between axes p < q: average of the four cells around the edge, replaced by
    the log-law value where wd > 0 (wd = distance from the wall to the first cell centre)."""
    n0, n1, n2 = out.shape
    m0, m1, m2 = nu_c.shape
    ex, ey, ez = (p == 0 or q == 0), (p == 1 or q == 1), (p == 2 or q == 2)
    for i_ in prange(n0):
        i = np.int64(i_)            # prange gives an unsigned index
        il = max(i - 1, 0) if ex else i; ih = min(i, m0 - 1) if ex else i
        for j in range(n1):
            jl = max(j - 1, 0) if ey else j; jh = min(j, m1 - 1) if ey else j
            for kk_ in range(n2):
                kl = max(kk_ - 1, 0) if ez else kk_; kh = min(kk_, m2 - 1) if ez else kk_
                # corners: (p lo, q lo), (p hi, q lo), (p lo, q hi), (p hi, q hi)
                a1i = ih if p == 0 else il; a1j = jh if p == 1 else jl; a1k = kh if p == 2 else kl
                a2i = ih if q == 0 else il; a2j = jh if q == 1 else jl; a2k = kh if q == 2 else kl
                v = 0.25 * (nu_c[il, jl, kl] + nu_c[a1i, a1j, a1k] + nu_c[a2i, a2j, a2k] + nu_c[ih, jh, kh])
                if ke and wd[i, j, kk_] > 0:
                    kv = 0.25 * (k[il, jl, kl] + k[a1i, a1j, a1k] + k[a2i, a2j, a2k] + k[ih, jh, kh])
                    v = _nu_wall(kv, wd[i, j, kk_])
                out[i, j, kk_] = v


@njit(parallel=True, cache=True)
def _k_edge_visc01(nu_c, k, ke, wd, out):
    _edge_visc(nu_c, k, ke, 0, 1, wd, out)


@njit(parallel=True, cache=True)
def _k_edge_visc02(nu_c, k, ke, wd, out):
    _edge_visc(nu_c, k, ke, 0, 2, wd, out)


@njit(parallel=True, cache=True)
def _k_edge_visc12(nu_c, k, ke, wd, out):
    _edge_visc(nu_c, k, ke, 1, 2, wd, out)


@njit(inline="always")
def _mterm(U, Uc, c, a, ne, nu_c, i, j, k, u0, h, tvd):
    """Advection and viscous term along axis a for velocity component c at the face (i, j, k)."""
    if a == c:
        vel = u0
        der = _ddx(_gv(Uc, c, a, i, j, k, -2), _gv(Uc, c, a, i, j, k, -1), u0,
                   _gv(Uc, c, a, i, j, k, 1), _gv(Uc, c, a, i, j, k, 2), vel, h, tvd)
        f1 = _at(nu_c, a, i, j, k, 0) * (_at(Uc, a, i, j, k, 1) - u0) / h       # viscosity at the cell centres
        f0 = _at(nu_c, a, i, j, k, -1) * (u0 - _at(Uc, a, i, j, k, -1)) / h
    else:
        Ua = U[a]                                                   # velocity a averaged to this c face
        vel = 0.25 * (_at2(Ua, c, -1, a, 0, i, j, k) + _at2(Ua, c, 0, a, 0, i, j, k)
                      + _at2(Ua, c, -1, a, 1, i, j, k) + _at2(Ua, c, 0, a, 1, i, j, k))
        der = _ddx(_gv(Uc, c, a, i, j, k, -2), _gv(Uc, c, a, i, j, k, -1), u0,
                   _gv(Uc, c, a, i, j, k, 1), _gv(Uc, c, a, i, j, k, 2), vel, h, tvd)
        f1 = _at(ne, a, i, j, k, 1) * (_gv(Uc, c, a, i, j, k, 1) - u0) / h       # viscosity on the edges
        f0 = _at(ne, a, i, j, k, 0) * (u0 - _gv(Uc, c, a, i, j, k, -1)) / h
    return -vel * der + (f1 - f0) / h


@njit(parallel=True, cache=True)
def _k_mom_u(U, us, nu_c, ne01, ne02, d, dt, tvd):
    """Predictor for u on the interior x faces: advection (upwind or TVD) and viscous terms along x, y, z."""
    u = U[0]
    n0, n1, n2 = u.shape
    for i_ in prange(1, n0 - 1):
        i = np.int64(i_)            # prange gives an unsigned index
        for j in range(n1):
            for k in range(n2):
                u0 = u[i, j, k]
                rhs = 0.0 + _mterm(U, u, 0, 0, ne01, nu_c, i, j, k, u0, d[0], tvd)
                rhs = rhs + _mterm(U, u, 0, 1, ne01, nu_c, i, j, k, u0, d[1], tvd)
                rhs = rhs + _mterm(U, u, 0, 2, ne02, nu_c, i, j, k, u0, d[2], tvd)
                us[i, j, k] = u0 + dt * rhs


@njit(parallel=True, cache=True)
def _k_mom_v(U, vs, nu_c, ne01, ne12, d, dt, tvd):
    """Predictor for v on the interior y faces."""
    v = U[1]
    n0, n1, n2 = v.shape
    for i_ in prange(n0):
        i = np.int64(i_)
        for j in range(1, n1 - 1):
            for k in range(n2):
                u0 = v[i, j, k]
                rhs = 0.0 + _mterm(U, v, 1, 0, ne01, nu_c, i, j, k, u0, d[0], tvd)
                rhs = rhs + _mterm(U, v, 1, 1, ne01, nu_c, i, j, k, u0, d[1], tvd)
                rhs = rhs + _mterm(U, v, 1, 2, ne12, nu_c, i, j, k, u0, d[2], tvd)
                vs[i, j, k] = u0 + dt * rhs


@njit(parallel=True, cache=True)
def _k_mom_w(U, ws, nu_c, ne02, ne12, T, d, dt, tvd, gb, Tref):
    """Predictor for w on the interior z faces, with buoyancy."""
    w = U[2]
    n0, n1, n2 = w.shape
    for i_ in prange(n0):
        i = np.int64(i_)
        for j in range(n1):
            for k in range(1, n2 - 1):
                u0 = w[i, j, k]
                rhs = 0.0 + _mterm(U, w, 2, 0, ne02, nu_c, i, j, k, u0, d[0], tvd)
                rhs = rhs + _mterm(U, w, 2, 1, ne12, nu_c, i, j, k, u0, d[1], tvd)
                rhs = rhs + _mterm(U, w, 2, 2, ne12, nu_c, i, j, k, u0, d[2], tvd)
                rhs = rhs + gb * (0.5 * (T[i, j, k - 1] + T[i, j, k]) - Tref)
                ws[i, j, k] = u0 + dt * rhs


@njit(parallel=True, cache=True)
def _k_fluxes(phi, U, inL, inR, phi_in, D, d, tvd, F0, F1, F2):
    """Face fluxes (advection + diffusion) of a cell-centred scalar. Inlet faces carry phi_in."""
    n0, n1, n2 = phi.shape
    for i_ in prange(n0 + 1):
        i = np.int64(i_)            # prange gives an unsigned index
        for j in range(n1):
            for k in range(n2):
                e = [0.0, 0.0, 0.0, 0.0]
                for s in range(4):
                    ii = i - 2 + s
                    if ii < 0:
                        e[s] = phi_in if inL[j, k] else phi[0, j, k]
                    elif ii > n0 - 1:
                        e[s] = phi_in if inR[j, k] else phi[n0 - 1, j, k]
                    else:
                        e[s] = phi[ii, j, k]
                vel = U[0][i, j, k]
                f = vel * _face(e[0], e[1], e[2], e[3], vel, tvd)
                if 0 < i < n0:
                    f = f - 0.5 * (D[i, j, k] + D[i - 1, j, k]) * (phi[i, j, k] - phi[i - 1, j, k]) / d[0]
                F0[i, j, k] = f
    for i_ in prange(n0):
        i = np.int64(i_)            # prange gives an unsigned index
        for j in range(n1 + 1):
            for k in range(n2):
                vel = U[1][i, j, k]
                f = vel * _face(phi[i, min(max(j - 2, 0), n1 - 1), k], phi[i, min(max(j - 1, 0), n1 - 1), k],
                                phi[i, min(j, n1 - 1), k], phi[i, min(j + 1, n1 - 1), k], vel, tvd)
                if 0 < j < n1:
                    f = f - 0.5 * (D[i, j, k] + D[i, j - 1, k]) * (phi[i, j, k] - phi[i, j - 1, k]) / d[1]
                F1[i, j, k] = f
        for j in range(n1):
            F2[i, j, 0] = 0.0
            for k in range(1, n2 + 1):
                vel = U[2][i, j, k]
                f = vel * _face(phi[i, j, max(k - 2, 0)], phi[i, j, k - 1], phi[i, j, min(k, n2 - 1)],
                                phi[i, j, min(k + 1, n2 - 1)], vel, tvd)
                if k < n2:
                    f = f - 0.5 * (D[i, j, k] + D[i, j, k - 1]) * (phi[i, j, k] - phi[i, j, k - 1]) / d[2]
                F2[i, j, k] = f


@njit(parallel=True, cache=True)
def _k_div(F0, F1, F2, d, out):
    n0, n1, n2 = out.shape
    for i_ in prange(n0):
        i = np.int64(i_)            # prange gives an unsigned index
        for j in range(n1):
            for k in range(n2):
                out[i, j, k] = (0.0 + (F0[i + 1, j, k] - F0[i, j, k]) / d[0] + (F1[i, j + 1, k] - F1[i, j, k]) / d[1]
                                + (F2[i, j, k + 1] - F2[i, j, k]) / d[2])


@njit(parallel=True, cache=True)
def _k_energy(T, div, S, dt, out):
    n0, n1, n2 = T.shape
    for i_ in prange(n0):
        i = np.int64(i_)            # prange gives an unsigned index
        for j in range(n1):
            for k in range(n2):
                out[i, j, k] = T[i, j, k] - dt * div[i, j, k] + dt * S[i, j, k] / (RHO * CP)


@njit(inline="always")
def _shear(U, p, q, i, j, k, sp_, sq_, d):
    """du_p/dx_q + du_q/dx_p on the edge (i + sp_ along p, j/k + sq_ along q), mirrored at walls."""
    Up, Uq = U[p], U[q]
    # U_p on face (ip) along p, cells (iq-1, iq) along q
    a = (_at2_mirror(Up, p, sp_, q, sq_, i, j, k) - _at2_mirror(Up, p, sp_, q, sq_ - 1, i, j, k)) / d[q]
    b = (_at2_mirror(Uq, q, sq_, p, sp_, i, j, k) - _at2_mirror(Uq, q, sq_, p, sp_ - 1, i, j, k)) / d[p]
    return a + b


@njit(inline="always")
def _at2_mirror(A, a, sa, b, sb, i, j, k):
    """A shifted sa along a and sb along b; outside the array along b the value is mirrored (minus)."""
    if a == 0:
        i += sa
    elif a == 1:
        j += sa
    else:
        k += sa
    if b == 0:
        i += sb
    elif b == 1:
        j += sb
    else:
        k += sb
    n0, n1, n2 = A.shape
    sign = 1.0
    if i < 0 or j < 0 or k < 0 or i > n0 - 1 or j > n1 - 1 or k > n2 - 1:
        sign = -1.0
    return sign * A[min(max(i, 0), n0 - 1), min(max(j, 0), n1 - 1), min(max(k, 0), n2 - 1)]


@njit(inline="always")
def _shear_c(U, p, q, i, j, k, d):
    """Shear du_p/dx_q + du_q/dx_p at the cell centre: average of the four edges around it."""
    return 0.25 * (_shear(U, p, q, i, j, k, 0, 0, d) + _shear(U, p, q, i, j, k, 1, 0, d)
                   + _shear(U, p, q, i, j, k, 0, 1, d) + _shear(U, p, q, i, j, k, 1, 1, d))


@njit(parallel=True, cache=True)
def _k_production(U, nut, k, wall_cell, ypw, d, P):
    """Shear production of k at the cell centres (log-law value in the wall cells)."""
    n0, n1, n2 = k.shape
    for i_ in prange(n0):
        i = np.int64(i_)            # prange gives an unsigned index
        for j in range(n1):
            for kk_ in range(n2):
                e0 = (U[0][i + 1, j, kk_] - U[0][i, j, kk_]) / d[0]
                e1 = (U[1][i, j + 1, kk_] - U[1][i, j, kk_]) / d[1]
                e2 = (U[2][i, j, kk_ + 1] - U[2][i, j, kk_]) / d[2]
                s = 2 * (0.0 + e0 ** 2 + e1 ** 2 + e2 ** 2)
                s = s + _shear_c(U, 0, 1, i, j, kk_, d) ** 2
                s = s + _shear_c(U, 0, 2, i, j, kk_, d) ** 2
                s = s + _shear_c(U, 1, 2, i, j, kk_, d) ** 2
                val = nut[i, j, kk_] * s
                if wall_cell[i, j, kk_]:
                    uc = 0.5 * (U[0][i + 1, j, kk_] + U[0][i, j, kk_])
                    vc = 0.5 * (U[1][i, j + 1, kk_] + U[1][i, j, kk_])
                    wc = 0.5 * (U[2][i, j, kk_ + 1] + U[2][i, j, kk_])
                    Up = np.sqrt(uc ** 2 + vc ** 2 + wc ** 2)
                    y = ypw[i, j, kk_]; kc = k[i, j, kk_]
                    tau = _nu_wall(kc, y) * Up / y
                    val = tau * CMU ** 0.25 * np.sqrt(kc) / (KAP * y)
                P[i, j, kk_] = val


@njit(parallel=True, cache=True)
def _k_keps_update(k, eps, rk_div, re_div, P, nut, T_old, wall_cell, ypw, dz, dt, gneg, Pr_t, kn, en):
    """Implicit-sink update of k and epsilon (rk_div, re_div are the flux divergences)."""
    n0, n1, n2 = k.shape
    for i_ in prange(n0):
        i = np.int64(i_)            # prange gives an unsigned index
        for j in range(n1):
            for z in range(n2):
                if z == 0:
                    dT = (T_old[i, j, 1] - T_old[i, j, 0]) / dz
                elif z == n2 - 1:
                    dT = (T_old[i, j, n2 - 1] - T_old[i, j, n2 - 2]) / dz
                else:
                    dT = (T_old[i, j, z + 1] - T_old[i, j, z - 1]) / (2.0 * dz)
                Gb = gneg * nut[i, j, z] / Pr_t * dT
                Gp, Gm = max(Gb, 0.0), max(-Gb, 0.0)
                kc, ec, Pc = k[i, j, z], eps[i, j, z], P[i, j, z]
                k_new = (kc + dt * (-rk_div[i, j, z] + Pc + Gp)) / (1 + dt * (ec + Gm) / kc)
                e_new = (ec + dt * (-re_div[i, j, z] + C1 * ec / kc * (Pc + Gp))) / (1 + dt * C2 * ec / kc)
                kv = max(k_new, 1e-10); ev = max(e_new, 1e-12)
                if wall_cell[i, j, z]:
                    ev = CMU ** 0.75 * kv ** 1.5 / (KAP * ypw[i, j, z])
                kn[i, j, z] = kv; en[i, j, z] = ev


@njit(parallel=True, cache=True)
def _k_bc_rhs(u, v, w, bL, bR, bT, U_in, d, dt, rhs):
    n0, n1, n2 = w.shape[0], w.shape[1], w.shape[2] - 1
    for j in range(n1):
        for k in range(n2):
            u[0, j, k] = U_in if bL[j, k] == INLET else (u[1, j, k] if bL[j, k] == OUTLET else 0.0)
            u[n0, j, k] = -U_in if bR[j, k] == INLET else (u[n0 - 1, j, k] if bR[j, k] == OUTLET else 0.0)
    for i in range(n0):
        for k in range(n2):
            v[i, 0, k] = 0.0; v[i, n1, k] = 0.0
        for j in range(n1):
            w[i, j, 0] = 0.0
            w[i, j, n2] = w[i, j, n2 - 1] if bT[i, j] == OUTLET else 0.0
    for i_ in prange(n0):
        i = np.int64(i_)            # prange gives an unsigned index
        for j in range(n1):
            for k in range(n2):
                rhs[(i * n1 + j) * n2 + k] = (0.0 + (u[i + 1, j, k] - u[i, j, k]) / d[0] + (v[i, j + 1, k] - v[i, j, k]) / d[1]
                                              + (w[i, j, k + 1] - w[i, j, k]) / d[2]) / dt


@njit(parallel=True, cache=True)
def _k_correct(u, v, w, p, bL, bR, bT, d, dt):
    n0, n1, n2 = p.shape
    for i_ in prange(n0):
        i = np.int64(i_)            # prange gives an unsigned index
        for j in range(n1):
            for k in range(n2):
                if i > 0:
                    u[i, j, k] -= dt * (p[i, j, k] - p[i - 1, j, k]) / d[0]
                if j > 0:
                    v[i, j, k] -= dt * (p[i, j, k] - p[i, j - 1, k]) / d[1]
                if k > 0:
                    w[i, j, k] -= dt * (p[i, j, k] - p[i, j, k - 1]) / d[2]
    for j in range(n1):
        for k in range(n2):
            if bL[j, k] == OUTLET:
                u[0, j, k] -= dt * (p[0, j, k] - 0.0) / (d[0] / 2)
            if bR[j, k] == OUTLET:
                u[n0, j, k] -= dt * (0.0 - p[n0 - 1, j, k]) / (d[0] / 2)
    for i in range(n0):
        for j in range(n1):
            if bT[i, j] == OUTLET:
                w[i, j, n2] -= dt * (0.0 - p[i, j, n2 - 1]) / (d[2] / 2)


@njit(parallel=True, cache=True)
def _k_speed(u, v, w, out):
    n0, n1, n2 = out.shape
    for i_ in prange(n0):
        i = np.int64(i_)            # prange gives an unsigned index
        for j in range(n1):
            for k in range(n2):
                uc = 0.5 * (u[i + 1, j, k] + u[i, j, k]); vc = 0.5 * (v[i, j + 1, k] + v[i, j, k])
                wc = 0.5 * (w[i, j, k + 1] + w[i, j, k])
                out[i, j, k] = np.sqrt(uc ** 2 + vc ** 2 + wc ** 2)


@njit(parallel=True, cache=True)
def _k_add(acc, a, dt):
    fa, fb = acc.ravel(), a.ravel()
    for m in prange(fa.size):
        fa[m] += dt * fb[m]


# ---------------------------------------------------------------------------------------------
# multigrid: room_cfd_3d.Multigrid (SciPy sparse products, which are already compiled code), with the
# dot products done here instead of by BLAS, whose threads would compete with the Numba threads.
# ---------------------------------------------------------------------------------------------
@njit(cache=True)
def _dot(a, b):
    s = 0.0
    for m in range(a.size):
        s += a[m] * b[m]
    return s


class FastMultigrid(Multigrid):
    def solve(self, b, x0, tol, maxit=200):
        A = self.A[0]
        x = x0.copy(); r = b - A @ x
        bnorm = max(np.sqrt(_dot(b, b)), 1e-300)
        if np.sqrt(_dot(r, r)) <= tol * bnorm:
            return x
        z = self.vcycle(r); d = z.copy(); rz = _dot(r, z)
        for _ in range(maxit):
            Ad = A @ d; a = rz / _dot(d, Ad)
            x += a * d; r -= a * Ad; self.iters += 1
            if np.sqrt(_dot(r, r)) <= tol * bnorm:
                break
            z = self.vcycle(r); rz, rz_old = _dot(r, z), rz
            d = z + (rz / rz_old) * d
        return x


# ---------------------------------------------------------------------------------------------
# the solver
# ---------------------------------------------------------------------------------------------
def run(case: Case, verbose=False, monitor_every=50):
    """Run the case and return time-averaged fields, as room_cfd_3d.run."""
    n = (case.nx, case.ny, case.nz)
    d = (case.L / case.nx, case.W / case.ny, case.H / case.nz)
    nx, ny, nz = n; dx, dy, dz = d
    da = np.array(d)
    shp = [tuple(n[k] + (1 if k == c else 0) for k in range(3)) for c in range(3)]
    bnd = boundaries(case)
    bL, bR, bT = bnd[(0, 0)], bnd[(0, 1)], bnd[(2, 1)]
    inL, inR = bL == INLET, bR == INLET
    A_in = (inL.sum() + inR.sum()) * dy * dz
    U_in = case.q / A_in
    h_in = A_in / case.W

    U = tuple(np.zeros(s) for s in shp)
    Q_tot = sum(b.power for b in case.heat) + sum(f.power for f in case.floor_flux)
    T_mix = case.T_in + Q_tot / (RHO * CP * case.q)
    T0 = T_mix if case.T_room0 is None else case.T_room0
    T = np.full(n, float(T0)); Tref = float(T0)
    beta = 1.0 / (273.15 + Tref)

    xc, yc, zc = [(np.arange(n[k]) + 0.5) * d[k] for k in range(3)]
    X, Y, Z = np.meshgrid(xc, yc, zc, indexing="ij")
    lwall = np.minimum.reduce([X, case.L - X, Y, case.W - Y, Z, case.H - Z])
    S = np.zeros(n)
    for b in case.heat:
        cells = (X > b.x0) & (X < b.x1) & (Y > b.y0) & (Y < b.y1) & (Z > b.z0) & (Z < b.z1)
        S[cells] += b.power / (cells.sum() * dx * dy * dz)
    qfloor = np.zeros((nx, ny))
    for f in case.floor_flux:
        sel = ((xc > f.x0) & (xc < f.x1))[:, None] & ((yc > f.y0) & (yc < f.y1))[None, :]
        qfloor[sel] += f.power / (sel.sum() * dx * dy)

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

    # wall distance on the edges that get the log-law viscosity (0 = none), as in room_cfd_3d.edge_viscosity
    pairs = ((0, 1), (0, 2), (1, 2))
    wd = {}
    for p, q in pairs:
        es = tuple(n[a] + (1 if a in (p, q) else 0) for a in range(3))
        w_ = np.zeros(es)
        for wa, other in ((q, p), (p, q)):
            for side, pos in ((0, 0), (1, n[wa])):
                m = bnd[(wa, side)]
                oth = other if other < wa else other - 1
                e = _edge(m, oth)
                sel = (_sl(e, oth, 0, -1) == WALL) & (_sl(e, oth, 1, None) == WALL)
                idx = [slice(None)] * 3; idx[wa] = pos
                w_[tuple(idx)] = np.where(sel, d[wa] / 2, w_[tuple(idx)])
        wd[(p, q)] = w_
    ne = {pq: np.zeros(wd[pq].shape) for pq in pairs}

    # pressure Poisson matrix, as in room_cfd_3d
    I = [sp.identity(m, format="csr") for m in n]
    Amat = (sp.kron(sp.kron(_lap1(nx, dx), I[1]), I[2]) + sp.kron(sp.kron(I[0], _lap1(ny, dy)), I[2])
            + sp.kron(sp.kron(I[0], I[1]), _lap1(nz, dz))).tolil()
    extra = np.zeros(n)
    extra[0][bL == OUTLET] -= 2.0 / dx ** 2
    extra[-1][bR == OUTLET] -= 2.0 / dx ** 2
    extra[:, :, -1][bT == OUTLET] -= 2.0 / dz ** 2
    Amat = (Amat.tocsr() + sp.diags(extra.ravel())).tocsc()
    if case.pressure == "multigrid":
        mgs = FastMultigrid(-Amat, n); p_last = np.zeros(Amat.shape[0])

        def solve(rhs):
            nonlocal p_last
            p_last = mgs.solve(-rhs, p_last, case.p_tol)
            return p_last
    else:
        solve = splu(Amat, permc_spec="MMD_AT_PLUS_A").solve

    rhs = np.zeros(nx * ny * nz)
    _k_bc_rhs(U[0], U[1], U[2], bL, bR, bT, U_in, da, 1.0, rhs)
    F = [np.zeros(s) for s in shp]; Fk = [np.zeros(s) for s in shp]
    div = np.zeros(n); div2 = np.zeros(n); P = np.zeros(n); spd = np.zeros(n)
    avg = dict(u=np.zeros(shp[0]), v=np.zeros(shp[1]), w=np.zeros(shp[2]), T=np.zeros(n), speed=np.zeros(n),
               nu_t=np.zeros(n), k=np.zeros(n))
    wa = 0.0
    t, step, t_avg0, h = 0.0, 0, case.t_end - case.t_avg, min(d)
    tvd = case.advection == "tvd"
    cfl = 0.25 if tvd else 0.4
    hist = {key: [] for key in ("t", "du", "dv", "dw", "dT", "div", "imb", "v_floor", "T_exh")}
    mon_pt = (min(int(1.0 / dx), nx - 1), ny // 2, min(int(0.1 / dz), nz - 1))
    outR, outL, outT = bR == OUTLET, bL == OUTLET, bT == OUTLET

    while t < case.t_end:
        mon = step % monitor_every == 0
        if mon:
            U0, T0_ = [a.copy() for a in U], T.copy()
        if ke:
            nu_c = NU_AIR + CMU * k * k / eps
        elif case.turbulence == "constant":
            nu_c = np.full(n, NU_AIR + case.nu_t)
        else:
            _k_speed(U[0], U[1], U[2], spd)
            nu_c = NU_AIR + 0.03874 * spd * lwall
        _k_edge_visc01(nu_c, k, ke, wd[(0, 1)], ne[(0, 1)])
        _k_edge_visc02(nu_c, k, ke, wd[(0, 2)], ne[(0, 2)])
        _k_edge_visc12(nu_c, k, ke, wd[(1, 2)], ne[(1, 2)])
        alpha_c = nu_c / case.Pr_t
        umax = max(max(np.abs(a).max() for a in U), U_in, 0.05)
        dt = min(cfl * h / umax, 0.15 * h * h / nu_c.max(), 0.5)

        # ---- momentum ----
        Us = tuple(a.copy() for a in U)
        _k_mom_u(U, Us[0], nu_c, ne[(0, 1)], ne[(0, 2)], da, dt, tvd)
        _k_mom_v(U, Us[1], nu_c, ne[(0, 1)], ne[(1, 2)], da, dt, tvd)
        _k_mom_w(U, Us[2], nu_c, ne[(0, 2)], ne[(1, 2)], T, da, dt, tvd, G * beta, Tref)

        # ---- projection ----
        _k_bc_rhs(Us[0], Us[1], Us[2], bL, bR, bT, U_in, da, dt, rhs)
        p = solve(rhs).reshape(n)
        _k_correct(Us[0], Us[1], Us[2], p, bL, bR, bT, da, dt)
        U = Us
        if mon:
            div_max = np.abs(sum(np.diff(U[c], axis=c) / d[c] for c in range(3))).max()

        # ---- energy ----
        _k_fluxes(T, U, inL, inR, case.T_in, alpha_c, da, tvd, F[0], F[1], F[2])
        F[2][:, :, 0] += qfloor / (RHO * CP)              # heat flux up into the air through the floor
        _k_div(F[0], F[1], F[2], da, div)
        T_old = T
        T = np.empty(n); _k_energy(T_old, div, S, dt, T)

        # ---- k and epsilon ----
        if ke:
            nut = nu_c - NU_AIR
            _k_production(U, nut, k, wall_cell, ypw, da, P)
            _k_fluxes(k, U, inL, inR, k_in, NU_AIR + nut / SK, da, False, Fk[0], Fk[1], Fk[2])
            _k_div(Fk[0], Fk[1], Fk[2], da, div)
            _k_fluxes(eps, U, inL, inR, e_in, NU_AIR + nut / SE, da, False, Fk[0], Fk[1], Fk[2])
            _k_div(Fk[0], Fk[1], Fk[2], da, div2)
            kn, en = np.empty(n), np.empty(n)
            _k_keps_update(k, eps, div, div2, P, nut, T_old, wall_cell, ypw, dz, dt, -G * beta, case.Pr_t, kn, en)
            k, eps = kn, en

        if mon:
            rms = lambda a: float(np.sqrt(np.mean(a * a)))
            q_open = ((F[0][-1].sum() - F[0][0].sum()) * dy * dz + F[2][:, :, -1].sum() * dx * dy)
            T_exh = np.concatenate([T[-1][outR], T[0][outL], T[:, :, -1][outT]]).mean()
            _k_speed(U[0], U[1], U[2], spd)
            for key, val in (("t", t + dt), ("du", rms(U[0] - U0[0]) / dt), ("dv", rms(U[1] - U0[1]) / dt),
                             ("dw", rms(U[2] - U0[2]) / dt), ("dT", rms(T - T0_) / dt), ("div", div_max),
                             ("imb", 100 * (RHO * CP * q_open - Q_tot) / max(Q_tot, 1.0)),
                             ("v_floor", float(spd[mon_pt])), ("T_exh", float(T_exh))):
                hist[key].append(val)
        t += dt; step += 1
        if t >= t_avg0:
            _k_speed(U[0], U[1], U[2], spd)
            for key, val in (("u", U[0]), ("v", U[1]), ("w", U[2]), ("T", T), ("speed", spd), ("nu_t", nu_c), ("k", k)):
                _k_add(avg[key], val, dt)
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
