"""Figures for chapter E3 Construction design. Approximate hand-calculation models, not structural design.
Assumptions: timber E = 11 000 MPa; I-joists with 45 x 45 mm timber flanges and a 10 mm OSB web (G = 1000 MPa);
solid joists 45 mm wide (G = 690 MPa); characteristic floor load 2.0 kN/m2 at c/c 0.6 m (q = 1.2 kN/m).
Writes SVG + PNG to figures/e3/: joist-load, joist-deflection, ijoist-hole."""
import numpy as np
import matplotlib
import matplotlib.ticker
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch, Circle
from pathlib import Path
import sys
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "figures" / "e3"
OUT.mkdir(parents=True, exist_ok=True)
INK, MUTED, WARM, COLD, GREY, WOOD, RED = "#1f1f1e", "#6b6a63", "#eb6834", "#2a78d6", "#d9d7cf", "#c9a46a", "#a00000"
OSB = "#e6d3a8"
plt.rcParams.update({"font.size": 9, "svg.fonttype": "none"})
E = 11000.0


def save(fig, name):
    for ext in ("svg", "png"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def arrow(ax, p0, p1, c=INK, lw=1.0, ms=9, style="-|>"):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms, lw=lw, color=c))


# ---------------------------------------------------------------- sections
def ijoist(h, bf=45, tf=45, tw=10):
    hw = h - 2 * tf
    I = 2 * (bf * tf**3 / 12 + bf * tf * ((h - tf) / 2) ** 2) + tw * hw**3 / 12
    return dict(kind="I", h=h, bf=bf, tf=tf, tw=tw, I=I, A=2 * bf * tf + tw * hw, GA=1000.0 * tw * hw)


def solid(h, b=45):
    return dict(kind="S", h=h, bf=b, tf=0, tw=b, I=b * h**3 / 12, A=b * h, GA=690.0 * 5 / 6 * b * h)


SECTIONS = [("45 × 220 solid", solid(220)), ("I-joist 220", ijoist(220)),
            ("45 × 300 solid", solid(300)), ("I-joist 300", ijoist(300))]
COLS = ["#b07a2a", "#7fb0e6", "#7a4f12", "#2a78d6"]


def chord(p, hh):
    """Area, own I and centroid (from the outer edge) of one chord above or below a web opening of height hh."""
    if p["kind"] == "I":                # flange + remaining web strip
        s = (p["h"] - 2 * p["tf"] - hh) / 2
        parts = [(p["bf"], p["tf"], p["tf"] / 2), (p["tw"], s, p["tf"] + s / 2)]
    else:                               # solid strip
        s = (p["h"] - hh) / 2
        parts = [(p["bf"], s, s / 2)]
    A = sum(b * t for b, t, _ in parts); yc = sum(b * t * y for b, t, y in parts) / A
    I = sum(b * t**3 / 12 + b * t * (y - yc) ** 2 for b, t, y in parts)
    return A, I, yc


def deflection(p, q, L, hole=None, n=8001):
    """Midspan deflection (mm) of a simply supported beam with a uniform load q (N/mm): bending + shear.
    hole = (x0, D): round hole of diameter D centred at mid-height, x0 from the support (mm). Over the hole the two
    chords carry the moment together and the shear force by local bending (Vierendeel action)."""
    x = np.linspace(0, L, n)
    M = q * x * (L - x) / 2; V = q * (L / 2 - x)
    m = np.where(x < L / 2, x / 2, (L - x) / 2); v = np.where(x < L / 2, 0.5, -0.5)
    EI = np.full(n, E * p["I"]); GA = np.full(n, float(p["GA"])); slip = 0.0
    if hole:
        x0, D = hole; r = D / 2
        inh = np.abs(x - x0) < r
        xi = x[inh]; hh = 2 * np.sqrt(np.maximum(r**2 - (xi - x0) ** 2, 0))
        Ic = np.empty_like(xi)
        for k, h_ in enumerate(hh):
            Ac, Ic[k], yc = chord(p, h_)
            EI[np.where(inh)[0][k]] = min(E * p["I"], E * (2 * Ic[k] + 2 * Ac * ((p["h"] - 2 * yc) / 2) ** 2))
        Vx = abs(q * (L / 2 - x0))
        # each chord takes V/2 with an antisymmetric local moment; relative slip by the unit-load method
        slip = np.trapezoid((Vx / 2) * (xi - x0) ** 2 / (E * Ic), xi)
        slip *= 0.5                     # a shear slip at x0 moves midspan by half of it
    return np.trapezoid(M * m / EI + V * v / GA, x) + slip




