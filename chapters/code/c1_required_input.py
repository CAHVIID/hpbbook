"""Heat the water must give to a first-order floor so that the floor's output follows a
daily heating demand exactly: q_in = q_demand + tau * d(q_demand)/dt.
Demand 0-10 W/m2 (mean 5 W/m2), peak at 04:00. Writes floor-required-input.svg/.png."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "c1"
C_LIGHT, C_HEAVY, C_DEMAND = "#2b7bb9", "#d0663a", "#222222"
MEAN, SWING, T_PEAK = 5.0, 5.0, 4.0
w = 2 * np.pi / 24
t = np.linspace(0, 48, 961)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
fig, ax = plt.subplots(figsize=(10, 4.4))
ax.axhline(0, color="#888", lw=0.8)
ax.axhspan(-15, 0, color="#dbe9f6", alpha=0.6, lw=0)
ax.text(47.5, -13.5, "the water would have to cool the floor", ha="right", fontsize=9, color="#2b5d8a")
ax.plot(t, MEAN + SWING * np.cos(w * (t - T_PEAK)), color=C_DEMAND, lw=2.4,
        label="Heating demand = required floor output")
for tau, c, name in ((1.0, C_LIGHT, "Light floor"), (12.0, C_HEAVY, "Heavy floor")):
    gain = np.sqrt(1 + (w * tau) ** 2)
    lead = np.arctan(w * tau) / w
    q_in = MEAN + SWING * gain * np.cos(w * (t - T_PEAK + lead))
    ax.plot(t, q_in, color=c, lw=2, ls=(0, (6, 3)),
            label=f"{name}, τ = {tau:g} h: water must give {round(MEAN - SWING * gain) + 0:.0f} to {MEAN + SWING * gain:.0f} W/m², {lead:.1f} h early")
    print(f"{name}: gain {gain:.2f}, lead {lead:.1f} h, input {q_in.min():.1f} to {q_in.max():.1f} W/m2")
ax.set_xlim(0, 48)
ax.set_ylim(-15, 30)
ax.set_xticks(range(0, 49, 6), [f"{h % 24:02d}:00" for h in range(0, 49, 6)])
ax.set_xlabel("Time of day, two days")
ax.set_ylabel("Heat flux [W/m²]")
ax.legend(loc="upper right", fontsize=9, frameon=False)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
for ext in ("svg", "png"):
    fig.savefig(OUT / f"floor-required-input.{ext}", dpi=200)
