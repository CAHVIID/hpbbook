"""Self-regulation in the control model: heavy and light floor (one figure each), constant supply of 40 C with PI control
and PWM, and 23 C with the loop always open (no room control). Setpoint 21 C. Room temperature, heat from the water
heat flux at the floor surface and return temperature over the cloudy and the sunny day. Prints heating energy,
deviation and return temperature, and writes floor-self-regulation-setpoint.svg/.png (heavy)
and floor-self-regulation-light.svg/.png (light)."""
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
import floor_control_improved as fc
OUT = Path(__file__).resolve().parent.parent / "figures" / "c1"

# (supply C, control mode, colour, label): 40 C with PI and PWM, 23 C with the loop always open
SUPPLIES = [(40.0, "pi", "#b2182b", "Supply 40 °C, PI control"), (23.0, "open", "#ef8a62", "Supply 23 °C, loop always open")]
SETPOINTS = [(21.0, "-")]
FIGURES = [("Heavy floor", "floor-self-regulation-setpoint"), ("Light floor", "floor-self-regulation-light")]
H = fc.DT / 3600

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})


def plot(FLOOR, name):
    fig, axs = plt.subplots(4, 1, figsize=(9, 10.6), sharex=True)
    print(FLOOR)
    print(f"{'supply':>6s} {'setpt':>6s} {'heat':>6s} {'below':>6s} {'above':>6s} {'return':>7s}")
    for sup, mode, col, lab in SUPPLIES:
        for sp, ls in SETPOINTS:
            p = dict(fc.DEFAULTS, curve_slope=0.0, T_supply_max=sup, T_set=sp)
            o = fc.simulate(fc.FLOORS[FLOOR], mode, p)
            t, n = o["t"], len(o["t"]) // 2
            below = sum(max(0.0, sp - x) for x in o["room"][:n]) * H      # cloudy day
            above = sum(max(0.0, x - sp) for x in o["room"][:n]) * H
            fl, ret = o["flow"][:n], o["t_ret"][:n]
            t_ret = sum(m * r for m, r in zip(fl, ret) if m > 0) / sum(fl)
            print(f"{sup:6.0f} {sp:6.0f} {o['summary']['heating_Wh']:6.0f} {below:6.1f} {above:6.1f} {t_ret:7.1f}")
            axs[0].plot(t, o["room"], color=col, ls=ls, lw=1.5, label=lab)
            axs[1].plot(t, o["heat"], color=col, ls=ls, lw=1.1)
            if mode == "pi": peak = max(o["heat"])
            axs[2].plot(t, o["q_floor"], color=col, ls=ls, lw=1.5)
            axs[3].plot(t, o["t_ret"], color=col, ls=ls, lw=1.0)   # gaps while the valve is closed
            axs[3].hlines(t_ret, 0, 24, color=col, ls=ls, lw=0.8, alpha=0.6)   # cloudy-day mean
    for sp, _ in SETPOINTS:
        axs[0].axhline(sp, color="#555", ls=":", lw=1)
    axs[0].text(47.5, 21.05, "setpoint", ha="right", fontsize=9, color="#555")
    axs[1].set_ylim(-3, 40); axs[1].axhline(0, color="#555", lw=0.8)
    axs[1].text(7.5, 37, f"PWM pulses at 40 °C reach about {peak:.0f} W/m²", fontsize=9, color="#b2182b", va="top")
    axs[2].axhline(0, color="#555", lw=0.8)
    axs[2].fill_between([0, 48], 0, -15, color="#2b7bb9", alpha=0.06, lw=0)
    axs[2].text(1, -9, "floor takes heat from the room", fontsize=9, color="#2b7bb9")
    axs[0].set_ylabel("Room [°C]"); axs[0].set_title("a) Room temperature", loc="left", fontsize=11)
    axs[1].set_ylabel("W/m²"); axs[1].set_title("b) Heat from the water to the floor", loc="left", fontsize=11)
    axs[2].set_ylabel("W/m²"); axs[2].set_title("c) Heat flux at the floor surface", loc="left", fontsize=11)
    axs[2].set_ylim(-15, None)
    axs[3].set_ylabel("°C"); axs[3].set_title("d) Return temperature (thin lines: flow-weighted mean, cloudy day)", loc="left", fontsize=11)
    axs[3].set_xlabel("Time [h]"); axs[3].set_xticks(range(0, 49, 6)); axs[3].set_xlim(0, 48)
    for ax in axs:
        ax.axvspan(24, 48, color="#f6c85f", alpha=0.18, lw=0)
        ax.grid(color="#e4e4e4", lw=0.6); ax.set_axisbelow(True)
        for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    axs[0].set_ylim(20, 24.6)
    axs[0].text(12, 24.6, "cloudy day", ha="center", va="top", fontsize=9)
    axs[0].text(36, 24.6, "sunny day", ha="center", va="top", fontsize=9)
    fig.legend(*axs[0].get_legend_handles_labels(), frameon=False, fontsize=9.5, ncol=2, loc="upper center")
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    for ext in ("svg", "png"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=200)
    plt.close(fig)


for floor, name in FIGURES:
    plot(floor, name)
