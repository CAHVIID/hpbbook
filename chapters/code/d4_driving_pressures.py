"""Driving pressures for natural ventilation in a Copenhagen summer: stack effect versus wind.

Afternoon (15:00) and night (03:00) conditions are the June-August hourly means of the Annex 80
Copenhagen TMY 2041-2060 file, with the room at 26 °C. Wind is the 10 m value in the file.

Stack:  dp = rho g h dT / T
Wind:   dp = dCp 0.5 rho v^2

Usage: python d4_driving_pressures.py <folder with 5A_Copenhagen_TMY_2041-2060.epw>
Writes figures/d4/driving-pressures.svg and .png.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "d4"
EPW = Path(sys.argv[1]) / "5A_Copenhagen_TMY_2041-2060.epw"
G, RHO, T, T_ROOM, DCP = 9.81, 1.2, 299, 26.0, 0.5
DARK, GREY, BLUE, ORANGE = "#262626", "#8C8C8C", "#2F6DB5", "#E07B39"
plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 13, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.edgecolor": GREY, "axes.grid": True,
                     "grid.color": "#EBEBEB", "axes.axisbelow": True, "legend.frameon": False})

month, hour, temp, wind = np.genfromtxt(EPW, delimiter=",", skip_header=8, usecols=(1, 3, 6, 21)).T
summer = (month >= 6) & (month <= 8)


def condition(h):
    """Rounded room-outdoor temperature difference (K) and wind speed (m/s) at hour h."""
    sel = summer & (hour == h)
    return round(T_ROOM - temp[sel].mean()), round(wind[sel].mean(), 1)


(dt_day, v_day), (dt_night, v_night) = condition(15), condition(3)
cases = [("Stack, one window\nh = 1.5 m", [RHO * G * 1.5 * dt / T for dt in (dt_day, dt_night)]),
         ("Stack, two storeys\nh = 5 m", [RHO * G * 5 * dt / T for dt in (dt_day, dt_night)]),
         (f"Wind, ΔCp = {DCP}", [DCP * 0.5 * RHO * v ** 2 for v in (v_day, v_night)])]

fig, ax = plt.subplots(figsize=(8.5, 4.6))
y, hgt = np.arange(len(cases)), 0.36
for k, (col, lab) in enumerate([(ORANGE, f"afternoon: ΔT {dt_day} K, wind {v_day} m/s"),
                                (BLUE, f"night: ΔT {dt_night} K, wind {v_night} m/s")]):
    off = (k - 0.5) * hgt
    vals = [c[1][k] for c in cases]
    ax.barh(y + off, vals, hgt, color=col, label=lab)
    for i, v in enumerate(vals):
        ax.text(v + 0.05, i + off, f"{v:.1f} Pa", va="center", color=DARK)
ax.set_yticks(y, [c[0] for c in cases])
ax.invert_yaxis()
ax.grid(axis="y", visible=False)
ax.set_xlabel("Driving pressure difference (Pa)")
ax.legend(loc="upper right")
ax.set_xlim(0, 4.8)
for ext in ("png", "svg"):
    fig.savefig(OUT / f"driving-pressures.{ext}", dpi=200, bbox_inches="tight")
print([(c[0].split("\n")[0], [round(v, 2) for v in c[1]]) for c in cases])
