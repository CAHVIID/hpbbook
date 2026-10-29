"""Ceiling fans in an IDA ICE model: SET, cooling effect, fan energy and cooling fan efficiency.

Input
  - TEMPERATURES.prn from IDA ICE for each zone (hourly air and operative temperature).
    Save the IDA ICE model "unpacked" to get one folder per zone with its .prn files.
  - IAQ.prn for each zone (relative humidity). Optional: RH_DEFAULT is used if it is missing.
  - The fan datasheet: diameter, and airflow and power at each speed.
  - The weather file (EPW) used in IDA ICE. Optional: needed for the adaptive comfort limit.

Method, for each hour in each zone
  1. Mean radiant temperature from the IDA ICE operative temperature, which is the mean of
     air and mean radiant temperature at still air: t_r = 2 t_op - t_air. It is a property of
     the surfaces, so it does not change when the fan runs.
  2. Air speed from the fan datasheet: S_F = 4 Q / (pi D^2), and the room-average speed for
     seated occupants S_O,avg from Raftery et al. (2019), equation eq-so-avg in chapter D6.
  3. In occupied hours the fan runs when PMV at still air is above PMV_ON. It runs at the
     lowest speed that brings PMV down to PMV_TARGET, or at maximum speed if none does.
     Outside occupied hours and in cool hours the fan is off and uses no power.
  4. SET at still air and with the fan (ASHRAE 55 two-node model), the cooling effect CE
     (pythermalcomfort.cooling_effect) and PMV with the fan by the ASHRAE 55 elevated air
     speed method. ISO 7730 PMV at elevated air speed underestimates the cooling, so it is
     not used.
  5. Equivalent operative temperature t_op - CE, compared with the EN 16798-1 adaptive
     category II upper limit.

Fan indicators
  - Cooling fan efficiency CFE = CE / P_fan (degC per W), ASHRAE 216: in the fan table at
    the reference condition, and as the mean over the hours the fan runs in each zone.

Output
  - fan_results.xlsx: sheet "fan" (one row per speed) and sheet "zones" (one column per zone).
  - hourly_results/<zone>.csv: hourly values for your own plots.

Requirements: pip install pythermalcomfort pandas openpyxl
Run: python fan_comfort.py
"""
import os

import numpy as np
import pandas as pd
from pythermalcomfort.models import cooling_effect, pmv_ppd_ashrae, set_tmp

# =============================================================================================
# INPUT: edit this section
# =============================================================================================

# Folder with the unpacked IDA ICE model (one sub-folder per zone)
MODEL_DIR = r"C:\path\to\row_house_unpacked"

# Columns in the .prn files, counted from 0 (column 0 is the time in hours).
# Open one TEMPERATURES.prn and one IAQ.prn in a text editor and check the header line.
TEMP_COLS = {"tdb": 1, "top": 2}   # mean air temperature, operative temperature (degC)
IAQ_COLS = {"rh": 2}               # relative humidity (% or fraction, both are accepted)

# Weather file used in IDA ICE (for the adaptive limit). Set to None to skip.
EPW_FILE = None

# Period to evaluate, as ((month, day), (month, day)), inclusive. None = whole file.
PERIOD = ((6, 1), (8, 31))

# Fan datasheet. One entry per speed, slowest first: airflow (m3/h) and electric power (W).
# Example: Fanco Breeze AC 132 (chapter D6, fan data table). Replace with your fan.
FAN = {
    "name": "Fanco Breeze AC 132",
    "diameter": 1.32,                # m
    "speeds": {                      # name: (airflow m3/h, power W)
        "low": (5625, 15.0),
        "high": (9030, 45.0),
    },
}

# Zones: folder name in MODEL_DIR, room width R (m), ceiling height C (m), occupied hours
# (clock hours 0-23 at the start of each hour).
BEDROOM = list(range(22, 24)) + list(range(0, 7))     # 22:00-07:00
LIVING = list(range(7, 22))                           # 07:00-22:00
ZONES = [
    # folder name,    R,   C,   occupied
    ("bedroom",       3.5, 2.5, BEDROOM),
    ("living_room",   4.5, 2.7, LIVING),
]

# Occupant
MET = 1.2                         # met, seated quiet activity
CLO_WARM, CLO_COOL = 0.5, 0.7     # clo above / below CLO_SWITCH operative temperature
CLO_SWITCH = 24.0                 # degC
V_STILL = 0.1                     # m/s, air speed without fan
RH_DEFAULT = 50.0                 # %, used if IAQ.prn is missing

# Fan control
PMV_ON = 0.5                      # the fan starts when PMV at still air is above this
PMV_TARGET = 0.5                  # the lowest speed that reaches this PMV is chosen

# Reference condition for the fan table (as in chapter D6)
REF = dict(tdb=28.0, tr=28.0, rh=50.0, met=1.2, clo=0.5)

OUT_FILE = "fan_results.xlsx"

