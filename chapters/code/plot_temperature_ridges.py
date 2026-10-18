"""Ridge plots of hourly air temperature by season in the DMI DRY files and the Annex 80 Copenhagen files.

One row per weather file, with the distribution of the hourly temperatures in winter
(October to March) and in summer (April to September). The curves are kernel density
estimates with a Gaussian kernel of 0.8 K, so the area under each curve is the same.
The tick under each curve marks the median.

The EPW files are read from the folder weather/ next to this script. Another folder can be given:

    python plot_temperature_ridges.py <folder with the EPW files>
"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt
import sys
from pathlib import Path
DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "weather"  # folder with the EPW files
OUT = Path(__file__).resolve().parent.parent / "figures" / "d1"

SETS = {
    'dry-temperature-ridges': [
        ('Denmark_DRY_2001-2010.epw',        'DRY 2001–2010'),
        ('DRY_2011-2023_epw-fil.epw',        'DRY 2011–2023'),
        ('DRY_rcp45_2035_2054_epw-fil.epw',  'RCP4.5, 2035–2054'),
        ('DRY_rcp45_2045_2064_epw-fil.epw',  'RCP4.5, 2045–2064'),
        ('DRY_rcp45_2055_2074_epw-fil.epw',  'RCP4.5, 2055–2074'),
        ('DRY_rcp45_2080_2099_epw-fil.epw',  'RCP4.5, 2080–2099'),
    ],
    'annex80-temperature-ridges': [
        ('5A_Copenhagen_TMY_2001-2020.epw',               'TMY 2001–2020'),
        ('5A_Copenhagen_TMY_2041-2060.epw',               'TMY 2041–2060'),
        ('5A_Copenhagen_TMY_2081-2100.epw',               'TMY 2081–2100'),
        ('5A_Copenhagen_HW_Midterm_Longest_2045.epw',     'Heat wave longest (2045)'),
        ('5A_Copenhagen_HW_Midterm_MostIntense_2055.epw', 'Heat wave most intense (2055)'),
        ('5A_Copenhagen_HW_Midterm_MostSevere_2054.epw',  'Heat wave most severe (2054)'),
    ],
}
SEASONS = [('Winter (October to March)', [10, 11, 12, 1, 2, 3], '#1c5cab', '#b7d3f6'),
           ('Summer (April to September)', [4, 5, 6, 7, 8, 9], '#eb6834', '#f8cdb8')]
INK, MUTED, SURF = '#0b0b0b', '#52514e', '#fcfcfb'
BW, STEP, SCALE = 0.8, 1.0, 10.0     # kernel width (K), row spacing, height of a density of 1 per K

plt.rcParams.update({'font.size': 9, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK,
                     'xtick.color': MUTED, 'ytick.color': MUTED, 'font.family': 'DejaVu Sans'})
x = np.linspace(-18, 34, 521)
for name, files in SETS.items():
    fig, ax = plt.subplots(figsize=(11, 6.2), facecolor=SURF, layout='constrained')
    ax.set_facecolor(SURF)
    top = (len(files) - 1) * STEP
    for row, (f, label) in enumerate(files):
        d = pd.read_csv(DATA / f, skiprows=8, header=None, usecols=[1, 6], names=['mo', 'T'])
        base = top - row * STEP
        ax.axhline(base, color='#d5d4cf', lw=0.6, zorder=1)
        ax.text(-18.3, base + 0.12, label, ha='right', va='bottom', fontsize=9, color=INK)
        for s, (season, months, edge, fill) in enumerate(SEASONS):
            T = d.loc[d.mo.isin(months), 'T'].to_numpy()
            dens = np.exp(-0.5 * ((x[:, None] - T[None, :]) / BW) ** 2).sum(1) / (len(T) * BW * np.sqrt(2 * np.pi))
            z = 10 + 2 * row + s
            ax.fill_between(x, base, base + SCALE * dens, color=fill, alpha=0.75, lw=0, zorder=z)
            ax.plot(x, base + SCALE * dens, color=edge, lw=1.3, zorder=z, label=season if row == 0 else None)
            med = float(np.median(T))
            ax.plot([med, med], [base - 0.07, base], color=edge, lw=2, zorder=40, clip_on=False)
            ax.text(med, base - 0.1, f'{med:.1f}', ha='center', va='top', fontsize=8, color=edge, zorder=40)
            print(name, label, season[:6], 'median', round(med, 1), 'hours above 26 °C', int((T > 26).sum()), 'below 0 °C', int((T < 0).sum()))
    for xv in (0, 26):
        ax.axvline(xv, color=MUTED, lw=0.6, ls=':', zorder=2)
        ax.text(xv + 0.3, top + 1.3, f'{xv} °C', fontsize=8, color=MUTED, va='top')
    ax.set_xlim(-18, 34); ax.set_ylim(-0.3, top + 1.35)
    ax.set_xticks(range(-15, 35, 5)); ax.set_yticks([])
    ax.set_xlabel('Air temperature, hourly (°C). Number under each curve: median')
    ax.legend(frameon=False, loc='upper left', ncols=2, fontsize=9)
    for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
    fig.savefig(OUT / f'{name}.png', dpi=200, facecolor=SURF)
    fig.savefig(OUT / f'{name}.svg', facecolor=SURF)
