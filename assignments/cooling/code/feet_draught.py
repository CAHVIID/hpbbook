"""Peak draught rate at feet level from an exported air-velocity field.

Use with the field exported from the IDA ICE flow element model (or any CFD tool) for the
hour you want to check, typically the hour with the largest airflow through the hatch and a
large indoor-outdoor temperature difference.

Input: one text/CSV file per case with one row per point. The columns are set in COLUMNS:
  x, y, z (m)                     point coordinates, z = height above the floor
  T (degC)                        air temperature
  speed (m/s), or u, v, w (m/s)   mean air speed or its components
  Tu (%) or k (m2/s2), optional   turbulence intensity or turbulent kinetic energy

Method
  1. Take the points at feet level, z = FEET_HEIGHT (nearest layer in the file), inside the
     occupied zone (WALL_DISTANCE from the walls).
  2. ISO 7730 draught rate at each point:
     DR = (34 - t_a)(v - 0.05)^0.62 (0.37 v Tu + 3.14), v >= 0.05 m/s, 0 <= DR <= 100 %.
     No "feet factor" is applied: the ISO model is conservative at the feet.
  3. ASHRAE 55-2020 ankle draught (Liu et al. 2017): PPD_AD = 100 e^z / (1 + e^z),
     z = -2.58 + 3.05 v - 1.06 TS, with TS the whole-body sensation. TS is taken as PMV
     (ISO 7730) at the occupied-zone mean temperature and speed, unless TS is set.
     Limit 20 %, equivalent to v < 0.35 TS + 0.39 m/s.

Output: peak DR and PPD_AD with their location, the share of the feet-level area above 20 %,
a table for all cases (feet_draught_summary.csv) and a DR map per case (PNG).

Requirements: pip install numpy pandas matplotlib pythermalcomfort
"""
import os
import sys

import numpy as np
import pandas as pd

# =============================================================================================
# INPUT: edit this section
# =============================================================================================

# Field files: name of the case -> file path
CASES = {
    "night, peak airflow": r"field_night.csv",
}

# Column names in the file (set to None if the column is not there)
COLUMNS = dict(x="x", y="y", z="z", T="T", speed=None, u="u", v="v", w="w", Tu=None, k=None)
SEPARATOR = r"[,;\s]+"            # comma, semicolon or whitespace

FEET_HEIGHT = 0.1                 # m above floor
WALL_DISTANCE = 0.6               # m, occupied zone starts this far from the walls (EN 16798-1 uses 0.5-1.0 m)
OCCUPIED_TOP = 1.8                # m, top of the occupied zone (for the mean TS)
TU_DEFAULT = 40.0                 # %, used when the file has neither Tu nor k
TS = None                         # whole-body sensation; None = PMV at the occupied-zone mean
MET, CLO, RH = 1.2, 0.5, 50.0     # for PMV
LIMIT = 20.0                      # %, DR and PPD_AD limit (category II / ASHRAE 55)

# =============================================================================================
# Calculation: no need to edit below
# =============================================================================================


def read_field(path):
    df = pd.read_csv(path, sep=SEPARATOR, engine="python", comment="#")
    c = COLUMNS
    out = pd.DataFrame({k: df[c[k]].astype(float) for k in ("x", "y", "z", "T")})
    if c["speed"]:
        out["V"] = df[c["speed"]].astype(float)
    else:
        out["V"] = np.sqrt(sum(df[c[k]].astype(float) ** 2 for k in ("u", "v", "w") if c[k]))
    if c["Tu"]:
        out["Tu"] = df[c["Tu"]].astype(float)
    elif c["k"]:  # isotropic turbulence: u' = sqrt(2k/3)
        out["Tu"] = 100 * np.sqrt(2 * df[c["k"]].astype(float) / 3) / np.maximum(out["V"], 0.05)
    else:
        out["Tu"] = TU_DEFAULT
    out["Tu"] = out["Tu"].clip(0, 70)  # ISO 7730 range is 10-60 %
    return out


