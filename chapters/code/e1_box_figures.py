"""Figures for chapter E1 Box building systems for type houses. Dimensions from lecture 19.1 (C. A. Hviid, 2025) and
the box layouts in lecture 21.3. Drawn to scale in metres unless noted. Writes SVG + PNG to figures/e1/:
build-methods, double-walls, bedroom-dimensions, box-width, box-height, floor-roof-solutions, pods-tech-room, box-layouts."""
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch, Circle
from pathlib import Path
import sys
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "figures" / "e1"
OUT.mkdir(parents=True, exist_ok=True)

INK, MUTED, WARM, COLD, GREY, CONC = "#1f1f1e", "#6b6a63", "#eb6834", "#2a78d6", "#d9d7cf", "#bdbab0"
INS, WOOD, AIR = "#f3e3a2", "#c9a46a", "#3a9a6a"
plt.rcParams.update({"font.size": 9, "svg.fonttype": "none"})


def save(fig, name):
    for ext in ("svg", "png"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def dim_h(ax, x0, x1, y, text, above=True, fs=8.5):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="<->", mutation_scale=8, lw=0.7, color=INK))
    ax.text((x0 + x1) / 2, y + (0.06 if above else -0.06), text, ha="center", va="bottom" if above else "top", fontsize=fs)


def dim_v(ax, x, y0, y1, text, left=True, fs=8.5):
    ax.add_patch(FancyArrowPatch((x, y0), (x, y1), arrowstyle="<->", mutation_scale=8, lw=0.7, color=INK))
    ax.text(x + (-0.07 if left else 0.07), (y0 + y1) / 2, text, ha="right" if left else "left", va="center", fontsize=fs)


def rect(ax, x, y, w, h, fc, ec=INK, lw=0.8, hatch=None, **kw):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, hatch=hatch, **kw))


# ---------------------------------------------------------------- 2. floor and roof: solution 1 vs solution 2
fig, axs = plt.subplots(1, 2, figsize=(10.5, 5.4))
for ax in axs:
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.9, 3.4); ax.set_ylim(-1.0, 4.55)

# Solution 1: low floor beams on concrete slab, roof on box
ax = axs[0]; ax.set_title("Solution 1: low floor on a slab, roof on the box", fontsize=10, loc="left")
ax.add_patch(Polygon([(-0.9, -0.15), (3.4, -0.15), (3.4, -1.0), (-0.9, -1.0)], fc="#e8e2d2", ec="none"))
ax.text(3.3, -0.85, "ground", ha="right", fontsize=8, color=MUTED)
rect(ax, -0.2, -0.44, 3.2, 0.40, INS, hatch="///")                       # EPS C60 2 x 200
rect(ax, -0.2, -0.04, 3.2, 0.12, CONC, hatch="...")                       # slab 120
gy = 0.08
rect(ax, 0, gy, 2.8, 0.02, "#444444", lw=0)                              # flexible layer
rect(ax, 0, gy + 0.02, 2.8, 0.10, WOOD)                                  # 0.10 floor beams
ax.text(-0.25, -0.30, "concrete slab on EPS\n(cast on site)", ha="right", va="center", fontsize=8)
ax.text(-0.05, gy + 0.62, "flexible layer +\n0.10 m beams", ha="right", va="center", fontsize=8)
fl = gy + 0.12
rect(ax, 0, fl, 0.10, 2.50, WOOD); rect(ax, 2.7, fl, 0.10, 2.50, WOOD)
rect(ax, 0, fl + 2.50, 2.8, 0.70, INS, hatch="///")
ax.text(1.4, fl + 2.85, "insulated roof on box", ha="center", va="center", fontsize=8.5, bbox=dict(fc="white", ec="none", pad=1))
ax.text(1.4, fl + 1.2, "room", ha="center", fontsize=10, color=MUTED)
dim_v(ax, 3.05, gy, fl, " 0.12", left=False, fs=8); dim_v(ax, 3.05, fl, fl + 2.5, "2.50", left=False)
dim_v(ax, 3.05, fl + 2.5, fl + 3.2, "0.70", left=False)
ax.text(1.4, fl + 3.35, "box height 3.3 m", ha="center", fontsize=8.5)
ax.text(1.4, -0.65, "floor 10–20 cm above ground", ha="center", fontsize=8.5)
ax.plot([-0.9, 3.0], [gy + 0.02, gy + 0.02], color="#990000", lw=1.3, ls=(0, (5, 3)))        # assembly interface box / site
ax.text(-0.88, gy + 0.05, "assembly\ninterface", fontsize=7.5, color="#990000", va="bottom")

# Solution 2: high floor beams, thin box roof + separate roof element
ax = axs[1]; ax.set_title("Solution 2: high floor, separate roof element", fontsize=10, loc="left")
ax.add_patch(Polygon([(-0.9, -0.15), (3.4, -0.15), (3.4, -1.0), (-0.9, -1.0)], fc="#e8e2d2", ec="none"))
by = 0.0                                                                  # underside of beams 0.15 m above ground (-0.15)
rect(ax, 0.25, by - 0.29, 2.3, 0.14, "#efe6d2", lw=0.5, hatch="oo")      # gravel layer
rect(ax, 0.25, by - 0.15, 2.3, 0.15, "#f6eab8", lw=0.6, hatch="\\\\")    # 0.15 soft insulation
ax.text(1.4, by - 0.075, "0.15 soft insulation", ha="center", va="center", fontsize=8, bbox=dict(fc="white", ec="none", pad=1))
for xs in (0.0, 2.55):
    rect(ax, xs, -0.85, 0.25, 0.85, "#c9c4b6", lw=0.7)                    # lightweight concrete foundation walls
ax.text(1.4, -0.75, "foundation walls, no slab", ha="center", fontsize=8.5)
ax.plot([-0.9, 0.0], [-0.15, -0.15], color=INK, lw=1.0)
dim_v(ax, -0.15, -0.15, by, "0.15", left=True, fs=8)
rect(ax, 0, by, 2.8, 0.30, INS, hatch="///")                             # 0.30 insulated floor beams
ax.text(1.4, by + 0.15, "0.30 m beams, low-density insulation", ha="center", va="center", fontsize=8, bbox=dict(fc="white", ec="none", pad=1))
fl = by + 0.30
rect(ax, 0, fl, 0.10, 2.50, WOOD); rect(ax, 2.7, fl, 0.10, 2.50, WOOD)
rect(ax, 0, fl + 2.50, 2.8, 0.15, WOOD)
ax.text(1.4, fl + 1.2, "room", ha="center", fontsize=10, color=MUTED)
ry = fl + 2.65
ax.add_patch(Polygon([(-0.3, ry), (3.1, ry), (1.4, ry + 1.7 * 0.268)], fc=INS, ec=INK, lw=0.8, hatch="///"))
ax.plot([-0.3, 1.4, 3.1], [ry, ry + 1.7 * 0.268, ry], color=INK, lw=1.4)
ax.text(1.4, ry + 0.62, "grid-truss roof, 15°, roofing felt\n(mounted on site)", ha="center", fontsize=8)
dim_v(ax, 3.05, by, fl, " 0.30", left=False, fs=8); dim_v(ax, 3.05, fl, fl + 2.5, "2.50", left=False)
dim_v(ax, 3.05, fl + 2.5, fl + 2.65, " 0.15", left=False, fs=8)
ax.text(-0.15, fl + 1.25, "box height\n2.95 m", ha="right", fontsize=8.5)
for yi, dy, va in ((by, 0.04, "bottom"), (ry, -0.04, "top")):            # assembly interfaces box / site
    ax.plot([-0.9, 3.2], [yi, yi], color="#990000", lw=1.3, ls=(0, (5, 3)))
    ax.text(-0.88, yi + dy, "assembly\ninterface", fontsize=7.5, color="#990000", va=va)
