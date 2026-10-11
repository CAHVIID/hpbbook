"""Hourly air temperature, daily global radiation and RH in the IEA EBC Annex 80 Copenhagen weather files."""
import pandas as pd, matplotlib.pyplot as plt, matplotlib.dates as mdates
import sys
from pathlib import Path
DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")  # folder with the EPW files
OUT = Path(__file__).resolve().parent.parent / "figures" / "ch02"

FILES = [
    ('5A_Copenhagen_TMY_2001-2020.epw',              'TMY 2001–2020'),
    ('5A_Copenhagen_HW_Midterm_Longest_2045.epw',    'Heat wave 2041–2060: longest (2045)'),
    ('5A_Copenhagen_TMY_2041-2060.epw',              'TMY 2041–2060'),
    ('5A_Copenhagen_HW_Midterm_MostIntense_2055.epw','Heat wave 2041–2060: most intense (2055)'),
    ('5A_Copenhagen_TMY_2081-2100.epw',              'TMY 2081–2100'),
    ('5A_Copenhagen_HW_Midterm_MostSevere_2054.epw', 'Heat wave 2041–2060: most severe (2054)'),
]
HOURLY, DAILY, RAD, RHH, RHD, INK, MUTED, SURF = '#b7d3f6', '#1c5cab', '#eb6834', '#a7e3cd', '#199e70', '#0b0b0b', '#52514e', '#fcfcfb'

def read_epw(path):
    d = pd.read_csv(path, skiprows=8, header=None, usecols=[1, 2, 3, 6, 8, 13], names=['mo', 'dy', 'hr', 'T', 'RH', 'GHI'])
    d.index = pd.to_datetime(dict(year=2001, month=d.mo, day=d.dy)) + pd.to_timedelta(d.hr - 1, unit='h')
    # the heat-wave files hold a few corrupt radiation values (up to 5.6e6 W/m²); drop and interpolate them
    d['GHI'] = d['GHI'].where(d['GHI'] <= 1400).interpolate()
    return d[['T', 'RH', 'GHI']]

plt.rcParams.update({'font.size': 9, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK,
                     'xtick.color': MUTED, 'ytick.color': MUTED, 'font.family': 'DejaVu Sans'})
import numpy as np
fig = plt.figure(figsize=(11, 12), facecolor=SURF, layout='constrained')
fig.get_layout_engine().set(h_pad=0.03, w_pad=0.04, hspace=0, wspace=0.02)
outer = fig.add_gridspec(3, 2, hspace=0.06, wspace=0.04)
axes = np.empty((3, 2), dtype=object); rhaxes = np.empty((3, 2), dtype=object)
for i in range(3):
    for j in range(2):
        inner = outer[i, j].subgridspec(2, 1, height_ratios=[3, 1.1], hspace=0)
        axes[i, j] = fig.add_subplot(inner[0], sharex=axes[0, 0] if (i or j) else None, sharey=axes[0, 0] if (i or j) else None)
        rhaxes[i, j] = fig.add_subplot(inner[1], sharex=axes[0, 0])
        plt.setp(axes[i, j].get_xticklabels(), visible=False)
        if i < 2: plt.setp(rhaxes[i, j].get_xticklabels(), visible=False)
rows = []
for ax, rax, (f, title) in zip(axes.flat, rhaxes.flat, FILES):
    w = read_epw(DATA / f); T = w['T']
    ghi = w['GHI'].resample('D').sum() / 1000  # kWh/m² per day
    daily = T.resample('D').mean()
    ax.set_facecolor(SURF)
    ax.plot(T.index, T.values, color=HOURLY, lw=0.5, label='Air temperature, hourly')
    ax.plot(daily.index + pd.Timedelta(hours=12), daily.values, color=DAILY, lw=1.4, label='Air temperature, daily mean')
    ax2 = ax.twinx()
    ax2.plot(ghi.index + pd.Timedelta(hours=12), ghi.values, color=RAD, lw=1.0, alpha=0.9, label='Global radiation, daily sum')
    ax2.set_ylim(0, 25); ax2.tick_params(colors=MUTED)
    for s_ in ('top', 'left'): ax2.spines[s_].set_visible(False)
    ax2.spines['right'].set_color(MUTED)
    if ax in axes[:, 1]: ax2.set_ylabel('Global radiation (kWh/m² per day)', color=INK)
    else: ax2.set_yticklabels([])
    ax.set_zorder(ax2.get_zorder() + 1); ax.patch.set_visible(False)
    rh = w['RH']; rhd = rh.resample('D').mean()
    rax.set_facecolor(SURF)
    rax.plot(rh.index, rh.values, color=RHH, lw=0.4, label='Relative humidity, hourly')
    rax.plot(rhd.index + pd.Timedelta(hours=12), rhd.values, color=RHD, lw=1.2, label='Relative humidity, daily mean')
    rax.set_ylim(0, 100); rax.set_yticks([0, 50, 100])
    rax.grid(axis='y', color='#e6e5e0', lw=0.6); rax.set_axisbelow(True)
    for s_ in ('top', 'right'): rax.spines[s_].set_visible(False)
    rax.text(0.01, 0.06, f'mean RH {rh.mean():.0f} %', transform=rax.transAxes, fontsize=8, color=MUTED)
    ax.axhline(26, color=MUTED, lw=0.8, ls=(0, (4, 3)))
    ax.set_title(title, loc='left', fontsize=10, color=INK, fontweight='bold')
    h26 = int((T > 26).sum())
    ax.text(0.01, 0.98, f'mean {T.mean():.1f} °C   max {T.max():.1f} °C   min {T.min():.1f} °C\n{h26} h above 26 °C   global radiation {ghi.sum():.0f} kWh/m²',
            transform=ax.transAxes, ha='left', va='top', fontsize=8, color=MUTED)
    ax.grid(axis='y', color='#e6e5e0', lw=0.6); ax.set_axisbelow(True)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    rows.append((title, T.min(), round(T.mean(), 1), T.max(), int((T < 0).sum()), h26, round(ghi.sum()), round(rh.mean())))
for ax in axes[:, 0]: ax.set_ylabel('Air temperature (°C)')
for ax in rhaxes[:, 0]: ax.set_ylabel('RH (%)')
axes[0, 0].text(pd.Timestamp('2001-12-29'), 26.6, '26 °C', fontsize=8, color=MUTED, ha='right')
ax = rhaxes[-1, 0]
ax.xaxis.set_major_locator(mdates.MonthLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
for a in rhaxes[-1]:
    for lbl in a.get_xticklabels(): lbl.set_fontsize(7.5)
ax.set_xlim(pd.Timestamp('2001-01-01'), pd.Timestamp('2001-12-31 23:00')); axes[0, 0].set_ylim(-16, 34)
h, l = axes[0, 0].get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels(); h3, l3 = rax.get_legend_handles_labels(); h += h2 + h3; l += l2 + l3
fig.legend(h, l, loc='outside upper left', ncol=3, frameon=False, fontsize=8.5)
fig.savefig(OUT / 'annex80-weather.png', dpi=200, facecolor=SURF)
fig.savefig(OUT / 'annex80-weather.svg', facecolor=SURF)
summary = pd.DataFrame(rows, columns=['Weather file', 'Min (°C)', 'Mean (°C)', 'Max (°C)', 'Hours below 0 °C',
                                     'Hours above 26 °C', 'Global radiation (kWh/m²)', 'Mean RH (%)'])
summary.to_csv('annex80-summary.csv', index=False)
print(summary.to_string(index=False))