# ---------------------------------------------------------------- 1. load on one joist
fig = plt.figure(figsize=(10.5, 4.6))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.25], wspace=0.12)
ax = fig.add_subplot(gs[0]); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("(a) Floor plan: load area of one joist", loc="left", fontsize=10)
L, cc = 4.0, 0.6
ax.add_patch(Rectangle((1.5 * cc, 0), cc, L, fc="#f7e2d5", ec="none"))
for i in range(5):
    ax.add_patch(Rectangle((i * cc - 0.0225, 0), 0.045, L, fc=WOOD, ec=INK, lw=0.6))
ax.add_patch(Rectangle((-0.3, -0.15), 5 * cc - 0.0, 0.15, fc=GREY, ec=INK, lw=0.6))
ax.add_patch(Rectangle((-0.3, L), 5 * cc - 0.0, 0.15, fc=GREY, ec=INK, lw=0.6))
ax.text(1.2 + cc / 2 + 0.0, L / 2, "load area\nc/c × L", ha="center", va="center", fontsize=8.5, color=RED,
        bbox=dict(fc="white", ec="none", pad=1))
arrow(ax, (2 * cc, L + 0.45), (3 * cc, L + 0.45), style="<->", ms=7, lw=0.7)
ax.text(2.5 * cc, L + 0.52, "c/c", ha="center", va="bottom", fontsize=8.5)
arrow(ax, (-0.55, 0), (-0.55, L), style="<->", ms=7, lw=0.7)
ax.text(-0.62, L / 2, "span L", ha="right", va="center", fontsize=8.5)
ax.text(1.2, -0.35, "support (wall)", ha="center", va="top", fontsize=8, color=MUTED)
ax.set_xlim(-1.3, 2.9); ax.set_ylim(-0.7, L + 0.8)

ax = fig.add_subplot(gs[1]); ax.axis("off"); ax.set_xlim(-0.6, 4.6); ax.set_ylim(-1.6, 1.6)
ax.set_title("(b) The joist as a simply supported beam", loc="left", fontsize=10)
ax.add_patch(Rectangle((0, -0.1), L, 0.2, fc=WOOD, ec=INK, lw=0.8))
for xs in (0, L):
    ax.add_patch(Polygon([(xs, -0.1), (xs - 0.15, -0.4), (xs + 0.15, -0.4)], fc="white", ec=INK, lw=0.8))
for xi in np.linspace(0.1, L - 0.1, 14):
    arrow(ax, (xi, 0.6), (xi, 0.12), c=RED, lw=0.8, ms=6)
ax.plot([0.1, L - 0.1], [0.6, 0.6], color=RED, lw=0.8)
ax.text(L / 2, 0.68, "q = load × c/c   (kN/m)", ha="center", va="bottom", color=RED, fontsize=9)
xx = np.linspace(0, L, 100); yy = -0.1 - 0.55 * np.sin(np.pi * xx / L)
ax.plot(xx, yy, ls="--", color=COLD, lw=1.2)
arrow(ax, (L / 2 + 0.25, -0.1), (L / 2 + 0.25, -0.65), c=COLD, style="<->", ms=7, lw=0.8)
ax.text(L / 2 + 0.35, -0.38, "δ", color=COLD, fontsize=11, va="center")
ax.text(L / 2, -1.25, "δ = 5 q L⁴ / (384 E I)", ha="center", fontsize=10)
save(fig, "joist-load")

