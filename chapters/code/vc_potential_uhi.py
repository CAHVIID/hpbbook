"""Hourly ventilative cooling potential, coloured by the temperature difference T_in - T_out (K),
for the rural reference year, the same year with a night-time urban heat island, and RCP4.5 2080-2099 with it.

Hours on days whose daily mean is below the balance point T_bp are marked as heating days (grey).
Other hours are coloured by dT = T_in - T_out: dT <= 0 means outdoor air cannot cool (red).
"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.cm import ScalarMappable
import sys
from pathlib import Path
DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")  # folder with the EPW files
OUT = Path(__file__).resolve().parent.parent / "figures" / "ch02"

T_IN, T_BP = 24.0, 12.0
UHI = np.array([2, 2, 2, 2, 2, 2, 1.5, 1, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, 1, 1.5, 2, 2, 2, 2])
CASES = [('DRY_2011-2023_epw-fil.epw', 0, 'DRY 2011–2023, rural (Sjælsmark)'),
         ('DRY_2011-2023_epw-fil.epw', 1, 'DRY 2011–2023 + 2 K night-time urban heat island'),
         ('DRY_rcp45_2080_2099_epw-fil.epw', 1, 'RCP4.5 2080–2099 + 2 K night-time urban heat island')]
INK, MUTED, SURF, GREY = '#0b0b0b', '#52514e', '#fcfcfb', '#e3e2dd'
BOUNDS = [-10, 0, 3, 6, 9, 12, 30]
COLS = ['#d6493a', '#f2b53c', '#bfe3d3', '#6cc3a0', '#199e70', '#0b6b4b']
LABELS = ['≤ 0', '0–3', '3–6', '6–9', '9–12', '> 12']

plt.rcParams.update({'font.size': 9, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK,
                     'xtick.color': MUTED, 'ytick.color': MUTED, 'font.family': 'DejaVu Sans'})
fig, axes = plt.subplots(3, 1, figsize=(11, 8.5), facecolor=SURF, layout='constrained', sharex=True)
cmap, norm = ListedColormap(COLS), BoundaryNorm(BOUNDS, len(COLS))
cmap.set_bad(GREY)
for ax, (f, uhi, title) in zip(axes, CASES):
    T = pd.read_csv(DATA / f, skiprows=8, header=None, usecols=[6])[6].to_numpy()[:8760].reshape(365, 24)
    heating = T.mean(1) < T_BP          # balance point on the rural daily mean
    T = T + uhi * UHI
    dT = np.ma.masked_array(T_IN - T, mask=np.repeat(heating[:, None], 24, 1))
    ax.imshow(dT.T, aspect='auto', cmap=cmap, norm=norm, origin='lower', extent=[0, 365, 0, 24], interpolation='nearest')
    summer = (T_IN - T)[120:273]                          # May-Sep
    night = summer[:, list(range(0, 7)) + list(range(19, 24))]
    ax.set_title(title, loc='left', fontsize=10, color=INK, fontweight='bold')
    ax.text(1.0, 1.02, f'May–Sep nights (19–07): mean ΔT {night.mean():.1f} K   hours with ΔT < 3 K: {(night < 3).sum()}',
            transform=ax.transAxes, ha='right', va='bottom', fontsize=8, color=MUTED)
    print(title, round(night.mean(), 2), int((night < 3).sum()))
    ax.set_yticks([0, 6, 12, 18, 24]); ax.set_ylabel('Hour of day')
    for s in ax.spines.values(): s.set_visible(False)
starts = np.cumsum([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30])
axes[-1].set_xticks(starts + 15); axes[-1].set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
axes[-1].tick_params(axis='x', length=0)
sm = ScalarMappable(cmap=ListedColormap(COLS), norm=BoundaryNorm(range(7), 6))
cb = fig.colorbar(sm, ax=axes, location='bottom', shrink=0.5, aspect=40, pad=0.02)
cb.set_ticks(np.arange(6) + 0.5); cb.set_ticklabels(LABELS); cb.outline.set_visible(False)
cb.set_label(f'Cooling potential ΔT = T_in − T_out (K), T_in = {T_IN:.0f} °C.  Grey: heating day (daily mean below {T_BP:.0f} °C)')
fig.savefig(OUT / 'vc-potential-uhi.png', dpi=200, facecolor=SURF)
fig.savefig(OUT / 'vc-potential-uhi.svg', facecolor=SURF)
