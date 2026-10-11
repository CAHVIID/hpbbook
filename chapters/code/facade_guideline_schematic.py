"""Schematic façade guideline: normalised daylight, cooling, heating and comfort against window-to-floor ratio.
The curves are shapes only, not simulation results: they show what a brute-force IDA ICE sweep is expected
to look like. Each line is the reference glazing without shading; the shaded band is the spread over
solar-control glazing and overhang depths, which lower both cooling and daylight. Reference window at WFR 25 %, so energy and comfort
curves pass 1 there. Writes facade-guideline-schematic.svg/.png."""
import numpy as np
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt

BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
INK, MUTED, GRID, SURF = "#1f1f1e", "#6b6a63", "#e4e3dc", "#fcfcfb"
w = np.linspace(0.05, 0.35, 61)
REF = 0.25

def shapes(orient):
    if orient == "South":
        sda = 2.0 * (1 - np.exp(-(w - 0.04) / 0.09))          # sDA300 / 50 %, reference glazing
        sda_lo = 2.0 * (1 - np.exp(-(w - 0.07) / 0.13))       # low-LT glazing + deep overhang
        cool = lambda x: 0.15 + 3.4 * (x - 0.05) ** 1.15 / (REF - 0.05) ** 0.15
        cool_lo = 0.6 * cool(w)                               # g 0.32 + 1.2 m overhang
        heat = 1 + 9 * (w - 0.17) ** 2 - 9 * (REF - 0.17) ** 2
        comf = np.clip((w - 0.12) / (REF - 0.12), 0, None) ** 1.8
    else:
        sda = 2.0 * (1 - np.exp(-(w - 0.05) / 0.11))
        sda_lo = 2.0 * (1 - np.exp(-(w - 0.06) / 0.14))
        cool = lambda x: 0.35 + 2.6 * (x - 0.05)
        cool_lo = 0.85 * cool(w)                              # overhang barely helps towards north
        heat = 0.75 + 1.0 * (w - 0.05)
        comf = np.clip((w - 0.18) / (REF - 0.18), 0, None) ** 1.6
    c = cool(w) / cool(REF)
    return sda, sda_lo, c, cool_lo / cool(REF), heat / np.interp(REF, w, heat), comf / max(np.interp(REF, w, comf), 1e-9)

fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.2), sharey=True, facecolor=SURF)
for ax, orient in zip(axes, ["North", "South"]):
    ax.set_facecolor(SURF)
    sda, sda_lo, cool, cool_lo, heat, comf = shapes(orient)
    wmin = np.interp(1.0, sda, w)                              # first WFR meeting sDA300 >= 50 %
    wmin_lo = np.interp(1.0, sda_lo, w)                        # same with solar control + overhang
    ax.axvspan(0.05, wmin, color=GRID, alpha=0.6, lw=0)
    ax.axvspan(wmin, wmin_lo, color=GRID, alpha=0.3, lw=0)
    ax.text(0.052, 2.32, "sDA300 < 50 %", fontsize=8.5, color=MUTED, va="top")
    ax.axhline(1, color=MUTED, lw=0.8, ls=(0, (4, 3)))
    ax.axvline(REF, color=MUTED, lw=0.8, ls=":")
    ax.text(REF + 0.003, 0.03, "reference\nwindow", fontsize=8, color=MUTED, va="bottom")
    ax.fill_between(w, sda_lo, sda, color=BLUE, alpha=0.12, lw=0)
    ax.fill_between(w, cool_lo, cool, color=ORANGE, alpha=0.14, lw=0)
    ax.plot(w, sda, color=BLUE, lw=2)
    ax.plot(w, cool, color=ORANGE, lw=2)
    ax.plot(w, heat, color=AQUA, lw=2, ls=(0, (6, 2)))
    ax.plot(w, comf, color=YELLOW, lw=2, ls=(0, (2, 1.5)))
    lab = dict(fontsize=9, color=INK, va="center")
    ax.text(0.352, sda[-1], "Daylight", **lab)
    ax.text(0.352, cool[-1], "Cooling", **lab)
    ax.text(0.352, heat[-1] - (0.07 if orient == "South" else 0), "Heating", **lab)
    ax.text(0.352, min(comf[-1], 2.35), "Comfort", **lab)
    for x, y in ((wmin, 1.55), (wmin_lo, 0.45)):
        ax.plot(x, 1, "o", ms=6, color=BLUE, mec=SURF, mew=2, zorder=5)
    ax.annotate("minimum WFR,\nreference glazing", (wmin, 1), (wmin + 0.025, 1.6), fontsize=8, color=INK,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    ax.annotate("with solar control\n+ overhang", (wmin_lo, 1), (wmin_lo + 0.03, 0.4), fontsize=8, color=INK,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    ax.set_title(orient, fontsize=10, color=INK, loc="left")
    ax.set_xlim(0.05, 0.35); ax.set_ylim(0, 2.4)
    ax.set_xticks(np.arange(0.05, 0.36, 0.05)); ax.set_xticklabels([f"{x:.0%}" for x in np.arange(0.05, 0.36, 0.05)])
    ax.set_xlabel("Window-to-floor ratio", fontsize=10, color=INK)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED); ax.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
axes[0].set_ylabel("Normalised value (–)", fontsize=10, color=INK)
fig.text(0.01, 0.005, "Schematic, not simulation results. Daylight: sDA300/50 %. Cooling, heating, comfort "
         "(hours above adaptive cat. II):\n"
         "relative to the reference window. Lines: reference glazing, no shading. Band: spread over solar-control glazing and overhang.",
         fontsize=7.5, color=MUTED)
fig.tight_layout(rect=(0, 0.07, 0.97, 1))
for ext in ("svg", "png"):
    fig.savefig(f"facade-guideline-schematic.{ext}", dpi=200, facecolor=SURF)
