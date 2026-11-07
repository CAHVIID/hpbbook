"""Estimated night-time urban heat island on warm summer nights across Denmark.

The urban areas are Natural Earth's 10 m urban areas (MODIS land cover, about 2002). Measured
intensities exist only for the four largest cities (Sørup et al. 2026, 3 % warmest days, night):
Copenhagen 1.5-2 K, Aarhus, Odense and Aalborg about 1 K. Following Oke (1973), who related the
heat island to the logarithm of city size, the other towns are given

  dT = a + b * log10(A_urban / km2), clipped at 0,

with a and b fitted to the four cities. The values for the smaller towns are therefore an
extrapolation, not measurements.

Usage: python d1_uhi_map.py <folder with ne_10m_urban_areas.geojson, ne_10m_admin_0_countries.geojson
       and ne_10m_populated_places_simple.geojson>
The files are from https://github.com/nvkelso/natural-earth-vector (public domain).
"""
import json, math, sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path as MPath
from matplotlib.collections import PolyCollection
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm

NE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "natural-earth"
OUT = Path(__file__).resolve().parent.parent / "figures" / "d1"
# Sørup et al. (2026): mean night-time intensity on the 3 % warmest days (K)
MEASURED = {"København": 1.75, "Århus": 1.0, "Odense": 1.0, "Aalborg": 1.0}
NAMES = {"København": "Copenhagen", "Århus": "Aarhus"}
CITY_RADIUS = {"København": 0.35, "Århus": 0.15, "Odense": 0.15, "Aalborg": 0.15}  # degrees


def rings(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    return [np.array(p[0]) for p in polys]


def load(name):
    return json.loads((NE / f"{name}.geojson").read_text(encoding="utf-8"))["features"]


countries = {f["properties"]["ADMIN"]: rings(f["geometry"]) for f in load("ne_10m_admin_0_countries")
             if f["properties"]["ADMIN"] in ("Denmark", "Sweden", "Germany")}
dk_paths = [MPath(r) for r in countries["Denmark"]]
places = {f["properties"]["name"]: (f["properties"]["longitude"], f["properties"]["latitude"])
          for f in load("ne_10m_populated_places_simple") if f["properties"]["adm0name"] == "Denmark"}

# Danish urban polygons: the ones whose mean vertex lies in Denmark
urban = []
for f in load("ne_10m_urban_areas"):
    for r in rings(f["geometry"]):
        c = r.mean(axis=0)
        if 7.5 < c[0] < 15.5 and 54.4 < c[1] < 58 and any(p.contains_point(c) for p in dk_paths):
            urban.append({"ring": r, "c": c, "area": f["properties"]["area_sqkm"]})

# Group the polygons of each measured city and fit dT = a + b log10(A)
for u in urban:
    u["city"] = next((n for n in MEASURED if math.dist(u["c"], places[n]) < CITY_RADIUS[n]), None)
city_area = {n: sum(u["area"] for u in urban if u["city"] == n) for n in MEASURED}
x = np.log10([city_area[n] for n in MEASURED])
b, a = np.polyfit(x, [MEASURED[n] for n in MEASURED], 1)
for u in urban:
    u["dT"] = MEASURED[u["city"]] if u["city"] else max(0.0, a + b * math.log10(u["area"]))
print(f"fit: dT = {a:.2f} + {b:.2f} log10(A); {len(urban)} Danish urban polygons")
for n in MEASURED:
    print(f"  {n}: {city_area[n]:.0f} km2, {MEASURED[n]} K")
others = sorted((u for u in urban if not u["city"]), key=lambda u: -u["area"])
print("  largest other towns:", [(round(u["area"]), round(u["dT"], 2)) for u in others[:8]])

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
fig, (ax, bx) = plt.subplots(1, 2, figsize=(11, 5.0), gridspec_kw={"width_ratios": [1.9, 1]},
                             constrained_layout=True)
for name, col in (("Sweden", "#ecebe7"), ("Germany", "#ecebe7"), ("Denmark", "#dcdad3")):
    ax.add_collection(PolyCollection(countries[name], facecolor=col, edgecolor="#b9b6ad", linewidth=0.3))
bounds = [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
cmap = LinearSegmentedColormap.from_list("uhi", ["#fdeee6", "#f6b391", "#eb6834", "#b8461b", "#6e2508"])
pc = PolyCollection([u["ring"] for u in urban], array=np.array([u["dT"] for u in urban]), cmap=cmap,
                    norm=BoundaryNorm(bounds, cmap.N), edgecolor="#6e2508", linewidth=0.2)
ax.add_collection(pc)
for n in MEASURED:
    lon, lat = places[n]
    ax.annotate(f"{NAMES.get(n, n)}\n{'1.5–2' if n == 'København' else '≈1'} K (measured)", (lon, lat),
                xytext=(8, -2), textcoords="offset points", fontsize=7.5, color="#222")
ax.set_xlim(7.9, 15.4); ax.set_ylim(54.5, 57.9)
ax.set_aspect(1 / math.cos(math.radians(56)))
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title("(a) Night-time heat island on warm summer nights [K]", loc="left", fontsize=10)
cb = fig.colorbar(pc, ax=ax, orientation="horizontal", shrink=0.6, pad=0.02, ticks=bounds)
cb.outline.set_visible(False)

A = np.array([u["area"] for u in others])
bx.scatter(A, [u["dT"] for u in others], s=10, color="#eb6834", alpha=0.6, label="Other towns (estimate)")
bx.scatter([city_area[n] for n in MEASURED], [MEASURED[n] for n in MEASURED], s=40, color="#6e2508",
           zorder=3, label="Sørup et al. (2026)")
LABEL_OFFSET = {"København": (-30, 8), "Århus": (6, 6), "Odense": (6, -12), "Aalborg": (-18, 8)}
for n in MEASURED:
    bx.annotate(NAMES.get(n, n), (city_area[n], MEASURED[n]), xytext=LABEL_OFFSET[n],
                textcoords="offset points", fontsize=7.5)
xx = np.logspace(0.5, 3.1, 50)
bx.plot(xx, np.maximum(0, a + b * np.log10(xx)), color="#6e2508", lw=1,
        label=f"ΔT = {a:.2f} + {b:.2f}·log10(A)")
bx.set_xscale("log"); bx.set_ylim(0, 2.2)
bx.set_xlabel("Urban area A [km²]"); bx.set_ylabel("ΔT [K]")
bx.set_title("(b) Heat island and city size", loc="left", fontsize=10)
bx.legend(frameon=False, fontsize=7.5, loc="upper left")
bx.grid(alpha=0.3, lw=0.5)
for s in ("top", "right"):
    bx.spines[s].set_visible(False)
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "uhi-map.png", dpi=200)
fig.savefig(OUT / "uhi-map.svg")