save(fig, "floor-roof-solutions")

# ---------------------------------------------------------------- 3. two pods around a technical room (plan)
fig, ax = plt.subplots(figsize=(8.6, 5.2)); ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(-0.3, 12.3); ax.set_ylim(-0.6, 7.0)
# central zone between living boxes (schematic)
rect(ax, 0, 0, 12, 6.4, "white", lw=1.0)
pw, ph, tw = 2.2, 3.0, 1.4
px = 6 - tw / 2 - pw
py = 3.4
rect(ax, px, py, pw, ph, "#e9e6de", lw=1.2); rect(ax, px + pw + tw, py, pw, ph, "#e9e6de", lw=1.2)
rect(ax, px + pw, py, tw, ph, "#f6f1e2", lw=1.0, ls="--")
ax.text(px + pw / 2, py + ph / 2, "bathroom\npod 1", ha="center", va="center", fontsize=9)
ax.text(px + pw + tw + pw / 2, py + ph / 2, "bathroom\npod 2", ha="center", va="center", fontsize=9)
ax.text(6, py + 0.25, "technical\nroom", ha="center", fontsize=8)
for xx in (px + pw - 0.08, px + pw + tw):                               # access walls with connections
    rect(ax, xx, py + 0.1, 0.08, ph - 0.2, WARM, lw=0)
rect(ax, 6 - 0.45, py + 1.55, 0.9, 0.7, "white", lw=0.9); ax.text(6, py + 1.9, "AHU", ha="center", va="center", fontsize=8)
ax.add_patch(Circle((6, py + 1.05), 0.28, fc="white", ec=INK, lw=0.9)); ax.text(6, py + 1.05, "DHW", ha="center", va="center", fontsize=6.5)
# rooms
for (x, y, w, h, t) in [(0, 3.4, 3.1, 3.0, "bedroom"), (8.9, 3.4, 3.1, 3.0, "bedroom"), (0, 0, 4.2, 3.4, "bedroom"),
                        (4.2, 0, 7.8, 3.4, "kitchen-dining-living")]:
    rect(ax, x, y, w, h, "none", lw=0.6); ax.text(x + w / 2, y + 0.25, t, ha="center", fontsize=8.5, color=MUTED)
# ducts: supply green to dry rooms, extract orange from pods
def duct(pts, c):
    xs, ys = zip(*pts); ax.plot(xs, ys, color=c, lw=2.0, solid_capstyle="round")
    ax.add_patch(FancyArrowPatch(pts[-2], pts[-1], arrowstyle="-|>", mutation_scale=11, color=c, lw=0))
duct([(5.75, py + 2.25), (5.75, 6.15), (1.6, 6.15), (1.6, 5.2)], AIR)
duct([(6.25, py + 2.25), (6.25, 6.15), (10.4, 6.15), (10.4, 5.2)], AIR)
duct([(5.55, py + 1.7), (2.1, py + 1.7), (2.1, 1.9)], AIR)
duct([(6.45, py + 1.75), (8.0, py + 1.75), (8.0, 1.9)], AIR)
duct([(px + 0.6, py + ph - 0.6), (px + 0.6, py + ph - 0.25), (5.6, py + ph - 0.25), (5.6, py + 2.25)], WARM)
duct([(px + pw + tw + pw - 0.6, py + ph - 0.6), (px + pw + tw + pw - 0.6, py + ph - 0.25), (6.4, py + ph - 0.25), (6.4, py + 2.25)], WARM)
ax.plot([], [], color=AIR, lw=2, label="supply air to dry rooms (above pod ceilings / in roof)")
ax.plot([], [], color=WARM, lw=2, label="extract air from wet rooms")
ax.add_patch(Rectangle((0, 0), 0, 0, fc=WARM, label="access wall with pipe and duct connections"))
ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False, fontsize=8)
save(fig, "pods-tech-room")

# ---------------------------------------------------------------- 4. box layouts from lecture 21.3, to scale
L = [("108 m²", [(0, 0, 4, 9, "Box 1\n9×4"), (4, 0, 4, 9, "Box 3\n9×4"), (8, 0, 4, 9, "Box 2\n9×4")], None,
      [(5.1, 5.4, 1.8, 2.2, "bath"), (5.1, 4.4, 1.8, 1.0, "tech"), (5.1, 3.2, 1.8, 1.2, "WC")]),
     ("144 m²", [(0, 0, 4, 12, "Box 1\n12×4"), (4, 0, 4, 12, "Box 3\n12×4"), (8, 0, 4, 12, "Box 2\n12×4")], None,
      [(5.1, 8.6, 1.8, 2.2, "bath"), (5.1, 7.6, 1.8, 1.0, "tech"), (5.1, 5.4, 1.8, 2.2, "bath")]),
     ("128 m²", [(0, 0, 4, 8, "Box 1\n8×4"), (4, 4, 8, 4, "Box 3\n8×4"), (12, 0, 4, 8, "Box 2\n8×4")], (4, 0, 8, 4),
      [(5.0, 4.4, 2.2, 2.4, "bath"), (7.2, 4.4, 1.2, 2.4, "tech"), (8.4, 4.4, 2.2, 2.4, "bath")]),
     ("153 m²", [(0, 0, 4, 9, "Box 1\n9×4"), (4, 5, 9, 4, "Box 3\n9×4"), (13, 0, 4, 9, "Box 2\n9×4")], (4, 0, 9, 5),
      [(5.4, 5.4, 2.2, 2.4, "bath"), (7.6, 5.4, 1.2, 2.4, "tech"), (8.8, 5.4, 2.2, 2.4, "bath")]),
     ("208 m²", [(0, 0, 4, 16, "Box 1\n16×4"), (9, 0, 4, 16, "Box 2\n16×4")], (4, 0, 5, 16),
      [(5.6, 12.4, 1.8, 2.2, "bath"), (5.6, 10.6, 1.8, 1.8, "tech +\nutility"), (5.6, 8.4, 1.8, 2.2, "bath")])]
order = {"108 m²": (0, 7.5), "144 m²": (15, 4.5), "208 m²": (30, 0.5), "128 m²": (0, -13), "153 m²": (20, -13)}
fig, ax = plt.subplots(figsize=(9.5, 8.6)); ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(-1, 44); ax.set_ylim(-14.5, 19.5)
for (title, boxes, site, pods) in L:
    ox, oy = order[title]
    for (x, y, w, h, t) in boxes:
        rect(ax, ox + x, oy + y, w, h, "#efece4", lw=1.1)
        if t.startswith("Box 3") and h == 4:
            ty, t = y + h - 0.55, t.replace("\n", " ")
        else:
            ty = (y + 1.3) if t.startswith("Box 3") else (y + h / 2)
        ax.text(ox + x + w / 2, oy + ty, t, ha="center", va="center", fontsize=10)
    if site:
        x, y, w, h = site
        rect(ax, ox + x, oy + y, w, h, "white", lw=0.9, ls="--")
        ax.text(ox + x + w / 2, oy + y + (h / 2 if h < 10 else 3.5), "open area\nunder roof\nelements", ha="center", va="center", fontsize=9, color=MUTED)
    for (x, y, w, h, t) in pods:
        rect(ax, ox + x, oy + y, w, h, "white", ec=COLD, lw=1.1)
        ax.text(ox + x + w / 2, oy + y + h / 2, t, ha="center", va="center", color=COLD,
                fontsize=6.5 if "utility" in t else 7.5, rotation=90 if w < 1.5 else 0)
    top = max(y + h for (x, y, w, h, t) in boxes + ([(*site, "")] if site else []))
    ax.text(ox, oy + top + 0.6, title, fontsize=14, fontweight="bold")
