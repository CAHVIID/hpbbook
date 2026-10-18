"""Measured circulation losses in Swedish multi-family buildings, from the summary values reported by Burke et al. (2020):
range and mean of their 134 measurements, and the earlier studies they review. The dashed line is the 4 kWh/m2 per year
assumed in design when no calculation is made. Writes dhw-circulation-burke.svg/.png."""
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "figures" / "c2"

PURPLE, INK, MUTED, GRID = "#8a5cc2", "#1f1f1e", "#6b6a63", "#e4e3dc"
# label, range (lo, hi) or None, list of (value, marker label)
rows = [
    ("Burke et al. (2020)\n134 buildings", (0.5, 76), [(14, "mean, older\nbuildings 14"), (6, "mean, newer\nbuildings 6", "below")]),
    ("Bergqvist\n12 buildings", (2.3, 28), [(9.1, "mean\n9.1", "below")]),
    ("Lindencrona & Lindsköld\n540 buildings", None, [(17.4, "mean\n17.4")]),
    ("Alros\n2 buildings", None, [(11, "11"), (37, "37")]),
]

fig, ax = plt.subplots(figsize=(8, 4.6))
y = range(len(rows))[::-1]
for yi, (lab, rng, pts) in zip(y, rows):
    if rng:
        ax.plot(rng, [yi, yi], color=PURPLE, alpha=0.35, linewidth=9, solid_capstyle="butt")
        ax.text(rng[1] + 1.2, yi, f"{rng[0]:g}–{rng[1]:g}", va="center", fontsize=9, color=MUTED)
    for v, t, *pos in pts:
        ax.plot(v, yi, "o", color=PURPLE, markersize=8, markeredgecolor="white")
        below = pos == ["below"]
        ax.text(v, yi - 0.2 if below else yi + 0.2, t, ha="center", va="top" if below else "bottom",
                fontsize=8.5, color=INK, linespacing=1.0)
ax.axvline(4, color=INK, linestyle="--", linewidth=1)
ax.text(4.8, -0.35, "assumed in design, 4 kWh/m²", fontsize=9, color=INK, va="center")
ax.set_yticks(list(y)); ax.set_yticklabels([r[0] for r in rows], fontsize=9.5, color=INK)
ax.set_xlabel("Circulation loss, kWh per m² floor area per year", fontsize=10, color=INK)
ax.set_xlim(0, 85); ax.set_ylim(-0.5, len(rows) - 0.25)
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(MUTED); ax.tick_params(axis="y", length=0); ax.tick_params(axis="x", colors=MUTED)
ax.xaxis.grid(True, color=GRID, linewidth=0.8); ax.set_axisbelow(True)
fig.tight_layout()
for ext in ("svg", "png"): fig.savefig(OUT / f"dhw-circulation-burke.{ext}", dpi=200)
