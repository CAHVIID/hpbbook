"""Ceiling fans in peak periods: thermal comfort, fan energy, cooling fan efficiency and cooling COP.

Replaces the old pmv_hourly_analysis.py from Assignment 4 (2025).

Input
  - TEMPERATURES.prn from IDA ICE for each zone (air and operative temperature, hourly).
    Save the IDA ICE model "unpacked" to get one folder per zone with the .prn files.
  - IAQ.prn for each zone (relative humidity). Optional: 50 % RH is used if missing.
  - The fan datasheet: diameter, and airflow and power at each speed.
  - The weather file (EPW) used in IDA ICE. Optional: needed for the adaptive comfort limit.

Method, for each occupied hour in each zone
  1. Mean radiant temperature from IDA ICE's operative temperature at still air:
     t_r = 2 * t_op - t_air.
  2. Fan air speed from the datasheet: S_F = 4 Q / (pi D^2), and the room-average speed
     for seated occupants from Raftery et al. (2019), S_O,avg (see the Ceiling fans chapter).
  3. The fan runs when the room is warm (PMV > PMV_ON at still air). It runs at the lowest
     speed that brings PMV down to PMV_TARGET, or at maximum speed if none does.
  4. Cooling effect CE from SET (ASHRAE 55, pythermalcomfort.cooling_effect), and PMV with
     the fan from the ASHRAE 55 elevated air speed method (pythermalcomfort.pmv_ppd_ashrae).
     PMV at elevated air speed from ISO 7730 underestimates the cooling, so it is not used.
  5. Equivalent operative temperature t_op - CE, compared with the EN 16798-1 adaptive
     category II upper limit.

Fan indicators
  - Cooling fan efficiency, CFE = CE / P_fan (degC per W), ASHRAE 216.
  - Cooling COP = Q_eq / P_fan. Q_eq is the cooling an air-based air-conditioner would have
    to deliver to supply the fan's airflow CE colder: Q_eq = q_fan * rho * cp * CE, with q_fan
    the fan airflow (m3/s). It is a "same comfort" yardstick, not heat removed from the room:
    the fan itself removes no heat.

Output
  - fan_results.xlsx: sheet "fan" (per speed) and sheet "zones" (per zone summary).
  - hourly_results/<zone>.csv: hourly values for your own plots.

Requirements: pip install pythermalcomfort pandas openpyxl
"""
import os

import numpy as np
import pandas as pd
from pythermalcomfort.models import cooling_effect, pmv_ppd_ashrae

# =============================================================================================
# INPUT: edit this section
# =============================================================================================

# Folder with the unpacked IDA ICE model (one sub-folder per zone)
MODEL_DIR = r"C:\path\to\row_house_assign_4_unpacked"

# Weather file used in IDA ICE (for the adaptive limit). Set to None to skip.
EPW_FILE = r"..\weather\5A_Copenhagen_HW_MostSevere_2054_clean.epw"

# Period to evaluate, as (month, day) from and to, inclusive. None = whole file.
PERIOD = ((7, 9), (8, 5))        # MostSevere 2054 heat wave, 9 July to 5 August

# Fan datasheet. One entry per speed: airflow (m3/h) and electric power (W).
# Example: Fanco Breeze AC 132 (Ceiling fans chapter, fan data table). Replace with your fan.
FAN = {
    "name": "Fanco Breeze AC 132",
    "diameter": 1.32,                # m
    "speeds": {                      # name: (airflow m3/h, power W)
        "low": (5625, 15.0),
        "high": (9030, 45.0),
    },
}

# Zones: folder name in MODEL_DIR, room width R (m), ceiling height C (m), occupied hours
# (list of clock hours 0-23).
BEDROOM = list(range(22, 24)) + list(range(0, 7))     # 22:00-07:00
LIVING = list(range(7, 22))                           # 07:00-22:00
ZONES = [
    # name,                       R,   C,   occupied   [example values: use your model]
    ("bedroom_1st_floor",         3.5, 2.5, BEDROOM),
    ("bedroom_2nd_floor",         3.5, 2.5, BEDROOM),
    ("dinning_room",              4.0, 2.5, LIVING),
    ("living_room_2nd_floor",     4.0, 2.5, LIVING),
    ("master_bedroom_2nd_floor2", 4.0, 2.5, BEDROOM),
]

# Occupant
MET = 1.2                         # met, seated quiet activity
CLO_WARM, CLO_COOL = 0.5, 0.7     # clo above / below CLO_SWITCH operative temperature
CLO_SWITCH = 24.0                 # degC
V_STILL = 0.1                     # m/s, air speed without fan
RH_DEFAULT = 50.0                 # %, used if IAQ.prn is missing

# Fan control
PMV_ON = 0.5                      # fan starts when PMV at still air exceeds this
PMV_TARGET = 0.5                  # lowest speed that reaches this PMV is chosen

# Reference condition for the fan table (ASHRAE 216 style comparison)
REF = dict(tdb=28.0, tr=28.0, rh=50.0, met=1.2, clo=0.5)

