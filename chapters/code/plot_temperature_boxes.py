"""Box plots of hourly air temperature by season in the DMI DRY files and the Annex 80 Copenhagen files.

Each weather file gives two boxes: winter (October to March) and summer (April to September).
Box: quartiles and median. Whiskers: lowest and highest hour of the season.

The EPW files are read from the folder weather/ next to this script. Other folders can be given:

    python plot_temperature_boxes.py <folder with DMI EPW files> <folder with Annex 80 EPW files>

A file that is not found is skipped with a warning.
"""
import pandas as pd, matplotlib.pyplot as plt
import sys
from pathlib import Path
DMI = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "weather"  # folder with the DMI EPW files
ANNEX80 = Path(sys.argv[2]) if len(sys.argv) > 2 else DMI          # folder with the Annex 80 EPW files
OUT = Path(__file__).resolve().parent.parent / "figures" / "d1"

SETS = {
    'dry-temperature-boxes': (DMI, [
        ('Denmark_DRY_2001-2010.epw',        'DRY\n2001–2010'),
        ('DRY_2011-2023_epw-fil.epw',        'DRY\n2011–2023'),
        ('DRY_rcp45_2035_2054_epw-fil.epw',  'RCP4.5\n2035–2054'),
        ('DRY_rcp45_2045_2064_epw-fil.epw',  'RCP4.5\n2045–2064'),
        ('DRY_rcp45_2055_2074_epw-fil.epw',  'RCP4.5\n2055–2074'),
        ('DRY_rcp45_2080_2099_epw-fil.epw',  'RCP4.5\n2080–2099'),
    ]),
    'annex80-temperature-boxes': (ANNEX80, [
        ('5A_Copenhagen_TMY_2001-2020.epw',               'TMY\n2001–2020'),
        ('5A_Copenhagen_TMY_2041-2060.epw',               'TMY\n2041–2060'),
        ('5A_Copenhagen_TMY_2081-2100.epw',               'TMY\n2081–2100'),
        ('5A_Copenhagen_HW_Midterm_Longest_2045.epw',     'Heat wave\nlongest'),
        ('5A_Copenhagen_HW_Midterm_MostIntense_2055.epw', 'Heat wave\nmost intense'),
        ('5A_Copenhagen_HW_Midterm_MostSevere_2054.epw',  'Heat wave\nmost severe'),
    ]),
}
SEASONS = [('Winter (October to March)', [10, 11, 12, 1, 2, 3], '#1c5cab', '#b7d3f6'),
           ('Summer (April to September)', [4, 5, 6, 7, 8, 9], '#eb6834', '#f8cdb8')]
INK, MUTED, SURF = '#0b0b0b', '#52514e', '#fcfcfb'

plt.rcParams.update({'font.size': 9, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK,
                     'xtick.color': MUTED, 'ytick.color': MUTED, 'font.family': 'DejaVu Sans'})
for name, (folder, files) in SETS.items():
    data = []
    for f, label in files:
        if not (folder / f).exists():
            print('skipped, not found:', folder / f); continue
        d = pd.read_csv(folder / f, skiprows=8, header=None, usecols=[1, 6], names=['mo', 'T'])
        data.append((label, d))
    n = len(data)
    fig, ax = plt.subplots(figsize=(11, 4.6), facecolor=SURF, layout='constrained')
    ax.set_facecolor(SURF)
    for s, (season, months, edge, fill) in enumerate(SEASONS):
        pos = [s * (n + 1) + i for i in range(n)]
        vals = [d.loc[d.mo.isin(months), 'T'].to_numpy() for _, d in data]
        ax.boxplot(vals, positions=pos, widths=0.6, whis=(0, 100), patch_artist=True,
                   boxprops=dict(facecolor=fill, edgecolor=edge), medianprops=dict(color=edge, lw=1.8),
                   whiskerprops=dict(color=edge), capprops=dict(color=edge))
        for p, v, (label, _) in zip(pos, vals, data):
            ax.text(p, v.max() + 0.8, f'{pd.Series(v).median():.1f}', ha='center', va='bottom', fontsize=8, color=edge)
            print(name, season[:6], label.replace('\n', ' '), 'median', round(float(pd.Series(v).median()), 1),
                  'q1', round(float(pd.Series(v).quantile(.25)), 1), 'q3', round(float(pd.Series(v).quantile(.75)), 1),
                  'min', v.min(), 'max', v.max())
        ax.text(pos[0] - 0.4, 1.01, season, transform=ax.get_xaxis_transform(), fontsize=10, color=INK, fontweight='bold', va='bottom')
    ax.set_xticks([s * (n + 1) + i for s in range(2) for i in range(n)])
    ax.set_xticklabels([label for _ in range(2) for label, _ in data], fontsize=8)
    ax.tick_params(axis='x', length=0)
    ax.axhline(0, color=MUTED, lw=0.6)
    ax.set_ylabel('Air temperature, hourly (°C)')
    ax.grid(axis='y', color='#e6e5e0', lw=0.6); ax.set_axisbelow(True)
    ax.set_ylim(-18, 38)
    for sp in ('top', 'right', 'bottom'): ax.spines[sp].set_visible(False)
    fig.savefig(OUT / f'{name}.png', dpi=200, facecolor=SURF)
    fig.savefig(OUT / f'{name}.svg', facecolor=SURF)
