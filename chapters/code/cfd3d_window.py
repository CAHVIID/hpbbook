"""Appendix C figure: full-width window against a 1.2 m wide window in 3D (16 °C supply, 6 ACH, gains for 26 °C).

Runs both cases with room_cfd_3d_numba.py (25 x 20 x 25 cells, 30 min, about 5 min each) and plots the mean air
speed at 0.1 m. Pass two saved result pickles (full, narrow) to plot without running. Writes to ../figures/appendix-cfd-3d/.
"""
import sys, pickle
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import room_cfd_3d_numba as m

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "figures" / "appendix-cfd-3d"; OUT.mkdir(parents=True, exist_ok=True)


def case(y0, y1):
    c = m.Case(nx=25, ny=20, nz=25, t_end=1800, t_avg=600, T_in=16.0,
               inlet=m.Opening("left", 0.9, 2.1, y0, y1), outlet=m.Opening("right", 2.3, 2.4))
    c.heat = [m.HeatBlock(2.3, 2.7, 0.0, c.W, 0.0, 1.2, 1.2 * 1005 * c.q * (26 - c.T_in))]
    return c


if len(sys.argv) > 2:
    runs = [pickle.load(open(p, "rb")) for p in sys.argv[1:3]]
else:
    runs = [m.run(case(None, None), verbose=True), m.run(case(1.4, 2.6), verbose=True)]
res = dict(zip(["Full-width window (4 m)", "Window 1.2 m wide"], runs))

fig, axs = plt.subplots(1, 2, figsize=(11, 4.4), sharey=True)
for a, (lab, r) in zip(axs, res.items()):
    oz = m.occupied_zone(r)
    print(f"{lab:24s} v_max {oz['v_max']:.2f} m/s, DR {oz['DR']:.0f} %, PPD_AD {oz['PPD_AD']:.0f} %, U_in {r['U_in']:.3f} m/s")
    c = r["case"]; kz = int(0.1 / r["dz"])
    uc = 0.5 * (r["u"][1:] + r["u"][:-1]); vc = 0.5 * (r["v"][:, 1:] + r["v"][:, :-1])
    im = a.pcolormesh(r["x"], r["y"], r["speed"][:, :, kz].T, cmap="viridis", vmin=0, vmax=0.3, shading="auto")
    a.streamplot(r["x"], r["y"], uc[:, :, kz].T, vc[:, :, kz].T, color="w", linewidth=0.5, density=1.0, arrowsize=0.6)
    a.contour(r["x"], r["y"], r["speed"][:, :, kz].T, levels=[0.15, 0.25], colors=["#ffd000", "#ff8800"], linewidths=1.2)
    op = c.inlet; y0 = 0 if op.y0 is None else op.y0; y1 = c.W if op.y1 is None else op.y1
    a.plot([0, 0], [y0, y1], color="#2a78d6", lw=6)
    a.add_patch(plt.Rectangle((0.6, 0.6), c.L - 1.2, c.W - 1.2, fill=False, ec="w", ls="--", lw=0.8))
    a.set_aspect("equal"); a.set_title(f"{lab}: speed at 0.1 m", fontsize=10); a.set_xlabel("x (m)")
axs[0].set_ylabel("y (m)")
fig.colorbar(im, ax=axs, shrink=0.85, label="Mean air speed (m/s)")
fig.savefig(OUT / "window-width-ankle.png", dpi=140, bbox_inches="tight")
