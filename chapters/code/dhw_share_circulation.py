"""Space heating, domestic hot water and circulation loss for three Danish building standards, apartment buildings.
Space heating and DHW as in dhw_share.py (13.0 kWh/m2 per year). Circulation loss: mean of measurements in Swedish
multi-family buildings, 14 kWh/m2 per year in older and 6 kWh/m2 per year in newer buildings (Burke et al. 2020).
Writes dhw-share-circulation.svg/.png."""
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "figures" / "c2"

RHO, CP = 994.1, 4.182
DHW = 0.250 * RHO * CP * (55 - 10) / 3600          # kWh/m2 per year
buildings = ["Energy label D", "Passive house", "Danish low-energy\nclass"]
space = [150, 15, 10]
circ = [14, 6, 6]                                    # older / newer buildings, Burke et al. (2020)
BLUE, ORANGE, PURPLE, INK, MUTED = "#2a78d6", "#eb6834", "#8a5cc2", "#1f1f1e", "#6b6a63"

fig, ax = plt.subplots(figsize=(8, 3.8))
y = range(len(buildings))[::-1]
for yi, s, c in zip(y, space, circ):
    ax.barh(yi, s, color=BLUE, height=0.55, edgecolor="white", linewidth=2)
    ax.barh(yi, DHW, left=s, color=ORANGE, height=0.55, edgecolor="white", linewidth=2)
    ax.barh(yi, c, left=s + DHW, color=PURPLE, height=0.55, edgecolor="white", linewidth=2)
    tot = s + DHW + c
    ax.text(tot + 2, yi, f"hot water {DHW / tot * 100:.0f} %, circulation {c / tot * 100:.0f} %",
            va="center", fontsize=10, color=INK)
    print(f"{s=} total {tot:.1f}  dhw {DHW/tot:.0%}  circ {c/tot:.0%}  dhw+circ {(DHW+c)/tot:.0%}  circ/(dhw+circ) {c/(DHW+c):.0%}")
ax.set_yticks(list(y)); ax.set_yticklabels(buildings, fontsize=10, color=INK)
ax.set_xlabel("Net heat demand, kWh per m² floor area per year", fontsize=10, color=INK)
ax.set_xlim(0, 250)
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(MUTED); ax.tick_params(axis="y", length=0); ax.tick_params(axis="x", colors=MUTED)
ax.xaxis.grid(True, color="#e4e3dc", linewidth=0.8); ax.set_axisbelow(True)
hs = [plt.Rectangle((0, 0), 1, 1, color=c) for c in (BLUE, ORANGE, PURPLE)]
ax.legend(hs, ["Space heating", f"Domestic hot water ({DHW:.0f} kWh/m²)", "Circulation loss"], frameon=False,
          loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, fontsize=9.5)
fig.tight_layout()
for ext in ("svg", "png"): fig.savefig(OUT / f"dhw-share-circulation.{ext}", dpi=200)