RHO, CP = 1.2, 1005.0             # air density (kg/m3) and specific heat (J/kgK)
OUT_FILE = "fan_results.xlsx"

# =============================================================================================
# Calculation: no need to edit below
# =============================================================================================

PMV_BINS = [-np.inf, -1.5, -1.0, -0.5, 0.5, 1.0, 1.5, np.inf]
PMV_LABELS = ["<-1.5", "-1.5..-1.0", "-1.0..-0.5", "-0.5..0.5", "0.5..1.0", "1.0..1.5", ">1.5"]


def read_prn(path, want):
    """Read an IDA ICE .prn file. `want` maps output name -> (keywords in header, fallback column)."""
    with open(path) as f:
        header = f.readline().lstrip("#").split()
    df = pd.read_csv(path, sep=r"\s+", skiprows=1, header=None)
    cols = [h.lower() for h in header] if len(header) == df.shape[1] else []
    out = pd.DataFrame({"time": df.iloc[:, 0].astype(float)})
    for name, (keys, fallback) in want.items():
        idx = next((i for i, c in enumerate(cols) if any(k in c for k in keys)), fallback)
        out[name] = df.iloc[:, idx].astype(float)
    # Keep one row per whole hour (IDA ICE may also write t = 0 and sub-hourly steps)
    out = out[np.isclose(out["time"] % 1, 0)].drop_duplicates("time")
    return out.set_index(out["time"].round().astype(int)).drop(columns="time")


def air_speed(q_m3h, D, R, C):
    """Fan air speed S_F and room-average speed for seated occupants S_O,avg (Raftery et al. 2019)."""
    s_f = 4 * q_m3h / 3600 / (np.pi * D**2)
    return s_f, s_f * (0.25 + 0.99 * D / R - 0.06 * C / D + 0.11 * D / 1.7 + 0.024)


def ce(tdb, tr, v, rh, clo):
    """Cooling effect (K), vectorised; zero at still air."""
    if np.all(np.asarray(v) <= V_STILL):
        return np.zeros(np.shape(tdb))
    return np.asarray(cooling_effect(tdb=tdb, tr=tr, vr=v, rh=rh, met=MET, clo=clo).ce, dtype=float)


def pmv(tdb, tr, v, rh, clo):
    """PMV with the ASHRAE 55 elevated air speed method (SET-based)."""
    r = pmv_ppd_ashrae(tdb=tdb, tr=tr, vr=v, rh=rh, met=MET, clo=clo, limit_inputs=False)
    return np.asarray(r.pmv, dtype=float)


def adaptive_upper_cat2(epw):
    """EN 16798-1 adaptive category II upper limit per hour of the year (degC)."""
    t = pd.read_csv(epw, skiprows=8, header=None)[6].to_numpy()
    daily = t[:8760].reshape(365, 24).mean(axis=1)
    trm = np.empty(365)
    trm[0] = daily[-7:].mean()                       # start-up from the last week of the year
    for d in range(1, 365):
        trm[d] = 0.2 * daily[d - 1] + 0.8 * trm[d - 1]
    limit = 0.33 * np.clip(trm, 10, 30) + 18.8 + 3   # outside 10-30 degC the model is not defined
    return np.repeat(limit, 24)                      # index 0 = hour ending 01:00 on 1 January


def period_hours(period):
    """Hour-of-year numbers (1..8760, IDA ICE time stamps) inside the period."""
    days = pd.date_range("2001-01-01", periods=8760, freq="h")  # non-leap year
    hours = np.arange(1, 8761)
    if period is None:
        return hours
    (m0, d0), (m1, d1) = period
    md = days.month * 100 + days.day
    return hours[(md >= m0 * 100 + d0) & (md <= m1 * 100 + d1)]


def q_eq(q_m3h, ce_k):
    """Equivalent cooling (W): the fan's airflow supplied CE colder."""
    return q_m3h / 3600 * RHO * CP * ce_k


def fan_table():
    """Air speed, CE and CFE per speed at the reference condition, in the first zone."""
    R, C = ZONES[0][1], ZONES[0][2]
    rows = []
    for name, (q, p) in FAN["speeds"].items():
        s_f, s_o = air_speed(q, FAN["diameter"], R, C)
        c = float(cooling_effect(vr=s_o, **REF).ce)
        rows.append(dict(speed=name, airflow_m3h=q, power_W=p, S_F=round(s_f, 2), S_O_avg=round(s_o, 2),
                         CE_K=round(c, 2), CFE_K_per_W=round(c / p, 3),
                         Q_eq_W=round(q_eq(q, c)), cooling_COP=round(q_eq(q, c) / p)))
    return pd.DataFrame(rows)


