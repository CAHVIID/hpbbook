"""Figures for the drain water heat recovery sections of ch 6.
Writes dwhr-units, dwhr-connections and dwhr-effectiveness (.svg/.png). Model in dwhr_model.py."""
import numpy as np
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon
import dwhr_model as m
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "figures" / "ch04"

BLUE, ORANGE, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#1f1f1e", "#6b6a63", "#e4e3dc"
GREEN, PURPLE, RED = "#2f9e6e", "#7b5cc4", "#c8423b"
COPPER, LIGHT = "#c27c3e", "#f3f2ee"


def style(ax):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED); ax.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)


def arrow(ax, p0, p1, color, lw=2.2):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=14, color=color, lw=lw))


# ---------------------------------------------------------------- A1 unit sections
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 5.8), gridspec_kw=dict(width_ratios=[1, 1.45]))
for ax in (a1, a2): ax.set_aspect("equal"); ax.axis("off")
GREY = "#d9d6cc"


def lab(ax, text, xy, xytext):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=9, color=INK, va="center",
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))


# vertical unit, section through the centre line
a1.set_xlim(-6.2, 5.4); a1.set_ylim(-1.0, 11.0)
a1.add_patch(Rectangle((-0.95, -0.3), 1.9, 10.6, color="white"))                       # air inside the pipe
a1.add_patch(Rectangle((-0.95, 0.8), 0.18, 8.4, color=ORANGE))                          # falling water film
a1.add_patch(Rectangle((0.77, 0.8), 0.18, 8.4, color=ORANGE))
for x in (-1.0, 1.0): a1.plot([x, x], [-0.3, 10.3], color=COPPER, lw=3, solid_capstyle="butt")  # copper drain pipe wall
for y in np.arange(1.1, 9.0, 0.48):                                                       # cold water coil, seen in section
    for x in (-1.42, 1.42):
        a1.add_patch(plt.Circle((x, y), 0.2, fc=BLUE, ec=COPPER, lw=1.5))
arrow(a1, (0, 10.8), (0, 9.6), ORANGE); arrow(a1, (0, 0.6), (0, -0.8), ORANGE)
a1.text(-6.1, 10.4, "warm drain water\nfrom the shower, 37 °C", fontsize=9, color=INK, va="center")
a1.text(-6.1, -0.5, "to the sewer, 18 °C", fontsize=9, color=INK, va="center")
arrow(a1, (3.0, 1.1), (1.7, 1.1), BLUE); a1.text(3.1, 1.1, "cold water in,\n10 °C", fontsize=9, color=INK, va="center")
arrow(a1, (1.7, 8.8), (3.0, 8.8), BLUE); a1.text(3.1, 8.8, "preheated water\nout, 29 °C", fontsize=9, color=INK, va="center")
lab(a1, "the drain water runs\ndown as a thin film\non the inside wall", (-0.86, 6.5), (-6.1, 7.2))
lab(a1, "copper drain pipe", (-1.0, 4.6), (-6.1, 4.6))
lab(a1, "cold water flows up in\na copper coil wound\naround the pipe", (-1.6, 2.6), (-6.1, 2.2))
a1.text(0, 5.0, "air", fontsize=9, color=MUTED, ha="center")
a1.set_title("Vertical unit, 1.5–2 m of drain pipe", fontsize=10, color=INK, loc="left")

