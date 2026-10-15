"""Schematic of a recirculating shower: shower head, collection in the shower floor, filter, UV lamp, electric heater
and pump in a loop, with fresh water make-up and a drain valve. Writes recirc-shower-schematic.svg/.png."""
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "figures" / "c4"

INK, MUTED, WARM, COLD, GREY = "#1f1f1e", "#6b6a63", "#eb6834", "#2a78d6", "#d9d7cf"
fig, ax = plt.subplots(figsize=(8, 4.6)); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")

def box(x, y, w, h, text, fc="white"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=fc, ec=INK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9.5, color=INK)

def arrow(p, q, c=WARM, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=12, color=c, lw=2, linestyle=ls))

# shower cubicle
ax.plot([0.6, 0.6, 3.4, 3.4], [5.5, 0.9, 0.9, 5.5], color=GREY, lw=3)
ax.plot([1.6, 2.4], [5.1, 5.1], color=INK, lw=4); ax.text(2.0, 5.35, "shower head", ha="center", fontsize=9, color=INK)
for x in (1.7, 1.85, 2.0, 2.15, 2.3):
    ax.plot([x, x + (x - 2.0) * 0.6], [5.0, 1.3], color=WARM, lw=0.8, ls=(0, (2, 3)))
ax.add_patch(FancyBboxPatch((1.2, 0.9), 1.6, 0.25, boxstyle="square,pad=0", fc=WARM, ec="none", alpha=0.6))
ax.text(2.0, 0.55, "collection in the shower floor", ha="center", fontsize=9, color=INK)

# treatment chain
box(4.4, 0.75, 1.2, 0.55, "filter")
box(6.1, 0.75, 1.2, 0.55, "UV lamp")
box(7.8, 0.75, 1.5, 0.55, "water quality\nsensors")
box(7.8, 2.6, 1.5, 0.6, "electric heater\n2.5 kW", fc="#fde6dc")
box(7.8, 4.4, 1.5, 0.55, "pump")
arrow((2.8, 1.02), (4.35, 1.02)); arrow((5.65, 1.02), (6.05, 1.02)); arrow((7.35, 1.02), (7.75, 1.02))
arrow((8.55, 1.35), (8.55, 2.55)); arrow((8.55, 3.25), (8.55, 4.35))
ax.annotate("", xy=(2.45, 5.1), xytext=(7.75, 4.67),
            arrowprops=dict(arrowstyle="-|>", color=WARM, lw=2, connectionstyle="angle,angleA=180,angleB=90,rad=0"))
ax.text(5.1, 4.82, "recirculated water, 40 °C", fontsize=9, color=WARM)

# fresh water and drain
arrow((6.1, 3.4), (7.75, 3.0), c=COLD); ax.text(4.0, 3.45, "fresh water from the central\nhot water system, about 15 L", fontsize=9, color=COLD)
arrow((9.35, 1.02), (9.85, 1.02), c=MUTED, ls="--"); ax.text(9.9, 0.3, "to drain if quality is poor", ha="right", fontsize=8.5, color=MUTED)
fig.tight_layout()
for ext in ("svg", "png"): fig.savefig(OUT / f"recirc-shower-schematic.{ext}", dpi=200)
