"""Floor heating control in a low-energy house: a cloudy spring day followed by a sunny one.

This is the reference model behind the interactive app in the floor heating chapter
(floor-control.mjs runs the same model in the browser).

Model, per m2 of floor:
- Floor: 1D heat conduction through the layers (finite differences, implicit Euler).
  The loop mass flow is proportional to the wax thermostat position. Heat transfer from
  the water to the pipe plane uses an effectiveness (NTU) model with UA = 1/R_pipe.
  The underside of the floor is adiabatic (the heat loss is in H_loss).
- Room: one node with the heat capacity of air, furniture and light internal parts.
  It gets solar and internal gains and loses heat to outdoors through H_loss.
  Windows are opened (heat removed) when the room exceeds T_vent.
- Control:
    ideal  instant convective heater with no delay (reference)
    onoff  room temperature sensor with hysteresis switching the wax thermostat
    pi     PI controller whose output is a PWM duty cycle for the wax thermostat
- Wax thermostat: dead time, then a linear stroke, separately for opening and closing.

Run:  python floor_control.py
"""
import math

DEFAULTS = dict(
    T_set=21.0,          # setpoint, C
    T_vent=24.0,         # windows opened above this, C
    H_loss=0.6,          # transmission + ventilation with heat recovery, W/(m2 floor K)
    C_room=40e3,         # room air, furniture, light internal parts, J/(m2 K)
    Q_int=3.0,           # internal gains, W/m2
    solar_cloudy=8.0,    # peak solar gain through windows on the cloudy day, W/m2 floor
    solar_sunny=40.0,    # same on the sunny day
    curve_slope=0.6,     # heating curve: T_supply = 20 + slope * (20 - T_out)
    T_supply_max=35.0,   # upper limit of the supply temperature, C
    flow_design=6.0,     # loop mass flow with the wax thermostat fully open, kg/(h m2 floor)
    hyst=0.25,           # on/off thermostat: switches at T_set -/+ hyst, K
    p_band=2.0,          # PI proportional band, K (100 % output at this error)
    Ti_min=90.0,         # PI integral time, min
    pwm_min=15.0,        # PWM cycle time, min
    dead_open_min=3.0, stroke_open_min=4.0,    # wax thermostat opening
    dead_close_min=2.0, stroke_close_min=5.0,  # wax thermostat closing
    warmup_days=4,       # cloudy days simulated before the two days shown
)

# Layers top -> bottom: (name, thickness m, conductivity W/mK, density kg/m3, specific heat J/kgK).
# "PIPE" marks the pipe plane.
FLOORS = {
    "Light floor": dict(R_pipe=0.10, layers=[
        ("pine boards", 0.022, 0.13, 500, 1600), "PIPE", ("EPS", 0.030, 0.035, 20, 1450),
        ("plywood", 0.018, 0.13, 500, 1600), ("mineral wool", 0.250, 0.037, 30, 850)]),
    "Heavy floor": dict(R_pipe=0.03, layers=[
        ("oak parquet", 0.014, 0.18, 700, 1700), ("concrete", 0.050, 1.7, 2300, 900), "PIPE",
        ("concrete", 0.050, 1.7, 2300, 900), ("EPS", 0.300, 0.037, 20, 1450)]),
}
H_SURF = 10.8   # floor surface to room, W/(m2 K)
DT = 60.0       # time step, s
DX = 0.002      # target node thickness, m
CP_WATER = 4186.0


def discretize(floor):
    k, C, dz, pipe = [], [], [], None
    for L in floor["layers"]:
        if L == "PIPE":
            pipe = len(k)
            continue
        _, d, lam, rho, c = L
        n = max(2, round(d / DX))
        k += [lam] * n; C += [rho * c * d / n] * n; dz += [d / n] * n
    return k, C, dz, pipe