# horizontal unit: channel drain, section along the channel plus section across it
a2.set_xlim(-0.6, 12.2); a2.set_ylim(-3.6, 7.6)
a2.add_patch(Rectangle((-0.6, 4.0), 12.8, 0.35, color=GREY))                              # floor
a2.add_patch(Rectangle((0.8, 2.0), 8.0, 2.0, fc="white", ec=MUTED, lw=1.2))               # channel body
a2.plot([0.8, 8.8], [4.0, 4.0], color=MUTED, lw=1.2, ls=(0, (2, 2)))                      # grate
a2.add_patch(Rectangle((0.85, 2.05), 7.35, 0.7, color=ORANGE))                            # shallow drain water layer
a2.add_patch(Rectangle((1.0, 2.2), 7.2, 0.32, fc=BLUE, ec=COPPER, lw=1.5))                # copper tubes, side view
a2.add_patch(Rectangle((8.2, 0.6), 0.6, 1.4, fc="white", ec=MUTED, lw=1.2))               # outlet
arrow(a2, (8.5, 1.9), (8.5, 0.2), ORANGE)
a2.text(8.95, 0.9, "to the sewer,\n24 °C", fontsize=9, color=INK, va="center")
for x in (2.2, 3.6, 5.0): arrow(a2, (x, 6.6), (x + 0.3, 4.3), ORANGE, lw=1.5)
a2.text(1.0, 7.0, "shower water falls through the grate, 37 °C", fontsize=9, color=INK)
arrow(a2, (1.6, 2.85), (6.6, 2.85), ORANGE, lw=1.2)
a2.text(9.3, 3.0, "A", fontsize=9, color=INK, weight="bold"); a2.plot([9.1, 9.1], [1.9, 4.1], color=INK, lw=1)
arrow(a2, (9.9, 2.3), (8.25, 2.3), BLUE); a2.text(10.0, 2.3, "cold in,\n10 °C", fontsize=9, color=INK, va="center")
arrow(a2, (1.0, 2.3), (-0.5, 2.3), BLUE); a2.text(-0.5, 1.8, "preheated\nout, 24 °C", fontsize=9, color=INK, va="top")
lab(a2, "copper tubes in the channel bottom,\ncold water flows against the drain water", (5.0, 2.36), (2.0, 0.9))
a2.text(1.6, 3.2, "drain water flows along the channel", fontsize=8.5, color=INK)
# section A-A across the channel
cx, cy = 4.0, -2.4
a2.text(cx - 2.4, cy + 1.25, "Section A, across the channel", fontsize=9, color=INK, weight="bold")
a2.plot([cx - 1.6, cx - 1.6, cx + 1.6, cx + 1.6], [cy + 0.9, cy - 0.8, cy - 0.8, cy + 0.9], color=MUTED, lw=1.2)
a2.add_patch(Rectangle((cx - 1.55, cy - 0.78), 3.1, 0.68, color=ORANGE))                 # water fills the bottom
for x in np.arange(cx - 1.25, cx + 1.3, 0.5):
    a2.add_patch(plt.Circle((x, cy - 0.45), 0.22, fc=BLUE, ec=COPPER, lw=1.5))
lab(a2, "the drain water flows around\nand over the tubes", (cx + 1.0, cy - 0.15), (cx + 2.3, cy + 0.5))
a2.set_title("Horizontal unit in a shower channel drain", fontsize=10, color=INK, loc="left")

handles = [Line2D([], [], color=ORANGE, lw=6), Line2D([], [], color=BLUE, lw=6), Line2D([], [], color=COPPER, lw=3)]
fig.legend(handles, ["warm drain water", "cold drinking water", "copper wall"], loc="lower center", ncol=3,
           frameon=False, fontsize=9)
fig.tight_layout(rect=(0, 0.06, 1, 1))
for ext in ("svg", "png"): fig.savefig(OUT / f"dwhr-units.{ext}", dpi=200)
plt.close(fig)