# ---------------------------------------------------------------- 1b. deflection vs joist height, load and c/c (solid 45 mm joists, span 4 m)
fig, axs = plt.subplots(1, 2, figsize=(11, 4.4), sharey=True)
hs = np.linspace(150, 350, 41); Lsp = 4000
def panel(ax, title, cases, cols):
    for (lab, q), c in zip(cases, cols):
        d = [deflection(solid(h), q, Lsp, n=801) for h in hs]
        ax.plot(hs, d, color=c, lw=2, label=lab)
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")
    ax.axhline(Lsp / 400, color=MUTED, lw=1, ls=":")
    ax.text(348, Lsp / 400 + 0.5, "L/400 = 10 mm", color=MUTED, fontsize=8, ha="right", va="bottom")
    ax.set_title(title, loc="left", fontsize=10)
    ax.set_xlim(150, 350); ax.set_ylim(0, 40); ax.set_xlabel("joist height h (mm)")
    ax.grid(color="#eeeeea", lw=0.6); ax.spines[["top", "right"]].set_visible(False)
panel(axs[0], "(a) Load, c/c 0.6 m", [("3.0 kN/m²", 1.8), ("2.0 kN/m²", 1.2), ("1.0 kN/m²", 0.6)], ["#123f7a", "#2a78d6", "#7fb0e6"])
panel(axs[1], "(b) Centre distance, 2.0 kN/m²", [("c/c 0.6 m", 1.2), ("c/c 0.45 m", 0.9), ("c/c 0.3 m", 0.6)], ["#7a4f12", "#b07a2a", "#d9b38a"])
axs[0].set_ylabel("midspan deflection δ (mm)")
save(fig, "joist-height")

# ---------------------------------------------------------------- 2. sections to scale + deflection vs span
fig = plt.figure(figsize=(11, 4.6))
gs = fig.add_gridspec(1, 2, width_ratios=[0.75, 1.15], wspace=0.12)
ax = fig.add_subplot(gs[0]); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("(a) Sections to scale", loc="left", fontsize=10)
x = 0
for (name, p), c in zip(SECTIONS, COLS):
    h = p["h"]
    if p["kind"] == "S":
        ax.add_patch(Rectangle((x, 0), 45, h, fc=WOOD, ec=INK, lw=0.7))
    else:
        ax.add_patch(Rectangle((x, 0), 45, 45, fc=WOOD, ec=INK, lw=0.7))
        ax.add_patch(Rectangle((x, h - 45), 45, 45, fc=WOOD, ec=INK, lw=0.7))
        ax.add_patch(Rectangle((x + 17.5, 45), 10, h - 90, fc=OSB, ec=INK, lw=0.7))
    ax.text(x + 22.5, -18, name.replace(" solid", "\nsolid").replace("I-joist ", "I-joist\n"), ha="center", va="top", fontsize=8)
    ax.text(x + 22.5, h + 14, f"A = {p['A']/1e3:.1f}\nI = {p['I']/1e6:.0f}", ha="center", va="bottom", fontsize=7.5, color=MUTED)
    x += 105
ax.text(0, 520, "A in 10³ mm², I in 10⁶ mm⁴", fontsize=8, color=MUTED)
ax.set_xlim(-15, x - 40); ax.set_ylim(-80, 545)

ax = fig.add_subplot(gs[1])
ax.set_title("(b) Midspan deflection, 2.0 kN/m², c/c 0.6 m", loc="left", fontsize=10)
spans = np.linspace(2.0, 6.0, 41)
for (name, p), c in zip(SECTIONS, COLS):
    d = [deflection(p, 1.2, s * 1000, n=801) for s in spans]
    ls = "-" if p["kind"] == "I" else (0, (5, 2))
    ax.plot(spans, d, color=c, lw=2, ls=ls, label=name)
for r, lab in ((300, "L/300"), (400, "L/400")):
    ax.plot(spans, spans * 1000 / r, color=MUTED, lw=1, ls=":")
    ax.text(6.02, 6000 / r, lab, color=MUTED, fontsize=8, va="center")