dim_h(ax, 0, 12, 6.6, "12 m", above=False, fs=10)
dim_v(ax, -0.6, 7.5, 16.5, "9 m", left=True, fs=10)
save(fig, "box-layouts")
print("written to", OUT)


# ================================================================ isometric helpers
import math
C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))


def iso(x, y, z):
    return ((x - y) * C30, (x + y) * S30 + z)


def cuboid(ax, x, y, z, w, d, h, fc="#efece4", ec=INK, lw=0.8, wire=False, alpha=1.0):
    """Box with x-extent w, y-extent d, z-extent h; draws the three visible faces (top, front-left, front-right)."""
    P = lambda a, b, c: iso(x + a, y + b, z + c)
    faces = [([P(0, 0, h), P(w, 0, h), P(w, d, h), P(0, d, h)], 1.0),       # top
             ([P(0, 0, 0), P(w, 0, 0), P(w, 0, h), P(0, 0, h)], 0.88),       # front (y = 0)
             ([P(0, 0, 0), P(0, d, 0), P(0, d, h), P(0, 0, h)], 0.76)]       # left (x = 0)
    for pts, shade in faces:
        if wire:
            ax.add_patch(Polygon(pts, closed=True, fc="none", ec=ec, lw=lw))
        else:
            import matplotlib.colors as mc
            r, g, b_ = mc.to_rgb(fc)
            ax.add_patch(Polygon(pts, closed=True, fc=(r * shade, g * shade, b_ * shade), ec=ec, lw=lw, alpha=alpha))


def window(ax, x, y, z, w, h, face="front", fc="#bcd4ea"):
    if face == "front":
        pts = [iso(x, y, z), iso(x + w, y, z), iso(x + w, y, z + h), iso(x, y, z + h)]
    else:
        pts = [iso(x, y, z), iso(x, y + w, z), iso(x, y + w, z + h), iso(x, y, z + h)]
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=INK, lw=0.6))


def truck(ax, x, y, L=9.0):
    cuboid(ax, x + L, y, 0.4, 1.8, 2.4, 2.4, fc="#c8c4b8")                    # cab
    cuboid(ax, x, y, 0.4, L, 2.4, 0.35, fc="#9c988c")                         # deck
    for xx in (x + 1.0, x + 2.6, x + L + 0.9):
        cx, cy = iso(xx, y, 0.4)
        ax.add_patch(Circle((cx, cy), 0.42, fc="#555", ec=INK, lw=0.6, zorder=0))


# ---------------------------------------------------------------- 5. three ways of building (isometric matrix)
fig, axs = plt.subplots(3, 3, figsize=(10.5, 8.2))
cols = ["On site", "2D elements (panels)", "3D volumes (boxes)"]
rows = ["Factory", "Transport", "Site"]
texts = [["Timber, boards and insulation\nare cut and stacked.", "Walls and roof elements are made\nwith insulation, windows and cladding.", "Closed room units are made with\nsurfaces, windows and installations."],
         ["Loose materials on a\nflatbed truck.", "Elements stacked on a truck;\nnormal transport width.", "One box per truck;\nwide, high special transport."],
         ["All trades work on site,\nexposed to weather.", "Elements are lifted into place\nand joined; finishing on site.", "Boxes are lifted onto foundations\nand joined; little work on site."]]
for ax in axs.flat:
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-10.5, 10.5); ax.set_ylim(-5.8, 12.6)
# factory row
ax = axs[0, 0]
for k in range(6):
    cuboid(ax, -2, 0, k * 0.35, 8, 0.6, 0.3, fc=WOOD)
    cuboid(ax, -2, 1.2, k * 0.35, 8, 1.2, 0.3, fc="#e9e6de")
cuboid(ax, -2, 3.2, 0, 3, 2, 1.4, fc=INS)
ax = axs[0, 1]
cuboid(ax, -3, 0, 0, 8, 0.4, 3, fc="#e9e6de"); window(ax, 0, 0, 1.0, 1.6, 1.4)
cuboid(ax, -3, 2.0, 0, 8, 0.4, 3, fc="#e9e6de"); window(ax, 2, 2.0, 1.0, 1.6, 1.4)
ax = axs[0, 2]
cuboid(ax, -4, 0, 0, 9, 4, 3.2, fc="#e9e6de"); window(ax, 0, 0, 1.0, 2.0, 1.4); window(ax, -4, 1.0, 1.0, 1.6, 1.4, face="left")
# transport row
for c, ax in enumerate(axs[1]):
    truck(ax, -5, 0)
ax = axs[1, 0]
for k in range(4):
    cuboid(ax, -4.5, 0.3, 0.75 + k * 0.32, 8, 1.8, 0.3, fc=WOOD if k % 2 else "#e9e6de")
ax = axs[1, 1]
for k in range(3):
    cuboid(ax, -4.5, 0.4, 0.75 + k * 0.42, 8, 1.6, 0.4, fc="#e9e6de")
ax = axs[1, 2]
cuboid(ax, -5, -0.9, 0.75, 9, 4.2, 3.2, fc="#e9e6de"); window(ax, -1, -0.9, 1.8, 2.0, 1.4)
# site row
ax = axs[2, 0]
cuboid(ax, -3, 0, 0, 8, 5, 0.25, fc=CONC)
for xx in [i * 0.8 for i in range(11)]:
    a1, b1 = iso(-3 + xx, 0, 0.25); a2, b2 = iso(-3 + xx, 0, 3.0); ax.plot([a1, a2], [b1, b2], color=WOOD, lw=1.6)
for yy in [i * 0.833 for i in range(7)]:
    a1, b1 = iso(-3, yy, 0.25); a2, b2 = iso(-3, yy, 3.0); ax.plot([a1, a2], [b1, b2], color=WOOD, lw=1.6)
for (p0, p1) in [((-3, 0, 3.0), (5, 0, 3.0)), ((-3, 0, 3.0), (-3, 5, 3.0))]:
    ax.plot(*zip(iso(*p0), iso(*p1)), color=WOOD, lw=2.2)
for k in range(3):
    cuboid(ax, 1.5, 6.2, k * 0.3, 3.5, 1.0, 0.25, fc=WOOD)
