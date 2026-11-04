"""Heating need and heat to remove across Denmark for one low-energy house, from the daily
equivalent outdoor temperature on DMI's 10 km climate grid (no simulation).

  T_eq = T_out + A_sol * I_glob / H
  heating:  sum (T_bal,h - T_eq)+   with T_bal,h = T_heat - Phi_int / H
  cooling:  sum (T_eq - T_bal,c)+   with T_bal,c = T_cool - Phi_int / H
  kWh/m2 = degree days * H * 24 / 1000 / A_floor

Data: DMI climateData API, 10kmGridValue, daily mean_temp (°C) and mean_radiation (MJ/m2 per day),
years 2011 and 2014-2023 (the grid has no radiation for 2012-2013). The first run downloads the data
(about 2.4 million values) into the cache folder given as first argument.
"""
import json, math, sys, urllib.request, datetime as dt, concurrent.futures as cf
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm

CACHE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "weather" / "dmi-grid"
OUT = Path(__file__).resolve().parent.parent / "figures" / "d1"
BASE = "https://opendataapi.dmi.dk/v2/climateData/collections/10kmGridValue/items"
YEARS = [2011] + list(range(2014, 2024))

# Reference low-energy house (single-family)
A_FLOOR = 150.0          # m2 heated floor area
H = 50.0                 # W/K, about 10 kWh/m2 space heating
A_SOL = 6.0              # m2, effective solar aperture relative to global horizontal radiation:
                         # 33 m2 windows (22 % of floor) x 0.7 glass x 0.5 g x 0.9 shading/dirt x 0.6 vertical/horizontal
PHI_INT = 5.0 * A_FLOOR  # W, internal gains 5 W/m2
T_HEAT, T_COOL = 20.0, 26.0
TB_H, TB_C = T_HEAT - PHI_INT / H, T_COOL - PHI_INT / H   # 12.5 and 18.5 °C


def get(par, y, m):
    start = dt.date(y, m, 1) - dt.timedelta(days=1)
    end = dt.date(y + (m == 12), m % 12 + 1, 1)
    url = (f"{BASE}?parameterId={par}&timeResolution=day&limit=30000"
           f"&datetime={start}T21:00:00Z/{end}T01:00:00Z")  # the interval must enclose the whole day
    for attempt in range(5):
        try:
            feats = json.load(urllib.request.urlopen(url, timeout=300))["features"]
            break
        except Exception:
            if attempt == 4:
                raise
    pre = f"{y}-{m:02d}"
    rows = [(f["properties"]["cellId"], f["properties"]["from"][:10], f["properties"]["value"])
            for f in feats if f["properties"]["from"].startswith(pre)]
    geo = {f["properties"]["cellId"]: f["geometry"]["coordinates"][0] for f in feats}
    return par, rows, geo


def load():
    data, cells = CACHE / "grid-daily.csv.gz", CACHE / "grid-cells.json"
    if not data.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        jobs = [(p, y, m) for p in ("mean_temp", "mean_radiation") for y in YEARS for m in range(1, 13)]
        parts, geo = {"mean_temp": [], "mean_radiation": []}, {}
        with cf.ThreadPoolExecutor(8) as ex:
            for par, rows, g in ex.map(lambda a: get(*a), jobs):
                parts[par] += rows
                geo.update(g)
        t = pd.DataFrame(parts["mean_temp"], columns=["cell", "date", "t"])
        r = pd.DataFrame(parts["mean_radiation"], columns=["cell", "date", "rad_mj"])
        t.merge(r, on=["cell", "date"]).to_csv(data, index=False)
        cells.write_text(json.dumps(geo))
    return pd.read_csv(data), json.loads(cells.read_text())


df, geo = load()
df["teq"] = df.t + A_SOL * (df.rad_mj * 1e6 / 86400) / H
df["hdd"] = (TB_H - df.teq).clip(lower=0)
df["cdd"] = (df.teq - TB_C).clip(lower=0)
nyears = df.date.str[:4].nunique()
res = df.groupby("cell")[["hdd", "cdd"]].sum() / nyears
res["heat"] = res.hdd * H * 24 / 1000 / A_FLOOR
res["cool"] = res.cdd * H * 24 / 1000 / A_FLOOR
print(f"T_bal,h = {TB_H} °C, T_bal,c = {TB_C} °C, {nyears} years, {len(res)} cells")
print(res.describe().round(1).to_string())

cells = [c for c in res.index if c in geo]
polys = [np.array(geo[c]) for c in cells]
STATIONS = {"Skagen": (10.636, 57.736), "Karup": (9.114, 56.297), "Esbjerg": (8.552, 55.526),
            "Aarhus": (10.613, 56.308), "Odense": (10.330, 55.476), "Sjælsmark": (12.415, 55.877),
            "Kastrup": (12.651, 55.614), "Bornholm": (14.759, 55.068)}
RAMPS = {"heat": ["#e6f0fd", "#9ec5f4", "#3987e5", "#1c5cab", "#0d366b"],
         "cool": ["#fdeee6", "#f6b391", "#eb6834", "#b8461b", "#6e2508"]}
PANELS = [("heat", "(a) Heating need [kWh/m² per year]"),
          ("cool", "(b) Heat to remove [kWh/m² per year]")]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
fig, axes = plt.subplots(1, 2, figsize=(11, 5.0), constrained_layout=True)
for ax, (key, title) in zip(axes, PANELS):
    v = res.loc[cells, key].values
    bounds = np.arange(math.floor(v.min()), math.ceil(v.max()) + 1e-9, 1.0)
    cmap = LinearSegmentedColormap.from_list(key, RAMPS[key])
    pc = PolyCollection(polys, array=v, cmap=cmap, norm=BoundaryNorm(bounds, cmap.N),
                        edgecolor="white", linewidth=0.3)
    ax.add_collection(pc)
    for n, (x, y) in STATIONS.items():
        ax.plot(x, y, "o", ms=3.5, mfc="white", mec="#222", mew=0.8)
        ax.annotate(n, (x, y), xytext=(4, 3), textcoords="offset points", fontsize=7, color="#222")
    ax.set_xlim(7.9, 15.5); ax.set_ylim(54.45, 57.95)
    ax.set_aspect(1 / math.cos(math.radians(56)))
    ax.set_title(title, loc="left", fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    cb = fig.colorbar(pc, ax=ax, orientation="horizontal", shrink=0.75, pad=0.02, ticks=bounds)
    cb.outline.set_visible(False)
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "regional-teq.png", dpi=200)
fig.savefig(OUT / "regional-teq.svg")
