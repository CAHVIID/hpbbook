"""1D finite-difference model of a light and a heavy floor heating construction.
Pipe plane is coupled to the water through R_pipe while the loop is open (wax thermostat on)
and is not forced while it is closed. Room and the space below held at 20 C (no downward loss), h = 10.8 W/m2K.
Prints time constants and heat stored, writes floor-step-response.svg/.png."""
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "figures" / "ch03"

H_SURF, T_ROOM, T_GROUND, T_WATER = 10.8, 20.0, 20.0, 30.0
# layers top -> bottom: (name, thickness m, lambda, rho, c); 'PIPE' marks the pipe plane
FLOORS = {
  "Light floor: 22 mm boards on aluminium plates": dict(R_pipe=0.10, layers=[
      ("pine boards", 0.022, 0.13, 500, 1600), "PIPE", ("EPS", 0.030, 0.035, 20, 1450),
      ("plywood", 0.018, 0.13, 500, 1600), ("mineral wool", 0.250, 0.037, 30, 850)]),
  "Heavy floor: 14 mm parquet on 100 mm concrete": dict(R_pipe=0.03, layers=[
      ("oak parquet", 0.014, 0.18, 700, 1700), ("concrete", 0.050, 1.7, 2300, 900), "PIPE",
      ("concrete", 0.050, 1.7, 2300, 900), ("EPS", 0.300, 0.037, 20, 1450)]),
}

def build(spec, dx=0.002):
    k, C, pipe = [], [], None
    for L in spec["layers"]:
        if L == "PIPE": pipe = len(k); continue
        _, d, lam, rho, c = L; n = max(2, int(round(d / dx)))
        k += [lam] * n; C += [rho * c * d / n] * n
    dz = []
    for L in spec["layers"]:
        if L == "PIPE": continue
        n = max(2, int(round(L[1] / dx))); dz += [L[1] / n] * n
    return np.array(k), np.array(C), np.array(dz), pipe

def simulate(spec, on, T0, hours, dt=30.0):
    """Backward-Euler time stepping (stable with thin, light insulation cells)."""
    k, C, dz, pipe = build(spec); n = len(k)
    G = 1 / (dz[:-1] / (2 * k[:-1]) + dz[1:] / (2 * k[1:]))   # node i <-> i+1
    Gtop = 1 / (1 / H_SURF + dz[0] / (2 * k[0])); Gbot = 1 / (dz[-1] / (2 * k[-1]) + 0.17)
    K = np.zeros((n, n)); b = np.zeros(n)
    for i, g in enumerate(G):
        K[i, i] += g; K[i + 1, i + 1] += g; K[i, i + 1] -= g; K[i + 1, i] -= g
    K[0, 0] += Gtop; b[0] += Gtop * T_ROOM; K[-1, -1] += Gbot; b[-1] += Gbot * T_GROUND
    if on:  # water couples into the two nodes either side of the pipe plane
        gp = 1 / spec["R_pipe"] / 2
        for j in (pipe - 1, pipe): K[j, j] += gp; b[j] += gp * T_WATER
    A = np.linalg.inv(np.diag(C / dt) + K)
    T = np.full(n, T0) if np.isscalar(T0) else T0.copy()
    steps = int(hours * 3600 / dt); q = np.empty(steps); t = np.arange(1, steps + 1) * dt / 3600
    for s in range(steps):
        T = A @ (C / dt * T + b)
        q[s] = Gtop * (T[0] - T_ROOM)
    return t, q, T

def t63(t, x):  # time to reach 63 % of the change
    return t[np.argmax(x >= 0.632)]

res = {}
for name, spec in FLOORS.items():
    k, C, dz, pipe = build(spec)
    tu, qu, Tss = simulate(spec, True, T_ROOM, 72)       # switch on from cold, run to steady state
    qss = qu[-1]
    td, qd, _ = simulate(spec, False, Tss, 72)           # switch off from steady state
    stored_after_off = np.trapezoid(np.clip(qd, 0, None), td)             # Wh/m2 delivered after the valve closes
    above = sum(C[:pipe]) / 1000
    res[name] = (tu, qu / qss, td, qd / qss)
    print(f"{name}\n  C above pipes {above:.0f} kJ/m2K, total {sum(C)/1000:.0f} kJ/m2K, q_ss {qss:.1f} W/m2"
          f"\n  63% rise {t63(tu, qu/qss):.2f} h, 63% decay {t63(td, 1-qd/qss):.2f} h, "
          f"heat after switch-off {stored_after_off:.0f} Wh/m2 = {stored_after_off/qss:.1f} h of full output")

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
fig, axs = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
cols = ["#2b7bb9", "#d0663a"]
for (name, (tu, nu, td, nd)), c in zip(res.items(), cols):
    axs[0].plot(tu, 100 * nu, color=c, lw=2.2, label=name)
    axs[1].plot(td, 100 * nd, color=c, lw=2.2)
for ax, title in zip(axs, ["a) Wax thermostat opens at t = 0", "b) Wax thermostat closes at t = 0"]):
    ax.axhline(63.2 if ax is axs[0] else 36.8, color="#888", lw=1, ls="--")
    ax.set_xlim(0, 24); ax.set_xticks(range(0, 25, 4)); ax.set_ylim(0, 105)
    ax.set_xlabel("Time [h]"); ax.set_title(title, loc="left", fontsize=11)
    ax.grid(color="#e1e4e6"); ax.spines[["top", "right"]].set_visible(False)
axs[0].set_ylabel("Heat output to room [% of steady state]")
axs[0].legend(loc="lower right", frameon=False, fontsize=9.5)
fig.tight_layout()
for ext in ("svg", "png"):
    fig.savefig(OUT / f"floor-step-response.{ext}", dpi=200)