ax = axs[2, 1]
cuboid(ax, -3, 0, 0, 8, 5, 2.8, wire=True, lw=0.5, ec=MUTED)
cuboid(ax, -3, 0, 0, 0.3, 5, 2.8, fc="#e9e6de"); cuboid(ax, -3, 0, 0, 8, 0.3, 2.8, fc="#e9e6de"); window(ax, 1, 0, 1.0, 1.6, 1.2)
cuboid(ax, 1.5, 6, 3.4, 3.5, 0.3, 2.8, fc="#e9e6de")                         # panel hanging
hx, hy = iso(3.25, 6.15, 6.2); bx, by = iso(3.25, 6.15, 6.2 + 1.2); ax.plot([hx, bx], [hy, by], color=INK, lw=0.8)
ax = axs[2, 2]
cuboid(ax, -3, 3.5, 0, 7.5, 3.5, 3.2, fc="#e9e6de")
cuboid(ax, -3, 0, 0, 7.5, 3.5, 3.2, fc="#e9e6de"); window(ax, 0.5, 0, 1.0, 2.0, 1.4); window(ax, -3, 1.0, 1.0, 1.4, 1.4, face="left")
for r in range(3):
    for c in range(3):
        axs[r, c].text(0, -5.6, texts[r][c], ha="center", va="bottom", fontsize=8)
for c in range(3):
    axs[0, c].set_title(cols[c], fontsize=11, fontweight="bold")
for r in range(3):
    axs[r, 0].text(-10.3, 3, rows[r], rotation=90, ha="center", va="center", fontsize=11, fontweight="bold", color=MUTED)
fig.subplots_adjust(wspace=0.02, hspace=0.08)
save(fig, "build-methods")

# ---------------------------------------------------------------- 6. double walls and gable element (plan)
fig, ax = plt.subplots(figsize=(9, 3.6)); ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(-1.2, 15.2); ax.set_ylim(-1.6, 6.1)
fw, iw = 0.55, 0.10
for k, x0 in enumerate((0, 4.5, 9.0)):                                       # three boxes along the facade, 4.5 m wide
    rect(ax, x0, 0, 4.5, 4.0, "#f7f5ef", lw=1.0)
    rect(ax, x0, 0, 4.5, fw, INS, lw=0.5, hatch="///")                       # facade wall (bottom)
    rect(ax, x0, 4.0 - iw, 4.5, iw, WOOD, lw=0.4)                            # internal wall to corridor box
    for xs in (x0, x0 + 4.5 - iw):
        if not (k == 0 and xs == x0) and not (k == 2 and xs > x0):
            rect(ax, xs, fw, iw, 4.0 - fw - iw, WOOD, lw=0.4)                # side walls at box joints
    ax.text(x0 + 2.25, 2.3, f"box {k + 1}", ha="center", fontsize=9, color=MUTED)
for xs in (0, 13.5 - iw):                                                    # gable walls of end boxes: thin in box
    rect(ax, xs, fw, iw, 4.0 - fw - iw, WOOD, lw=0.4)
rect(ax, -fw, 0, fw, 4.0, INS, ec=AIR, lw=1.4, hatch="///")                  # gable elements added on site
rect(ax, 13.5, 0, fw, 4.0, INS, ec=AIR, lw=1.4, hatch="///")
for xj in (4.5, 9.0):
    ax.add_patch(FancyArrowPatch((xj, 5.2), (xj, 4.15), arrowstyle="-|>", mutation_scale=10, color=WARM, lw=1.2))
ax.text(6.75, 5.45, "double walls where boxes meet (2 × 0.1 m)", ha="center", fontsize=8.5, color=WARM)
ax.text(-0.3, -0.5, "gable element\nadded on site", ha="center", va="top", fontsize=8.5, color=AIR)
ax.text(13.8, -0.5, "gable element\nadded on site", ha="center", va="top", fontsize=8.5, color=AIR)
ax.text(6.75, -0.45, "facade wall made with the box", ha="center", va="top", fontsize=8.5)
save(fig, "double-walls")

# ---------------------------------------------------------------- 7. bedroom: two furnished plans with a double bed
LINE = COLD
def room_plan(ax, W, D, wardrobe, door, window, title):
    t = 0.12
    rect(ax, -t, -t, W + 2 * t, D + 2 * t, "#d5dbe6", ec=LINE, lw=1.0)       # walls
    rect(ax, 0, 0, W, D, "white", ec=LINE, lw=1.0)
    # window opening in the right wall
    wy0, wy1 = window
    rect(ax, W - 0.01, wy0, t + 0.02, wy1 - wy0, "white", ec=LINE, lw=0.8)
    ax.plot([W + t / 2, W + t / 2], [wy0, wy1], color=LINE, lw=0.8)
    # door: opening and swing
    side, d0, dw = door
    if side == "left":
        rect(ax, -t - 0.01, d0, t + 0.02, dw, "white", ec="white", lw=0)
        ax.add_patch(matplotlib.patches.Arc((0, d0), 2 * dw, 2 * dw, theta1=0, theta2=90, color=LINE, lw=0.7, ls="--"))
        ax.plot([0, dw], [d0, d0], color=LINE, lw=0.8)
    else:
        rect(ax, d0, -t - 0.01, dw, t + 0.02, "white", ec="white", lw=0)
        ax.add_patch(matplotlib.patches.Arc((d0, 0), 2 * dw, 2 * dw, theta1=0, theta2=90, color=LINE, lw=0.7, ls="--"))
        ax.plot([d0, d0], [0, dw], color=LINE, lw=0.8)
    # wardrobe
    wx, wy, ww, wd = wardrobe
    rect(ax, wx, wy, ww, wd, "#eef2f8", ec=LINE, lw=0.9)
    ax.text(wx + ww / 2, wy + wd / 2, "wardrobe", ha="center", va="center", fontsize=7.5, color=LINE,
            rotation=90 if wd > ww else 0)
    # bed centred in the free width, headboard at the back wall
    free_x0 = wx + ww if wd > ww else 0
    free_W = W - free_x0
    bx = free_x0 + (free_W - 1.8) / 2; by = D - 2.0
    rect(ax, bx, by, 1.8, 2.0, "#efece4", ec=LINE, lw=1.0)
    rect(ax, bx + 0.08, D - 0.42, 0.78, 0.34, "white", ec=LINE, lw=0.6); rect(ax, bx + 0.94, D - 0.42, 0.78, 0.34, "white", ec=LINE, lw=0.6)
    for nx in (bx - 0.55, bx + 1.85):
        rect(ax, nx, D - 0.45, 0.5, 0.4, "white", ec=LINE, lw=0.6)
    ax.text(bx + 0.9, by + 0.85, "1.8 × 2.0", ha="center", va="center", fontsize=8)
    # access dimensions (inside the room)
    ya = by + 0.55
    dim_h(ax, free_x0, bx, ya, f"{bx - free_x0:.2f}", fs=7.5)
    dim_h(ax, bx + 1.8, W, ya, f"{W - bx - 1.8:.2f}", fs=7.5)
    foot0 = wy + wd if ww > wd else 0
    dim_v(ax, bx + 1.2, foot0, by, f"{by - foot0:.2f}", left=False, fs=7.5)
    # overall dimensions
    dim_h(ax, 0, W, -0.55, f"{W:.2f} m", above=False, fs=9)
    dim_v(ax, W + 0.5, 0, D, f"{D:.2f} m", left=False, fs=9)
    # wardrobe depth
    if ww > wd:
        dim_v(ax, -0.45, wy, wy + wd, f"{wd:.2f}", left=True, fs=7.5)
    else:
        dim_h(ax, wx, wx + ww, D + 0.25, f"{ww:.2f}", fs=7.5)
    ax.set_title(f"{title}   {W:.2f} × {D:.2f} = {W * D:.1f} m²", fontsize=10, loc="left")