def run_zone(name, R, C, occ_hours, limit):
    folder = os.path.join(MODEL_DIR, name)
    d = read_prn(os.path.join(folder, "TEMPERATURES.prn"),
                 {"tdb": (["tair", "air"], 2), "top": (["top", "oper"], 3)})
    iaq = os.path.join(folder, "IAQ.prn")
    if os.path.exists(iaq):
        rh = read_prn(iaq, {"rh": (["relhum", "rh"], 3)})["rh"]
        d["rh"] = (rh * 100 if rh.max() <= 1.5 else rh).reindex(d.index)
    else:
        d["rh"] = RH_DEFAULT
    d = d.loc[d.index.intersection(period_hours(PERIOD))]

    d["tr"] = 2 * d["top"] - d["tdb"]
    d["clo"] = np.where(d["top"] > CLO_SWITCH, CLO_WARM, CLO_COOL)
    d["occupied"] = np.isin((d.index - 1) % 24, occ_hours)   # clock hour at the start of the hour
    d["pmv_still"] = pmv(d["tdb"], d["tr"], V_STILL, d["rh"], d["clo"])

    # Fan control: lowest speed that reaches PMV_TARGET
    d["speed"], d["v"], d["P_W"], d["q_fan_m3h"] = "off", V_STILL, 0.0, 0.0
    d["pmv_fan"], d["CE"] = d["pmv_still"], 0.0
    todo = d["occupied"] & (d["pmv_still"] > PMV_ON)
    for sp, (q, p) in FAN["speeds"].items():
        idx = d.index[todo]
        if len(idx) == 0:
            break
        v = air_speed(q, FAN["diameter"], R, C)[1]
        x = d.loc[idx]
        pm = pmv(x["tdb"], x["tr"], v, x["rh"], x["clo"])
        last = sp == list(FAN["speeds"])[-1]
        ok = idx[(pm <= PMV_TARGET) | last]
        d.loc[ok, ["speed", "v", "P_W", "q_fan_m3h"]] = sp, v, p, q
        d.loc[ok, "pmv_fan"] = pm[(pm <= PMV_TARGET) | last]
        todo.loc[ok] = False
    on = d["speed"] != "off"
    if on.any():
        x = d.loc[on]
        d.loc[on, "CE"] = ce(x["tdb"], x["tr"], x["v"], x["rh"], x["clo"])
    d["top_eq"] = d["top"] - d["CE"]
    d["Q_eq_W"] = q_eq(d["q_fan_m3h"], d["CE"])

    occ = d[d["occupied"]]
    e_fan = d["P_W"].sum() / 1000
    e_eq = d["Q_eq_W"].sum() / 1000
    s = dict(zone=name, occupied_h=len(occ), fan_h=int(on.sum()))
    for sp in FAN["speeds"]:
        s[f"fan_h_{sp}"] = int((d["speed"] == sp).sum())
    s.update(fan_kWh=round(e_fan, 2),
             mean_CE_K=round(d.loc[on, "CE"].mean(), 2) if on.any() else 0.0,
             CFE_K_per_W=round((d.loc[on, "CE"] / d.loc[on, "P_W"]).mean(), 3) if on.any() else np.nan,
             Q_eq_kWh=round(e_eq, 1),
             cooling_COP=round(e_eq / e_fan) if e_fan > 0 else np.nan,
             max_top=round(occ["top"].max(), 1), max_top_eq=round(occ["top_eq"].max(), 1))
    if limit is not None:
        lim = limit[d.index - 1]
        d["adaptive_cat2_upper"] = lim
        s["h_above_cat2_no_fan"] = int((d["occupied"] & (d["top"] > lim)).sum())
        s["h_above_cat2_fan"] = int((d["occupied"] & (d["top_eq"] > lim)).sum())
    for tag, col in (("no_fan", "pmv_still"), ("fan", "pmv_fan")):
        counts = pd.cut(occ[col], PMV_BINS, labels=PMV_LABELS).value_counts().reindex(PMV_LABELS)
        for lab, n in counts.items():
            s[f"PMV {lab} ({tag})"] = int(n)
    return s, d


def main():
    pd.set_option("display.width", 160)
    limit = adaptive_upper_cat2(EPW_FILE) if EPW_FILE else None
    fan = fan_table()
    print(f"\nFan: {FAN['name']}, D = {FAN['diameter']} m, reference {REF}")
    print(fan.to_string(index=False))

    summaries = []
    os.makedirs("hourly_results", exist_ok=True)
    for name, R, C, occ in ZONES:
        print(f"Zone {name} ...")
        s, d = run_zone(name, R, C, occ, limit)
        summaries.append(s)
        d.round(3).to_csv(os.path.join("hourly_results", f"{name}.csv"), index_label="hour_of_year")
    zones = pd.DataFrame(summaries)
    total = zones.select_dtypes("number").sum()
    total["cooling_COP"] = round(total["Q_eq_kWh"] / total["fan_kWh"]) if total["fan_kWh"] else np.nan
    for col in ("mean_CE_K", "CFE_K_per_W", "max_top", "max_top_eq"):
        total[col] = np.nan
    zones = pd.concat([zones, total.to_frame().T.assign(zone="TOTAL")], ignore_index=True)

    with pd.ExcelWriter(OUT_FILE) as xl:
        fan.to_excel(xl, sheet_name="fan", index=False)
        zones.T.to_excel(xl, sheet_name="zones", header=False)
    print("\n", zones.set_index("zone").T.to_string())
    print(f"\nWritten {OUT_FILE} and hourly_results/*.csv")


if __name__ == "__main__":
    main()
