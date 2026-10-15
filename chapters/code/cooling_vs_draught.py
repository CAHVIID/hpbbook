"""Cooling power against draught risk for a low opening, as functions of airflow and outdoor temperature.

Room: 4 x 5 m floor, 2.6 m high, indoor air at T_IN. Outdoor air enters through a low opening
and runs along the floor.

Cooling power:   Phi = rho cp Q (T_in - T_out), linear in the airflow and in the temperature difference.
Floor stream:    u = K Q / x at 0.1 m above the floor (Nielsen et al. 2000), evaluated X m from the wall.
                 K = 4.4 1/m near isothermal, rising linearly to 10 1/m at dT = 10 K (assumption:
                 the book gives only the two ends of this range).
Local air temp.: t_a = T_in - 0.5 dT (assumption: the stream has warmed halfway before it reaches the ankles).
Draught rate:    ISO 7730, DR = (34 - t_a)(v - 0.05)^0.62 (0.37 v Tu + 3.14), Tu = 40 %.

Writes figures/d4/cooling-vs-draught.svg and .png.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "d4"
RHO, CP = 1.2, 1005.0
AREA, VOL, T_IN, X, TU = 4 * 5, 4 * 5 * 2.6, 24.0, 1.0, 40.0
T_OUT = [(22, '#bfe3d3'), (20, '#6cc3a0'), (16, '#199e70'), (12, '#0b6b4b')]
INK, MUTED, SURF = '#0b0b0b', '#52514e', '#fcfcfb'

plt.rcParams.update({'font.size': 9, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK,
                     'xtick.color': MUTED, 'ytick.color': MUTED, 'font.family': 'DejaVu Sans'})
ach = np.linspace(0, 10, 201)
q = ach * VOL / 3600                                   # m3/s
fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4.2), facecolor=SURF, layout='constrained')
for t_out, col in T_OUT:
    dT = T_IN - t_out
    phi = RHO * CP * q * dT / AREA                     # W/m2 floor
    k = 4.4 + (10 - 4.4) * min(dT, 10) / 10
    v = k * q / X
    dr = np.clip((34 - (T_IN - 0.5 * dT)) * np.clip(v - 0.05, 0, None) ** 0.62 * (0.37 * v * TU + 3.14), 0, 100)
    a.plot(ach, phi, color=col, lw=2, label=f'{t_out} °C outdoors (ΔT = {dT:.0f} K)'); b.plot(ach, dr, color=col, lw=2)
    limit = ach[np.argmax(dr > 20)] if (dr > 20).any() else np.nan
    print(f'T_out {t_out}: at 4 ACH {np.interp(4, ach, phi):.0f} W/m2, DR {np.interp(4, ach, dr):.0f} %, DR = 20 % at {limit:.1f} ACH')
b.axhline(20, color='#d6493a', lw=1, ls='--'); b.text(6.2, 21.5, 'limit DR = 20 %', color='#d6493a', fontsize=8)
a.set_title('(a) Cooling power grows linearly', loc='left', fontsize=10, color=INK, fontweight='bold')
b.set_title('(b) Draught rate at the ankles grows faster', loc='left', fontsize=10, color=INK, fontweight='bold')
a.set_ylabel('Cooling power (W/m² floor)'); b.set_ylabel('ISO 7730 draught rate (%)')
b.set_ylim(0, 100); a.set_ylim(0, None)
a.legend(frameon=False, fontsize=8, loc='upper left')
for ax in (a, b):
    ax.set_facecolor(SURF); ax.set_xlim(0, 10); ax.set_xlabel('Air change rate (1/h)')
    ax.grid(color='#e6e5e0', lw=0.6); ax.set_axisbelow(True)
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
for ext in ('svg', 'png'):
    fig.savefig(OUT / f'cooling-vs-draught.{ext}', dpi=200, facecolor=SURF)
