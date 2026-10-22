"""Four KPIs (heating energy, deviation, return temperature, peak-to-average ratio) for the light and heavy floor
under on/off and PI/PWM control, for two supply strategies (40 C, heating curve),
compared with self-regulation (23 C fixed, loop always open, no room control).
Runs floor_control_improved.py and judges each case by the deviation from the setpoint on the cloudy day
(K h below + above), the heating energy over both days and the flow-weighted return temperature
on the cloudy day. Prints the table and writes
floor-performance.svg/.png. An optional argument scales the loop flow, e.g. 2 writes floor-performance-flow2x."""
import math, sys, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
import floor_control_improved as fc
OUT = Path(__file__).resolve().parent.parent / "figures" / "c1"
# Optional arguments: a bare number scales the default loop flow (e.g. 2 writes floor-performance-flow2x);
# key=value pairs override model inputs and name=... sets the file suffix, e.g.
#   H_loss=0.4 solar_cloudy=0 flow_design=2 name=lowloss
ARGS = sys.argv[1:]
FLOW = next((float(a) for a in ARGS if "=" not in a), 1.0)            # factor on the default loop flow
OVERRIDE = {k: float(v) for k, v in (a.split("=") for a in ARGS if "=" in a) if k != "name"}
OVERRIDE.setdefault("flow_design", FLOW * fc.DEFAULTS["flow_design"])
SUFFIX = next((a.split("=")[1] for a in ARGS if a.startswith("name=")), "" if FLOW == 1 else f"flow{FLOW:g}x")
NAME = "floor-performance" + (f"-{SUFFIX}" if SUFFIX else "")
BASE = dict(fc.DEFAULTS, **OVERRIDE)

SUPPLIES = [("40 °C constant", dict(curve_slope=0.0, T_supply_max=40.0)),
            ("Heating curve", dict(curve_slope=0.6, T_supply_max=40.0)),   # 24.8-30.8 C over the day
            ("23 °C constant, loop open", dict(curve_slope=0.0, T_supply_max=23.0))]
OPEN = {"23 °C constant, loop open"}   # no room control: the loop is always open (self-regulation only)
CONTROLS = [("onoff", "On/off", "#d0663a"), ("pi", "PI + PWM", "#2b7bb9")]
FLOORS = [("Light floor", "o"), ("Heavy floor", "s")]


def cloudy_day(floor, mode, p):
    """Deviation (K h) and flow-weighted return temperature (C) over the cloudy day (first day shown)."""
    o = fc.simulate(fc.FLOORS[floor], mode, p)
    n, h = len(o["room"]) // 2, fc.DT / 3600
    room, flow, ret, heat = o["room"][:n], o["flow"][:n], o["t_ret"][:n], o["heat"][:n]
    below = sum(max(0.0, p["T_set"] - x) for x in room) * h
    above = sum(max(0.0, x - p["T_set"]) for x in room) * h
    m = sum(flow)
    t_ret = sum(q * t for q, t in zip(flow, ret) if q > 0) / m if m > 0 else math.nan
    k = round(3600 / fc.DT)                                     # peak-to-average ratio of the hourly heat input
    hourly = [sum(max(0.0, x) for x in heat[i:i + k]) / k for i in range(0, n, k)]
    mean = sum(hourly) / len(hourly)
    par = max(hourly) / mean if mean > 0 else math.nan          # nan: the loop never opened
    return below, above, t_ret, o["summary"]["heating_Wh"], par   # heating energy over both days


res = {}
for s, extra in SUPPLIES:
    p = dict(BASE, **extra)
    for f, _ in FLOORS:
        for c, _, _ in CONTROLS:
            res[s, f, c] = cloudy_day(f, "open" if s in OPEN else c, p)
ideal = {f: cloudy_day(f, "ideal", BASE) for f, _ in FLOORS}

print(f"{'supply':16s} {'floor':12s} {'control':6s} {'below':>6s} {'above':>6s} {'total':>6s} {'return':>7s} {'heat':>6s} {'peak/avg':>8s}")
for f, _ in FLOORS:
    print(f"{'(any)':16s} {f:12s} {'ideal':6s} {ideal[f][0]:6.1f} {ideal[f][1]:6.1f} {sum(ideal[f][:2]):6.1f} {'':7s} {ideal[f][3]:6.0f} {ideal[f][4]:8.1f}")
for (s, f, c), (b, a, r, q, pr) in res.items():
    print(f"{s:16s} {f:12s} {c:6s} {b:6.1f} {a:6.1f} {b + a:6.1f} {r:7.1f} {q:6.0f} {pr:8.1f}")

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
# Two supply strategies under room control, and self-regulation (23 C, loop always open) as its own group
CONTROLLED = [s for s, _ in SUPPLIES if s not in OPEN]
SELF = next(s for s, _ in SUPPLIES if s in OPEN)
SHADES = {"40 °C constant": "#b2182b", "Heating curve": "#ef8a62", SELF: "#67a9cf"}
LABELS = {SELF: "Self-regulation: 23 °C fixed, loop always open"}
w, GAP = 0.36, 3.7
xt, xl = [], []
NOFLOW = []
fig, axs = plt.subplots(2, 2, figsize=(12, 9.6))
axs = axs.ravel()
AX_HEAT, AX_DEV, AX_RET, AX_PEAK = axs   # the four KPIs in the order of the chapter
VALUE = [(AX_HEAT, lambda r: r[3], "{:.0f}"), (AX_DEV, lambda r: r[0] + r[1], "{:.0f}"),
         (AX_RET, lambda r: r[2], "{:.1f}"), (AX_PEAK, lambda r: r[4], "{:.1f}")]
