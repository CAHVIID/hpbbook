"""Figure: PWM control of a wax thermostat (chapter 3).

A triangular carrier spans the proportional band around the setpoint. The
valve is open whenever the measured room temperature lies below the carrier,
so the open time in each cycle grows as the room gets colder.

Writes figures/ch03/pwm-principle.svg and .png.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

OUT = Path(__file__).resolve().parent.parent / "figures" / "ch03"

T_SET = 21.0        # setpoint, °C
BAND = 1.0          # proportional band, K
PERIOD = 20.0       # PWM cycle, min
N_CYCLES = 7
t = np.linspace(0, N_CYCLES * PERIOD, 14001)

# Triangular carrier between T_SET - BAND/2 and T_SET + BAND/2
phase = (t % PERIOD) / PERIOD
carrier = T_SET - BAND / 2 + BAND * (1 - np.abs(2 * phase - 1))

# Smooth, made-up room temperature that wanders through the band
room = (T_SET
        - 0.30 * np.cos(2 * np.pi * t / 95)
        + 0.12 * np.sin(2 * np.pi * t / 37 + 0.6)
        - 0.10 * np.exp(-((t - 10) / 12) ** 2))

valve = room < carrier

C_ROOM = "#222222"
C_CARRIER = "#888888"
C_VALVE = "#d0663a"

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(10, 5.0), sharex=True,
    gridspec_kw={"height_ratios": [3, 1], "hspace": 0.12})

lo, hi = T_SET - BAND / 2, T_SET + BAND / 2
ymin, ymax = lo - 0.45, hi + 0.45
ax1.add_patch(Rectangle((0, hi), t[-1], ymax - hi, color="#2b7bb9", alpha=0.12, lw=0))
ax1.add_patch(Rectangle((0, ymin), t[-1], lo - ymin, color=C_VALVE, alpha=0.12, lw=0))
ax1.text(t[-1] * 0.62, (hi + ymax) / 2, "Valve always closed in this zone",
         ha="center", va="center", fontsize=11, color="#2b5f8a")
ax1.text(t[-1] * 0.38, (lo + ymin) / 2, "Valve always open in this zone",
         ha="center", va="center", fontsize=11, color="#9a4523")

for y in (lo, hi):
    ax1.axhline(y, color="#555", ls="--", lw=1)
ax1.axhline(T_SET, color="#555", lw=0.8)
ax1.plot(t, carrier, color=C_CARRIER, lw=1)
ax1.plot(t, room, color=C_ROOM, lw=2.2)

ax1.annotate("Measured room temperature", xy=(40, np.interp(40, t, room)),
             xytext=(14, hi + 0.30), fontsize=10,
             arrowprops=dict(arrowstyle="-", color="#444", lw=0.8))
ax1.text(t[-1] + 5, T_SET + 0.12, "Setpoint", va="center", fontsize=10)
ax1.annotate("", xy=(t[-1] + 3, lo), xytext=(t[-1] + 3, hi),
             arrowprops=dict(arrowstyle="<->", color="#444", lw=0.8),
             annotation_clip=False)
ax1.text(t[-1] + 5, T_SET - 0.2, "Proportional\nband", va="center", fontsize=10)

ax1.set_xlim(0, t[-1])
ax1.set_ylim(ymin, ymax)
ax1.set_ylabel("Temperature [°C]")
for s in ("top", "right"):
    ax1.spines[s].set_visible(False)

# Valve signal with duty cycle per period
ax2.fill_between(t, 0, valve.astype(float), step="post", color=C_VALVE, alpha=0.85, lw=0)
for k in range(N_CYCLES):
    m = (t >= k * PERIOD) & (t < (k + 1) * PERIOD)
    duty = valve[m].mean()
    ax2.text((k + 0.5) * PERIOD, 1.12, f"{duty:.0%}", ha="center", va="bottom", fontsize=10)
    ax1.axvline(k * PERIOD, color="#ccc", lw=0.6, zorder=0)
    ax2.axvline(k * PERIOD, color="#ccc", lw=0.6, zorder=0)

# Mark one period and link one pulse to the crossing points above
k = 5
y_per = lo - 0.25
ax1.annotate("", xy=(k * PERIOD, y_per), xytext=((k + 1) * PERIOD, y_per),
             arrowprops=dict(arrowstyle="<->", color="#444", lw=0.8))
ax1.text((k + 0.5) * PERIOD, y_per - 0.05, "PWM cycle", ha="center", va="top", fontsize=10)

edges = np.flatnonzero(np.diff(valve.astype(int)))
first = [e for e in edges if PERIOD <= t[e] < 2 * PERIOD]
for e in first:
    con_y = room[e]
    ax1.plot([t[e], t[e]], [ymin, con_y], color="#666", ls=":", lw=1)
    ax2.plot([t[e], t[e]], [0, 1.6], color="#666", ls=":", lw=1, clip_on=False)

ax2.set_ylim(0, 1.6)
ax2.set_yticks([0, 1], ["closed", "open"])
ax2.set_ylabel("Valve")
ax2.set_xlabel("Time [min]")
ax2.set_xticks(np.arange(0, t[-1] + 1, PERIOD))
for s in ("top", "right"):
    ax2.spines[s].set_visible(False)

fig.subplots_adjust(left=0.08, right=0.87, top=0.97, bottom=0.11)
for ext in ("svg", "png"):
    fig.savefig(OUT / f"pwm-principle.{ext}", dpi=200)
