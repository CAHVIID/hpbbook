"""Compare room_cfd.py (NumPy) with room_cfd_numba.py (Numba): run time and results.

    python compare_numba.py [nx ny t_end]

Runs the window case of cfd_examples.py (16 °C supply, 6 ACH, gains for 26 °C) with both
versions and with the three turbulence models, and prints run times and the largest differences.
"""
import sys, time
import numpy as np
import room_cfd as A, room_cfd_numba as B

nx, ny, t_end = (int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])) if len(sys.argv) > 3 else (100, 50, 300.0)


def case(mod, t=None, **kw):
    t = t or t_end
    c = mod.Case(inlet=mod.Opening("left", 0.9, 2.1), outlet=mod.Opening("right", 2.3, 2.4), T_in=16.0, ach=6,
                 nx=nx, ny=ny, t_end=t, t_avg=t / 3, **kw)
    c.heat = [mod.HeatBlock(2.3, 2.7, 0.0, 1.2, 1.2 * 1005 * c.q * 10.0 / c.W)]
    return c


t0 = time.time(); B.run(case(B, t=1.0)); print(f"Numba compile (first call only): {time.time() - t0:.1f} s")
for kw in (dict(), dict(turbulence="chen-xu"), dict(advection="upwind"), dict(turbulence="constant")):
    t0 = time.time(); ra = A.run(case(A, **kw)); ta = time.time() - t0
    t0 = time.time(); rb = B.run(case(B, **kw)); tb = time.time() - t0
    d = {f: np.abs(ra[f] - rb[f]).max() for f in ("u", "v", "T", "speed", "nu_t")}
    print(f"{str(kw or 'default (k-epsilon, TVD)'):34s} NumPy {ta:6.2f} s  Numba {tb:6.2f} s  x{ta / tb:4.1f}  "
          f"steps {ra['steps']}/{rb['steps']}  max diff u {d['u']:.1e} T {d['T']:.1e} nu_t {d['nu_t']:.1e}")
