"""Appendix C figure: the IEA Annex 20 room in 3D against the measurements and the 2D model on the same x-z grid.

Runs the room (9 x 3 x 3 m, slot across the full width, isothermal, k-epsilon) with room_cfd_3d_numba.py on
72 x 18 x 36 cells (30 min simulated, roughly half an hour), and the 2D model on 72 x 36 cells. Pass a saved
3D result pickle to plot without running it. Measurements from ../background/airflow/. Writes to
../figures/appendix-cfd-3d/.
"""
import sys, pickle
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import room_cfd as r2
from pathlib import Path
import room_cfd_3d_numba as m

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "figures" / "appendix-cfd-3d"; OUT.mkdir(parents=True, exist_ok=True)
H, L, U0 = 3.0, 9.0, 0.455; h, t = 0.056 * H, 0.16 * H
if len(sys.argv) > 1:
    r3 = pickle.load(open(sys.argv[1], "rb"))
else:
    nx, ny, nz, W = 72, 18, 36, 3.0
    dz = H / nz; h_in = sum(1 for k in range(nz) if (k + 0.5) * dz > H - h) * dz
    c = m.Case(L=L, W=W, H=H, nx=nx, ny=ny, nz=nz, ach=U0 * h_in * W * 3600 / (L * H * W), T_in=20.0, T_room0=20.0,
               inlet=m.Opening("left", H - h, H), outlet=m.Opening("right", 0.0, t), t_end=1800, t_avg=600)
    r3 = m.run(c, verbose=True)
c3 = r3["case"]
c2 = r2.Case(L=L, H=H, W=1.0, nx=c3.nx, ny=c3.nz, ach=c3.ach, T_in=20.0, T_room0=20.0, inlet=r2.Opening("left", H - h, H),
             outlet=r2.Opening("right", 0.0, t), t_end=1800, t_avg=600)
q2 = r2.run(c2)
MEAS = HERE.parent / "background" / "airflow" / "nielsen-1990-annex20-2d-measurements.csv"
meas = {}
for line in MEAS.read_text().splitlines()[1:]:
    p, cc, u = line.split(","); meas.setdefault(p, []).append((float(cc), float(u)))
j = c3.ny // 2
models = {"3D, mid-width": (r3["u"][:, j, :], r3["z"], r3["dx"]), "2D, same x-z mesh": (q2["u"], q2["y"], q2["dx"])}
models["3D, 1/4 width"] = (r3["u"][:, c3.ny // 4, :], r3["z"], r3["dx"])

def line(u, z, dx, p):
    un = u / U0; xf = np.arange(un.shape[0]) * dx
    if p in ("x=H", "x=2H"):
        i = int(round((H if p == "x=H" else 2 * H) / dx)); return un[i], z / H
    zl = h / 2 if p == "y=h/2" else H - h / 2
    return xf / H, np.array([np.interp(zl, z, ui) for ui in un])

titles = {"x=H": "x = H", "x=2H": "x = 2H", "y=h/2": "z = h/2 (floor)", "y=H-h/2": "z = H − h/2 (ceiling)"}
cols = {"3D, mid-width": "#2a78d6", "2D, same x-z mesh": "#eb6834", "3D, 1/4 width": "#2aa36b"}
fig, ax = plt.subplots(1, 4, figsize=(13, 4.0))
for a, p in zip(ax, titles):
    cm, um = np.array(meas[p]).T
    for lab, (u, z, dx) in models.items():
        X, Y = line(u, z, dx, p); a.plot(X, Y, color=cols.get(lab, "0.4"), lw=1.5, label=lab)
        mod = np.interp(cm, Y, X) if p.startswith("x") else np.interp(cm, X, Y)
        print(f"{lab:20s} {p:8s} RMS error u/u0 {np.sqrt(np.mean((mod - um) ** 2)):.3f}")
    if p.startswith("x"):
        a.plot(um, cm, "ko", ms=3.5, label="Measured"); a.set_xlabel("u/u$_0$"); a.set_ylabel("z/H"); a.axvline(0, color="0.7", lw=0.8)
    else:
        a.plot(cm, um, "ko", ms=3.5, label="Measured"); a.set_xlabel("x/H"); a.set_ylabel("u/u$_0$"); a.axhline(0, color="0.7", lw=0.8)
    a.set_title(titles[p], fontsize=10); a.grid(alpha=0.25); a.spines[["top", "right"]].set_visible(False)
ax[0].legend(fontsize=8, frameon=False)
fig.tight_layout(); fig.savefig(OUT / "annex20-3d-profiles.png", dpi=150, bbox_inches="tight")
# net flow through the vertical lines (continuity check, as for the measurements)
for lab, (u, z, dx) in models.items():
    for xl in (H, 2 * H):
        i = int(round(xl / dx)); print(f"{lab:20s} net flow at x = {xl/H:.0f}H: {np.trapezoid(u[i], z) / (U0 * h):+.2f} (inlet = 1)")
