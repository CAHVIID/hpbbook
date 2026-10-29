"""Section through a bathroom pod set in a recess in the floor slab, with the installation shaft next to it and the
connections between pod and building. Dimensions from the Probad interface document (2021). Drawn to scale in mm,
except the pipes. Writes pod-section.svg/.png."""
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "figures" / "e1"

INK, MUTED, WARM, COLD, GREY, CONC = "#1f1f1e", "#6b6a63", "#eb6834", "#2a78d6", "#d9d7cf", "#bdbab0"
DRAIN, AIR, POWER = "#7a5c3e", "#3a9a6a", "#b8a200"
fig, ax = plt.subplots(figsize=(9, 6.2)); ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(-1100, 5300); ax.set_ylim(-1050, 2950)

slab, recess, gap = 300, 200, 30           # slab thickness, recess depth (75 mm drain under pod), side clearance
x0, w = 0, 2580                            # pod outer width
floor, wall, hin, roof = 100, 45, 2220, 40  # pod floor incl. tile, wall incl. tile, internal height, roof
ffl = 0                                    # finished floor level of pod = dwelling floor
storey = 2900                              # floor to floor (illustrative)

# slab with recess, and the slab above
def conc(x, y, ww, hh): ax.add_patch(Rectangle((x, y), ww, hh, fc=CONC, ec=INK, lw=0.8, hatch="..."))
conc(-1100, -slab, 1100 - gap, slab); conc(-gap, -slab, w + 2 * gap, slab - recess)
conc(x0 + w + gap, -slab, 80, slab - recess)
conc(-1100, storey - slab, 3800 + 1100, slab)
ax.text(-1050, ffl + 40, "dwelling floor", fontsize=8.5, color=MUTED)

# shims and neoprene blocks
top_recess = -recess
for xs in (60, w - 160):
    ax.add_patch(Rectangle((xs, top_recess), 100, 30, fc=INK, ec="none"))
pod_bottom = top_recess + 30 + 70         # drain run under the pod (75 mm pipe builds 90 mm)

# pod: floor, walls, roof
base = ffl - floor
ax.add_patch(Rectangle((x0, base), w, floor, fc="#e9e6de", ec=INK, lw=1.2))
ax.add_patch(Rectangle((x0, ffl), wall, hin, fc="#e9e6de", ec=INK, lw=1.2))
ax.add_patch(Rectangle((x0 + w - wall, ffl), wall, hin, fc="#e9e6de", ec=INK, lw=1.2))
ax.add_patch(Rectangle((x0, ffl + hin), w, roof, fc="#e9e6de", ec=INK, lw=1.2))
ax.text(w / 2, 1150, "bathroom pod\nfactory-finished:\nmembrane, tiles, fittings,\npipes, cables, lights", ha="center",
        va="center", fontsize=9.5, color=INK)

# installation shaft
sx = x0 + w + gap + 80
ax.add_patch(Rectangle((sx, -slab - 350), 520, storey + slab + 350 + 100, fc="none", ec=MUTED, lw=1, ls=(0, (4, 3))))
conc(sx + 520, -slab, 3800 - (sx + 520), slab)
ax.text(sx + 260, -slab - 400, "installation shaft", ha="center", va="top", fontsize=9, color=MUTED)
ax.plot([sx + 90] * 2, [-slab - 300, storey + 100], color=DRAIN, lw=5)        # drain stack
ax.plot([sx + 200] * 2, [-slab - 300, storey + 100], color=COLD, lw=2)        # cold water
ax.plot([sx + 260] * 2, [-slab - 300, storey + 100], color=WARM, lw=2)        # hot water
ax.plot([sx + 400] * 2, [-slab - 300, storey + 100], color=AIR, lw=7, alpha=0.7)  # exhaust duct

# floor drain and WC connection to the stack
ax.plot([700, 700], [ffl - 10, pod_bottom - 45], color=DRAIN, lw=3)
ax.plot([700, sx + 90], [pod_bottom - 45, pod_bottom - 45], color=DRAIN, lw=3)
ax.plot([w - 300, sx + 90], [260, 260], color=DRAIN, lw=4)
ax.text(4000, pod_bottom - 45, "75 mm floor drain\nunder the pod", fontsize=8, color=DRAIN, va="center")
ax.text(4000, 260, "WC drain 110 mm,\n260 mm above floor", fontsize=8, color=DRAIN, va="center")

# water from the distribution cabinet in the roof
ax.add_patch(Rectangle((w - 900, ffl + hin + roof), 550, 95, fc="white", ec=INK, lw=0.8))
ax.text(w - 625, ffl + hin + roof + 160, "distribution cabinet", fontsize=8, ha="center", color=INK)
for dx, c in ((0, COLD), (25, WARM)):
    ax.plot([w - 350, sx + 200 + dx * 2.4], [ffl + hin + roof + 40 + dx] * 2, color=c, lw=1.6)
ax.text(4000, ffl + hin + roof + 50, "hot and cold water,\nPEX 20 mm, 2 m coils", fontsize=8, color=COLD, va="center")

# exhaust from the roof sleeve
ax.plot([400, 400, sx + 400], [ffl + hin + roof, ffl + hin + roof + 170, ffl + hin + roof + 170], color=AIR, lw=5,
        alpha=0.7)
ax.text(4000, ffl + hin + roof + 300, "exhaust valve and sleeve\nin the roof, bend 170 mm", fontsize=8,
        color=AIR, va="center")

# electricity
ax.plot([1500, 1500, -500], [ffl + hin + roof, ffl + hin + roof + 90, ffl + hin + roof + 90], color=POWER, lw=1.6)
ax.text(-1050, ffl + hin + roof - 60, "cables to the\nconsumer unit,\n8 m coils", fontsize=8, color=POWER, va="top")

# leaders to the labels right of the shaft
for y in (pod_bottom - 45, 260, ffl + hin + roof + 50, ffl + hin + roof + 300):
    ax.plot([sx + 540, 3950], [y, y], color=GREY, lw=0.6)

# dimensions
def dim(x, y1, y2, label, side=-1):
    ax.add_patch(FancyArrowPatch((x, y1), (x, y2), arrowstyle="<->", mutation_scale=8, color=INK, lw=0.8))
    ax.text(x + side * 30, (y1 + y2) / 2, label, fontsize=8, ha="right" if side < 0 else "left", va="center",
            color=INK, rotation=0)
dim(-150, ffl, ffl + hin, "2220 mm\ninside")
ax.annotate("recess 110–200 mm\n(200 mm with a 75 mm\ndrain under the pod)", xy=(1300, -200), xytext=(-1050, -760), fontsize=8, color=INK,
            arrowprops=dict(arrowstyle="-", color=INK, lw=0.6))
ax.annotate("neoprene pads\nand shims", xy=(110, top_recess + 15), xytext=(700, -800), fontsize=8, color=INK,
            arrowprops=dict(arrowstyle="-", color=INK, lw=0.6))
ax.annotate("≥ 30 mm\nall round", xy=(-15, -60), xytext=(-1050, 330), fontsize=8, color=INK,
            arrowprops=dict(arrowstyle="-", color=INK, lw=0.6))
ax.text(w / 2, 90, "floor 100 mm incl. tile, falls to the drain", fontsize=8, ha="center", color=INK)

OUT.mkdir(parents=True, exist_ok=True)
for ext in ("svg", "png"):
    fig.savefig(OUT / f"pod-section.{ext}", dpi=200, bbox_inches="tight")
