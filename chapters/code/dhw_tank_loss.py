"""Standing loss of a 200 L hot water tank for the energy label classes A+ to C (EU 812/2013, 814/2013).
The class limit on the standing loss S (W) at 65 C tank and 20 C ambient is S = a + b V^0.4. The tank is held at 55 C
while it is charged 00-06 and cools without tapping 06-24 in a room at 22 C. Writes dhw-tank-loss.svg/.png."""
import numpy as np
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "figures" / "c2"

RHO, CP = 994.1, 4.182                         # mean density (kg/m3) and cp (kJ/kgK) of water, 10-55 C
V = 200                                        # tank volume, L
C = RHO * V / 1000 * CP * 1000                 # heat capacity, J/K
LIMITS = {"A+": (5.5, 3.16), "A": (8.5, 4.25), "B": (12, 5.93), "C": (16.66, 8.33)}
T_SET, T_ROOM, T_TEST = 55, 22, 45             # tank and room temperature, test temperature difference 65-20 K
BLUE, ORANGE, INK, MUTED = "#2a78d6", "#eb6834", "#1f1f1e", "#6b6a63"
COLORS = {"A+": "#1b9e5a", "A": "#7fbf3f", "B": BLUE, "C": ORANGE}

t = np.linspace(0, 24, 481)
fig, ax = plt.subplots(figsize=(8, 3.6))
print(f"C = {C/3.6e6:.3f} kWh/K")
for k, (a, b) in LIMITS.items():
    S = a + b * V ** 0.4                       # standing loss at the test condition, W
    UA = S / T_TEST                            # W/K
    tau = C / UA / 3600                        # time constant, h
    T = np.where(t <= 6, T_SET, T_ROOM + (T_SET - T_ROOM) * np.exp(-(t - 6) / tau))
    q_night = UA * (T_SET - T_ROOM) * 6 / 1000                 # kWh
    q_day = C * (T_SET - T[-1]) / 3.6e6                        # kWh
    ax.plot(t, T, color=COLORS[k], lw=2)
    ax.text(24.3, T[-1], f"{k}  {T[-1]:.1f} °C", va="center", fontsize=10, color=COLORS[k])
    print(f"{k}: S={S:.0f} W UA={UA:.2f} W/K tau={tau:.0f} h T24={T[-1]:.2f} night={q_night:.2f} day={q_day:.2f} "
          f"sum={q_night+q_day:.2f} kWh/day {365*(q_night+q_day):.0f} kWh/yr")
ax.axvspan(0, 6, color="#e4e3dc", alpha=0.6, lw=0)
ax.text(3, 47.4, "charging\n00–06", ha="center", fontsize=10, color=MUTED)
ax.set_xlim(0, 24); ax.set_ylim(47, 56); ax.set_xticks(range(0, 25, 3))
ax.set_xlabel("Hour of the day", fontsize=10, color=INK); ax.set_ylabel("Tank temperature, °C", fontsize=10, color=INK)
for s in ("top", "right"): ax.spines[s].set_visible(False)
for s in ("left", "bottom"): ax.spines[s].set_color(MUTED)
ax.tick_params(colors=MUTED); ax.yaxis.grid(True, color="#e4e3dc", linewidth=0.8); ax.set_axisbelow(True)
fig.tight_layout(rect=(0, 0, 0.9, 1))
for ext in ("svg", "png"): fig.savefig(OUT / f"dhw-tank-loss.{ext}", dpi=200)
