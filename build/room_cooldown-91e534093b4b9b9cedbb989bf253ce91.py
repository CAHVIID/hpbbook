"""Temperature drop in a room after the heating stops: a one-node RC model.

The room (air, furniture and internal construction) is one heat store C [J/K]
that loses heat through the envelope and ventilation, UA [W/K], to the outdoor
temperature T_out. Optional constant gains Phi [W] (people, appliances, sun).

    C dT/dt = UA (T_out - T) + Phi

With constant T_out and Phi the solution is

    T(t) = T_inf + (T_0 - T_inf) exp(-t / tau),   tau = C / UA,   T_inf = T_out + Phi / UA

Give UA and either C or tau; the other follows from tau = C / UA.

Examples
    python room_cooldown.py                                  # compare the default cases
    python room_cooldown.py --UA 12 --tau 18                 # one case, tau in hours
    python room_cooldown.py --UA 50 --C 800 --hours 12       # one case, C in kJ/K
    python room_cooldown.py --UA 12 --tau 18 --gains 60 --t_out -5
"""
import argparse
import math

import matplotlib.pyplot as plt

# Default cases for a 20 m2 room. UA and C per m2 of floor times 20 m2.
CASES = [
    # name,                          UA [W/K],  C [kJ/K]
    ("Older house, heavy",           2.5 * 20, 150 * 20),
    ("Low-energy house, light",      0.6 * 20,  40 * 20),
    ("Low-energy house, heavy",      0.6 * 20, 150 * 20),
]


def simulate(UA, C, T0=21.0, T_out=0.0, gains=0.0, hours=24.0, dt=60.0):
    """Step the heat balance forward in time (explicit Euler, dt in s).

    Returns lists of time [h] and room temperature [C]. The analytical solution
    is printed alongside, so students can check the numerical result.
    """
    t, T = [0.0], [T0]
    for _ in range(int(hours * 3600 / dt)):
        dTdt = (UA * (T_out - T[-1]) + gains) / C
        T.append(T[-1] + dTdt * dt)
        t.append(t[-1] + dt / 3600)
    return t, T


def analytical(UA, C, t_h, T0, T_out, gains):
    tau = C / UA
    T_inf = T_out + gains / UA
    return T_inf + (T0 - T_inf) * math.exp(-t_h * 3600 / tau)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--UA", type=float, help="heat loss coefficient, W/K")
    ap.add_argument("--C", type=float, help="heat capacity, kJ/K")
    ap.add_argument("--tau", type=float, help="time constant, h (instead of C)")
    ap.add_argument("--T0", type=float, default=21.0, help="room temperature when the heating stops, C (default 21)")
    ap.add_argument("--t_out", type=float, default=0.0, help="outdoor temperature, C (default 0)")
    ap.add_argument("--gains", type=float, default=0.0, help="constant internal and solar gains, W (default 0)")
    ap.add_argument("--hours", type=float, default=48.0, help="simulated time, h (default 48)")
    a = ap.parse_args()

    if a.UA is not None:
        if a.tau is not None:
            C = a.tau * 3600 * a.UA          # J/K
        elif a.C is not None:
            C = a.C * 1e3
        else:
            ap.error("give --C or --tau together with --UA")
        cases = [(f"UA = {a.UA:g} W/K, tau = {C / a.UA / 3600:.1f} h", a.UA, C)]
    else:
        cases = [(n, UA, C * 1e3) for n, UA, C in CASES]

    print(f"T0 = {a.T0} C, T_out = {a.t_out} C, gains = {a.gains} W\n")
    print(f"{'case':34s} {'UA W/K':>7s} {'C kJ/K':>8s} {'tau h':>6s} {'T_inf C':>8s} {'T(8 h)':>7s} {'T(24 h)':>8s}")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for name, UA, C in cases:
        t, T = simulate(UA, C, a.T0, a.t_out, a.gains, a.hours)
        tau_h = C / UA / 3600
        T_inf = a.t_out + a.gains / UA
        print(f"{name:34s} {UA:7.1f} {C / 1e3:8.0f} {tau_h:6.1f} {T_inf:8.1f} "
              f"{analytical(UA, C, 8, a.T0, a.t_out, a.gains):7.1f} {analytical(UA, C, 24, a.T0, a.t_out, a.gains):8.1f}")
        line, = ax.plot(t, T, lw=2, label=f"{name} (tau = {tau_h:.1f} h)")
        if tau_h <= a.hours:   # mark 63 % of the drop at t = tau
            ax.plot(tau_h, analytical(UA, C, tau_h, a.T0, a.t_out, a.gains), "o", color=line.get_color())
    ax.axhline(a.t_out, color="#999", lw=1, ls="--")
    ax.text(a.hours, a.t_out + 0.3, "outdoor", ha="right", va="bottom", color="#777", fontsize=9)
    ax.set_xlabel("time after the heating stops [h]")
    ax.set_ylabel("room temperature [°C]")
    ax.set_xlim(0, a.hours)
    ax.grid(True, color="#e4e4e4")
    ax.legend(frameon=False, fontsize=9)
    ax.set_title("Temperature drop after the heating stops (dots: t = tau, 63 % of the drop)", fontsize=10)
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
