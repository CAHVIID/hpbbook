"""Charts for the four cooling-assignment lecture decks. Run: python3 make_figures.py"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import brentq
from pythermalcomfort.models import cooling_effect

ROOT = Path("/mnt/project-files")
OUT = Path(__file__).parent / "figures"
RED, DARK, GREY, LIGHT, BLUE, ORANGE = "#990000", "#262626", "#8C8C8C", "#D9D9D9", "#2F6DB5", "#E07B39"
plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 13, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.edgecolor": GREY, "axes.labelcolor": DARK,
                     "xtick.color": DARK, "ytick.color": DARK, "axes.grid": True, "grid.color": "#EBEBEB",
                     "axes.axisbelow": True, "legend.frameon": False})

def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=200, bbox_inches="tight"); fig.savefig(OUT / f"{name}.svg", bbox_inches="tight"); plt.close(fig)

def epw(name):
    d = np.genfromtxt(ROOT / name, delimiter=",", skip_header=8, usecols=(1, 2, 3, 6, 13))
    return d[:, 0].astype(int), d[:, 1].astype(int), d[:, 2].astype(int), d[:, 3], d[:, 4]

# 1 Annex 80 Copenhagen typical years: summer hours > 26 C and May-Sep GHI
files = [("2001–2020", "5A_Copenhagen_TMY_2001-2020.epw"), ("2041–2060", "5A_Copenhagen_TMY_2041-2060.epw"),
         ("2081–2100", "5A_Copenhagen_TMY_2081-2100.epw")]
h26, ghi = [], []
for lab, f in files:
    m, _, _, t, g = epw(f); s = (m >= 5) & (m <= 9)
    h26.append(int((t > 26).sum())); ghi.append(g[s].sum() / 1000)
fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4))
x = np.arange(3); cols = [GREY, RED, GREY]
a.bar(x, h26, color=cols); a.set_xticks(x, [l for l, _ in files]); a.set_title("Hours with outdoor air > 26 °C", loc="left", fontsize=13)
for i, v in enumerate(h26): a.text(i, v + 1.5, f"{v}", ha="center")
b.bar(x, ghi, color=cols); b.set_xticks(x, [l for l, _ in files]); b.set_title("Global horizontal irradiation May–Sep (kWh/m²)", loc="left", fontsize=13)
b.set_ylim(500, 760)
for i, v in enumerate(ghi): b.text(i, v + 4, f"{v:.0f}", ha="center")
for ax in (a, b): ax.grid(axis="x", visible=False)
fig.text(0, -0.04, "Annex 80 Copenhagen typical years (Qian 2021). Red: the file used in parts 1–3.", color=GREY, fontsize=11)
save(fig, "annex80-typical-years"); print("TMY h>26:", h26, "GHI:", [round(v) for v in ghi])

# 2 Pareto front schematic (no data)
rng = np.random.default_rng(3)
c = rng.uniform(0.12, 1, 400); h = rng.uniform(0.12, 1, 400)
gap = c * h - 0.12; keep = (gap > 0) & (rng.uniform(0, 0.25, 400) < gap); c, h = c[keep][:55], h[keep][:55]
fc = np.linspace(0.13, 0.95, 60)
fig, ax = plt.subplots(figsize=(6.4, 4.6))
ax.scatter(c, h, s=30, color=LIGHT, edgecolor=GREY, label="Evaluated designs (dominated)")
ax.plot(fc, 0.12 / fc, color=RED, lw=2.5, label="Pareto front: no design is better on both")
cx = 0.33; ax.scatter([cx], [0.12 / cx], s=180, facecolor="none", edgecolor=DARK, lw=2, zorder=5)
ax.annotate("Chosen design\n(meets sDA300 ≥ 50 %)", (cx, 0.12 / cx), (0.5, 0.75), arrowprops=dict(arrowstyle="->", color=DARK), bbox=dict(fc="white", ec="none", alpha=0.9), zorder=6)
ax.set_xlim(0, 1.05); ax.set_ylim(0, 1.05)
ax.set_xlabel("Cooling demand  →"); ax.set_ylabel("Heating demand  →"); ax.set_xticklabels([]); ax.set_yticklabels([])
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=1); ax.text(0.98, 0.02, "Schematic, not results", transform=ax.transAxes, color=GREY, fontsize=11, ha="right")
save(fig, "pareto-schematic")

# 3 Draught: near-floor speed vs ACH (low opening) against DR and ankle limits
def v_dr(ta, dr=20, tu=40):
    return brentq(lambda v: (34 - ta) * (v - 0.05) ** 0.62 * (0.37 * v * tu + 3.14) - dr, 0.051, 2)
V = 40.0  # 4 x 4 x 2.5 m zone
ach = np.linspace(0, 12, 200); q0 = ach * V / 3600
fig, ax = plt.subplots(figsize=(8.5, 4.8))
for K, ls in [(4.4, "-"), (10, "--")]:
    ax.plot(ach, K * q0 / 1.0, ls, color=BLUE, lw=2.2, label=f"Floor flow, K = {K:g} 1/m")
lims = [(v_dr(26), "DR 20 % at 26 °C", RED, "-"), (v_dr(20), "DR 20 % at 20 °C", RED, ":"),
        (0.39, "Ankle draught 20 %, TS = 0", DARK, "-"), (0.35 * -0.5 + 0.39, "Ankle draught 20 %, TS = −0.5", DARK, ":")]
for v, lab, col, ls in lims:
    ax.axhline(v, color=col, ls=ls, lw=1.6); ax.text(12.1, v, f"{lab}  ({v:.2f} m/s)", va="center", color=col, fontsize=11)
ax.set_xlim(0, 12); ax.set_ylim(0, 0.6); ax.set_xlabel("Airflow through the opening (ACH, 40 m³ zone)")
ax.set_ylabel("Air speed 0.1 m above floor,\n1 m from wall (m/s)"); ax.legend(loc="upper left")
save(fig, "floor-speed-vs-ach"); print("DR limits:", round(v_dr(26), 3), round(v_dr(20), 3))

# 4 Ceiling wall jet from high bottom-hung hatch (Svidt, Heiselberg & Nielsen 2000)
x = np.linspace(2.6, 6, 100)
fig, ax = plt.subplots(figsize=(7.5, 4.6))
for a0, n, ls in [(0.10, 3, "-"), (0.10, 6, "--"), (0.20, 6, ":")]:
    U0 = n * V / 3600 / a0
    ax.plot(x, 7 * U0 * np.sqrt(a0) / (x - 2), ls, color=RED, lw=2.2, label=f"a₀ = {a0:.2f} m², {n} ACH (U₀ = {U0:.1f} m/s)")
ax.axvline(4, color=GREY, lw=1); ax.text(4.05, 0.05, "Opposite wall of a 4 m room", color=GREY, fontsize=11)
ax.set_xlabel("Distance from hatch along the ceiling, x (m)"); ax.set_ylabel("Max. jet speed u_m (m/s)")
ax.set_ylim(0, 1.6); ax.legend(loc="upper right")
save(fig, "ceiling-jet-decay")

# 5 Cooling effect vs air speed
vs = np.linspace(0.1, 1.2, 23)
fig, ax = plt.subplots(figsize=(7.5, 4.6))
for t, col in [(26, GREY), (28, RED), (30, DARK)]:
    ce = [cooling_effect(tdb=t, tr=t, vr=v, rh=50, met=1.2, clo=0.5).ce for v in vs]
    ax.plot(vs, ce, color=col, lw=2.2, label=f"{t} °C")
    if t == 28: print("CE 28C at 0.5 m/s:", cooling_effect(tdb=28, tr=28, vr=0.5, rh=50, met=1.2, clo=0.5).ce)
ax.set_xlabel("Relative air speed at the occupant (m/s)"); ax.set_ylabel("Cooling effect (°C)")
ax.legend(title="Air = radiant temp.", loc="lower right"); ax.set_xlim(0, 1.2); ax.set_ylim(0, 5)
fig.text(0, -0.04, "SET method (ASHRAE 55), 50 % RH, 1.2 met, 0.5 clo, pythermalcomfort.", color=GREY, fontsize=11)
save(fig, "cooling-effect-vs-speed")

# 6 CFE of six fans (ceiling fans chapter, table tab-cfe)
fans = [("Westinghouse Contractor's Choice", 0.05, "AC"), ("Minka Aire Light Wave", 0.05, "AC"), ("Fanco Breeze AC 132", 0.09, "AC"),
        ("Hunter Erling 52850", 0.16, "DC"), ("CasaFan Eco Genuino 152", 0.22, "DC"), ("CasaFan Eco Genuino 122", 0.31, "DC")]
fig, ax = plt.subplots(figsize=(8, 4.2))
y = np.arange(len(fans))
ax.barh(y, [f[1] for f in fans], color=[GREY if f[2] == "AC" else RED for f in fans])
ax.set_yticks(y, [f"{f[0]} ({f[2]})" for f in fans]); ax.invert_yaxis(); ax.grid(axis="y", visible=False)
for i, f in enumerate(fans): ax.text(f[1] + 0.005, i, f"{f[1]:.2f}", va="center")
ax.set_xlabel("Cooling fan efficiency, CFE (°C per W) at max. speed")
fig.text(0, -0.05, "All six give 3.5–3.9 °C cooling effect in a 4.5 × 4.5 m room. Grey: AC motor, red: DC motor.", color=GREY, fontsize=11)
save(fig, "cfe-fans")

# 7 Heat wave MostSevere 2054: daily outdoor max/min and adaptive cat. II upper limit
m, d, hr, t, g = epw("5A_Copenhagen_HW_Midterm_MostSevere_2054.epw")
day = (np.cumsum(np.r_[1, (d[1:] != d[:-1])]) - 1)
tmean = np.array([t[day == k].mean() for k in range(365)]); tmax = np.array([t[day == k].max() for k in range(365)]); tmin = np.array([t[day == k].min() for k in range(365)])
trm = np.zeros(365); trm[0] = tmean[0]
for k in range(1, 365): trm[k] = 0.8 * trm[k - 1] + 0.2 * tmean[k - 1]
upper = 0.33 * trm + 18.8 + 3
import datetime as dt
dates = [dt.date(2054, 1, 1) + dt.timedelta(k) for k in range(365)]
s, e = (dt.date(2054, 7, 9) - dt.date(2054, 1, 1)).days, (dt.date(2054, 8, 5) - dt.date(2054, 1, 1)).days
w = slice(s - 7, e + 8)
fig, ax = plt.subplots(figsize=(10, 4.4))
ax.axvspan(dates[s], dates[e], color="#F3E0E0", lw=0)
ax.fill_between(dates[w], tmin[w], tmax[w], color=ORANGE, alpha=0.25, lw=0, label="Outdoor daily min–max")
ax.plot(dates[w], tmean[w], color=ORANGE, lw=1.8, label="Outdoor daily mean")
ax.plot(dates[w], upper[w], color=RED, lw=2.4, label="Adaptive cat. II upper limit (EN 16798-1)")
ax.text(dates[s + 1], 33.2, "Heat wave 9 Jul – 5 Aug 2054", color=RED, fontsize=12)
ax.set_ylabel("Temperature (°C)"); ax.set_ylim(8, 35); ax.legend(loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.32))
import matplotlib.dates as mdates; ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
save(fig, "heatwave-2054")
hw = slice(s, e + 1)
print("HW: max", tmax[hw].max(), "days>28", int((tmax[hw] > 28).sum()), "min", tmin[hw].min(), "upper range", upper[hw].min().round(1), upper[hw].max().round(1))

# 8 Hourly warmest week, outdoor vs limit: hours when venting can still cool (T_out < 24 C)
kmax = s + int(np.argmax([tmean[k - 3:k + 4].mean() for k in range(s + 3, e - 3)])) + 0
sel = (day >= kmax) & (day < kmax + 7)
hrs = np.arange(sel.sum())
fig, ax = plt.subplots(figsize=(10, 4.2))
ax.plot(hrs / 24, t[sel], color=ORANGE, lw=1.8, label="Outdoor air")
ax.plot(hrs / 24, upper[day[sel]], color=RED, lw=2.2, label="Adaptive cat. II upper limit")
ax.fill_between(hrs / 24, t[sel], 24, where=t[sel] < 24, color=BLUE, alpha=0.25, lw=0, label="Outdoor < 24 °C: venting can cool")
ax2 = ax.twinx(); ax2.plot(hrs / 24, g[sel], color=GREY, lw=1, alpha=0.7); ax2.set_ylabel("GHI (W/m²)", color=GREY); ax2.set_ylim(0, 2500); ax2.grid(False)
ax2.spines["right"].set_visible(True); ax2.tick_params(colors=GREY)
ax.set_xlabel(f"Days from {dates[kmax].strftime('%d %b')} 2054"); ax.set_ylabel("Temperature (°C)"); ax.set_ylim(5, 36)
ax.legend(loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.36))
save(fig, "heatwave-week")
print("warmest week starts", dates[kmax], "night hours <24:", int((t[sel] < 24).sum()), "max GHI", g[sel].max())
