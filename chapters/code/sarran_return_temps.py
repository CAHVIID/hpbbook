"""Energy-weighted mean return riser temperature for the improvement scenarios in
Sarran et al. (2022), Fig. 12 (CC BY 4.0). 'Current case' is their Table 7; the other two
series are read from the figure (+/- 0.2 K), except 31.0 C at 37 C, which is given in the text.
Writes sarran-return-temps.svg/.png."""
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "figures" / "c1"

SETPOINTS = ["45.6", "43", "40", "37", "35", "33"]
SERIES = [("As found", "#1b9e77", [37.5, 36.4, 34.4, 32.5, 31.3, 30.2]),
          ("Lower pump curve", "#2b5fb9", [36.9, 35.9, 34.1, 32.2, 31.1, 30.0]),
          ("Lower pump curve + balancing", "#ef8a62", [34.0, 33.1, 32.0, 31.0, 30.4, 29.9])]
UNMET = {("Lower pump curve + balancing", "35")} | {(s, "33") for s, _, _ in SERIES}

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
fig, ax = plt.subplots(figsize=(8, 4.2))
w = 0.26
for k, (name, col, vals) in enumerate(SERIES):
    for i, (sp, v) in enumerate(zip(SETPOINTS, vals)):
        unmet = (name, sp) in UNMET
        ax.bar(i + (k - 1) * w, v - 26, w, bottom=26, color="white" if unmet else col,
               edgecolor=col, hatch="////" if unmet else None, lw=1)
        ax.text(i + (k - 1) * w, v + 0.15, f"{v:.1f}", ha="center", fontsize=7.5)
ax.axvspan(4.11, 5.5, color="#d62728", alpha=0.05, lw=0)
ax.text(4.8, 38.6, "heat demand\nnot covered (hatched)", ha="center", va="top", fontsize=9, color="#b22222")
ax.set_xticks(range(len(SETPOINTS)), SETPOINTS)
ax.set_xlabel("Mixed supply temperature setpoint [°C]")
ax.set_ylabel("Return temperature to the riser [°C]")
ax.set_ylim(26, 39); ax.set_xlim(-0.5, 5.5)
ax.grid(axis="y", color="#e4e4e4", lw=0.6); ax.set_axisbelow(True)
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
ax.legend(handles=[Patch(facecolor=c, edgecolor=c, label=n) for n, c, _ in SERIES],
          frameon=False, fontsize=9, loc="upper right", bbox_to_anchor=(0.69, 1.0))
fig.tight_layout()
for ext in ("svg", "png"):
    fig.savefig(OUT / f"sarran-return-temps.{ext}", dpi=200)
