"""Small figures for the floor heating chapter (chapter 3).

- en1264-curve:      EN 1264 basic characteristic curve, q = 8.92 (theta_F - theta_i)^1.1
- floor-lump-balance: energy balance of the floor as one lump
- floor-daily-swing: first-order floor following a heating demand that swings over 24 h

Writes figures/ch03/<name>.svg and .png.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).resolve().parent.parent / "figures" / "ch03"
C_LIGHT, C_HEAVY, C_DEMAND = "#2b7bb9", "#d0663a", "#222222"


def save(fig, name):
    for ext in ("svg", "png"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=200)


def strip(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def en1264_curve():
    dT = np.linspace(0, 16, 400)
    q = 8.92 * dT ** 1.1
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(dT, q, color=C_DEMAND, lw=2.2)
    marks = [
        (1.1, "Low-energy house", C_LIGHT, (2.2, 30)),
        (9.0, "Limit, occupied zone: 29 °C floor, 20 °C room\n(bathroom: 33 °C floor, 24 °C room)", C_HEAVY, (0.6, 125)),
        (15.0, "Limit, perimeter zone:\n35 °C floor, 20 °C room", C_HEAVY, (9.6, 190)),
    ]
    for x, label, c, xy in marks:
        y = 8.92 * x ** 1.1
        ax.plot([x, x, 0], [0, y, y], color=c, ls="--", lw=1)
        ax.plot(x, y, "o", color=c, ms=6)
        ax.annotate(f"{label}\n{x:g} K → {y:.0f} W/m²", xy=(x, y), xytext=xy, fontsize=9,
                    arrowprops=dict(arrowstyle="-", color="#666", lw=0.8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 230)
    ax.set_xlabel("Floor surface minus room temperature, θ$_F$ − θ$_i$ [K]")
    ax.set_ylabel("Heat flux q [W/m²]")
    ax.grid(color="#e4e4e4", lw=0.6)
    strip(ax)
    fig.tight_layout()
    save(fig, "en1264-curve")


def lump_balance():
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    # room above, floor lump, insulation below
    ax.text(5, 4.85, "Room, $T_r$", ha="center", va="center", fontsize=12)
    ax.add_patch(FancyBboxPatch((2.5, 1.5), 5, 1.7, boxstyle="round,pad=0.02,rounding_size=0.15",
                                fc="#f6e3d9", ec=C_HEAVY, lw=1.6))
    ax.text(5, 2.75, "Floor above the insulation", ha="center", fontsize=11, weight="bold")
    ax.text(5, 2.3, "heat capacity $C$, temperature $T_f$", ha="center", fontsize=10)
    ax.add_patch(FancyBboxPatch((2.5, 0.75), 5, 0.6, boxstyle="square,pad=0", fc="#eeeeee",
                                ec="#999", hatch="///", lw=0.8))
    ax.text(5, 0.45, "Insulation (adiabatic)", ha="center", va="center", fontsize=9, color="#555")

    def arrow(p0, p1, c):
        ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=18, lw=2, color=c))

    arrow((0.4, 2.35), (2.45, 2.35), C_HEAVY)
    ax.text(0.4, 2.55, "$\\dot E_{in}$\nwater in the pipes\n(0 when the loop is closed)",
            fontsize=9, va="bottom")
    arrow((5, 3.25), (5, 4.45), C_LIGHT)
    ax.text(5.15, 3.75, "$\\dot E_{out} = (T_f - T_r)/R$\nthrough covering and surface",
            fontsize=9, va="center")
    ax.text(7.7, 2.35, "$\\dot E_{gen}$ = 0\n(no heat generated\ninside the floor)", fontsize=9,
            va="center")
    ax.text(5, 1.8, "$\\dot E_{stored} = C\\,\\mathrm{d}T_f/\\mathrm{d}t$", ha="center", fontsize=10,
            color="#7a3a1d")
    fig.tight_layout()
    save(fig, "floor-lump-balance")


def daily_swing():
    w = 2 * np.pi / 24
    t = np.linspace(0, 48, 961)
    t_peak = 4.0                      # demand peaks at 04:00
    demand = np.cos(w * (t - t_peak))
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.axhline(0, color="#888", lw=0.8)
    ax.plot(t, 100 * demand, color=C_DEMAND, lw=2.2, label="Heating demand")
    for tau, c, name in ((1.0, C_LIGHT, "Light floor"), (12.0, C_HEAVY, "Heavy floor")):
        amp = 1 / np.sqrt(1 + (w * tau) ** 2)
        lag = np.arctan(w * tau) / w
        ax.plot(t, 100 * amp * np.cos(w * (t - t_peak - lag)), color=c, lw=2,
                label=f"{name}, τ = {tau:g} h: {amp:.0%} of the swing, {lag:.1f} h late")
        tp = t_peak + 24 + lag
        ax.plot(tp, 100 * amp, "o", color=c, ms=6)
        ax.annotate("", xy=(tp, 100 * amp + 6), xytext=(t_peak + 24, 100 * amp + 6),
                    arrowprops=dict(arrowstyle="->", color=c, lw=1.2))
    ax.axvline(t_peak + 24, color="#bbb", lw=0.8, ls=":")
    ax.text(t_peak + 24 - 0.3, -112, "04:00", ha="right", fontsize=9, color="#666")
    ax.text(0.5, 108, "heating demand above the daily mean", fontsize=9, color="#666")
    ax.text(0.5, -108, "below the daily mean (sun, surplus)", fontsize=9, color="#666", va="top")
    ax.set_xlim(0, 48)
    ax.set_ylim(-125, 175)
    ax.set_yticks(range(-100, 101, 50))
    ax.set_xticks(range(0, 49, 6), [f"{h % 24:02d}:00" for h in range(0, 49, 6)])
    ax.set_xlabel("Time of day, two days")
    ax.set_ylabel("Deviation from daily mean\n[% of the demand swing]")
    ax.legend(loc="upper right", fontsize=9, frameon=False)
    strip(ax)
    fig.tight_layout()
    save(fig, "floor-daily-swing")


if __name__ == "__main__":
    en1264_curve()
    lump_balance()
    daily_swing()
