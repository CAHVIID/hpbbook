"""Space heating vs. domestic hot water net heat demand for three Danish house standards.
Space heating: label D estimated from the label scale; passive house and low-energy class as given (kWh/m2 per year); DHW is the Be18 calculation
value 250 L/m2 per year heated from 10 to 55 C with mean water properties = 13.0 kWh/m2. Writes dhw-share.svg/.png."""
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "figures" / "ch04"

RHO, CP = 994.1, 4.182                     # mean density (kg/m3) and cp (kJ/kgK) of water, 10-55 C
DHW = 0.250 * RHO * CP * (55 - 10) / 3600  # kWh/m2 per year
houses = ["Energy label D", "Passive house", "Danish low-energy\nclass"]
space = [150, 15, 10]   # D: estimated from the label scale, see the chapter text
BLUE, ORANGE, INK, MUTED = "#2a78d6", "#eb6834", "#1f1f1e", "#6b6a63"

fig, ax = plt.subplots(figsize=(8, 3.4))
y = range(len(houses))[::-1]
for yi, s, name in zip(y, space, houses):
    ax.barh(yi, s, color=BLUE, height=0.55, edgecolor="white", linewidth=2)
    ax.barh(yi, DHW, left=s, color=ORANGE, height=0.55, edgecolor="white", linewidth=2)
    share = DHW / (s + DHW) * 100
    ax.text(s + DHW + 2, yi, f"hot water {share:.0f} %", va="center", fontsize=10, color=INK)
ax.set_yticks(list(y)); ax.set_yticklabels(houses, fontsize=10, color=INK)
ax.set_xlabel("Net heat demand, kWh per m² floor area per year", fontsize=10, color=INK)
ax.set_xlim(0, 200)
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(MUTED); ax.tick_params(axis="y", length=0); ax.tick_params(axis="x", colors=MUTED)
ax.xaxis.grid(True, color="#e4e3dc", linewidth=0.8); ax.set_axisbelow(True)
h1 = plt.Rectangle((0, 0), 1, 1, color=BLUE); h2 = plt.Rectangle((0, 0), 1, 1, color=ORANGE)
ax.legend([h1, h2], ["Space heating", f"Domestic hot water ({DHW:.0f} kWh/m²)"], frameon=False,
          loc="lower right", fontsize=10)
fig.tight_layout()
for ext in ("svg", "png"): fig.savefig(OUT / f"dhw-share.{ext}", dpi=200)
print(f"DHW = {DHW:.1f} kWh/m2")