for i, (f, _) in enumerate(FLOORS):
    base = i * GAP
    for j, (c, lab, _) in enumerate(CONTROLS):
        xt.append(base + j); xl.append(lab.replace(" + ", " +\n"))
        for k, s in enumerate(CONTROLLED):
            x = base + j + (k - 0.5) * w
            for ax, val, fmt in VALUE:
                b = ax.bar(x, val(res[s, f, c]), w, color=SHADES[s], edgecolor="#555", lw=0.5,
                           label=s if (i, j) == (0, 0) else None)
                v = val(res[s, f, c])
                if v == v:
                    ax.bar_label(b, [fmt.format(v)], fontsize=7.5, padding=1)
                else:        # loop never opened on the cloudy day
                    NOFLOW.append((ax, x))
    x = base + 2                                       # self-regulation: no room control, same for both controls
    xt.append(x); xl.append("Self-\nregulation")
    for ax, val, fmt in VALUE:
        b = ax.bar(x, val(res[SELF, f, "pi"]), w, color=SHADES[SELF], edgecolor="#555", lw=0.5,
                   label=LABELS[SELF] if i == 0 else None)
        ax.bar_label(b, [fmt.format(val(res[SELF, f, "pi"]))], fontsize=7.5, padding=1)
    x0, x1 = base - 0.45, base + 2.3                   # ideal heater reference per floor
    AX_DEV.plot([x0, x1], [sum(ideal[f][:2])] * 2, color="#333", ls=(0, (5, 3)), lw=1)
    AX_HEAT.plot([x0, x1], [ideal[f][3]] * 2, color="#333", ls=(0, (5, 3)), lw=1)
    AX_PEAK.plot([x0, x1], [ideal[f][4]] * 2, color="#333", ls=(0, (5, 3)), lw=1)
AX_DEV.text(-0.45, sum(ideal["Light floor"][:2]) + 0.8, "ideal heater", fontsize=8.5, color="#333")
AX_HEAT.text(-0.45, ideal["Light floor"][3] - 12, "ideal heater", fontsize=8.5, color="#333")
AX_HEAT.set_ylabel("Heating energy [Wh/m²]")
AX_HEAT.set_title("a) Heating energy, both days", fontsize=11, loc="left")
AX_HEAT.set_ylim(0, max(200, 1.08 * max(r[3] for r in res.values())))
AX_DEV.set_ylabel("Deviation from the setpoint [K·h]")
AX_DEV.set_title("b) Deviation from the setpoint, cloudy day", fontsize=11, loc="left")
AX_DEV.set_ylim(0, 45)
AX_RET.set_ylabel("Return temperature, flow-weighted [°C]")
AX_RET.set_title("c) Return temperature, cloudy day", fontsize=11, loc="left")
AX_RET.set_ylim(20, max(32, 1.04 * max(r[2] for r in res.values() if r[2] == r[2])))
AX_PEAK.text(-0.45, ideal["Light floor"][4] + 0.2, "ideal heater", fontsize=8.5, color="#333")
AX_PEAK.axhline(1, color="#999", lw=0.8)
AX_PEAK.set_ylabel("Peak hour / mean [-]")
AX_PEAK.set_title("d) Peak-to-average ratio of the heat input, cloudy day", fontsize=11, loc="left")
AX_PEAK.set_ylim(0, max(15, 1.08 * max(r[4] for r in res.values() if r[4] == r[4])))
for ax, x in NOFLOW:
    ax.text(x, ax.get_ylim()[0] + 0.02 * (ax.get_ylim()[1] - ax.get_ylim()[0]), "no\nflow", ha="center", va="bottom", fontsize=7, color="#555")
for ax in axs:
    ax.set_xticks(xt, xl, fontsize=8.5)
    for i, (f, _) in enumerate(FLOORS):
        ax.annotate(f, (i * GAP + 1, 0), xycoords=("data", "axes fraction"), xytext=(0, -38),
                    textcoords="offset points", ha="center", va="top", fontsize=10, fontweight="bold")
    ax.grid(axis="y", color="#e4e4e4", lw=0.6); ax.set_axisbelow(True)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
h, l = AX_HEAT.get_legend_handles_labels()
fig.legend(h, l, ncol=3, frameon=False, fontsize=9.5, loc="upper center")
fig.tight_layout(rect=(0, 0, 1, 0.965), h_pad=2.5)
for ext in ("svg", "png"):
    fig.savefig(OUT / f"{NAME}.{ext}", dpi=200)