# ---------------------------------------------------------------- A2 connections
E = 0.60
res = {c: m.shower(E, c) for c in (1, 2, 3)}
fig, axes = plt.subplots(1, 3, figsize=(10.5, 4.4))
titles = {1: "1  Preheat to the shower mixer", 2: "2  Preheat to the water heater", 3: "3  Preheat to both (equal flow)"}
for ax, c in zip(axes, (1, 2, 3)):
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_aspect("equal"); ax.axis("off")
    r = res[c]
    # components
    ax.add_patch(Rectangle((0.3, 6.3), 2.2, 2.8, fc=LIGHT, ec=INK)); ax.text(1.4, 7.7, "water\nheater\n55 °C", ha="center", va="center", fontsize=8.5)
    ax.add_patch(plt.Circle((6.0, 8.6), 0.45, fc="white", ec=INK)); ax.text(6.0, 8.6, "M", ha="center", va="center", fontsize=9)
    ax.text(6.0, 9.4, "mixer 40 °C", ha="center", fontsize=8.5)
    ax.plot([6.0, 6.0], [8.15, 5.6], color=PURPLE, lw=2); ax.text(6.2, 6.5, "shower\n8 L/min", fontsize=8.5)
    ax.add_patch(Rectangle((7.4, 0.6), 1.0, 4.4, fc=LIGHT, ec=COPPER, lw=2)); ax.text(8.6, 2.8, "DWHR", fontsize=8.5, rotation=90, va="center")
    ax.plot([6.0, 7.9, 7.9], [5.2, 5.2, 5.0], color=ORANGE, lw=2.4); arrow(ax, (7.9, 0.6), (7.9, -0.2), ORANGE)
    ax.text(3.6, 5.45, "drain 37 °C", fontsize=8.5, color=INK)
    ax.text(5.9, -0.1, f"{37 - (r['t_p'] - 10) * r['v_cold_side'] / 8:.0f} °C", fontsize=8.5, color=INK)
    # cold mains
    ax.text(0.2, 0.3, "cold 10 °C", fontsize=8.5)
    vc = r["v_cold_side"]; tp = r["t_p"]
    if c == 1:
        ax.plot([0.5, 1.4, 1.4], [0.9, 0.9, 6.3], color=BLUE, lw=2)                      # mains to heater
        ax.plot([1.4, 7.0, 7.0], [0.9, 0.9, 1.0], color=BLUE, lw=2); arrow(ax, (7.0, 0.9), (7.4, 0.9), BLUE)
        ax.plot([7.4, 6.9, 6.9, 6.45], [4.6, 4.6, 8.6, 8.6], color=GREEN, lw=2)        # preheated to mixer cold
    elif c == 2:
        ax.plot([0.5, 4.5, 4.5, 5.6, 5.6], [0.9, 0.9, 7.6, 7.6, 8.3], color=BLUE, lw=2)   # mains to mixer cold
        ax.plot([4.5, 7.0], [0.9, 0.9], color=BLUE, lw=2); arrow(ax, (7.0, 0.9), (7.4, 0.9), BLUE)
        ax.plot([7.4, 3.2, 3.2, 1.4, 1.4], [4.6, 4.6, 5.6, 5.6, 6.3], color=GREEN, lw=2)  # preheated to heater
    else:
        ax.plot([0.5, 7.0], [0.9, 0.9], color=BLUE, lw=2); arrow(ax, (7.0, 0.9), (7.4, 0.9), BLUE)
        ax.plot([7.4, 6.9, 6.9, 6.45], [4.6, 4.6, 8.6, 8.6], color=GREEN, lw=2)
        ax.plot([6.9, 3.2, 3.2, 1.4, 1.4], [4.6, 4.6, 5.6, 5.6, 6.3], color=GREEN, lw=2)
    ax.plot([2.5, 5.55], [8.6, 8.6], color=RED, lw=2)                                    # hot to mixer
    ax.text(4.7 if c == 2 else 2.2, 2.4, f"{vc:.1f} L/min\nat {tp:.0f} °C", fontsize=8.5, color=GREEN)
    ax.set_title(titles[c], fontsize=9.5, color=INK, loc="left")
    ax.text(0.2, -1.2, f"Heat from the heater cut by {r['saving'] * 100:.0f} %", fontsize=9.5, color=INK, weight="bold")
fig.tight_layout()
for ext in ("svg", "png"): fig.savefig(OUT / f"dwhr-connections.{ext}", dpi=200)
plt.close(fig)

# ---------------------------------------------------------------- A3 effectiveness plots
fig, (p1, p2) = plt.subplots(1, 2, figsize=(9.5, 3.9))
v = np.linspace(4, 14, 101)
cols = [BLUE, GREEN, PURPLE, ORANGE, RED]
for (name, typ, e), col in zip(m.PRODUCTS, cols):
    p1.plot(v, [m.shower(e, 3, v=x)["eps"] for x in v], color=col, lw=2, label=f"{name} ({typ})")
    p1.plot([8], [e], "o", color=col, ms=5)
p1.axvline(8, color=MUTED, lw=0.8, ls="--"); p1.text(8.2, 0.33, "PHI test\n8 L/min", fontsize=8.5, color=MUTED)
p1.set_xlabel("Shower flow, L/min", fontsize=10, color=INK); p1.set_ylabel("Effectiveness ε, equal flow", fontsize=10, color=INK)
p1.set_ylim(0.3, 0.95); p1.legend(frameon=False, fontsize=7.5, loc="upper right"); style(p1)
p1.set_title("Effectiveness falls with flow", fontsize=10, color=INK, loc="left")
er = np.linspace(0.3, 0.75, 46)
for c, col, lab in ((3, GREEN, "3 to both (equal flow)"), (2, ORANGE, "2 to the water heater"), (1, BLUE, "1 to the shower mixer")):
    p2.plot(er, [m.shower(x, c)["saving"] * 100 for x in er], color=col, lw=2, label=lab)
p2.set_xlabel("Certified effectiveness at 8 L/min", fontsize=10, color=INK); p2.set_ylabel("Shower heat saved, %", fontsize=10, color=INK)
p2.legend(frameon=False, fontsize=8.5, loc="upper left"); style(p2)
p2.set_title("Saving by connection, 8 L/min shower", fontsize=10, color=INK, loc="left")
fig.tight_layout()
for ext in ("svg", "png"): fig.savefig(OUT / f"dwhr-effectiveness.{ext}", dpi=200)
print("connections at eps 0.60:", {c: (round(r['t_p'], 1), round(r['v_cold_side'], 2), round(r['saving'], 3)) for c, r in res.items()})