ax.set_xlim(2, 6); ax.set_ylim(0, 30)
ax.set_xlabel("span L (m)"); ax.set_ylabel("deflection δ (mm)")
ax.grid(color="#eeeeea", lw=0.6); ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, fontsize=8, loc="upper left")
save(fig, "joist-deflection")

# ---------------------------------------------------------------- 2b. joists across (short way) vs along (long way) a 4 x 12 m box
fig = plt.figure(figsize=(11, 6.4))
gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.05], hspace=0.45, wspace=0.18)
BL, BW = 12.0, 4.0
def box_plan(ax, title, across):
    ax.set_aspect("equal"); ax.axis("off"); ax.set_title(title, loc="left", fontsize=10)
    ax.add_patch(Rectangle((0, 0), BL, BW, fc="white", ec="none"))
    sup = "#555555"
    if across:   # supports = long walls
        ax.add_patch(Rectangle((0, -0.12), BL, 0.12, fc=sup, ec="none")); ax.add_patch(Rectangle((0, BW), BL, 0.12, fc=sup, ec="none"))
        ax.add_patch(Rectangle((-0.12, -0.12), 0.12, BW + 0.24, fc=GREY, ec="none")); ax.add_patch(Rectangle((BL, -0.12), 0.12, BW + 0.24, fc=GREY, ec="none"))
        for x in np.arange(0.3, BL, 0.6):
            ax.add_patch(Rectangle((x - 0.03, 0), 0.06, BW, fc=WOOD, ec="none"))
        arrow(ax, (BL + 0.5, 0), (BL + 0.5, BW), style="<->", ms=7, lw=0.7)
        ax.text(BL + 0.65, BW / 2, "span\n≈ 4 m", va="center", fontsize=8.5)
        ax.text(BL / 2, -0.35, "long walls carry the joists", ha="center", va="top", fontsize=8, color=MUTED)
    else:        # supports = gables
        ax.add_patch(Rectangle((-0.12, -0.12), 0.12, BW + 0.24, fc=sup, ec="none")); ax.add_patch(Rectangle((BL, -0.12), 0.12, BW + 0.24, fc=sup, ec="none"))
        ax.add_patch(Rectangle((0, -0.12), BL, 0.12, fc=GREY, ec="none")); ax.add_patch(Rectangle((0, BW), BL, 0.12, fc=GREY, ec="none"))
        for y in np.arange(0.3, BW, 0.6):
            ax.add_patch(Rectangle((0, y - 0.03), BL, 0.06, fc=WOOD, ec="none"))
        arrow(ax, (0, -0.5), (BL, -0.5), style="<->", ms=7, lw=0.7)
        ax.text(BL / 2, -0.62, "span ≈ 12 m; gables carry the joists", ha="center", va="top", fontsize=8.5)
    ax.set_xlim(-0.4, BL + 2.0); ax.set_ylim(-1.4, BW + 0.4)
box_plan(fig.add_subplot(gs[0, 0]), "(a) Joists across the box (short way)", True)
box_plan(fig.add_subplot(gs[1, 0]), "(b) Joists along the box (long way)", False)
ax = fig.add_subplot(gs[:, 1])
ax.set_title("(c) Midspan deflection, 2.0 kN/m², c/c 0.6 m", loc="left", fontsize=10)
spans = np.linspace(2, 13, 45)
for lab, p, c, ls in (("45 × 295 solid", solid(295), "#7a4f12", (0, (5, 2))), ("I-joist 45 × 295", ijoist(295), "#2a78d6", "-")):
    ax.plot(spans, [deflection(p, 1.2, L_ * 1000, n=801) for L_ in spans], color=c, lw=2, ls=ls, label=lab)
ax.plot(spans, spans * 1000 / 400, color=MUTED, lw=1, ls=":", label="L/400")
for xv, t in ((4, "short way"), (12, "long way")):
    ax.axvline(xv, color=GREY, lw=1, zorder=0); ax.text(xv + 0.12, 0.55, t, fontsize=8, color=MUTED, rotation=90, va="bottom")
