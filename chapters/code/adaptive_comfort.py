"""Adaptive comfort limits of EN 16798-1 for buildings without mechanical cooling.

Comfort temperature: theta_c = 0.33 theta_rm + 18.8, valid for a running mean outdoor
temperature theta_rm of 10 to 30 °C. Category limits of the operative temperature:
    I:   theta_c + 2 / - 3
    II:  theta_c + 3 / - 4
    III: theta_c + 4 / - 5

Writes figures/d2/adaptive-comfort.svg and .png.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures" / "d2"
OUT.mkdir(exist_ok=True)
INK, MUTED, SURF = '#0b0b0b', '#52514e', '#fcfcfb'
CATS = [('III', 4, -5, '#d9efe6'), ('II', 3, -4, '#a7e3cd'), ('I', 2, -3, '#6cc3a0')]

plt.rcParams.update({'font.size': 9, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK,
                     'xtick.color': MUTED, 'ytick.color': MUTED, 'font.family': 'DejaVu Sans'})
rm = np.linspace(10, 30, 50)
tc = 0.33 * rm + 18.8
fig, ax = plt.subplots(figsize=(7, 4.4), facecolor=SURF, layout='constrained')
ax.set_facecolor(SURF)
for cat, up, lo, col in CATS:
    ax.fill_between(rm, tc + lo, tc + up, color=col, lw=0)
    ax.text(30.2, tc[-1] + up, f'{cat} upper', va='center', fontsize=8, color=MUTED)
    ax.text(30.2, tc[-1] + lo, f'{cat} lower', va='center', fontsize=8, color=MUTED)
ax.plot(rm, tc, color=INK, lw=1.2, ls='--')
ax.text(30.2, tc[-1], 'comfort', va='center', fontsize=8, color=INK)
ax.plot(rm, tc + 3, color='#d6493a', lw=2)
ax.annotate('Category II upper limit\n0.33 θ$_{rm}$ + 18.8 + 3', xy=(15, 0.33 * 15 + 21.8), xytext=(10.5, 31),
            color='#d6493a', fontsize=9, arrowprops=dict(arrowstyle='-', color='#d6493a', lw=0.8))
for x in (15, 20):
    y = 0.33 * x + 21.8
    ax.plot([x], [y], 'o', color='#d6493a', ms=5)
    ax.text(x + 0.3, y - 0.9, f'{y:.1f} °C', fontsize=8, color='#d6493a')
ax.set_xlim(10, 33); ax.set_ylim(16, 34)
ax.set_xticks(range(10, 31, 5))
ax.set_xlabel('Running mean outdoor temperature θ$_{rm}$ (°C)')
ax.set_ylabel('Operative temperature (°C)')
ax.grid(color='#e6e5e0', lw=0.6); ax.set_axisbelow(True)
for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
for ext in ('svg', 'png'):
    fig.savefig(OUT / f'adaptive-comfort.{ext}', dpi=200, facecolor=SURF)
