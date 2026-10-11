"""Validation of room_cfd.py against the IEA Annex 20 two-dimensional test case (Nielsen 1990, case 2D1).

Isothermal room, L = 9 m, H = 3 m, inlet slot h = 0.168 m under the ceiling, outlet t = 0.48 m at the
floor of the opposite wall, u0 = 0.455 m/s (Re = 5000), inlet k = 1.5 (0.04 u0)^2, eps = k^1.5 / (h/10).
Runs k-epsilon and Chen & Xu and compares u/u0 with the measurements in
../background/airflow/nielsen-1990-annex20-2d-measurements.csv. Writes to ../figures/appendix-cfd/.

    python cfd_annex20.py [ny]        # ny = 107 (default, about 35 min per run) or 54 (about 5 min)

Contact: Christian Hviid, cahv@dtu.dk. Use at own risk; see the disclaimer in room_cfd.py.
"""
import sys
from pathlib import Path
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from room_cfd import Case, Opening, run

HERE = Path(__file__).parent
OUT = HERE.parent / "figures" / "appendix-cfd"; OUT.mkdir(parents=True, exist_ok=True)
MEAS = HERE.parent / "background" / "airflow" / "nielsen-1990-annex20-2d-measurements.csv"
H, L, U0 = 3.0, 9.0, 0.455
h, t = 0.056 * H, 0.16 * H
ny = int(sys.argv[1]) if len(sys.argv) > 1 else 107
nx, dy = 3 * ny, H / ny
h_in = sum(1 for j in range(ny) if (j + 0.5) * dy > H - h) * dy     # slot height on the grid
ach = U0 * h_in * 3600 / (L * H)                                       # so the inlet speed is exactly u0

res = {}
for label, turb in (("k-ε", "k-epsilon"), ("Chen & Xu", "chen-xu")):
    c = Case(L=L, H=H, W=1.0, nx=nx, ny=ny, ach=ach, T_in=20.0, T_room0=20.0, inlet=Opening("left", H - h, H),
             outlet=Opening("right", 0.0, t), turbulence=turb, Tu_in=0.04, t_end=1800, t_avg=600)
    res[label] = run(c)
    print(label, "done, inlet speed", round(res[label]["U_in"], 4), flush=True)

meas = {}
for line in MEAS.read_text().splitlines()[1:]:
    p, cc, u = line.split(","); meas.setdefault(p, []).append((float(cc), float(u)))

def model_line(r, p):
    un = r["u"] / U0; xf = np.arange(un.shape[0]) * r["dx"]
    if p in ("x=H", "x=2H"):
        i = int(round((H if p == "x=H" else 2 * H) / r["dx"])); return un[i], r["y"] / H
    yl = h / 2 if p == "y=h/2" else H - h / 2
    return xf / H, np.array([np.interp(yl, r["y"], ui) for ui in un])

titles = {"x=H": "x = H", "x=2H": "x = 2H", "y=h/2": "y = h/2 (floor)", "y=H-h/2": "y = H − h/2 (ceiling)"}
colors = {"k-ε": "#2a78d6", "Chen & Xu": "#eb6834"}
fig, ax = plt.subplots(1, 4, figsize=(13, 4.0))
for a, p in zip(ax, titles):
    cm, um = np.array(meas[p]).T
    for label, r in res.items():
        X, Y = model_line(r, p); a.plot(X, Y, color=colors[label], lw=1.6, label=label)
        mod = np.interp(cm, Y, X) if p.startswith("x") else np.interp(cm, X, Y)
        print(f"{label:10s} {p:8s} RMS error u/u0 {np.sqrt(np.mean((mod - um) ** 2)):.3f}")
    if p.startswith("x"):
        a.plot(um, cm, "ko", ms=3.5, label="Measured"); a.set_xlabel("u/u$_0$"); a.set_ylabel("y/H"); a.axvline(0, color="0.7", lw=0.8)
    else:
        a.plot(cm, um, "ko", ms=3.5, label="Measured"); a.set_xlabel("x/H"); a.set_ylabel("u/u$_0$"); a.axhline(0, color="0.7", lw=0.8)
    a.set_title(titles[p], fontsize=10); a.grid(alpha=0.25); a.spines[["top", "right"]].set_visible(False)
ax[0].legend(fontsize=8, frameon=False)
fig.tight_layout(); fig.savefig(OUT / "annex20-profiles.png", dpi=150, bbox_inches="tight")

fig, axs = plt.subplots(2, 1, figsize=(9, 6.2), sharex=True)
for a, (label, r) in zip(axs, res.items()):
    uc = 0.5 * (r["u"][1:] + r["u"][:-1]); vc = 0.5 * (r["v"][:, 1:] + r["v"][:, :-1])
    im = a.contourf(r["x"], r["y"], r["speed"].T / U0, np.linspace(0, 1, 21), cmap="viridis", extend="max")
    a.streamplot(r["x"], r["y"], uc.T, vc.T, color="w", density=1.3, linewidth=0.6, arrowsize=0.7)
    a.set_aspect("equal"); a.set_title(label, fontsize=10); a.set_ylabel("Height (m)")
axs[1].set_xlabel("x (m)")
fig.colorbar(im, ax=axs, shrink=0.8, label="Speed / u$_0$")
fig.savefig(OUT / "annex20-fields.png", dpi=150, bbox_inches="tight")
