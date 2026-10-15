"""Consumer electricity price over one day in DK2 against the hot water demand of the family of four.
Spot: Elspotprices, DK2, 30 September 2025 (Energi Data Service). Network tariff: Radius winter 2026
(00-06 low, 06-17 and 21-24 high, 17-21 peak). Energinet system 7.2 and net 4.3 ore/kWh, elafgift 0.8
ore/kWh (2026-27), VAT 25 %. Writes dhw-price-day.svg/.png and prints the numbers used in the text."""
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dhw_tank as d
OUT = Path(__file__).resolve().parent.parent / "figures" / "c2"

SPOT = np.array([752.72, 732.80, 736.30, 707.27, 737.72, 835.20, 1057.62, 1820.42, 1560.53, 1058.29,
                 859.46, 721.75, 656.14, 642.19, 651.37, 722.50, 776.61, 1064.64, 2198.24, 2667.19,
                 1098.60, 865.88, 758.40, 690.25]) / 1000            # DKK/kWh, hour starting 00..23
TARIFF = np.array([0.1062] * 6 + [0.3185] * 11 + [0.9556] * 4 + [0.3185] * 3)   # Radius, winter 2026
OTHER = 0.072 + 0.043 + 0.008                                         # Energinet system + net, elafgift
VAT = 0.25 * (SPOT + TARIFF + OTHER)
PRICE = SPOT + TARIFF + OTHER + VAT

WH = 994 * 4.182 / 3600
h = np.zeros(24)
for t, name, vol, flow, t_use in d.PROFILES["Family of 4, morning and evening"]:
    h[int(t)] += vol * WH * (t_use - 10) / 1000          # kWh of heat drawn in each hour

BLUE, TEAL, GRAY, LGRAY, ORANGE, INK, MUTED, GRID = "#2a78d6", "#1c9a8a", "#8c8b84", "#c9c8c0", "#eb6834", "#1f1f1e", "#6b6a63", "#e4e3dc"
x = np.arange(24) + 0.5
fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 5.4), sharex=True, gridspec_kw=dict(height_ratios=[1.6, 1]))
b = np.zeros(24)
for v, c, lab in [(SPOT, BLUE, "Spot price (DK2)"), (TARIFF, TEAL, "Network tariff (Radius, winter)"),
                  (np.full(24, OTHER), GRAY, "Energinet tariffs and electricity tax"), (VAT, LGRAY, "VAT 25 %")]:
    a1.bar(x, v, 0.85, bottom=b, color=c, label=lab, linewidth=0); b += v
a1.axhline(PRICE.mean(), color=INK, ls="--", lw=1)
a1.text(13.5, PRICE.mean() + 0.08, f"daily average {PRICE.mean():.2f} DKK/kWh", ha="center", fontsize=9, color=INK)
a1.set_ylabel("DKK per kWh", fontsize=10, color=INK)
a1.legend(frameon=False, fontsize=8.5, loc="upper left")
a2.bar(x, h, 0.85, color=ORANGE, linewidth=0)
a2.set_ylabel("Hot water heat, kWh", fontsize=10, color=INK)
a2.set_xlabel("Hour of day", fontsize=10, color=INK)
a2.set_xticks(range(0, 25, 3)); a2.set_xlim(0, 24)
for ax in (a1, a2):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED); ax.grid(True, axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
fig.tight_layout()
for ext in ("svg", "png"): fig.savefig(OUT / f"dhw-price-day.{ext}", dpi=200)

night = PRICE[:6].mean()
at_tap = (PRICE * h).sum() / h.sum()
print("consumer price min/max", PRICE.min().round(2), PRICE.argmin(), PRICE.max().round(2), PRICE.argmax())
print("spot min/max", SPOT.min(), SPOT.max(), "ratio", round(SPOT.max() / SPOT.min(), 1))
print("spot share at 03 and 19:", round(SPOT[3] * 1.25 / PRICE[3], 2), round(SPOT[19] * 1.25 / PRICE[19], 2))
print("daily mean price", PRICE.mean().round(2), "night 00-06", night.round(2), "demand-weighted", at_tap.round(2))
print("heat/day", h.sum().round(2), "share 17-21", (h[17:21].sum() / h.sum()).round(2), "share 06-08", (h[6:8].sum()/h.sum()).round(2))
for cop in (1.0, 2.5):
    e = h.sum() / cop
    print(f"COP {cop}: heat at tap time {e*at_tap:.2f} DKK/day, at night {e*night:.2f} DKK/day, saving/yr {365*e*(at_tap-night):.0f} DKK")