# =============================================================================================
# Calculation: no need to edit below
# =============================================================================================

PMV_BINS = [-np.inf, -0.5, 0.5, 1.0, 1.5, np.inf]
PMV_LABELS = ["< -0.5", "-0.5..0.5", "0.5..1.0", "1.0..1.5", "> 1.5"]


def read_prn(path, cols):
    """Read an IDA ICE .prn file. Lines that do not start with a number (headers) are skipped.

    Returns one row per whole hour, indexed by the hour of the year (1 = 00:00-01:00, 1 January)."""
    rows = []
    with open(path) as f:
        for line in f:
            parts = line.split()
            try:
                rows.append([float(p) for p in parts])
            except ValueError:
                continue                     # header or comment line
    df = pd.DataFrame(rows)
    out = pd.DataFrame({"time": df[0]})
    for name, i in cols.items():
        out[name] = df[i]
    # IDA ICE may write t = 0 and extra time steps: keep one value per whole hour
    out = out[np.isclose(out["time"] % 1, 0) & (out["time"] > 0)].drop_duplicates("time", keep="last")
    return out.set_index(out["time"].round().astype(int)).drop(columns="time")


def air_speed(q_m3h, D, R, C):
    """Fan air speed S_F and room-average speed for seated occupants S_O,avg (Raftery et al. 2019)."""
    s_f = 4 * q_m3h / 3600 / (np.pi * D**2)
    return s_f, s_f * (0.25 + 0.99 * D / R - 0.06 * C / D + 0.11 * D / 1.7 + 0.024)


def arr(x):
    return np.asarray(x, dtype=float)


def set_temp(tdb, tr, v, rh, clo):
    """Standard Effective Temperature (degC), ASHRAE 55 two-node model, as used for the cooling effect."""
    return arr(set_tmp(tdb=tdb, tr=tr, v=v, rh=rh, met=MET, clo=clo,
                       calculate_ce=True, limit_inputs=False, round_output=False).set)


def ce(tdb, tr, v, rh, clo):
    """Cooling effect (K) of air speed v relative to still air."""
    return arr(cooling_effect(tdb=tdb, tr=tr, vr=v, rh=rh, met=MET, clo=clo).ce)


def pmv(tdb, tr, v, rh, clo):
    """PMV with the ASHRAE 55 elevated air speed method (SET-based)."""
    return arr(pmv_ppd_ashrae(tdb=tdb, tr=tr, vr=v, rh=rh, met=MET, clo=clo, limit_inputs=False,
                              round_output=False).pmv)


def adaptive_upper_cat2(epw):
    """EN 16798-1 adaptive category II upper limit for each hour of the year (degC)."""
    t = pd.read_csv(epw, skiprows=8, header=None)[6].to_numpy()
    daily = t[:8760].reshape(365, 24).mean(axis=1)
    trm = np.empty(365)
    trm[0] = daily[-7:].mean()                       # start-up from the last week of the year
    for d in range(1, 365):
        trm[d] = 0.2 * daily[d - 1] + 0.8 * trm[d - 1]
    limit = 0.33 * np.clip(trm, 10, 30) + 18.8 + 3   # the model is defined for 10-30 degC
    return np.repeat(limit, 24)                      # index 0 = hour ending 01:00 on 1 January


def period_hours(period):
    """Hour-of-year numbers (1..8760, IDA ICE time stamps) inside the period."""
    start = pd.date_range("2001-01-01", periods=8760, freq="h")  # non-leap year
    hours = np.arange(1, 8761)
    if period is None:
        return hours
    (m0, d0), (m1, d1) = period
    md = start.month * 100 + start.day
    return hours[(md >= m0 * 100 + d0) & (md <= m1 * 100 + d1)]


def fan_table(R, C):
    """Air speed, cooling effect and CFE for each speed at the reference condition."""
    rows = []
    for name, (q, p) in FAN["speeds"].items():
        s_f, s_o = air_speed(q, FAN["diameter"], R, C)
        c = float(cooling_effect(vr=s_o, **REF).ce)
        rows.append(dict(speed=name, airflow_m3h=q, power_W=p, S_F=round(s_f, 2), S_O_avg=round(s_o, 2),
                         CE_K=round(c, 2), CFE_K_per_W=round(c / p, 3)))
    return pd.DataFrame(rows)


