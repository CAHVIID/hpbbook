"""Monthly cloud cover (DMI DRY) and global horizontal irradiation (Annex 80 TMY), May-Sep."""
import csv, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
from pathlib import Path
DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")  # folder with the EPW files
OUT = Path(__file__).resolve().parent.parent / "figures" / "d1"
def load(f):
    return list(csv.reader(open(DATA / f, encoding="latin-1")))[8:]
months = [5, 6, 7, 8, 9]; mlab = ["May", "Jun", "Jul", "Aug", "Sep"]
def tsc(rows):  # mean total sky cover, tenths
    return [sum(float(r[22]) for r in rows if int(r[1]) == m) / sum(1 for r in rows if int(r[1]) == m) for m in months]
def ghi(rows):  # monthly GHI sum, kWh/m2 (cap corrupt values)
    return [sum(min(float(r[13]), 1500) for r in rows if int(r[1]) == m) / 1000 for m in months]
dry = [("DRY 2001–2010", "Denmark_DRY_2001-2010.epw", "#9a9a9a"),
       ("DRY 2011–2023", "DRY_2011-2023_epw-fil.epw", "#2a78d6"),
       ("DRY RCP4.5 2045–2064", "DRY_rcp45_2045_2064_epw-fil.epw", "#eb6834")]
a80 = [("TMY 2001–2020", "5A_Copenhagen_TMY_2001-2020.epw", "#9a9a9a"),
       ("TMY 2041–2060", "5A_Copenhagen_TMY_2041-2060.epw", "#2a78d6"),
       ("TMY 2081–2100", "5A_Copenhagen_TMY_2081-2100.epw", "#eb6834")]
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
out = []
for name, f, c in dry:
    v = tsc(load(f)); out.append((name, "cloud tenths", v))
    ax[0].plot(mlab, v, color=c, lw=2, marker="o", ms=6, label=name)
ax[0].set_ylim(0, 10); ax[0].set_ylabel("Mean total sky cover (tenths)")
ax[0].set_title("(a) Cloud cover, DMI DRY Sjælsmark", loc="left", fontsize=10)
w = 0.27
for i, (name, f, c) in enumerate(a80):
    v = ghi(load(f)); out.append((name, "GHI kWh/m2", v))
    ax[1].bar([k + (i - 1) * w for k in range(5)], v, width=w - 0.02, color=c, label=name)
ax[1].set_xticks(range(5)); ax[1].set_xticklabels(mlab)
ax[1].set_ylabel("Global horizontal irradiation (kWh/m²)")
ax[1].set_title("(b) Solar irradiation, Annex 80 Copenhagen", loc="left", fontsize=10)
for a in ax:
    a.grid(axis="y", color="#e5e5e5"); a.set_axisbelow(True); a.legend(frameon=False, fontsize=8.5)
fig.tight_layout()
fig.savefig(OUT / "cloud-cover.png", dpi=200); fig.savefig(OUT / "cloud-cover.svg")
for n, u, v in out: print(n, u, [round(x, 1) for x in v], "sum/mean", round(sum(v) if "GHI" in u else sum(v)/5, 1))