def climate(t_h, p):
    """Outdoor temperature (2 C at 03, 12 C at 15) and solar gain (07-19) at hour t_h."""
    day, h = int(t_h // 24), t_h % 24
    t_out = 7 - 5 * math.cos(2 * math.pi * (h - 3) / 24)
    last = p["warmup_days"] + 1
    peak = p["solar_sunny"] if day == last else p["solar_cloudy"]
    sol = peak * max(0.0, math.sin(math.pi * (h - 7) / 12))
    return t_out, sol


def thomas(a, b, c, d):
    """Solve a tridiagonal system (a: sub, b: diagonal, c: super)."""
    n = len(b)
    cp, dp = [0.0] * n, [0.0] * n
    cp[0], dp[0] = c[0] / b[0], d[0] / b[0]
    for i in range(1, n):
        m = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / m if i < n - 1 else 0.0
        dp[i] = (d[i] - a[i] * dp[i - 1]) / m
    x = [0.0] * n
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


def simulate(floor, mode, p=DEFAULTS):
    """Returns a dict of time series for the last two days and summary results."""
    k, C, dz, pipe = discretize(floor)
    n = len(k) + 1                      # node 0 = room, nodes 1..n-1 = floor, top to bottom
    G = [1 / (dz[i] / (2 * k[i]) + dz[i + 1] / (2 * k[i + 1])) for i in range(len(k) - 1)]
    Gtop = 1 / (1 / H_SURF + dz[0] / (2 * k[0]))
    Cv = [p["C_room"]] + C
    # static part of the matrix
    b0, a, c = [0.0] * n, [0.0] * n, [0.0] * n
    b0[0] = Cv[0] / DT + Gtop + p["H_loss"]; c[0] = -Gtop
    b0[1] += Gtop; a[1] = -Gtop
    for i, g in enumerate(G):
        j = i + 1
        b0[j] += g; b0[j + 1] += g; c[j] = -g; a[j + 1] = -g
    for j in range(1, n):
        b0[j] += Cv[j] / DT
    pipe_nodes = (pipe, pipe + 1)       # floor nodes either side of the pipe plane (room offset +1)

    T = [p["T_set"]] * n
    pos, cmd, timer, integ, duty = 0.0, False, 0.0, 0.4, 0.0
    cycle_steps = max(1, round(p["pwm_min"] * 60 / DT))
    Kp, Ti = 1 / p["p_band"], p["Ti_min"] * 60
    days = p["warmup_days"] + 2
    steps = int(days * 24 * 3600 / DT)
    t_show = p["warmup_days"] * 24
    out = dict(t=[], room=[], q_floor=[], heat=[], vent=[], solar=[], t_out=[], t_sup=[], surface=[], t_ret=[], flow=[])
    for s in range(steps):
        th = s * DT / 3600
        t_out, sol = climate(th, p)
        b = b0[:]
        d = [Cv[j] / DT * T[j] for j in range(n)]
        d[0] += p["H_loss"] * t_out + p["Q_int"] + sol
        heat, mcp = 0.0, 0.0
        t_sup = min(p["T_supply_max"], 20 + p["curve_slope"] * (20 - t_out))   # heating curve
        if mode == "ideal":
            heat = max(0.0, p["H_loss"] * (p["T_set"] - t_out) - p["Q_int"] - sol
                       + p["C_room"] * (p["T_set"] - T[0]) / 600)
            d[0] += heat
        else:
            if mode == "onoff":
                if T[0] < p["T_set"] - p["hyst"]: new = True
                elif T[0] > p["T_set"] + p["hyst"]: new = False
                else: new = cmd
            else:  # pi with PWM output, updated at the start of every cycle
                if s % cycle_steps == 0:
                    e = p["T_set"] - T[0]
                    u = Kp * e + integ
                    if 0 < u < 1 or (u >= 1 and e < 0) or (u <= 0 and e > 0):   # anti-windup
                        integ = min(1.0, max(0.0, integ + Kp / Ti * e * cycle_steps * DT))
                    duty = min(1.0, max(0.0, Kp * e + integ))
                new = (s % cycle_steps) < duty * cycle_steps
            if new != cmd:
                cmd, timer = new, 0.0
            timer += DT
            if cmd and timer > p["dead_open_min"] * 60:
                pos = min(1.0, pos + DT / (p["stroke_open_min"] * 60))
            if not cmd and timer > p["dead_close_min"] * 60:
                pos = max(0.0, pos - DT / (p["stroke_close_min"] * 60))
            if pos < 1e-9:
                pos = 0.0   # avoid a tiny floating-point flow when closed
            mcp = pos * p["flow_design"] / 3600 * CP_WATER          # W/K per m2 floor
            gp = mcp * (1 - math.exp(-1 / floor["R_pipe"] / mcp)) / 2 if mcp > 0 else 0.0
            for j in pipe_nodes:
                b[j] += gp; d[j] += gp * t_sup
        T = thomas(a, b, c, d)
        if mode != "ideal":
            heat = sum(gp * (t_sup - T[j]) for j in pipe_nodes)
        vent = 0.0
        if T[0] > p["T_vent"]:
            vent = (T[0] - p["T_vent"]) * p["C_room"] / DT
            T[0] = p["T_vent"]
        if th >= t_show:
            out["t"].append(th - t_show); out["room"].append(T[0])
            out["q_floor"].append(Gtop * (T[1] - T[0]) if mode != "ideal" else heat)
            out["heat"].append(heat); out["vent"].append(vent); out["solar"].append(sol)
            out["t_out"].append(t_out); out["t_sup"].append(t_sup)
            out["surface"].append(T[0] + Gtop * (T[1] - T[0]) / H_SURF)   # floor surface temperature
            out["flow"].append(mcp / CP_WATER * 3600)                       # kg/(h m2)
            out["t_ret"].append(t_sup - heat / mcp if mcp > 0 else float("nan"))
    h = DT / 3600
    out["summary"] = dict(
        heating_Wh=sum(out["heat"]) * h,
        vented_Wh=sum(out["vent"]) * h,
        below_Kh=sum(max(0.0, p["T_set"] - x) for x in out["room"]) * h,
        above_Kh=sum(max(0.0, x - p["T_set"]) for x in out["room"]) * h,
    )
    m_sum = sum(out["flow"])
    out["summary"]["return_mw"] = (sum(m * t for m, t in zip(out["flow"], out["t_ret"]) if m > 0) / m_sum
                                   if m_sum > 0 else float("nan"))   # mass-flow-weighted return temperature
    return out


if __name__ == "__main__":
    print(f"{'':12s} {'control':6s} {'heating':>9s} {'vented':>8s} {'below':>7s} {'above':>7s} {'return':>7s}")
    print(f"{'':12s} {'':6s} {'Wh/m2':>9s} {'Wh/m2':>8s} {'K h':>7s} {'K h':>7s} {'C':>7s}")
    for name, floor in FLOORS.items():
        for mode in ("ideal", "onoff", "pi"):
            r = simulate(floor, mode)["summary"]
            print(f"{name:12s} {mode:6s} {r['heating_Wh']:9.0f} {r['vented_Wh']:8.0f} "
                  f"{r['below_Kh']:7.1f} {r['above_Kh']:7.1f} {r['return_mw']:7.1f}")