def run_zone(name, R, C, occ_hours, limit):
    folder = os.path.join(MODEL_DIR, name)
    d = read_prn(os.path.join(folder, "TEMPERATURES.prn"), TEMP_COLS)
    iaq = os.path.join(folder, "IAQ.prn")
    if os.path.exists(iaq):
        rh = read_prn(iaq, IAQ_COLS)["rh"]
        d["rh"] = (rh * 100 if rh.max() <= 1.5 else rh).reindex(d.index).fillna(RH_DEFAULT)
    else:
        d["rh"] = RH_DEFAULT
    d = d.loc[d.index.intersection(period_hours(PERIOD))].copy()
    if d.empty:
        raise ValueError(f"{name}: no hours inside PERIOD, check the .prn file and PERIOD")

    d["tr"] = 2 * d["top"] - d["tdb"]
    d["clo"] = np.where(d["top"] > CLO_SWITCH, CLO_WARM, CLO_COOL)
    d["occupied"] = np.isin((d.index - 1) % 24, occ_hours)
    d["SET_still"] = set_temp(d["tdb"], d["tr"], V_STILL, d["rh"], d["clo"])
    d["pmv_still"] = pmv(d["tdb"], d["tr"], V_STILL, d["rh"], d["clo"])

    # Fan control: in occupied, warm hours, the lowest speed that reaches PMV_TARGET
    d["speed"], d["v"], d["P_W"] = "off", V_STILL, 0.0
    d["pmv_fan"], d["SET_fan"], d["CE"] = d["pmv_still"], d["SET_still"], 0.0
    todo = (d["occupied"] & (d["pmv_still"] > PMV_ON)).to_numpy().copy()
    speeds = list(FAN["speeds"].items())
    for k, (sp, (q, p)) in enumerate(speeds):
        idx = d.index[todo]
        if len(idx) == 0:
            break
        v = air_speed(q, FAN["diameter"], R, C)[1]
        x = d.loc[idx]
        pm = pmv(x["tdb"], x["tr"], v, x["rh"], x["clo"])
        take = (pm <= PMV_TARGET) | (k == len(speeds) - 1)
        ok = idx[take]
        d.loc[ok, ["speed", "v", "P_W"]] = sp, v, p
        d.loc[ok, "pmv_fan"] = pm[take]
        todo[d.index.isin(ok)] = False
    on = (d["speed"] != "off").to_numpy()
    if on.any():
        x = d.loc[on]
        d.loc[on, "CE"] = ce(x["tdb"], x["tr"], x["v"], x["rh"], x["clo"])
        d.loc[on, "SET_fan"] = set_temp(x["tdb"], x["tr"], x["v"], x["rh"], x["clo"])
    d["top_eq"] = d["top"] - d["CE"]
    d["CFE"] = np.where(on, d["CE"] / d["P_W"].where(d["P_W"] > 0), np.nan)

    occ = d[d["occupied"]]
    s = dict(zone=name, hours=len(d), occupied_h=len(occ), fan_h=int(on.sum()))
    for sp in FAN["speeds"]:
        s[f"fan_h_{sp}"] = int((d["speed"] == sp).sum())
    s.update(fan_kWh=round(d["P_W"].sum() / 1000, 2),
             mean_CE_K=round(d.loc[on, "CE"].mean(), 2) if on.any() else 0.0,
             mean_CFE_K_per_W=round(d.loc[on, "CFE"].mean(), 3) if on.any() else np.nan,
             max_SET_still=round(occ["SET_still"].max(), 1), max_SET_fan=round(occ["SET_fan"].max(), 1),
             max_top=round(occ["top"].max(), 1), max_top_eq=round(occ["top_eq"].max(), 1))
    if limit is not None:
        lim = limit[d.index - 1]
        d["adaptive_cat2_upper"] = lim
        s["h_above_cat2_no_fan"] = int((d["occupied"] & (d["top"] > lim)).sum())
        s["h_above_cat2_fan"] = int((d["occupied"] & (d["top_eq"] > lim)).sum())
    for tag, col in (("no fan", "pmv_still"), ("fan", "pmv_fan")):
        counts = pd.cut(occ[col], PMV_BINS, labels=PMV_LABELS).value_counts().reindex(PMV_LABELS)
        for lab, n in counts.items():
            s[f"PMV {lab} h ({tag})"] = int(n)
    return s, d


def main():
    pd.set_option("display.width", 160)
    limit = adaptive_upper_cat2(EPW_FILE) if EPW_FILE else None
    fan = fan_table(ZONES[0][1], ZONES[0][2])
    print(f"\nFan: {FAN['name']}, D = {FAN['diameter']} m, room {ZONES[0][0]}, reference {REF}")
    print(fan.to_string(index=False))

    summaries = []
    os.makedirs("hourly_results", exist_ok=True)
    for name, R, C, occ in ZONES:
        print(f"Zone {name} ...")
        s, d = run_zone(name, R, C, occ, limit)
        summaries.append(s)
        d.round(3).to_csv(os.path.join("hourly_results", f"{name}.csv"), index_label="hour_of_year")
    zones = pd.DataFrame(summaries).set_index("zone").T

    with pd.ExcelWriter(OUT_FILE) as xl:
        fan.to_excel(xl, sheet_name="fan", index=False)
        zones.to_excel(xl, sheet_name="zones")
    print("\n", zones.to_string())
    print(f"\nWritten {OUT_FILE} and hourly_results/*.csv")


if __name__ == "__main__":
    main()
