"""Compare the DRY 2011–2023 file with summer 2018 spliced in against the Annex 80 Copenhagen files.

Same indicators as tab-annex80-summary (annual) and tab-heat-waves (hot days, tropical nights), plus summer
(June–August) percentiles and degree-hours. Writes figures/d1/heatwave-2018-compare.* and prints the tables.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from pythermalcomfort.models import utci

DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "weather"
OUT = Path(__file__).resolve().parent.parent / "figures" / "d1"
FILES = [
    ('DRY_2011-2023_epw-fil.epw',                     'DRY 2011–2023'),
    ('DRY_2011-2023_heatwave2018.epw',                'DRY 2011–2023 + summer 2018'),
    ('5A_Copenhagen_TMY_2001-2020.epw',               'Annex 80 TMY 2001–2020'),
    ('5A_Copenhagen_TMY_2041-2060.epw',               'Annex 80 TMY 2041–2060'),
    ('5A_Copenhagen_HW_Midterm_Longest_2045.epw',     'Heat wave longest (2045)'),
    ('5A_Copenhagen_HW_Midterm_MostIntense_2055.epw', 'Heat wave most intense (2055)'),
    ('5A_Copenhagen_HW_Midterm_MostSevere_2054.epw',  'Heat wave most severe (2054)'),
]
LAT, LON, TZ = 55.88, 12.41, 1.0

def read_epw(path):
    d = pd.read_csv(path, skiprows=8, header=None, usecols=[1, 2, 3, 6, 8, 9, 13, 14, 15, 21],
                    names=['mo', 'dy', 'hr', 'T', 'RH', 'p', 'GHI', 'DNI', 'DHI', 'WS'])
    for c in ('GHI', 'DHI'): d[c] = d[c].where(d[c] <= 1400).interpolate()  # corrupt hours in the Annex 80 heat-wave files
    d.index = pd.to_datetime(dict(year=2001, month=d.mo, day=d.dy)) + pd.to_timedelta(d.hr - 1, unit='h')
    return d

def sun_altitude(doy, hour):
    g = 2 * np.pi / 365 * (doy - 1 + (hour - 12) / 24)
    decl = (0.006918 - 0.399912*np.cos(g) + 0.070257*np.sin(g) - 0.006758*np.cos(2*g)
            + 0.000907*np.sin(2*g) - 0.002697*np.cos(3*g) + 0.00148*np.sin(3*g))
    eot = 229.18 * (0.000075 + 0.001868*np.cos(g) - 0.032077*np.sin(g) - 0.014615*np.cos(2*g) - 0.040849*np.sin(2*g))
    ha = np.radians(15 * (hour + (eot + 4*LON - 60*TZ) / 60 - 12))
    lat = np.radians(LAT)
    return np.degrees(np.arcsin(np.sin(lat)*np.sin(decl) + np.cos(lat)*np.cos(decl)*np.cos(ha)))

def outdoor_utci(d):
    """UTCI for a person standing in the sun, Tmrt from SolarCal (ASHRAE 55 App. C), as in tab-annex80-summary."""
    doy = d.index.dayofyear.values
    # time stamps differ between files; pick the shift that best matches GHI
    best = max((-1.5, -0.5, 0.5), key=lambda o: np.corrcoef(d.GHI, np.sin(np.radians(np.clip(sun_altitude(doy, d.hr.values + o), 0, 90))))[0, 1])
    alt = sun_altitude(doy, d.hr.values + best); beta = np.clip(alt, 0, 90)
    fp = 0.308 * np.cos(np.radians(beta * (1 - beta**2 / 48402)))
    erf = (0.5*0.725*(d.DHI + 0.2*d.GHI) + fp*0.725*np.where(alt > 0, d.DNI, 0)) * 0.7 / 0.95
    tr = d['T'] + erf / (0.725 * 6.012)
    return utci(tdb=d['T'].values, tr=tr.values, v=d.WS.clip(0.5, 17).values, rh=d.RH.clip(5, 100).values,
                limit_inputs=False, round_output=False).utci

def enthalpy(d):
    p = d.p.where((d.p > 80000) & (d.p < 110000), 101325)
    pw = d.RH.clip(0, 100) / 100 * 611.2 * np.exp(17.62 * d['T'] / (243.12 + d['T']))
    x = 0.622 * pw / (p - pw)
    return 1.006 * d['T'] + x * (2501 + 1.86 * d['T'])

def longest_run(mask):
    run = best = 0
    for m in mask:
        run = run + 1 if m else 0; best = max(best, run)
    return best

annual, waves, summer, series = [], [], [], {}
for f, name in FILES:
    d = read_epw(DATA / f); T = d['T']
    tmax = T.resample('D').max()
    n = T[(T.index.hour >= 21) | (T.index.hour < 9)]
    night = n.groupby((n.index - pd.Timedelta(hours=9)).normalize()).min()  # 21:00 to 09:00 next morning
    s = T[(T.index.month >= 6) & (T.index.month <= 8)]
    annual.append((name, T.min(), T.mean(), T.max(), int((T < 0).sum()), int((T > 26).sum()),
                   d.GHI.sum() / 1000, d.RH.mean(), enthalpy(d).mean(), int((outdoor_utci(d) > 26).sum())))
    waves.append((name, int((tmax > 25).sum()), longest_run(tmax > 25), int((night > 20).sum()), night.max()))
    summer.append((name, s.mean(), s.quantile(0.95), s.quantile(0.99), (s - 26).clip(0).sum(),
                   tmax['2001-06':'2001-08'].mean(), night['2001-06':'2001-08'].mean()))
    series[name] = d

pd.options.display.float_format = '{:.1f}'.format
print(pd.DataFrame(annual, columns=['File', 'Min', 'Mean', 'Max', 'h<0', 'h>26', 'GHI kWh/m2', 'RH %', 'h kJ/kg', 'UTCI>26 h']).to_string(index=False))
print(pd.DataFrame(waves, columns=['File', 'Days>25', 'Longest run', 'Tropical nights', 'Warmest night min']).to_string(index=False))
print(pd.DataFrame(summer, columns=['File', 'JJA mean', 'P95', 'P99', 'Kh>26', 'Mean daily max', 'Mean night min']).to_string(index=False))

# figure: (a) hours above each temperature in June–August, (b) daily max from June to August
INK, MUTED, SURF = '#0b0b0b', '#52514e', '#fcfcfb'
STYLE = {'DRY 2011–2023': ('#9aa3ad', '-', 1.2), 'DRY 2011–2023 + summer 2018': ('#d1352b', '-', 2.2),
         'Annex 80 TMY 2041–2060': ('#1c5cab', '--', 1.2), 'Heat wave longest (2045)': ('#199e70', '-', 1.2),
         'Heat wave most intense (2055)': ('#eb6834', '-', 1.2), 'Heat wave most severe (2054)': ('#7b3fa0', '-', 1.2)}
plt.rcParams.update({'font.size': 9, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK, 'xtick.color': MUTED,
                     'ytick.color': MUTED, 'font.family': 'DejaVu Sans'})
fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4.2), facecolor=SURF, layout='constrained')
th = np.arange(18, 33.01, 0.1)
for name, (c, ls, lw) in STYLE.items():
    T = series[name]['T']; s = T[(T.index.month >= 6) & (T.index.month <= 8)]
    a.plot(th, [(s > x).sum() for x in th], color=c, ls=ls, lw=lw, label=name)
    if name not in ('DRY 2011–2023', 'DRY 2011–2023 + summer 2018', 'Heat wave most severe (2054)'): continue
    tmax = T.resample('D').max()['2001-06':'2001-08']
    b.plot(tmax.index, tmax.values, color=c, ls=ls, lw=lw)
a.set_yscale('log'); a.set_ylim(1, 1000); a.set_xlim(18, 33)
a.set_xlabel('Air temperature (°C)'); a.set_ylabel('Hours above, June–August')
a.set_title('(a) Hours above a given temperature', loc='left', fontsize=10, color=INK, fontweight='bold')
b.axhline(25, color=MUTED, lw=0.8, ls=(0, (4, 3)))
b.set_ylabel('Daily maximum air temperature (°C)')
b.xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator()); b.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b'))
b.set_title('(b) Daily maximum, June–August (three files)', loc='left', fontsize=10, color=INK, fontweight='bold')
for ax in (a, b):
    ax.set_facecolor(SURF); ax.grid(color='#e6e5e0', lw=0.6); ax.set_axisbelow(True)
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
fig.legend(loc='outside lower center', ncol=3, frameon=False, fontsize=8.5)
fig.savefig(OUT / 'heatwave-2018-compare.png', dpi=200, facecolor=SURF)
fig.savefig(OUT / 'heatwave-2018-compare.svg', facecolor=SURF)
