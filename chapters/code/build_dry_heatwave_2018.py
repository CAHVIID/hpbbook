"""DRY 2011–2023 with a real heat wave: July and August replaced by DMI measurements of summer 2018, Sjælsmark (06188).

Usage: python build_dry_heatwave_2018.py [--fetch]
--fetch downloads the hourly observations from the DMI open data API (no key needed) and caches them in
weather/dmi_06188_2018_jul_aug.csv; without it the cached CSV is used.

DMI gives global radiation only. Direct normal and diffuse radiation are split from it with the Erbs et al. (1982)
model, and illuminance is global/direct/diffuse irradiance times the luminous efficacies of July–August in the
original DRY file. Fields DMI does not measure (sky IR, visibility, precipitable water, ...) are kept from the DRY.
"""
import sys, json, urllib.request
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent / "weather"
BASE = HERE / "DRY_2011-2023_epw-fil.epw"
OUT = HERE / "DRY_2011-2023_heatwave2018.epw"
CACHE = HERE / "dmi_06188_2018_jul_aug.csv"
LAT, LON = 55.8764, 12.4121
PARAMS = {'T': 'temp_mean_past1h', 'RH': 'humidity_past1h', 'p': 'pressure', 'GHI': 'radia_glob_past1h',
          'WS': 'wind_speed_past1h', 'WD': 'wind_dir_past1h', 'CC': 'cloud_cover', 'P': 'precip_past1h'}
# DRY hour h of a day is the hour ending at h:00 UTC (best match of the mean daily GHI profile with DMI's UTC data)
HOURS = pd.date_range('2018-07-01 01:00', '2018-09-01 00:00', freq='h', tz='UTC')

def fetch():
    url = "https://opendataapi.dmi.dk/v2/metObs/collections/observation/items?stationId=06188&parameterId={}" \
          "&datetime=2018-06-30T00:00:00Z/2018-09-01T02:00:00Z&limit=300000"
    cols = {}
    for k, p in PARAMS.items():
        f = json.load(urllib.request.urlopen(url.format(p), timeout=300))['features']
        s = pd.Series({pd.Timestamp(x['properties']['observed']): x['properties']['value'] for x in f}).sort_index()
        cols[k] = s.reindex(HOURS)
    d = pd.DataFrame(cols); d.index.name = 'utc_hour_ending'
    d.to_csv(CACHE)
    return d

def sun(t):
    """Cosine of the zenith angle and extraterrestrial normal irradiance at UTC times t."""
    doy = t.dayofyear.values; hr = t.hour.values + t.minute.values / 60
    g = 2 * np.pi / 365 * (doy - 1 + (hr - 12) / 24)
    decl = (0.006918 - 0.399912*np.cos(g) + 0.070257*np.sin(g) - 0.006758*np.cos(2*g)
            + 0.000907*np.sin(2*g) - 0.002697*np.cos(3*g) + 0.00148*np.sin(3*g))
    eot = 229.18 * (0.000075 + 0.001868*np.cos(g) - 0.032077*np.sin(g) - 0.014615*np.cos(2*g) - 0.040849*np.sin(2*g))
    ha = np.radians(15 * (hr + (eot + 4*LON) / 60 - 12))
    lat = np.radians(LAT)
    cz = np.sin(lat)*np.sin(decl) + np.cos(lat)*np.cos(decl)*np.cos(ha)
    return cz, 1367 * (1 + 0.033 * np.cos(2 * np.pi * doy / 365))

def erbs(ghi, cz, i0):
    kt = np.where(cz > 0.05, ghi / (i0 * np.clip(cz, 0.05, None)), 1.0).clip(0, 1)
    kd = np.where(kt <= 0.22, 1 - 0.09*kt,
         np.where(kt <= 0.80, 0.9511 - 0.1604*kt + 4.388*kt**2 - 16.638*kt**3 + 12.336*kt**4, 0.165))
    dhi = np.where(cz > 0.05, kd * ghi, ghi)
    dni = np.where(cz > 0.05, (ghi - dhi) / np.clip(cz, 0.05, None), 0).clip(0, 1100)
    return dni, dhi

def main():
    d = fetch() if '--fetch' in sys.argv else pd.read_csv(CACHE, index_col=0, parse_dates=True)
    d = d.interpolate(limit=3)  # cloud cover misses 8 single hours
    cz, i0 = sun(d.index - pd.Timedelta(minutes=30))  # sun at mid-hour
    dni, dhi = erbs(d.GHI.values, cz, i0)
    T, RH = d['T'].values, d['RH'].clip(1, 100).values
    a = np.log(RH / 100) + 17.62 * T / (243.12 + T)
    td = 243.12 * a / (17.62 - a)  # dew point, Magnus (WMO)

    head = BASE.read_text().splitlines()[:8]
    rows = [r.split(',') for r in BASE.read_text().splitlines()[8:]]
    summer = [i for i, r in enumerate(rows) if r[1] in ('7', '07', '8', '08')]
    assert len(summer) == len(d) == 1488
    o = np.array([[float(rows[i][c]) for c in (13, 14, 15, 16, 17, 18)] for i in summer]).sum(0)
    eff = o[3:] / o[:3]  # lm/W for global, direct, diffuse in the original July-August
    for k, i in enumerate(summer):
        r = rows[i]
        r[0] = '2018'
        r[6], r[7], r[8] = f'{T[k]:.1f}', f'{td[k]:.1f}', f'{RH[k]:.0f}'
        r[9] = f'{d.p.iloc[k] * 100:.0f}'
        r[10] = f'{max(i0[k] * cz[k], 0):.1f}'; r[11] = f'{i0[k] if cz[k] > 0 else 0:.1f}'
        r[13], r[14], r[15] = f'{d.GHI.iloc[k]:.0f}', f'{dni[k]:.1f}', f'{dhi[k]:.1f}'
        r[16], r[17], r[18] = (f'{d.GHI.iloc[k] * eff[0]:.0f}', f'{dni[k] * eff[1]:.0f}', f'{dhi[k] * eff[2]:.0f}')
        r[20], r[21] = f'{d.WD.iloc[k]:.0f}', f'{d.WS.iloc[k]:.1f}'
        cc = d.CC.iloc[k]
        r[22] = f'{10 if cc > 100 else round(cc / 10):.0f}'  # DMI %, 112 = sky obscured; EPW tenths
        r[33] = f'{d.P.iloc[k]:.1f}'
    # spread the jumps on 30 Jun/1 Jul and 31 Aug/1 Sep over 13 hours (6 on each side), as at DRY month seams
    n = 6
    for i in (summer[0], summer[-1] + 1):
        for c, fmt in ((6, '{:.1f}'), (7, '{:.1f}'), (8, '{:.0f}')):
            x = [float(rows[j][c]) for j in range(i - n, i + n)]
            jump = x[n] - x[n - 1]
            for k in range(-n, n):
                f = jump * (k + n + 1) / (2*n + 1) if k < 0 else -jump * (n - k) / (2*n + 1)
                rows[i + k][c] = fmt.format(min(x[k + n] + f, 100) if c == 8 else x[k + n] + f)
    head[5] +=' -- July and August replaced by DMI 06188 Sjaelsmark observations 2018 (DNI and DHI from GHI with Erbs)'
    OUT.write_text('\n'.join(head + [','.join(r) for r in rows]) + '\n')
    print(OUT, 'efficacies', eff.round(1))

if __name__ == '__main__':
    main()