fig, axs = plt.subplots(1, 2, figsize=(11.5, 5.2), gridspec_kw=dict(width_ratios=[3.76 + 1.6, 4.45 + 1.6]))
for ax in axs:
    ax.set_aspect("equal"); ax.axis("off")
axs[0].set_xlim(-0.9, 4.86); axs[0].set_ylim(-1.0, 4.0)
axs[1].set_xlim(-0.6, 5.55); axs[1].set_ylim(-1.0, 4.0)
room_plan(axs[0], 3.76, 3.63, wardrobe=(0, 0, 3.76, 0.60), door=("left", 0.75, 0.9), window=(1.6, 3.0), title="(a)")
room_plan(axs[1], 4.45, 2.95, wardrobe=(0, 0, 0.60, 2.95), door=("bottom", 0.70, 0.9), window=(0.9, 2.3), title="(b)")
fig.subplots_adjust(wspace=0.05)
save(fig, "bedroom-dimensions")

# ---------------------------------------------------------------- 8. external width: box on truck (rear view) + width chains in plan
fig = plt.figure(figsize=(11.5, 6.2))
gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.9], hspace=0.25, wspace=0.05)
ax = fig.add_subplot(gs[:, 0]); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.6, 5.1); ax.set_ylim(-0.4, 5.0)
ax.plot([-0.6, 5.1], [0, 0], color=INK, lw=1.2)
rect(ax, 1.0, 0.25, 2.5, 0.55, GREY)                                         # low-loader seen from behind
for xw in (1.05, 2.95):
    rect(ax, xw, 0, 0.5, 0.55, "#555", lw=0.4)
rect(ax, 0, 0.8, 4.5, 3.3, "#efece4", lw=1.1)
rect(ax, 0, 0.8, 0.55, 3.3, INS, lw=0.5, hatch="///")
rect(ax, 4.4, 0.8, 0.1, 3.3, WOOD, lw=0.4)
dim_h(ax, 0, 4.5, 4.35, "4.5 m", fs=10)
ax.text(2.25, 2.4, "box seen\nfrom behind", ha="center", fontsize=8.5, color=MUTED)
ax.set_title("(a) Maximum width on the road", fontsize=10, loc="left")


def chain(ax, segs, dims, title, total):
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.75, total + 0.75); ax.set_ylim(-1.3, 2.7)
    for x, w, t, fc, h, ec in segs:
        rect(ax, x, 0, w, 1.6, fc, ec=ec, lw=1.3 if ec != INK else 0.8, hatch=h, ls="--" if ec == AIR else "-")
        if t == "room": ax.text(x + w / 2, 0.8, t, ha="center", va="center", fontsize=9, color=MUTED)
    for (x0, x1, t, fs) in dims:
        dim_h(ax, x0, x1, -0.45, t, above=False, fs=fs)
    ax.set_title(title, fontsize=10, loc="left")


# (b) facade insulation made with the box
ax = fig.add_subplot(gs[0, 1])
segs = [(0, 0.55, "", INS, "///", INK), (0.55, 3.85, "room", "white", None, INK), (4.4, 0.1, "", WOOD, None, INK),
        (4.5, 0.1, "", WOOD, None, INK), (4.6, 3.85, "room", "white", None, INK), (8.45, 0.55, "", INS, "///", INK)]
chain(ax, segs, [(0, 0.55, "0.55", 7.5), (0.55, 4.4, "3.85", 9), (4.6, 8.45, "3.85", 9), (8.45, 9.0, "0.55", 7.5)],
      "(b) Facade insulation made with the box", 9.0)
ax.set_xlim(-1.0, 10.0)
dim_h(ax, 0, 4.5, 2.05, "box 1: 4.5 m", fs=8.5); dim_h(ax, 4.5, 9.0, 2.05, "box 2: 4.5 m", fs=8.5)
ax.text(4.5, -0.85, "0.1 + 0.1", ha="center", fontsize=7.5)

# (c) facade insulation as a separate 2D element mounted on site
ax = fig.add_subplot(gs[1, 1])
e = 0.5
gp = 0.08                                                                  # gap: element drawn apart from the box
segs = [(-e - gp, e, "", INS, "///", AIR), (0, 0.1, "", WOOD, None, INK), (0.1, 4.3, "room", "white", None, INK),
        (4.4, 0.1, "", WOOD, None, INK), (4.5, 0.1, "", WOOD, None, INK), (4.6, 4.3, "room", "white", None, INK),
        (8.9, 0.1, "", WOOD, None, INK), (9.0 + gp, e, "", INS, "///", AIR)]
chain(ax, segs, [(-e - gp, -gp, "0.5", 7.5), (0.1, 4.4, "4.3", 9), (4.6, 8.9, "4.3", 9), (9.0 + gp, 9.0 + gp + e, "0.5", 7.5)],
      "(c) Facade insulation as a separate 2D element, mounted on site", 9.0)
ax.set_xlim(-1.0, 10.0)
dim_h(ax, 0, 4.5, 2.05, "box 1: 4.5 m", fs=8.5); dim_h(ax, 4.5, 9.0, 2.05, "box 2: 4.5 m", fs=8.5)
ax.text(4.5, -0.85, "0.1 + 0.1", ha="center", fontsize=7.5)
ax.text(-0.25 - gp, 1.75, "2D element", ha="center", va="bottom", fontsize=7.5, color=AIR)
ax.text(9.25 + gp, 1.75, "2D element", ha="center", va="bottom", fontsize=7.5, color=AIR)
save(fig, "box-width")

# ---------------------------------------------------------------- 9. external height: four ways to use 4.1 m
cases = [("Low-loader,\nfloor beams 0.30", 0.8, 0.30, 0.50, None),
         ("Solution 1:\nlow floor beams", 0.8, 0.10, 0.70, None),
         ("Solution 2:\nthin box roof", 0.8, 0.30, 0.15, "separate roof\nelement\nadded on site"),
         ("Special low-loader,\nfloor beams 0.30", 0.3, 0.30, 1.00, None)]
fig, ax = plt.subplots(figsize=(10.5, 5.6)); ax.axis("off"); ax.set_xlim(-1.2, 15.6); ax.set_ylim(-1.3, 5.6)
ax.plot([-1.2, 15.6], [0, 0], color=INK, lw=1.2)
ax.plot([-0.2, 15.3], [4.1, 4.1], color=WARM, lw=1.2, ls="--"); ax.text(15.3, 4.18, "4.1 m", color=WARM, ha="right", fontsize=9)
for i, (t, deck, fl, rf, extra) in enumerate(cases):
    x = 0.4 + i * 3.8; w = 2.2
    rect(ax, x, 0, w, deck, GREY, lw=0.6); ax.text(x + w + 0.08, deck / 2, f"{deck:.1f} loader", fontsize=7.5, va="center")
    y = deck
    rect(ax, x, y, w, fl, WOOD, lw=0.6); ax.text(x + w + 0.08, y + fl / 2, f"{fl:.2f} floor", fontsize=7.5, va="center"); y += fl
    rect(ax, x, y, w, 2.5, "white", lw=0.8); ax.text(x + w / 2, y + 1.25, "room\n2.50", ha="center", va="center", fontsize=9, color=MUTED); y += 2.5
    rect(ax, x, y, w, rf, INS, lw=0.6, hatch="///"); ax.text(x + w + 0.08, y + rf / 2, f"{rf:.2f} roof", fontsize=7.5, va="center"); y += rf
    if extra:
        rect(ax, x - 0.1, y + 0.08, w + 0.2, 0.6, "none", ec=AIR, lw=1.2, ls="--")
        ax.text(x + w / 2, y + 0.75, extra, ha="center", va="bottom", fontsize=7.5, color=AIR)
    ax.text(x + w / 2, -0.25, t, ha="center", va="top", fontsize=8.5)
    ax.text(x + w / 2, y - rf / 2 if False else 4.1 - 4.1, "", fontsize=1)
