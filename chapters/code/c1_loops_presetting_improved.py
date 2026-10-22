"""Floor plan with one floor heating loop per room, and the pre-setting of the loop valves.

- floor-loops:          a 100 m² single-storey house, 8 x 12.5 m, with the loops drawn to scale from the
                        manifold. The loop lengths are measured on the drawing.
- presetting-valve:     pressure drop against flow for a loop valve with pre-settings 1-7 and N, with the
                        operating point of each loop in the house.
- presetting-flows:     flow in each loop with all valves fully open and with the pre-settings,
                        against the design flow.

Assumptions (illustrative, not product data):
- Pipe PE-X 16 x 2 mm (inner diameter 12 mm), water at 33 °C. Friction: 64/Re below Re = 2300,
  Blasius above. Bends and fittings are ignored.
- Design heat flux 12 W/m² in living rooms and bedrooms, 10 W/m² in the hall, 40 W/m² in the
  bathroom (comfort floor). Supply/return 35/30 °C.
- Valve flow coefficients Kv for pre-settings 1-7 and N are typical values for a small
  pre-settable valve, read approximately from a manufacturer chart.
- The pump is set so that the loop with the largest pressure drop gets its design flow with its
  valve fully open (N). Each other loop gets the pre-setting closest to the Kv it needs.

Writes figures/c1/<name>.svg and .png.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter

OUT = Path(__file__).resolve().parent.parent / "figures" / "c1"
INK, MUTED, SURF = "#0b0b0b", "#52514e", "#fcfcfb"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "font.family": "DejaVu Sans"})

# room: name, wall rectangle (x0, y0, x1, y1) in m
ROOMS = [("Living and kitchen", (0, 0, 6.5, 8)), ("Hall", (6.5, 2.5, 8.5, 8)), ("Bathroom", (6.5, 0, 8.5, 2.5)),
         ("Bedroom 1", (8.5, 4.5, 12.5, 8)), ("Bedroom 2", (8.5, 0, 12.5, 4.5))]
MANIFOLD = (6.62, 5.0)
# loop: label, room, area covered (x0, y0, x1, y1), spacing (m), design heat flux (W/m²), colour
LOOPS = [("1", "Living and kitchen", (0, 4, 6.5, 8), 0.3, 12, "#d6493a"),
         ("2", "Living and kitchen", (0, 0, 6.5, 4), 0.3, 12, "#eb6834"),
         ("3", "Hall", (6.5, 2.5, 8.5, 8), 0.3, 10, "#8a5cc2"),
         ("4", "Bathroom", (6.5, 0, 8.5, 2.5), 0.15, 40, "#199e70"),
         ("5", "Bedroom 1", (8.5, 4.5, 12.5, 8), 0.3, 12, "#1c5cab"),
         ("6", "Bedroom 2", (8.5, 0, 12.5, 4.5), 0.3, 12, "#2a9fd6")]
MARGIN = 0.15
# The hall coil keeps clear of the wall by the manifold, leaving a corridor for the leads.
COIL_RECT = {"3": (6.75, 2.5, 8.5, 8)}
# x of the vertical run of each lead (feed, return), m: living room leads between the coil turns and the
# wall, the others in the corridor in the hall
LEAD_X = {"1": (6.34, 6.38), "2": (6.26, 6.30), "3": (6.655, 6.625), "4": (6.595, 6.565),
          "5": (6.69, 6.72), "6": (6.75, 6.78)}
D_IN, RHO, NU, CP = 0.012, 995.0, 0.74e-6, 4180.0
SETTINGS = {"1": 0.18, "2": 0.25, "3": 0.31, "4": 0.40, "5": 0.55, "6": 0.68, "7": 0.80, "N": 0.95}  # Kv, m³/h


def save(fig, name):
    for ext in ("svg", "png"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=200, facecolor=SURF)


def serpentine(rect, s, entry):
    """Coil in rect with lanes along the long side, starting and ending at the corner nearest entry."""
    x0, y0, x1, y1 = rect
    w, h = x1 - x0, y1 - y0
    flipx, flipy = abs(entry[0] - x1) < abs(entry[0] - x0), abs(entry[1] - y1) < abs(entry[1] - y0)
    vertical = h >= w                                    # lanes run along y
    a, b = (w, h) if vertical else (h, w)                # a: across the lanes, b: along the lanes
    n = int((a - 2 * MARGIN) / s) + 1
    pts = []
    for k in range(n):
        p = MARGIN + k * s
        ends = [MARGIN + s / 2, b - MARGIN] if k % 2 == 0 else [b - MARGIN, MARGIN + s / 2]
        pts += [(p, ends[0]), (p, ends[1])]
    pts += [(pts[-1][0], MARGIN / 2), (MARGIN / 2, MARGIN / 2)]   # return ends beside the start, not on it
    pts = np.array(pts)
    if not vertical: pts = pts[:, ::-1]
    x = x0 + (w - pts[:, 0] if flipx else pts[:, 0]); y = y0 + (h - pts[:, 1] if flipy else pts[:, 1])
    return np.column_stack([x, y])


def plength(p):
    return float(np.hypot(*np.diff(p, axis=0).T).sum())


def pipe_dp(m_kgh, L):
    """Pressure drop (Pa) in L metres of pipe at a mass flow in kg/h."""
    v = m_kgh / 3600 / RHO / (np.pi * D_IN ** 2 / 4)
    re = max(v * D_IN / NU, 1e-9)
    f = 64 / re if re < 2300 else 0.316 * re ** -0.25
    return f * L / D_IN * RHO * v ** 2 / 2


def valve_dp(m_kgh, kv):
    return (m_kgh / RHO / kv) ** 2 * 1e5           # Kv in m³/h at 1 bar


def flow_at(dp, L, kv):
    lo, hi = 0.0, 2000.0
    for _ in range(80):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if pipe_dp(m, L) + valve_dp(m, kv) < dp else (lo, m)
    return m


# ---------------------------------------------------------------- floor plan
fig, ax = plt.subplots(figsize=(11, 7.4), facecolor=SURF, layout="constrained")
ax.set_facecolor(SURF)
loops = []
for i, (lab, room, rect, s, q, col) in enumerate(LOOPS):
    x0, y0, x1, y1 = rect
    corner = min([(x0, y0), (x0, y1), (x1, y0), (x1, y1)], key=lambda c: abs(c[0] - MANIFOLD[0]) + abs(c[1] - MANIFOLD[1]))
    coil = serpentine(COIL_RECT.get(lab, rect), s, MANIFOLD)
    off = 0.06 * (i - 2.5)
    def lead(end, o, xv):
        """Lead from the manifold to a coil end: out of the manifold at its own height, along x = xv,
        then straight into the coil end, so that no two pipes run on top of each other."""
        return np.array([(MANIFOLD[0] + 0.1, MANIFOLD[1] + o), (xv, MANIFOLD[1] + o), (xv, end[1]), end])
    feed, ret = lead(coil[0], off, LEAD_X[lab][0]), lead(coil[-1], off + 0.025, LEAD_X[lab][1])
    L = plength(coil) + plength(feed) + plength(ret)
    area = (x1 - x0) * (y1 - y0)
    phi = q * area
    loops.append(dict(lab=lab, room=room, L=L, area=area, phi=phi, m=phi / (CP * 5) * 3600, col=col))
    ax.plot(coil[:, 0], coil[:, 1], color=col, lw=1.0)
    ax.plot(feed[:, 0], feed[:, 1], color=col, lw=1.0, ls=(0, (3, 1.5)))
    ax.plot(ret[:, 0], ret[:, 1], color=col, lw=1.0, ls=(0, (3, 1.5)))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ax.text(cx, cy, f"{lab}\n{L:.0f} m", ha="center", va="center", fontsize=10, color=INK,
            bbox=dict(boxstyle="circle,pad=0.3", fc=SURF, ec=col, lw=1.5), zorder=5)
for name, (x0, y0, x1, y1) in ROOMS:
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, ec=INK, lw=2.2, zorder=4))
    ty = y1 - 0.12
    ax.text(x0 + 0.12, ty, name, ha="left", va="top", fontsize=9, color=INK, zorder=6,
            bbox=dict(fc=SURF, ec="none", pad=1.2))
ax.add_patch(Rectangle((MANIFOLD[0] - 0.12, MANIFOLD[1] - 0.35), 0.22, 0.7, fc=INK, ec=INK, zorder=7))
ax.annotate("Manifold", xy=(MANIFOLD[0] + 0.1, MANIFOLD[1] + 0.35), xytext=(7.0, 7.1), fontsize=9, color=INK, zorder=8,
            arrowprops=dict(arrowstyle="-", color=INK, lw=0.8), bbox=dict(fc=SURF, ec="none", pad=1.2))
ax.set_xlim(-0.3, 12.8); ax.set_ylim(-0.3, 8.3); ax.set_aspect("equal"); ax.axis("off")
save(fig, "floor-loops-improved")

# ---------------------------------------------------------------- pre-setting
for lp in loops:
    lp["dp_pipe"] = pipe_dp(lp["m"], lp["L"])
    lp["dp_open"] = lp["dp_pipe"] + valve_dp(lp["m"], SETTINGS["N"])
crit = max(loops, key=lambda lp: lp["dp_open"])
DP = crit["dp_open"]
for lp in loops:
    kv_need = lp["m"] / RHO / np.sqrt(max(DP - lp["dp_pipe"], 1e-9) / 1e5)
    lp["set"] = min(SETTINGS, key=lambda k: abs(np.log(SETTINGS[k] / kv_need)))
    lp["kv_need"] = kv_need
    lp["m_open"] = flow_at(DP, lp["L"], SETTINGS["N"])
    lp["m_set"] = flow_at(DP, lp["L"], SETTINGS[lp["set"]])
    lp["dp_valve"] = valve_dp(lp["m_set"], SETTINGS[lp["set"]])
    print(f"loop {lp['lab']} {lp['room']:18s} L {lp['L']:5.1f} m  A {lp['area']:5.1f} m2  phi {lp['phi']:4.0f} W  "
          f"design {lp['m']:5.1f} kg/h  pipe dp {lp['dp_pipe']:6.0f} Pa  Kv need {lp['kv_need']:.2f}  setting {lp['set']}  "
          f"flow open {lp['m_open']:5.1f}  flow preset {lp['m_set']:5.1f} kg/h")
print(f"manifold dp {DP:.0f} Pa, critical loop {crit['lab']}")

fig, ax = plt.subplots(figsize=(7.5, 5), facecolor=SURF, layout="constrained")
ax.set_facecolor(SURF)
q = np.logspace(np.log10(5), np.log10(1000), 100)            # l/h
for k, kv in SETTINGS.items():
    dp = (q / 1000 / kv) ** 2 * 100                            # kPa
    ax.loglog(q, dp, color=MUTED if k != "N" else INK, lw=1.0 if k != "N" else 1.6)
    qa = kv * 1000 * np.sqrt(30 / 100)
    ax.text(qa, 30 * 1.12, k, ha="center", va="bottom", fontsize=9, color=INK)
for lp in loops:
    ax.plot(lp["m_set"] / RHO * 1000, lp["dp_valve"] / 1000, "o", color=lp["col"], ms=7, zorder=5,
            label=f"Loop {lp['lab']}, {lp['room'].lower()}: setting {lp['set']}")
ax.set_xlim(5, 1000); ax.set_ylim(0.01, 40)
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}")); ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
ax.set_xlabel("Flow (l/h)"); ax.set_ylabel("Pressure drop over the valve (kPa)")
ax.grid(which="both", color="#e6e5e0", lw=0.5); ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=8, loc="lower right")
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
save(fig, "presetting-valve-improved")

fig, ax = plt.subplots(figsize=(7.5, 3.8), facecolor=SURF, layout="constrained")
ax.set_facecolor(SURF)
x = np.arange(len(loops)); w = 0.27
ax.bar(x - w, [lp["m"] for lp in loops], w, color="#c9c8c2", label="Design flow")
ax.bar(x, [lp["m_open"] for lp in loops], w, color="#d6493a", label="All valves fully open (N)")
ax.bar(x + w, [lp["m_set"] for lp in loops], w, color="#199e70", label="With pre-settings")
ax.set_xticks(x, [f"Loop {lp['lab']}\n{lp['room']}\n{lp['L']:.0f} m, setting {lp['set']}" for lp in loops], fontsize=8)
ax.tick_params(axis="x", length=0)
ax.set_ylabel("Flow (kg/h)")
ax.grid(axis="y", color="#e6e5e0", lw=0.6); ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=8, loc="upper right")
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
save(fig, "presetting-flows-improved")