ax.set_yscale("log"); ax.set_xlim(2, 13); ax.set_ylim(0.5, 1000)
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
ax.set_xlabel("span L (m)"); ax.set_ylabel("deflection δ (mm, log scale)")
ax.grid(color="#eeeeea", lw=0.6, which="both"); ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, fontsize=8.5, loc="upper left")
save(fig, "joist-direction")

# ---------------------------------------------------------------- 3. round hole for a duct: solid 45 x 295 vs I-joist 295, span 4 m
fig = plt.figure(figsize=(11, 6.6))
gs = fig.add_gridspec(2, 2, height_ratios=[0.8, 1.25], hspace=0.38, wspace=0.25)
ax = fig.add_subplot(gs[0, :]); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("(a) Simply supported joist, span 4.0 m, with a round hole Ø160 at distance x from the support", loc="left", fontsize=10)
H, Lb, D, x0 = 295, 4000, 160, 1100
ax.add_patch(Rectangle((0, 0), Lb, 45, fc=WOOD, ec=INK, lw=0.7))
ax.add_patch(Rectangle((0, H - 45), Lb, 45, fc=WOOD, ec=INK, lw=0.7))
ax.add_patch(Rectangle((0, 45), Lb, H - 90, fc=OSB, ec=INK, lw=0.7))
ax.add_patch(Circle((x0, H / 2), D / 2, fc="white", ec=INK, lw=0.8))
for xs_ in (0, Lb):
    ax.add_patch(Polygon([(xs_, 0), (xs_ - 70, -110), (xs_ + 70, -110)], fc="white", ec=INK, lw=0.8))
for xi in np.linspace(80, Lb - 80, 24):
    arrow(ax, (xi, H + 170), (xi, H + 10), c=RED, lw=0.7, ms=5)
ax.plot([80, Lb - 80], [H + 170, H + 170], color=RED, lw=0.7)
ax.text(Lb / 2, H + 185, "2.0 kN/m² × c/c 0.6 m", ha="center", va="bottom", color=RED, fontsize=8.5)
arrow(ax, (0, -190), (x0, -190), style="<->", ms=7, lw=0.7)
ax.text(x0 / 2, -205, "x", ha="center", va="top", fontsize=9)
arrow(ax, (0, -330), (Lb, -330), style="<->", ms=7, lw=0.7)
ax.text(Lb / 2, -345, "L = 4.0 m", ha="center", va="top", fontsize=9)
arrow(ax, (Lb + 90, 0), (Lb + 90, H), style="<->", ms=7, lw=0.7)
ax.text(Lb + 115, H / 2, "295", va="center", fontsize=8.5)
ax.set_xlim(-150, Lb + 300); ax.set_ylim(-480, H + 330)

xs = np.linspace(150, 2000, 38)
for k, (lab, p, c, ls) in enumerate([("(b) Solid joist 45 × 295", solid(295), "#7a4f12", (0, (5, 2))),
                                     ("(c) I-joist 45 × 295", ijoist(295), "#2a78d6", "-")]):
    ax = fig.add_subplot(gs[1, k])
    d0 = deflection(p, 1.2, Lb)
    y = np.array([deflection(p, 1.2, Lb, hole=(x_, D)) for x_ in xs])
    ax.axhline(d0, color=MUTED, lw=1.2, ls=":")
    ax.text(0.08, d0 - 0.002, "no hole", color=MUTED, fontsize=8, va="top")
    ax.plot(xs / 1000, y, color=c, lw=2, ls=ls)
    ax.text(xs[-1] / 1000, y[-1] + 0.002, "hole Ø160", color=INK, fontsize=8.5, ha="right", va="bottom")
    ax.set_title(lab, loc="left", fontsize=10)
    ax.set_xlim(0, 2); ax.set_ylim(d0 - 0.02, d0 + 0.06)
    ax.set_xlabel("distance x from support to hole centre (m)")
    if k == 0: ax.set_ylabel("midspan deflection δ (mm)")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%.2f"))
    ax.grid(color="#eeeeea", lw=0.6); ax.spines[["top", "right"]].set_visible(False)
save(fig, "ijoist-hole")
print("ok")
