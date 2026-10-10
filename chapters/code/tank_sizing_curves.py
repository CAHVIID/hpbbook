"""Cumulative-curve sizing of a hot water tank (worked example of the tank sizing section).
Profile: 'Family of 4, morning and evening' from code/dhw_tank.py; cold water 10 C; standing loss
42 W (UA 1.2 W/K, tank 55 C, room 20 C). Left: uniform charging over 24 h. Right: night only, 00-06.
Writes tank-sizing-curves.svg/.png and prints the hourly table."""
import sys
sys.path.insert(0, "code")
import numpy as np
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import dhw_tank as d
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "figures" / "ch04"

WH = 994 * 4.182 / 3600                # Wh per litre and kelvin, mean properties 10-55 C (1.155)
T_COLD, T_SET, ETA, LOSS = 10.0, 55.0, 0.85, 0.042   # C, C, usable fraction, kW standing loss
h = np.zeros(24)
for t, name, vol, flow, t_use in d.PROFILES["Family of 4, morning and evening"]:
    h[int(t)] += vol * WH * (t_use - T_COLD) / 1000          # kWh drawn in each hour
dem = h + LOSS                                               # step 1: demand incl. loss
Q_day = dem.sum()
BLUE, ORANGE, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#1f1f1e", "#6b6a63", "#e4e3dc"

fig, axes = plt.subplots(1, 2, figsize=(9, 3.8), sharey=True)
for ax, (title, allowed) in zip(axes, [("Uniform charging, 00–24", range(24)), ("Night charging, 00–06", range(6))]):
    ch = np.array([Q_day / len(allowed) if k in allowed else 0 for k in range(24)])   # step 2
    D = np.concatenate([[0], np.cumsum(dem)])                                          # step 3
    C = np.concatenate([[0], np.cumsum(ch)])
    S = C - D
    C = C - S.min()                       # lift the charge curve until it just touches the demand curve
    gap = C - D
    k = gap.argmax(); Q_store = gap.max()
    V = Q_store * 1000 / (WH * (T_SET - T_COLD) * ETA)                                 # step 4
    x = np.arange(25)
    ax.fill_between(x, D, C, color=BLUE, alpha=0.10, linewidth=0)
    ax.plot(x, C, color=BLUE, lw=2, label="Cumulative charge")
    ax.plot(x, D, color=ORANGE, lw=2, label="Cumulative demand")
    ax.annotate("", xy=(k, C[k]), xytext=(k, D[k]), arrowprops=dict(arrowstyle="<->", color=INK, lw=1))
    ax.text(k + 0.4, (C[k] + D[k]) / 2, f"{Q_store:.1f} kWh\n≈ {V:.0f} L", fontsize=10, color=INK, va="center")
    ax.set_title(f"{title}: {Q_day / len(allowed):.2f} kW", fontsize=10, color=INK, loc="left")
    ax.set_xticks(range(0, 25, 6)); ax.set_xlim(0, 24); ax.set_xlabel("Hour of day", fontsize=10, color=INK)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED); ax.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
    print(f"{title}: P = {Q_day/len(allowed):.2f} kW, Q_store = {Q_store:.2f} kWh, V = {V:.0f} L")
axes[0].set_ylabel("Heat, kWh", fontsize=10, color=INK)
axes[0].legend(frameon=False, fontsize=9, loc="upper left")
fig.tight_layout()
for ext in ("svg", "png"): fig.savefig(OUT / f"tank-sizing-curves.{ext}", dpi=200)
print(f"Q_day = {Q_day:.2f} kWh (tapping {h.sum():.2f} + loss {24*LOSS:.2f}); Wh/(L K) = {WH:.4f}")