save(fig, "box-height")
print("written to", OUT)


# ---------------------------------------------------------------- 10. foundations: solution 1 (slab) vs solution 2 (crawl space with soft insulation)
SOIL, STONE, LECA, SOFT = "#e8e2d2", "#efe6d2", "#c9c4b6", "#f6eab8"


def soil(ax, x0, x1, y0, y1):
    rect(ax, x0, y0, x1 - x0, y1 - y0, SOIL, ec="none", lw=0, hatch="//", alpha=1.0)


fig, axs = plt.subplots(1, 2, figsize=(12, 6.3))
for ax in axs:
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.25, 2.0); ax.set_ylim(-1.2, 1.25)

# (a) Solution 1: box with 0.10 m beams on a concrete slab on EPS
ax = axs[0]; ax.set_title("(a) Solution 1: box on a concrete slab", fontsize=10.5, loc="left")
g = -0.05                                                                   # outside ground just below slab top
soil(ax, -1.25, -0.65, -1.2, g); soil(ax, -0.65, 1.75, -1.2, -0.54)
rect(ax, -0.45, -1.0, 0.30, 1.15, CONC, lw=0.7, hatch="..")                 # foundation wall, up to 0.13 under the outer wall
rect(ax, -0.15, -0.40, 0.15, 0.55, INS, lw=0.6, hatch="///")                # edge insulation between foundation and slab
rect(ax, -0.65, -1.0, 0.20, 1.0 + g, INS, lw=0.6, hatch="///")              # edge insulation outside
rect(ax, -0.15, -0.54, 1.90, 0.14, STONE, lw=0.5, hatch="oo")               # capillary-breaking gravel, to the inner face of the foundation
rect(ax, 0.0, -0.40, 1.75, 0.20, INS, lw=0.6, hatch="///"); rect(ax, 0.0, -0.20, 1.75, 0.20, INS, lw=0.6, hatch="///")
rect(ax, 0.0, 0.0, 1.75, 0.13, CONC, lw=0.8, hatch="..")                    # slab 0.13, stops at the inner face of the outer wall
rect(ax, 0.0, 0.13, 1.75, 0.02, "#444", lw=0)                               # flexible layer under the wooden floor only
rect(ax, 0.0, 0.15, 1.75, 0.10, WOOD, lw=0.6)                               # 0.10 floor beams
rect(ax, 0.0, 0.25, 1.75, 0.025, "#e9e6de", lw=0.5)                         # floor
rect(ax, -0.50, 0.15, 0.50, 1.10, INS, lw=0.7, hatch="///")                 # facade wall of the box
rect(ax, -0.50, 0.15, 0.04, 1.10, "#8c8a83", lw=0.4)                        # cladding
ax.plot([-1.25, -0.65], [g, g], color=INK, lw=1.2)
for (y0, y1, t) in [(0.15, 0.25, "0.10 floor beams"), (0.0, 0.13, "0.13 concrete slab"),
                    (-0.40, 0.0, "2 × 0.20 EPS C60"), (-0.54, -0.40, "gravel")]:
    ax.text(1.72, (y0 + y1) / 2, t, ha="right", va="center", fontsize=8, bbox=dict(fc="white", ec="none", pad=0.5))
ax.annotate("flexible layer", xy=(1.0, 0.14), xytext=(0.9, 0.62), fontsize=8, arrowprops=dict(arrowstyle="-", lw=0.6))
ax.text(0.85, 0.95, "box", fontsize=10, color=MUTED, ha="center")
dim_v(ax, -0.78, g, 0.275, "0.3", left=True, fs=8)
ax.text(-1.2, g + 0.03, "ground", fontsize=8, color=MUTED, va="bottom")
ax.plot([-1.22, 1.85], [0.15, 0.15], color="#990000", lw=1.3, ls=(0, (5, 3)))     # assembly interface box / site
ax.text(-1.22, 0.17, "assembly\ninterface", fontsize=7.5, color="#990000", va="bottom")
ax.annotate("edge insulation", xy=(-0.55, -0.6), xytext=(-1.2, -0.95), fontsize=8, arrowprops=dict(arrowstyle="-", lw=0.6), bbox=dict(fc="white", ec="none", pad=0.5))

# (b) Solution 2: box with 0.30 m beams on a lightweight concrete wall, 0.30 m soft insulation below
ax = axs[1]; ax.set_title("(b) Solution 2: box on a foundation wall", fontsize=10.5, loc="left")
cl, bh, si = 0.15, 0.30, 0.15                                               # clearance, beam height, soft insulation
yb = cl                                                                     # underside of floor beams
yw = yb                                                                     # underside of the box wall = underside of floor beams
soil(ax, -1.25, 1.75, -1.2, -1.05); soil(ax, -1.25, -0.40, -1.05, 0.0); soil(ax, -0.10, 1.75, -1.05, yb - si - 0.14)
rect(ax, -0.50, -1.05, 0.50, 0.20, CONC, lw=0.7, hatch="..")                # footing
rect(ax, -0.40, -0.85, 0.30, 0.85 + yw, LECA, lw=0.7)                       # lightweight concrete wall, 0.30 wide, up to the box wall
for yy in (-0.65, -0.45, -0.25, -0.05):
    ax.plot([-0.40, -0.10], [yy, yy], color=INK, lw=0.4)
ax.add_patch(Circle((-0.65, -0.90), 0.06, fc="white", ec=INK, lw=0.7))       # drain
ax.text(-0.65, -1.02, "drain", ha="center", va="top", fontsize=7.5)
rect(ax, -0.10, yb - si - 0.14, 1.85, 0.14, STONE, lw=0.5, hatch="oo")      # gravel layer
rect(ax, -0.10, yb - si, 1.85, si, SOFT, lw=0.6, hatch="\\\\")             # soft insulation 0.30, up to the lightweight concrete wall
rect(ax, 0.05, yb, 1.70, bh, INS, lw=0.7, hatch="///")                      # insulated floor beams
for xx in (0.05, 0.65, 1.25):
    rect(ax, xx, yb, 0.045, bh, WOOD, lw=0.4)
