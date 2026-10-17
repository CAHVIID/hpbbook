"""Schematic of the three window types tested by Heiselberg et al. (1999). Drawn, not copied."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.path import Path
RED, DARK, GREY, BLUE = "#990000", "#262626", "#8C8C8C", "#2F6DB5"
plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 13})
fig, axs = plt.subplots(1, 3, figsize=(12.5, 4.8))
H = 3.0

def room(ax, title, sub):
    ax.set_xlim(-0.6, 3.6); ax.set_ylim(-0.3, 3.35); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((-0.25, 0), 0.25, H, color="#D9D9D9", lw=0))
    ax.plot([0, 3.4], [0, 0], color=DARK, lw=1.5); ax.plot([0, 3.4], [H, H], color=DARK, lw=1.5)
    ax.add_patch(Rectangle((0, 0), 3.4, 1.8, color="#F6E6E6", lw=0)); ax.text(3.35, 1.62, "occupied zone", ha="right", color=RED, fontsize=11)
    ax.text(-0.55, H + 0.15, "cold side", color=BLUE, fontsize=11)
    ax.set_title(title, loc="left", fontsize=14, fontweight="bold", color=DARK); ax.text(-0.55, -0.27, sub, fontsize=11, color=GREY)

def opening(ax, y0, y1):  # glazed opening in the wall
    ax.add_patch(Rectangle((-0.25, y0), 0.25, y1 - y0, color="white", lw=0))
    ax.plot([-0.25, 0], [y0, y0], color=DARK, lw=1.5); ax.plot([-0.25, 0], [y1, y1], color=DARK, lw=1.5)

def flow(ax, pts, ls="-", col=BLUE):
    codes = [Path.MOVETO] + [Path.CURVE4] * (len(pts) - 1)
    ax.add_patch(FancyArrowPatch(path=Path(pts, codes), arrowstyle="-|>", mutation_scale=18, color=col, lw=2.4, linestyle=ls))

# Type 1: side-hung, opens over the full height; slow cold air falls and spreads along the floor
a = axs[0]; room(a, "Type 1: side-hung", "full-height opening near the occupied zone")
opening(a, 0.6, 2.4)
a.plot([0, 0], [0.6, 2.4], color=DARK, lw=1, ls=":")  # hinge line seen in section
for k, y in enumerate((1.1, 1.6, 2.1)):
    flow(a, [(-0.2, y), (0.3 + 0.25 * k, y), (0.35 + 0.35 * k, 0.12 + 0.1 * k), (1.8 + 0.5 * k, 0.12 + 0.1 * k)])
a.text(1.0, 2.2, "slow inflow over the\nwhole height falls and\nspreads along the floor", fontsize=11, color=BLUE)

# Type 2: narrow bottom-hung window high in the wall: ceiling jet, or drops
a = axs[1]; room(a, "Type 2: bottom-hung, high", "narrow window high in the wall")
opening(a, 2.45, 2.85)
a.plot([0, 0.32], [2.45, 2.8], color=DARK, lw=3)  # sash tilted in at the top, hinge at the bottom
flow(a, [(-0.2, 2.6), (0.6, 2.95), (1.8, 2.95), (3.1, 2.9)])
flow(a, [(-0.2, 2.55), (0.9, 2.75), (0.9, 0.2), (2.6, 0.15)], ls="--")
a.text(1.6, 2.55, "ceiling jet (small ΔT,\nlarge momentum)", fontsize=11, color=BLUE)
a.text(1.65, 0.75, "drops (large ΔT,\nweak driving force)", fontsize=11, color=BLUE)

# Type 3: horizontal pivot near the occupied zone; the sash angle steers the jet
a = axs[2]; room(a, "Type 3: horizontal pivot", "sash turns about a horizontal axis")
opening(a, 1.55, 2.35)
a.plot([0.28, -0.08], [2.25, 1.65], color=DARK, lw=3)  # bottom-hung opening in: top edge tilts in
a.plot([-0.08, 0.28], [2.25, 1.65], color=GREY, lw=2, ls="--")  # top-hung opening in: bottom edge tilts in
a.plot([0.1], [1.95], "o", color=DARK, ms=6)
flow(a, [(-0.2, 2.0), (0.5, 2.85), (1.8, 2.97), (3.2, 2.9)])
flow(a, [(-0.2, 1.9), (0.6, 1.5), (0.8, 0.25), (1.6, 0.18)], ls="--")
a.text(1.35, 2.3, "bottom-hung, opening in:\nceiling jet", fontsize=11, color=BLUE)
a.text(1.45, 0.75, "top-hung, opening in:\nfree jet, high velocity", fontsize=11, color=BLUE)

fig.text(0.01, -0.03, "Schematic after Heiselberg et al. (1999). Solid and dashed arrows: two outcomes or two configurations. Proportions are illustrative.", color=GREY, fontsize=11)
fig.tight_layout()
for ext in ("png", "svg"): fig.savefig(f"/mnt/project-files/cooling/slides/figures/window-types-heiselberg.{ext}", dpi=200, bbox_inches="tight")
