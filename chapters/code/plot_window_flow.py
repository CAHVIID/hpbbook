"""Figure: single-sided airflow against indoor-outdoor temperature difference,
side-hung window at three opening angles vs a bottom-hung (tilt) window."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from window_flow import total_flow, side_hung, bottom_hung

W, H = 0.8, 1.3
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures", "ch08")
cases = [
    ("Side-hung, 90°", side_hung, dict(w=W, h=H, angle_deg=90), "#2a78d6", "-", 0),
    ("Side-hung, 30°", side_hung, dict(w=W, h=H, angle_deg=30), "#2a78d6", "--", 0),
    ("Side-hung, 10°", side_hung, dict(w=W, h=H, angle_deg=10), "#2a78d6", ":", -7),
    ("Bottom-hung, 120 mm", bottom_hung, dict(w=W, h=H, stroke=0.12), "#eb6834", "-", 7),
]
dT = np.linspace(0.25, 10, 40)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(6.4, 4.0))
for name, kind, geo, c, ls, dy in cases:
    q = [total_flow(kind, t, 0, **geo)[0] * 3600 for t in dT]
    ax.plot(dT, q, color=c, ls=ls, lw=2)
    ax.annotate(name, (dT[-1], q[-1]), xytext=(6, dy), textcoords="offset points",
                va="center", fontsize=9, color="#333")
ax.axvspan(0, 5, color="#f2f1ec", zorder=0)
ax.text(2.5, 545, "summer: ΔT < 5 K", ha="center", fontsize=9, color="#555")
ax.set_xlim(0, 10); ax.set_ylim(0, 580)
ax.set_xlabel("Indoor–outdoor temperature difference ΔT (K)")
ax.set_ylabel("Airflow, no wind (m³/h)")
ax.grid(axis="y", color="#e4e3dd", lw=0.8)
ax.set_title("Single-sided stack flow, sash 0.8 × 1.3 m", loc="left", fontsize=10)
fig.subplots_adjust(right=0.74, bottom=0.13)
for ext in ("png", "svg"):
    fig.savefig(f"{OUT}/window-flow-dt.{ext}", dpi=200)
