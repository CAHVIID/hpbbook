"""Single-sided buoyancy and wind flow through a side-hung and a bottom-hung window.

Draft calculations for the side-hung window chapter. The buoyancy flow integrates the
orifice equation over the height of the gap, so the shape of the opening matters:
  side-hung (hinge at the side, angle a): vertical gap of width s = min(2 w sin(a/2), w)
                                           over the full sash height h
  bottom-hung (hinge at the bottom, stroke s at the top): two triangular side gaps whose
                                           width grows from 0 to s, plus a top slot w*s
The neutral plane is found from the mass balance. Wind: Warren & Parkins (1985),
Q = 0.025 A v. Combined as Q = sqrt(Q_stack^2 + Q_wind^2) (DIN/TS 4108-8 style).
"""
import numpy as np

G, T_REF, RHO, CP, CD = 9.81, 293.15, 1.2, 1005.0, 0.6


def _flows(width, h, zn, dT, top_slot=0.0, n=2000):
    """Inflow and outflow (m3/s) for gap width(z) and neutral plane height zn."""
    z = np.linspace(0, h, n)
    dz = z[1] - z[0]
    b = width(z)
    v = np.sqrt(2 * G * abs(dT) / T_REF * np.abs(z - zn))
    qin = CD * np.sum((b * v)[z < zn]) * dz
    qout = CD * np.sum((b * v)[z >= zn]) * dz
    qout += CD * top_slot * np.sqrt(2 * G * abs(dT) / T_REF * max(h - zn, 0))
    return qin, qout


def stack_flow(width, h, dT, top_slot=0.0):
    """Buoyancy-driven exchange flow (m3/s) and neutral plane height (m)."""
    lo, hi = 0.0, h
    for _ in range(60):
        zn = 0.5 * (lo + hi)
        qin, qout = _flows(width, h, zn, dT, top_slot)
        lo, hi = (zn, hi) if qin < qout else (lo, zn)
    return qin, zn


def side_hung(w, h, angle_deg):
    s = min(2 * w * np.sin(np.radians(angle_deg) / 2), w)
    return (lambda z: np.full_like(z, s)), 0.0, s * h


def bottom_hung(w, h, stroke):
    return (lambda z: 2 * stroke * z / h), w * stroke, stroke * (w + h)


def total_flow(kind, dT, wind, **geo):
    width, top, area = kind(**geo)
    qs, zn = stack_flow(width, geo["h"], dT, top)
    qw = 0.025 * area * wind
    return np.hypot(qs, qw), qs, qw, area, zn


if __name__ == "__main__":
    W, H, VOL = 0.8, 1.3, 4 * 5 * 2.6
    cases = {
        "side-hung 90 deg": (side_hung, dict(w=W, h=H, angle_deg=90)),
        "side-hung 30 deg": (side_hung, dict(w=W, h=H, angle_deg=30)),
        "side-hung 10 deg": (side_hung, dict(w=W, h=H, angle_deg=10)),
        "bottom-hung 120 mm": (bottom_hung, dict(w=W, h=H, stroke=0.12)),
    }
    for dT in (2, 5, 20):
        for wind in (0, 2):
            print(f"\ndT = {dT} K, wind = {wind} m/s")
            for name, (kind, geo) in cases.items():
                q, qs, qw, a, zn = total_flow(kind, dT, wind, **geo)
                print(f"  {name:20s} A = {a:5.3f} m2  zn = {zn:4.2f} m  Q_stack = {qs*3600:5.0f}"
                      f"  Q_wind = {qw*3600:4.0f}  Q = {q*3600:5.0f} m3/h  n = {q*3600/VOL:4.1f} 1/h"
                      f"  P = {RHO*CP*q*dT/1000:4.2f} kW")
