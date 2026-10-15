"""Time-varying primary energy factors for electricity from the CO2 emission intensity, DK1+DK2, 2021.
CO2 per period: mean of DeclarationEmissionHour (Energi Data Service) over 2021, from the lecture slides.
Each period's factor is the BR18 factor 1.9 scaled by its CO2 intensity relative to the time-weighted
daily mean, so that the factor averaged over the 24 hours is exactly 1.9. Writes dhw-pef-periods.svg/.png."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
OUT = Path(__file__).resolve().parent.parent / "figures" / "c2"

PERIODS = [(0, 6, 98.8), (6, 17, 121.7), (17, 22, 116.2), (22, 24, 99.6)]   # start h, end h, g CO2/kWh
F_BR18 = 1.9
co2 = np.array([c for _, _, c in PERIODS])
hours = np.array([b - a for a, b, _ in PERIODS])
c_mean = (co2 * hours).sum() / 24                  # time-weighted daily mean, g/kWh
pef = F_BR18 * co2 / c_mean

BLUE, INK, MUTED, GRID = "#2a78d6", "#1f1f1e", "#6b6a63", "#e4e3dc"
fig, ax = plt.subplots(figsize=(8, 3.6))
for (a, b, c), f in zip(PERIODS, pef):
    ax.bar(a, f, b - a, align="edge", color=BLUE, alpha=0.85, edgecolor="white", linewidth=2)
    ax.text((a + b) / 2, f + 0.05, f"{f:.2f}", ha="center", fontsize=11, color=INK)
    ax.text((a + b) / 2, 0.12, f"{c:.0f}\ng/kWh", ha="center", fontsize=9, color="white")
ax.axhline(F_BR18, color=INK, lw=1, ls="--")
ax.text(24, F_BR18 + 0.04, "BR18: 1.9", ha="right", va="bottom", fontsize=9, color=INK)
ax.set_xlim(0, 24); ax.set_ylim(0, 2.5); ax.set_xticks([0, 6, 12, 17, 22, 24])
ax.set_xlabel("Hour of day", fontsize=10, color=INK)
ax.set_ylabel("Primary energy factor", fontsize=10, color=INK)
for s in ("top", "right"): ax.spines[s].set_visible(False)
for s in ("left", "bottom"): ax.spines[s].set_color(MUTED)
ax.tick_params(colors=MUTED); ax.grid(True, axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
fig.tight_layout()
for ext in ("svg", "png"): fig.savefig(OUT / f"dhw-pef-periods.{ext}", dpi=200)
print("PEF", pef.round(2), "time-weighted mean", round((pef * hours).sum() / 24, 2),
      "time-weighted CO2", round((co2 * hours).sum() / 24, 1))
