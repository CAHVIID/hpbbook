# Writes sarran-pump-curves.svg/.png: pump curves and operating points of the apartment pump
# before and after balancing. Values read from Sarran et al. (2022), Fig. 11 (CC BY 4.0).
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "figures" / "c1"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10.5})
INK, GRID, MUTED, TEAL, RED, BLUE = "#222", "#e4e4e4", "#777", "#1b8a8a", "#c4502a", "#2b7bb9"

# proportional-pressure pump curves (piecewise linear, read from the figure): flow kg/s, head kPa
high = ([0, 0.42, 0.69, 0.8], [19, 38.5, 23, 16.5])
low = ([0, 0.69, 0.8], [12, 23, 16.5])
# system curves dp = (m / K)^2, through the operating points read from the figure
P1, P2, P3 = (0.54, 32.0), (0.41, 18.5), (0.085, 13.5)
k_now, k_bal = P1[1] / P1[0]**2, P3[1] / P3[0]**2

fig, ax = plt.subplots(figsize=(8, 4.8), dpi=200)
for s in ("top", "right"): ax.spines[s].set_visible(False)
for s in ("left", "bottom"): ax.spines[s].set_color("#999")
ax.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)

m = np.linspace(0, 0.8, 300)
for k, lab, x, ha in ((k_now, "system curve,\nas found", 0.665, "left"), (k_bal, "system curve,\nbalanced", 0.16, "left")):
    sel = k * m**2 <= 45
    ax.plot(m[sel], k * m[sel]**2, color=BLUE, lw=1.6, ls="--")
    ax.text(x, 43.5, lab, color=BLUE, fontsize=9, ha=ha, va="top")
ax.plot(*high, color=TEAL, lw=2.2); ax.plot(*low, color=RED, lw=2.2)
ax.text(0.17, 31.5, "high pump curve (as found)", color=TEAL, fontsize=9.5, ha="left", va="bottom", rotation=19)
ax.text(0.30, 20.5, "low pump curve", color=RED, fontsize=9.5, ha="left", va="bottom")

for (q, h), lab, dx, dy in ((P1, "1  as found", 0.02, 1.5), (P2, "2  low pump curve", 0.02, -3),
                            (P3, "3  low pump curve\n    + balancing", 0.02, -5)):
    ax.plot(q, h, "o", ms=8, color=INK, mec="white", mew=2, zorder=5)
    ax.text(q + dx, h + dy, lab, fontsize=9.5, color=INK, va="center")

ax.set_xlim(0, 0.8); ax.set_ylim(0, 45)
ax.set_xlabel("water flow through the floor loops [kg/s]", color=INK)
ax.set_ylabel("pump head [kPa]", color=INK)
ax.tick_params(colors="#555")
fig.tight_layout()
fig.savefig(OUT / "sarran-pump-curves.svg"); fig.savefig(OUT / "sarran-pump-curves.png")
print(f"pump hydraulic power as found {P1[0]*P1[1]:.1f} W, balanced {P3[0]*P3[1]:.1f} W (flow kg/s ~ l/s)")
