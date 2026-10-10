# Writes riser-pump-curve.svg/.png: riser pump curve at low load, and the pressure a thermostatic
# valve must absorb before the spring-loaded check valve in the shunt bypass opens. Example numbers.
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "figures" / "ch03"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10.5})
INK, GRID, MUTED, RED, BLUE = "#222", "#e4e4e4", "#777", "#c4502a", "#2b7bb9"

Q = np.linspace(0, 1000, 300)                 # riser flow, l/h
H0, Qmax = 45.0, 2000.0                        # constant-speed pump: shut-off head kPa, flow at zero head
H_const = H0 * (1 - (Q / Qmax) ** 2)
Qd = 600.0; Hd = H0 * (1 - (Qd / Qmax) ** 2)   # design point on the constant-speed curve
H_prop = 0.5 * Hd + 0.5 * Hd * Q / Qd           # proportional-pressure mode through the same design point
p_open = 10.0                                    # spring-loaded check valve opening pressure, kPa (example)
Q_low = 80.0                                     # low-energy house in mild weather: small primary flow

fig, ax = plt.subplots(figsize=(8, 4.8), dpi=200)
for s in ("top", "right"): ax.spines[s].set_visible(False)
for s in ("left", "bottom"): ax.spines[s].set_color("#999")
ax.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)

# system curves: design and low load (thermostatic valves throttled)
for k, lab, x_lab in ((Hd / Qd**2, "system at design", 980), ((H0 * (1 - (Q_low / Qmax)**2)) / Q_low**2, "system at low load", 150)):
    m = k * Q**2 <= 68
    ax.plot(Q[m], k * Q[m]**2, color="#aaa", lw=1.4, ls="--")
ax.text(785, 66, "system curve,\ndesign", color=MUTED, fontsize=9, ha="left", va="top")
ax.text(112, 66, "system curve,\nlow load", color=MUTED, fontsize=9, ha="left", va="top")

ax.plot(Q, H_const, color=INK, lw=2.2)
ax.plot(Q, H_prop, color=BLUE, lw=2.2)
ax.plot(Q, H_const + p_open, color=RED, lw=1.6, ls=(0, (5, 3)))
ax.fill_between(Q, H_const, H_const + p_open, color=RED, alpha=0.08, lw=0)
ax.text(840, H0 * (1 - (840 / Qmax)**2) - 2.5, "riser pump,\nconstant speed", color=INK, fontsize=9.5, ha="left", va="top")
ax.text(870, 0.5 * Hd + 0.5 * Hd * 870 / Qd + 1.5, "riser pump,\nproportional pressure", color=BLUE, fontsize=9.5, ha="left", va="bottom")
ax.text(300, H0 * (1 - (300 / Qmax)**2) + p_open + 1.5, "pressure the thermostatic valve must absorb\nbefore the check valve opens", color=RED, fontsize=9.5, ha="left", va="bottom")

# operating points
for q, h, c, lab, dx, dy in ((Qd, Hd, INK, "A  design", 25, -4.5),
                             (Q_low, H0 * (1 - (Q_low / Qmax)**2), INK, "B  low load", 25, -5),
                             (Q_low, 0.5 * Hd + 0.5 * Hd * Q_low / Qd, BLUE, "C  low load, proportional pressure", 25, -1.5)):
    ax.plot(q, h, "o", ms=8, color=c, mec="white", mew=2, zorder=5)
    ax.text(q + dx, h + dy, lab, fontsize=9.5, color=INK if c == INK else BLUE, va="center")
xa = 200; ya = H0 * (1 - (xa / Qmax)**2)
ax.annotate("", xy=(xa, ya + p_open), xytext=(xa, ya),
            arrowprops=dict(arrowstyle="<->", color=RED, lw=1.2))
ax.text(xa + 12, ya + p_open / 2, f"check valve opening, {p_open:.0f} kPa", color=RED, fontsize=8.5, ha="left", va="center")

ax.set_xlim(0, 1000); ax.set_ylim(0, 68)
ax.set_xlabel("flow drawn from the riser [l/h]", color=INK)
ax.set_ylabel("differential pressure [kPa]", color=INK)
ax.tick_params(colors="#555")
fig.tight_layout()
fig.savefig(OUT / "riser-pump-curve.svg"); fig.savefig(OUT / "riser-pump-curve.png")
print(f"design {Qd:.0f} l/h at {Hd:.1f} kPa; low load B {H0*(1-(Q_low/Qmax)**2):.1f} kPa, C {0.5*Hd+0.5*Hd*Q_low/Qd:.1f} kPa")
