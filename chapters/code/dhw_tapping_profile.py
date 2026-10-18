"""Daily tapping profile: the heat power drawn at the taps over one day, and the cumulative heat.

Uses the profile "Family of 4, morning and evening" from dhw-tank.mjs (the profiles are generated
by build_profiles.py). Each tapping is drawn as a block from its start for volume/flow minutes,
with the power rho V' cp (theta - theta_c) and cold water at 10 °C.

Writes figures/c2/tapping-profile.svg and .png.
"""
import json, re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "figures" / "c2"
PROFILE, T_COLD, RHO, CP = "Family of 4, morning and evening", 10.0, 994.0, 4182.0
INK, MUTED, SURF = "#0b0b0b", "#52514e", "#fcfcfb"
COLS = {"shower": "#1c5cab", "washbasin": "#6cc3a0", "kitchen tap": "#eb6834", "washing up": "#d6493a"}

src = (HERE / "dhw-tank.mjs").read_text(encoding="utf-8")
line = next(l for l in src.splitlines() if l.strip().startswith(json.dumps(PROFILE) + ":"))
taps = json.loads(re.sub(r",\s*$", "", line.split(":", 1)[1].strip()))

plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(11, 4.2), facecolor=SURF, layout="constrained")
ax.set_facecolor(SURF)
t = np.linspace(0, 24, 24 * 60 + 1); cum = np.zeros_like(t)
seen, showers = set(), []
for start, name, vol, flow, temp in taps:
    dur = vol / flow / 60                                          # h
    p = RHO * flow / 60000 * CP * (temp - T_COLD) / 1000          # kW
    e = p * dur                                                    # kWh
    col = COLS.get(name, MUTED)
    ax.bar(start, p, width=max(dur, 0.04), align="edge", color=col, label=name if name not in seen else None, zorder=3)
    seen.add(name)
    cum += e * np.clip((t - start) / dur, 0, 1)
    if name == "shower":
        showers.append((start, dur, p, flow, temp))
groups = []                                       # showers less than 1 h apart share one label
for sh in showers:
    if groups and sh[0] - groups[-1][-1][0] < 1: groups[-1].append(sh)
    else: groups.append([sh])
for g in groups:
    start, dur, p, flow, temp = g[0]
    what = f"{len(g)} showers" if len(g) > 1 else "Shower"
    each = " each" if len(g) > 1 else ""
    ax.text((g[0][0] + g[-1][0] + g[-1][1]) / 2, p + 0.4, f"{what}, {flow} L/min at {temp} °C\n{p:.0f} kW{each}",
            ha="center", va="bottom", fontsize=8, color=COLS["shower"])
ax2 = ax.twinx()
ax2.plot(t, cum, color=INK, lw=1.4, label="Cumulative heat")
ax2.set_ylabel("Cumulative heat drawn (kWh)")
ax2.set_ylim(0, cum[-1] * 1.25)
ax2.text(23.8, cum[-1] * 1.03, f"{cum[-1]:.1f} kWh per day", ha="right", va="bottom", fontsize=9, color=INK)
ax.set_xlim(0, 24); ax.set_ylim(0, 22)
ax.set_xticks(range(0, 25, 3), [f"{h:02d}:00" for h in range(0, 25, 3)])
ax.set_xlabel("Time of day"); ax.set_ylabel("Heat power while tapping (kW)")
ax.grid(axis="y", color="#e6e5e0", lw=0.6); ax.set_axisbelow(True)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=8, loc="upper left", ncols=5)
for a in (ax, ax2): a.spines["top"].set_visible(False)
print("tappings", len(taps), "daily heat", round(float(cum[-1]), 2), "kWh")
for ext in ("svg", "png"):
    fig.savefig(OUT / f"tapping-profile.{ext}", dpi=200, facecolor=SURF)
