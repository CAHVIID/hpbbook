"""Light transmittance of six glazings against how test subjects rated the daylight behind them.

Data: Dubois and Johnsen (2003), By og Byg Documentation 044, pilot study with 18 subjects looking into a 1:7.5 scale model
of an office under overcast skies. LT is the manufacturer's value; the category is the authors' summary of
the 7-point ratings (colour, brightness, details, acceptability). The report gives no medians, only box plots.

Writes d3/glazing-lt-rating (.png, .svg).
"""
from pathlib import Path

import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures" / "d3"
INK, MUTED, GRID, SURF = '#0b0b0b', '#52514e', '#e4e3dc', '#fcfcfb'
plt.rcParams.update({'font.size': 9, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK,
                     'xtick.color': MUTED, 'ytick.color': MUTED, 'font.family': 'DejaVu Sans'})

CATS = ['Poor', 'Moderate', 'Good', 'Excellent']
COLS = ['#a3341f', '#eb6834', '#7aa6e0', '#2a78d6']        # one ramp from poor to excellent
GLAZ = [('Reference', 77, 'Excellent'), ('A', 79, 'Good'), ('D', 76, 'Good'),
        ('B', 70, 'Moderate'), ('E', 66, 'Moderate'), ('C', 50, 'Poor')]
NOTE = {'Excellent': '', 'Good': '', 'Moderate': 'colour unacceptable to some',
        'Poor': 'colour unacceptable to most'}

fig, ax = plt.subplots(figsize=(6.2, 2.6), facecolor=SURF)
ax.set_facecolor(SURF)
for y, c in enumerate(CATS):
    ax.axhline(y, color=GRID, lw=0.8, zorder=0)
for name, lt, cat in GLAZ:
    y = CATS.index(cat)
    ax.plot(lt, y, 'o', ms=9, color=COLS[y], mec=SURF, mew=2, zorder=3)
    dx = -1.0 if name in ('D', 'E') else 1.0
    ax.annotate(f'{name} {lt} %', (lt, y), xytext=(dx * 8, 8), textcoords='offset points',
                ha='right' if dx < 0 else 'left', fontsize=8, color=INK)
for y, c in enumerate(CATS):
    if NOTE[c]:
        ax.text(84.5, y, NOTE[c], va='center', ha='right', fontsize=8, color=MUTED, style='italic')
ax.set_yticks(range(4), CATS)
ax.set_xlim(45, 85)
ax.set_ylim(-0.6, 3.6)
ax.set_xlabel('Light transmittance of the glazing (%)')
ax.set_ylabel('Rated daylight quality')
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
fig.tight_layout()
OUT.mkdir(parents=True, exist_ok=True)
for ext in ('png', 'svg'):
    fig.savefig(OUT / f'glazing-lt-rating.{ext}', dpi=200, facecolor=SURF)