ax.plot([0.05, 1.75], [yb + bh, yb + bh], color=AIR, lw=1.6)               # radon + vapour barrier
rect(ax, 0.05, yb + bh, 1.70, 0.025, "#e9e6de", lw=0.5)                     # floor
rect(ax, -0.45, yw, 0.50, 1.07, INS, lw=0.7, hatch="///")                   # facade wall of the box, resting on the lightweight concrete wall
rect(ax, -0.45, yw, 0.04, 1.07, "#8c8a83", lw=0.4)
ax.plot([-1.25, -0.40], [0, 0], color=INK, lw=1.2)
ax.text(-1.2, 0.05, "ground", fontsize=8, color=MUTED)
ax.plot([-1.22, 1.80], [yb, yb], color="#990000", lw=1.3, ls=(0, (5, 3)))     # assembly interface box / site
ax.text(-1.22, yb + 0.02, "assembly\ninterface", fontsize=7.5, color="#990000", va="bottom", ha="left")
ax.annotate("radon and vapour barrier", xy=(1.3, yb + bh), xytext=(0.65, 0.95), fontsize=8, color=AIR,
            arrowprops=dict(arrowstyle="-", lw=0.6, color=AIR))
ax.text(-0.25, -0.40, "lightweight\nconcrete", ha="center", fontsize=7.5, rotation=90, va="center")
ax.text(1.0, yb + bh / 2, "0.30 floor beams, insulated", ha="center", va="center", fontsize=8, bbox=dict(fc="white", ec="none", pad=0.5))
ax.text(1.0, yb - si / 2, "0.15 soft insulation", ha="center", va="center", fontsize=8, bbox=dict(fc="white", ec="none", pad=0.5))
ax.text(1.0, yb - si - 0.07, "gravel", ha="center", va="center", fontsize=7.5, bbox=dict(fc="white", ec="none", pad=0.5))
ax.plot([1.75, 1.95], [0, 0], color=INK, lw=0.6, ls=":"); ax.plot([1.75, 1.95], [yb, yb], color=INK, lw=0.6, ls=":")
dim_v(ax, 1.85, 0.0, yb, "", left=False); ax.text(1.9, yb / 2, "0.15", fontsize=8, va="center")
dim_v(ax, 1.85, yb, yb + bh, "", left=False); ax.text(1.9, yb + bh / 2, "0.30", fontsize=8, va="center")
fig.subplots_adjust(wspace=0.04)
save(fig, "foundations")


# ---------------------------------------------------------------- 11. flat roof element added on site on the thin box roof (Solution 2), example build-up
GYP, OSB, FELT, RED = "#e9e6de", "#d8c08e", "#3b3a37", "#990000"
LAY = [  # (name, thickness, colour, hatch), bottom to top
    ("2 × 13 mm gypsum board", 0.026, GYP, None),
    ("0.10 joists, insulated", 0.10, INS, "///"),
    ("15 mm OSB, underside of roof element", 0.015, OSB, None),
    ("0.40 I-joists c/c 0.6, mineral wool", 0.40, INS, "///"),
    ("0.05–0.15 ventilated gap, fall battens", 0.10, "white", None),
    ("22 mm plywood deck", 0.022, OSB, None),
    ("2 layers of roofing felt", 0.010, FELT, None)]
fig, axs = plt.subplots(2, 1, figsize=(9.6, 7.8), gridspec_kw=dict(height_ratios=[1.3, 1]))
# (a) section across the joists
ax = axs[0]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.75, 2.75); ax.set_ylim(-0.2, 0.9)
ax.set_title("(a) Section across the joists", fontsize=10.5, loc="left")
W, y = 1.6, 0.0
ys = {}
for (t, h, c, ha) in LAY:
    rect(ax, 0, y, W, h, c, lw=0.6, hatch=ha)
    ys[t] = (y, y + h); y += h
top = y
b0, b1 = ys[LAY[1][0]]
for xx in (0.3, 0.9, 1.5):                                                    # solid joists of the box roof
    rect(ax, xx - 0.0225, b0, 0.045, b1 - b0, WOOD, lw=0.4)
ax.plot([0, W], [b1, b1], color=AIR, lw=1.6)                                 # vapour barrier under the OSB
ys["vapour barrier"] = (b1, b1)
j0, j1 = ys[LAY[3][0]]
g0, g1 = ys[LAY[4][0]]
for xx in (0.2, 0.8, 1.4):                                                    # I-joists: flanges + web, fall batten on top
    rect(ax, xx - 0.0225, j0, 0.045, 0.045, WOOD, lw=0.5); rect(ax, xx - 0.0225, j1 - 0.045, 0.045, 0.045, WOOD, lw=0.5)
    rect(ax, xx - 0.005, j0 + 0.045, 0.01, j1 - j0 - 0.09, WOOD, lw=0.4)
    rect(ax, xx - 0.0225, g0, 0.045, g1 - g0, WOOD, lw=0.5)
names = [l[0] for l in LAY][::-1]; names.insert(5, "vapour barrier")                 # top to bottom
for i, t in enumerate(names):
    y0, y1 = ys[t]
    yt = top + 0.12 - i * 0.13
    ax.annotate(t, xy=(W, (y0 + y1) / 2), xytext=(W + 0.25, yt), fontsize=8.5, va="center",
                color=AIR if t == "vapour barrier" else INK, arrowprops=dict(arrowstyle="-", lw=0.5, color=MUTED))
yi = ys[LAY[2][0]][0]                                                         # assembly interface: top of the box, under the OSB of the roof element
ax.plot([-0.75, W + 0.15], [yi, yi], color=RED, lw=1.3, ls=(0, (5, 3)))
ax.text(-0.73, yi + 0.02, "assembly\ninterface", fontsize=7.5, color=RED, va="bottom")
dim_v(ax, -0.06, 0, yi, "", left=True); ax.text(-0.09, yi / 2, "0.13 box roof", ha="right", va="center", fontsize=8)
dim_v(ax, -0.06, yi, top, "", left=True); ax.text(-0.09, (yi + top) / 2 + 0.04, "≈ 0.55\nroof element\nadded on site", ha="right", va="center", fontsize=8)
ax.text(0.8, -0.07, "room", ha="center", fontsize=9, color=MUTED)
# (b) section along the joists: fall 1:40 over the 4 m box width
ax = axs[1]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.6, 4.75); ax.set_ylim(-0.75, 0.95)
ax.set_title("(b) Section along the joists, fall 1:40 to the gutter", fontsize=10.5, loc="left")
B = 4.0
rect(ax, B - 0.5, -0.7, 0.5, 0.7, INS, lw=0.6, hatch="///")                 # insulated facade wall of the box
rect(ax, 0.0, -0.7, 0.1, 0.7, WOOD, lw=0.6)                                 # 0.1 m stud wall towards the next box (double wall)
ax.text(0.15, -0.56, "0.1 m studs,\ndouble wall to\nthe next box", fontsize=7.5, va="bottom")
ax.text(B - 0.55, -0.56, "facade", fontsize=7.5, va="bottom", ha="right")
ax.text(B / 2, -0.4, "room", ha="center", fontsize=9, color=MUTED)
rect(ax, 0, 0, B, 0.126, INS, lw=0.6, hatch="///"); rect(ax, 0, 0, B, 0.026, GYP, lw=0.5)
yi = 0.126
rect(ax, 0, yi, B, 0.015, OSB, lw=0.5)
rect(ax, 0, yi + 0.015, B, 0.40, INS, lw=0.6, hatch="///")
yj = yi + 0.415
hi, lo = yj + 0.15, yj + 0.05                                                # fall battens 0.15 -> 0.05 m
ax.add_patch(Polygon([(0, yj), (B, yj), (B, lo), (0, hi)], fc="white", ec=INK, lw=0.6))
ax.add_patch(Polygon([(0, hi), (B, lo), (B, lo + 0.032), (0, hi + 0.032)], fc=FELT, ec=INK, lw=0.6))
for x0 in (1.0, 2.1, 3.2):
    ax.add_patch(FancyArrowPatch((x0, yj + 0.035), (x0 + 0.6, yj + 0.035), arrowstyle="->", mutation_scale=9, lw=0.8, color=COLD))
