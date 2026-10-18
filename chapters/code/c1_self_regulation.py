"""Self-regulation of a floor held at a constant surface temperature.

- floor-self-regulation: a) heat flux from the floor against room temperature for a floor surface at 23 °C,
                         heating below 23 °C and cooling above. b) the same floor over a sunny day, with the
                         room temperature swinging around the floor temperature.

Assumptions (illustrative):
- Heating side: EN 1264 basic characteristic, q = 8.92 (theta_F - theta_i)^1.1.
- Cooling side: EN 1264-5 floor cooling, q = 7 (theta_i - theta_F), lower because warm air above a cool
  floor is stable and convection is weak.
- The floor surface stays at 23 °C, as it roughly does with a low, constant supply temperature and a heavy floor.

Writes figures/c1/<name>.svg and .png.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "c1"
C_HEAT, C_COOL, C_FLOOR, INK = "#d0663a", "#2b7bb9", "#555555", "#222222"
T_FLOOR = 23.0


def save(fig, name):
    for ext in ("svg", "png"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=200)


def strip(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def flux(t_room):
    """Heat flux from floor to room, W/m². Positive is heating, negative cooling."""
    d = T_FLOOR - np.asarray(t_room, dtype=float)
    return np.where(d >= 0, 8.92 * np.abs(d) ** 1.1, -7.0 * np.abs(d))


fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw=dict(width_ratios=[1, 1.35]))

# a) flux against room temperature
tr = np.linspace(19, 27, 400)
q = flux(tr)
a.fill_between(tr, 0, q, where=q >= 0, color=C_HEAT, alpha=0.18, lw=0)
a.fill_between(tr, 0, q, where=q < 0, color=C_COOL, alpha=0.18, lw=0)
a.plot(tr, q, color=INK, lw=2)
a.axhline(0, color="#999", lw=0.8)
a.axvline(T_FLOOR, color=C_FLOOR, ls="--", lw=1)
a.text(T_FLOOR + 0.1, 33, "Floor surface\n23 °C", fontsize=8.5, color=C_FLOOR, va="top")
a.text(19.3, 6, "Floor heats", color=C_HEAT, fontsize=10, weight="bold")
a.text(24.0, -6, "Floor cools", color=C_COOL, fontsize=10, weight="bold", va="top")
for t in (20, 22):
    a.plot(t, flux(t), "o", color=C_HEAT, ms=5)
    a.annotate(f"{t} °C: {float(flux(t)):.0f} W/m²", xy=(t, flux(t)), xytext=(t + 0.25, flux(t) + 3) if t == 20 else (20.2, flux(t) - 7), fontsize=8)
a.plot(25, flux(25), "o", color=C_COOL, ms=5)
a.annotate(f"25 °C: −{-float(flux(25)):.0f} W/m²", xy=(25, flux(25)), xytext=(23.6, flux(25) - 8), fontsize=8)
a.set_xlim(19, 27)
a.set_ylim(-30, 38)
a.set_xlabel("Room temperature [°C]")
a.set_ylabel("Heat flux from the floor [W/m²]")
a.set_title("a) Output against room temperature", loc="left", fontsize=10)
a.grid(color="#e4e4e4", lw=0.6)
strip(a)

# b) a sunny day
h = np.linspace(0, 24, 481)
t_room = 23.0 + 2.0 * np.cos(2 * np.pi * (h - 15) / 24)        # 21 °C at 03:00, 25 °C at 15:00
qd = flux(t_room)
b.fill_between(h, 0, qd, where=qd >= 0, color=C_HEAT, alpha=0.25, lw=0, label="Heating")
b.fill_between(h, 0, qd, where=qd < 0, color=C_COOL, alpha=0.25, lw=0, label="Cooling")
b.plot(h, qd, color=INK, lw=1.6)
b.axhline(0, color="#999", lw=0.8)
b.set_xlim(0, 24)
b.set_ylim(-30, 38)
b.set_xticks(range(0, 25, 3), [f"{x:02d}:00" for x in range(0, 25, 3)], fontsize=8)
b.set_xlabel("Time of day")
b.set_ylabel("Heat flux from the floor [W/m²]")
b.set_title("b) A sunny spring day", loc="left", fontsize=10)
b.grid(color="#e4e4e4", lw=0.6)
strip(b)
bt = b.twinx()
bt.plot(h, t_room, color=C_HEAT, lw=1.4, ls=(0, (4, 2)), label="Room temperature")
bt.axhline(T_FLOOR, color=C_FLOOR, lw=1, ls="--", label="Floor surface")
bt.set_ylim(17, 27)
bt.set_ylabel("Temperature [°C]")
bt.spines["top"].set_visible(False)
h1, l1 = b.get_legend_handles_labels()
h2, l2 = bt.get_legend_handles_labels()
b.legend(h1 + h2, l1 + l2, fontsize=8, frameon=False, loc="lower left", ncol=2)

fig.tight_layout()
save(fig, "floor-self-regulation")

day = 24 / (len(h) - 1)
print(f"heating {qd[qd > 0].sum() * day:.0f} Wh/m², cooling {-qd[qd < 0].sum() * day:.0f} Wh/m²")
