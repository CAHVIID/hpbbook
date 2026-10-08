"""Figure: on/off control vs. proportional control with a narrow and a wide band (chapter 3).

Top: controller output vs. room temperature. Bottom: room temperature after a
cold start, simulated with a small floor-heating room model. The valve follows
the controller output after a dead time (a continuous valve, i.e. PWM averaged).

Writes figures/ch03/proportional-band.svg and .png.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "ch03"

T_SET = 21.0      # setpoint, °C
HYST = 0.25       # on/off hysteresis, ± K
XP_NARROW = 0.5   # proportional band, K
XP_WIDE = 4.0

# Room model per m² floor: water -> floor node -> room node -> outdoor
T_W, T_OUT = 35.0, 0.0      # °C
K_WF, H_FR, UA = 25.0, 10.0, 4.5  # W/(m²K)
C_F, C_R = 10.0, 12.0       # Wh/(m²K)
DEAD = 0.2                  # valve dead time, h
DT = 1 / 600                # h
t = np.arange(0, 12, DT)


def simulate(controller):
    n_dead = round(DEAD / DT)
    u_hist = [1.0] * n_dead
    Tf, Tr = 24.0, 18.0
    on = True
    Tr_out = np.empty_like(t)
    for i in range(len(t)):
        if controller == "onoff":
            if Tr < T_SET - HYST:
                on = True
            elif Tr > T_SET + HYST:
                on = False
            u = float(on)
        else:
            u = np.clip(0.5 + (T_SET - Tr) / controller, 0, 1)
        u_hist.append(u)
        y = u_hist.pop(0)
        q_w = y * K_WF * (T_W - Tf)
        q_fr = H_FR * (Tf - Tr)
        Tf += DT * (q_w - q_fr) / C_F
        Tr += DT * (q_fr - UA * (Tr - T_OUT)) / C_R
        Tr_out[i] = Tr
    return Tr_out


C_ONOFF, C_NARROW, C_WIDE = "#888888", "#d0663a", "#2b7bb9"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.3),
                               gridspec_kw={"width_ratios": [1, 1.5], "wspace": 0.28})

# a) Controller output vs. room temperature
T = np.linspace(T_SET - 3, T_SET + 3, 601)
ax1.plot([T[0], T_SET + HYST, T_SET + HYST], [100, 100, 0], color=C_ONOFF, lw=1.8,
         label=f"On/off, ±{HYST} K hysteresis")
ax1.plot([T_SET - HYST, T_SET - HYST, T[-1]], [100, 0, 0], color=C_ONOFF, lw=1.8, ls="--")
for xp, c, name in ((XP_NARROW, C_NARROW, "Narrow"), (XP_WIDE, C_WIDE, "Wide")):
    ax1.plot(T, 100 * np.clip(0.5 + (T_SET - T) / xp, 0, 1), color=c, lw=2,
             label=f"{name} proportional band, {xp:g} K")
ax1.axvline(T_SET, color="#555", lw=0.8)
ax1.axhline(50, color="#555", lw=0.8)
ax1.annotate("", xy=(T_SET - XP_WIDE / 2, 108), xytext=(T_SET + XP_WIDE / 2, 108),
             arrowprops=dict(arrowstyle="<->", color=C_WIDE, lw=1), annotation_clip=False)
ax1.text(T_SET + 0.1, 111, "wide band", color=C_WIDE, fontsize=9, va="bottom",
         ha="left")
ax1.set_xlim(T[0], T[-1])
ax1.set_ylim(-5, 120)
ax1.set_yticks([0, 50, 100])
ax1.set_xlabel("Room temperature [°C]")
ax1.set_ylabel("Controller output (valve open) [%]")
ax1.set_title("a) Controller output", loc="left", fontsize=11)
fig.legend(loc="upper center", ncol=3, fontsize=9.5, frameon=False)

# b) Room temperature after a cold start
for ctrl, c in (("onoff", C_ONOFF), (XP_NARROW, C_NARROW), (XP_WIDE, C_WIDE)):
    Tr = simulate(ctrl)
    ax2.plot(t, Tr, color=c, lw=2 if ctrl != "onoff" else 1.6)
    if ctrl == XP_WIDE:
        T_end = Tr[-1]
ax2.axhline(T_SET, color="#555", lw=0.8)
ax2.text(0.15, T_SET + 0.05, "Setpoint", fontsize=9, va="bottom")
ax2.annotate("", xy=(11.6, T_end), xytext=(11.6, T_SET),
             arrowprops=dict(arrowstyle="<->", color="#444", lw=0.8))
ax2.text(11.45, (T_end + T_SET) / 2, "Offset", fontsize=9, ha="right", va="center")
ax2.set_xlim(0, t[-1])
ax2.set_xticks(range(0, 13, 2))
ax2.set_xlabel("Time [h]")
ax2.set_ylabel("Room temperature [°C]")
ax2.set_title("b) Room temperature after a cold start", loc="left", fontsize=11)

for ax in (ax1, ax2):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

fig.subplots_adjust(left=0.07, right=0.98, top=0.84, bottom=0.13)
for ext in ("svg", "png"):
    fig.savefig(OUT / f"proportional-band.{ext}", dpi=200)
print("wide-band offset:", round(T_end - T_SET, 2), "K")
