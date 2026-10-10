"""Figures for the room CFD appendix: a normal window (0.9-2.1 m) against a balcony door
(0-2.1 m) at 16 and 22 °C supply, 6 ACH, gains set for a well-mixed 26 °C room.

Writes to ../figures/appendix-cfd/. Each run takes a few minutes on the default mesh:

    python cfd_examples.py
"""
from pathlib import Path
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from room_cfd import Case, Opening, HeatBlock, run, occupied_zone
import room_cfd_plots as plots

OUT = Path(__file__).parent.parent / "figures" / "appendix-cfd"
OUT.mkdir(parents=True, exist_ok=True)
openings = {"Window (0.9–2.1 m)": Opening("left", 0.9, 2.1), "Door (0.0–2.1 m)": Opening("left", 0.0, 2.1)}
supply, T_ROOM, ACH = [16.0, 22.0], 26.0, 6

res = {}
for name, op in openings.items():
    for Tin in supply:
        c = Case(inlet=op, outlet=Opening("right", 2.3, 2.4), T_in=Tin, ach=ACH, t_end=1800, t_avg=600)
        c.heat = [HeatBlock(2.3, 2.7, 0.0, 1.2, 1.2 * 1005 * c.q * (T_ROOM - Tin) / c.W)]
        res[(name, Tin)] = r = run(c)
        oz = occupied_zone(r)
        print(f"{name:20s} {Tin:4.1f} °C  v_max {oz['v_max']:.2f} m/s  DR {oz['DR']:.0f} %  TS {oz['TS']:+.2f}  PPD_AD {oz['PPD_AD']:.0f} %")

fig, axs = plt.subplots(2, 2, figsize=(11, 6.4), sharex=True, sharey=True)
for a, ((name, Tin), r) in zip(axs.flat, res.items()):
    c = r["case"]; X, Y = np.meshgrid(r["x"], r["y"], indexing="ij")
    uc = 0.5 * (r["u"][1:] + r["u"][:-1]); vc = 0.5 * (r["v"][:, 1:] + r["v"][:, :-1])
    im = a.pcolormesh(X, Y, r["T"], cmap="coolwarm", vmin=16, vmax=28, shading="auto")
    a.streamplot(r["x"], r["y"], uc.T, vc.T, color="k", linewidth=0.5, density=1.1, arrowsize=0.6)
    a.contour(X, Y, r["speed"], levels=[0.15, 0.25], colors=["#ffd000", "#ff8800"], linewidths=1.2)
    a.add_patch(plt.Rectangle((2.3, 0), 0.4, 1.2, fill=False, ec="0.2", ls=":"))
    a.plot([0, 0], [c.inlet.start, c.inlet.end], color="#2a78d6", lw=5)
    a.plot([c.L, c.L], [c.outlet.start, c.outlet.end], color="0.3", lw=5)
    oz = occupied_zone(r)
    a.set_title(f"{name}, supply {Tin:.0f} °C\nfloor speed max {oz['v_max']:.2f} m/s, DR {oz['DR']:.0f} %, ankle PPD$_{{AD}}$ {oz['PPD_AD']:.0f} %", fontsize=9)
    a.set_aspect("equal"); a.set_xlim(0, c.L); a.set_ylim(0, c.H)
for a in axs[1]: a.set_xlabel("x (m)")
for a in axs[:, 0]: a.set_ylabel("Height (m)")
fig.colorbar(im, ax=axs, shrink=0.8, label="Air temperature (°C)")
fig.savefig(OUT / "window-vs-door.png", dpi=170, bbox_inches="tight")   # no SVG: the streamlines make it 4 MB

sub = {n.split(" (")[0]: res[(n, 16.0)] for n in openings}
plots.floor_line(sub, h=0.1).savefig(OUT / "window-vs-door-floor-line.png", dpi=160, bbox_inches="tight")
plots.convergence(res[("Window (0.9–2.1 m)", 16.0)]).savefig(OUT / "convergence-example.png", dpi=150, bbox_inches="tight")