def draught_rate(ta, v, tu):
    v = np.maximum(v, 0.05)
    return np.clip((34 - ta) * (v - 0.05) ** 0.62 * (0.37 * v * tu + 3.14), 0, 100)


def ankle_ppd(v, ts):
    z = -2.58 + 3.05 * v - 1.06 * ts
    return 100 * np.exp(z) / (1 + np.exp(z))


def whole_body_ts(f):
    if TS is not None:
        return TS
    from pythermalcomfort.models import pmv_ppd_iso
    oz = f[(f["z"] <= OCCUPIED_TOP)]
    ta, v = oz["T"].mean(), oz["V"].mean()
    return float(pmv_ppd_iso(tdb=ta, tr=ta, vr=v, rh=RH, met=MET, clo=CLO, limit_inputs=False).pmv)


def feet_level(f):
    z = f["z"].unique()
    zf = z[np.argmin(np.abs(z - FEET_HEIGHT))]
    x0, x1, y0, y1 = f["x"].min(), f["x"].max(), f["y"].min(), f["y"].max()
    s = f[np.isclose(f["z"], zf)]
    inside = s["x"].between(x0 + WALL_DISTANCE, x1 - WALL_DISTANCE)
    if y1 - y0 > 2 * WALL_DISTANCE:   # 2D fields have a single y
        inside &= s["y"].between(y0 + WALL_DISTANCE, y1 - WALL_DISTANCE)
    return s[inside].copy(), zf


def analyse(name, path):
    f = read_field(path)
    ts = whole_body_ts(f)
    s, zf = feet_level(f)
    s["DR"] = draught_rate(s["T"], s["V"], s["Tu"])
    s["PPD_AD"] = ankle_ppd(s["V"], ts)
    i, j = s["DR"].idxmax(), s["PPD_AD"].idxmax()
    res = dict(case=name, feet_height_m=zf, TS=round(ts, 2), points=len(s),
               v_max=round(s["V"].max(), 2), T_at_v_max=round(s.loc[s["V"].idxmax(), "T"], 1),
               DR_peak=round(s.loc[i, "DR"], 1), DR_peak_xy=(round(s.loc[i, "x"], 2), round(s.loc[i, "y"], 2)),
               DR_area_above_limit_pct=round(100 * (s["DR"] > LIMIT).mean(), 1),
               PPD_AD_peak=round(s.loc[j, "PPD_AD"], 1),
               PPD_AD_area_above_limit_pct=round(100 * (s["PPD_AD"] > LIMIT).mean(), 1),
               v_ankle_limit=round(0.35 * ts + 0.39, 2))
    plot_map(name, s)
    return res


def plot_map(name, s):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, 4.5))
    if s["y"].nunique() > 1:
        sc = ax.scatter(s["x"], s["y"], c=s["DR"], cmap="viridis_r", vmin=0, vmax=40, s=25, marker="s")
        ax.set_ylabel("y (m)")
        ax.set_aspect("equal")
    else:  # 2D section: DR along the floor
        ax.plot(s["x"], s["DR"], color="#1f6f8b")
        ax.axhline(LIMIT, color="0.4", ls="--", lw=1)
        ax.set_ylabel("DR at feet (%)")
        sc = None
    ax.set_xlabel("x, distance from the opening wall (m)")
    ax.set_title(f"{name}: draught rate at feet level")
    if sc is not None:
        fig.colorbar(sc, label="DR (%)")
    fig.tight_layout()
    fig.savefig(f"feet_draught_{name.replace(' ', '_').replace(',', '')}.png", dpi=150)
    plt.close(fig)


def main():
    cases = {os.path.splitext(os.path.basename(p))[0]: p for p in sys.argv[1:]} or CASES
    rows = [analyse(n, p) for n, p in cases.items()]
    t = pd.DataFrame(rows)
    t.to_csv("feet_draught_summary.csv", index=False)
    print(t.set_index("case").T.to_string())


if __name__ == "__main__":
    main()