ax.text(0.06, yj + 0.075, "ventilated gap", ha="left", fontsize=7.5, color=COLD)
ax.add_patch(Polygon([(B, lo + 0.03), (B + 0.18, lo + 0.03), (B + 0.18, lo - 0.08), (B + 0.05, lo - 0.08)], fc="white", ec=INK, lw=0.8))
ax.text(B + 0.22, lo - 0.1, "gutter", fontsize=8, va="center")
dim_v(ax, -0.1, yj, hi, "0.15", left=True, fs=8); dim_v(ax, B + 0.12, yj, lo, "", left=False)
ax.text(B + 0.22, lo + 0.03, "0.05", fontsize=8, va="center")
dim_h(ax, 0, B, -0.62, "4.0 m box width", above=True, fs=8.5)
ax.plot([-0.6, B + 0.5], [yi, yi], color=RED, lw=1.3, ls=(0, (5, 3)))
ax.text(-0.58, yi + 0.02, "assembly\ninterface", fontsize=7.5, color=RED, va="bottom")
fig.subplots_adjust(hspace=0.12)
save(fig, "flat-roof-element")


# ---------------------------------------------------------------- 12. box layouts with facade windows, venting hatches and roof lights (schematic)
# windows: (x0, y0, x1, y1) on the outer facade; hatches: same, short; roof lights: (x, y) centre of a 0.9 m square
WIN = {
    "108 m²": dict(w=[(1.0, 0, 3.0, 0), (5.0, 0, 7.0, 0), (9.0, 0, 11.0, 0), (1.2, 9, 2.8, 9), (9.2, 9, 10.8, 9),
                      (0, 3.5, 0, 5.5), (12, 3.5, 12, 5.5)],
               h=[(3.2, 0, 3.7, 0), (7.2, 0, 7.7, 0), (3.0, 9, 3.5, 9), (8.5, 9, 9.0, 9)],
               s=[(6.0, 8.3), (6.0, 2.0)]),
    "144 m²": dict(w=[(1.0, 0, 3.0, 0), (5.0, 0, 7.0, 0), (9.0, 0, 11.0, 0), (1.2, 12, 2.8, 12), (9.2, 12, 10.8, 12),
                      (0, 4.0, 0, 6.0), (0, 8.0, 0, 9.5), (12, 4.0, 12, 6.0), (12, 8.0, 12, 9.5)],
               h=[(3.2, 0, 3.7, 0), (7.2, 0, 7.7, 0), (3.0, 12, 3.5, 12), (8.5, 12, 9.0, 12)],
               s=[(6.0, 4.3), (6.0, 2.0), (6.0, 11.4)]),
    "208 m²": dict(w=[(4.4, 0, 8.6, 0), (4.4, 16, 8.6, 16), (0, 1.0, 0, 3.0), (0, 5.0, 0, 6.6), (0, 9.4, 0, 11.0),
                      (0, 13.0, 0, 15.0), (13, 1.0, 13, 3.0), (13, 5.0, 13, 6.6), (13, 9.4, 13, 11.0), (13, 13.0, 13, 15.0)],
               h=[(0, 3.3, 0, 3.8), (0, 11.4, 0, 11.9), (13, 3.3, 13, 3.8), (13, 11.4, 13, 11.9), (1.5, 0, 2.0, 0), (11.0, 16, 11.5, 16)],
               s=[(6.5, 6.6), (6.5, 4.0)]),
    "128 m²": dict(w=[(4.4, 0, 11.6, 0), (1.0, 0, 3.0, 0), (13.0, 0, 15.0, 0), (1.2, 8, 2.8, 8), (13.2, 8, 14.8, 8),
                      (0, 3.0, 0, 5.0), (16, 3.0, 16, 5.0)],
               h=[(4.2, 8, 4.7, 8), (11.3, 8, 11.8, 8), (3.3, 0, 3.8, 0), (12.2, 0, 12.7, 0)],
               s=[(6.0, 3.3), (10.0, 3.3)]),
    "153 m²": dict(w=[(4.4, 0, 12.6, 0), (1.0, 0, 3.0, 0), (14.0, 0, 16.0, 0), (1.2, 9, 2.8, 9), (14.2, 9, 15.8, 9),
                      (0, 3.5, 0, 5.5), (17, 3.5, 17, 5.5)],
               h=[(4.4, 9, 4.9, 9), (12.1, 9, 12.6, 9), (3.3, 0, 3.8, 0), (13.2, 0, 13.7, 0)],
               s=[(6.3, 4.2), (10.7, 4.2), (8.5, 2.0)])}
WCOL, HCOL = COLD, WARM
fig, ax = plt.subplots(figsize=(9.5, 8.9)); ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(-1, 44); ax.set_ylim(-16.5, 19.5)
for (title, boxes, site, pods) in L:
    ox, oy = order[title]
    for (x, y, w, h, t) in boxes:
        rect(ax, ox + x, oy + y, w, h, "#efece4", lw=1.1)
    if site:
        x, y, w, h = site
        rect(ax, ox + x, oy + y, w, h, "white", lw=0.9, ls="--")
    for (x, y, w, h, t) in pods:
        rect(ax, ox + x, oy + y, w, h, "white", ec=MUTED, lw=0.8)
        big = t == "bath" and w >= 2.2                                       # largest bathrooms get a roof light
        if big:
            rect(ax, ox + x + w / 2 - 0.35, oy + y + h - 1.0, 0.7, 0.7, "#cfe1f5", ec=WCOL, lw=1.0)
        ax.text(ox + x + w / 2, oy + y + (0.6 if big else h / 2), t, ha="center", va="center", color=MUTED,
                fontsize=6 if "utility" in t else 7, rotation=90 if w < 1.5 else 0)
    f = WIN[title]
    for (x0, y0, x1, y1) in f["w"]:
        ax.plot([ox + x0, ox + x1], [oy + y0, oy + y1], color=WCOL, lw=4.5, solid_capstyle="butt")
    for (x0, y0, x1, y1) in f["h"]:
        ax.plot([ox + x0, ox + x1], [oy + y0, oy + y1], color=HCOL, lw=4.5, solid_capstyle="butt")
    for (x, y) in f["s"]:
        rect(ax, ox + x - 0.45, oy + y - 0.45, 0.9, 0.9, "#cfe1f5", ec=WCOL, lw=1.0)
    top = max(y + h for (x, y, w, h, t) in boxes + ([(*site, "")] if site else []))
    ax.text(ox, oy + top + 0.6, title, fontsize=14, fontweight="bold")
ax.plot([], [], color=WCOL, lw=4.5, label="facade window")
ax.plot([], [], color=HCOL, lw=4.5, label="venting hatch")
ax.add_patch(Rectangle((0, 0), 0, 0, fc="#cfe1f5", ec=WCOL, label="roof window or sun tunnel"))
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=3, frameon=False, fontsize=10)
save(fig, "box-layouts-windows")
