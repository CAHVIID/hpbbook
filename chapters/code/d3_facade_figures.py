"""Figures for D3 Façade design.

1. d3/design-variables: section and elevation of the 4 x 4 x 2.5 m centre zone with the four design
   variables (window size, glazing, overhang, side fins). Drawing only.
2. d3/facade-radiation: monthly solar radiation on vertical north, east/west and south façades and on
   the horizontal, from the Annex 80 Copenhagen TMY 2041-2060. Isotropic sky, ground reflectance 0.2.
3. d3/overhang: (a) section of the south window (sill 0.9 m, height 1.1 m) with a 1.0 m overhang at the
   window head and the noon sun in June, March/September and December; (b) monthly direct (beam)
   radiation on the window with and without the overhang. The overhang is as long as the window
   (2.3 m), so the sun from the side passes its ends; diffuse radiation is not reduced (conservative).
4. d3/pareto-concept: what a Pareto front of cooling against heating demand looks like. Concept only,
   no simulation results.
5. d3/side-fins, side-fins-east, side-fins-west: (a) plan of the 2.3 m wide window with 0.5 m side
   fins (both sides towards south, only the south side towards east and west); the
   -2win variants split the glass into two windows, each with its own fin and the sun at two hours on 21 June; (b) monthly
   direct radiation on the window with and without the fins. The fins are taken as infinitely tall (2D), so
   only the horizontal angle between sun and façade normal matters; diffuse radiation is not reduced.

Sun position: Spencer (1971) declination and equation of time, EPW hour h taken at h - 0.5 local
standard time (UTC+1). Run from anywhere: python d3_facade_figures.py [path to EPW].
"""
import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Rectangle

OUT = Path(__file__).resolve().parent.parent / "figures" / "d3"
EPW = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/mnt/project-files/5A_Copenhagen_TMY_2041-2060.epw")
BLUE, ORANGE, AQUA, YELLOW, VIOLET = '#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#6250d6'
INK, MUTED, GRID, SURF, WALL, GLASS = '#0b0b0b', '#52514e', '#e4e3dc', '#fcfcfb', '#d9d7cf', '#bcd7f2'
plt.rcParams.update({'font.size': 9, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK,
                     'xtick.color': MUTED, 'ytick.color': MUTED, 'font.family': 'DejaVu Sans'})
MONTHS = 'JFMAMJJASOND'
H_WIN, SILL, D_OH = 1.1, 0.9, 1.0                         # south window height, sill and overhang depth
W_WIN = 2.3                                                # window width; the overhang is as long as the window


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ('svg', 'png'):
        fig.savefig(OUT / f'{name}.{ext}', dpi=200, facecolor=SURF)
    plt.close(fig)


def read_epw(path):
    rows = list(csv.reader(open(path)))
    lat, lon = float(rows[0][6]), float(rows[0][7])
    d = np.array([[float(r[1]), float(r[2]), float(r[3]), float(r[13]), float(r[14]), float(r[15])]
                  for r in rows[8:]])
    return lat, lon, d                                      # month, day, hour, GHI, DNI, DHI (Wh/m2)


def sun(lat, lon, month, day, hour):
    doy = np.array([np.datetime64(f'2002-{int(m):02d}-{int(dd):02d}').astype('datetime64[D]').item().timetuple().tm_yday
                    for m, dd in zip(month, day)])
    b = 2 * np.pi * (doy - 1) / 365
    decl = (0.006918 - 0.399912 * np.cos(b) + 0.070257 * np.sin(b) - 0.006758 * np.cos(2 * b)
            + 0.000907 * np.sin(2 * b) - 0.002697 * np.cos(3 * b) + 0.00148 * np.sin(3 * b))
    eot = 229.18 * (0.000075 + 0.001868 * np.cos(b) - 0.032077 * np.sin(b) - 0.014615 * np.cos(2 * b)
                    - 0.040849 * np.sin(2 * b))           # minutes
    solar_time = hour - 0.5 + (4 * (lon - 15) + eot) / 60
    w = np.radians(15 * (solar_time - 12))
    phi = np.radians(lat)
    sin_alt = np.sin(phi) * np.sin(decl) + np.cos(phi) * np.cos(decl) * np.cos(w)
    alt = np.arcsin(np.clip(sin_alt, -1, 1))
    az = np.arctan2(np.sin(w), np.cos(w) * np.sin(phi) - np.tan(decl) * np.cos(phi))  # from south, west +
    return alt, az


def on_vertical(alt, az, facade_az, ghi, dni, dhi, rho=0.2):
    cos_i = np.cos(alt) * np.cos(az - facade_az)
    beam = dni * np.clip(cos_i, 0, None) * (alt > 0)
    return beam, 0.5 * dhi + 0.5 * rho * ghi


lat, lon, d = read_epw(EPW)
alt, az = sun(lat, lon, d[:, 0], d[:, 1], d[:, 2])
month = d[:, 0].astype(int)
ghi, dni, dhi = d[:, 3], d[:, 4], d[:, 5]

# ---------- 2. radiation on façades ----------
series = []
for name, faz, col in [('South', 0, ORANGE), ('East / west', np.pi / 2, YELLOW), ('North', np.pi, BLUE)]:
    beam, diff = on_vertical(alt, az, faz, ghi, dni, dhi)
    series.append((name, np.array([(beam + diff)[month == m].sum() / 1000 for m in range(1, 13)]), col))
series.append(('Horizontal', np.array([ghi[month == m].sum() / 1000 for m in range(1, 13)]), MUTED))
fig, ax = plt.subplots(figsize=(7.5, 3.8), facecolor=SURF, layout='constrained')
x = np.arange(12)
for name, v, col in series:
    ax.plot(x, v, color=col, lw=2, marker='o', ms=4, ls='--' if name == 'Horizontal' else '-',
            label=f'{name}: {v.sum():.0f} kWh/m² per year')
    print(f'{name}: annual {v.sum():.0f} kWh/m2, May-Aug {v[4:8].sum():.0f}, Jun {v[5]:.0f}')
ax.set_xticks(x, list(MONTHS)); ax.set_xlim(-0.3, 11.3)
ax.legend(frameon=False, loc='upper left', fontsize=8)
ax.set_ylabel('Solar radiation, kWh/m² per month')
ax.set_facecolor(SURF); ax.grid(axis='y', color=GRID); ax.set_axisbelow(True)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
save(fig, 'facade-radiation')

# ---------- 3. overhang ----------
beam_s, diff_s = on_vertical(alt, az, 0.0, ghi, dni, dhi)
tan_prof = np.tan(alt) / np.clip(np.cos(az), 1e-6, None)    # profile angle, south façade
dv = D_OH * np.clip(tan_prof, 0, None)                       # shadow depth below the window head
dh = D_OH * np.abs(np.tan(np.where(np.cos(az) > 0, az, 0.0)))  # sideways shift of the shadow
y_end = np.minimum(H_WIN, np.where(dh > 0, W_WIN * dv / np.maximum(dh, 1e-9), H_WIN))
y_end = np.minimum(y_end, dv)
area = W_WIN * y_end - np.where(dv > 0, dh / np.maximum(dv, 1e-9), 0) * y_end ** 2 / 2
shaded = np.clip(area / (W_WIN * H_WIN), 0, 1) * (np.cos(az) > 0)
beam_oh = beam_s * (1 - shaded)
m_beam = np.array([beam_s[month == m].sum() / 1000 for m in range(1, 13)])
m_oh = np.array([beam_oh[month == m].sum() / 1000 for m in range(1, 13)])
print(f'South window beam: annual {m_beam.sum():.0f} -> {m_oh.sum():.0f} kWh/m2; May-Aug {m_beam[4:8].sum():.0f} -> '
      f'{m_oh[4:8].sum():.0f}; Nov-Feb {m_beam[[10,11,0,1]].sum():.0f} -> {m_oh[[10,11,0,1]].sum():.0f}')
fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4.0), facecolor=SURF, layout='constrained',
                           gridspec_kw={'width_ratios': [1, 1.35]})
a.set_aspect('equal'); a.axis('off')
head = SILL + H_WIN
a.add_patch(Rectangle((-0.3, 0), 0.3, 2.5, color=WALL))                       # wall
a.add_patch(Rectangle((-0.3, SILL), 0.3, H_WIN, color=GLASS, ec=MUTED, lw=0.8))
a.add_patch(Rectangle((0, head), D_OH, 0.08, color=MUTED))                     # overhang
a.plot([-0.3, 3.2], [0, 0], color=MUTED, lw=1); a.plot([-0.3, 3.2], [2.5, 2.5], color=MUTED, lw=0.6, ls=':')
noon = 90 - lat
for decl, lab, col in [(23.44, 'June 21: 58°', ORANGE), (0, 'Mar/Sep 21: 34°', YELLOW), (-23.44, 'Dec 21: 11°', BLUE)]:
    h = np.radians(noon + decl)
    x0, y0 = D_OH, head                                                         # ray past the overhang tip
    y_hit = head - D_OH * np.tan(h)
    a.plot([x0 + 1.6 * np.cos(h), 0], [y0 + 1.6 * np.sin(h), y_hit], color=col, lw=1.6)
    a.text(x0 + 1.65 * np.cos(h), y0 + 1.65 * np.sin(h), lab, color=INK, fontsize=8,
           ha='left', va='bottom' if decl > -1 else 'center')
a.annotate('', (0, head + 0.25), (D_OH, head + 0.25), arrowprops=dict(arrowstyle='<->', color=INK, lw=0.8))
a.text(D_OH / 2, head + 0.3, f'{D_OH} m', ha='center', fontsize=8)
a.text(-0.4, SILL + H_WIN / 2, f'{H_WIN} m', ha='right', va='center', fontsize=8)
a.text(-0.4, SILL / 2, f'sill {SILL} m', ha='right', va='center', fontsize=8, color=MUTED)
a.set_xlim(-1.3, 3.4); a.set_ylim(-0.1, 3.9)
a.set_title(f'(a) Noon sun past a {D_OH} m overhang, south', loc='left', fontsize=9)
a.text(1.6, 0.35, f'overhang {W_WIN} m long,\nas wide as the window', fontsize=7.5, color=MUTED)
w = 0.38
b.bar(x - w / 2, m_beam, w, color=ORANGE, label='Without overhang')
b.bar(x + w / 2, m_oh, w, color=BLUE, label=f'With {D_OH} m overhang')
b.set_xticks(x, list(MONTHS)); b.set_ylabel('Direct radiation on window, kWh/m² per month')
b.legend(frameon=False, loc='upper right'); b.set_ylim(0, 70); b.set_facecolor(SURF)
b.grid(axis='y', color=GRID); b.set_axisbelow(True)
for s in ('top', 'right'): b.spines[s].set_visible(False)
b.set_title('(b) Direct sun on the south window, 2050 TMY', loc='left', fontsize=9)
save(fig, 'overhang')
prof_full = np.degrees(np.arctan(H_WIN / D_OH))
print(f'Overhang shades the whole window when the profile angle exceeds {prof_full:.1f} deg '
      f'(noon: declination > {prof_full - noon:.1f} deg)')

# ---------- 1. design variables ----------
fig, (a, b) = plt.subplots(1, 2, figsize=(10, 3.8), facecolor=SURF, layout='constrained',
                           gridspec_kw={'width_ratios': [1, 1.1]})
for ax in (a, b):
    ax.set_aspect('equal'); ax.axis('off')
# section
a.add_patch(Rectangle((0, -0.3), 4.6, 0.3, color=WALL)); a.add_patch(Rectangle((0, 2.5), 4.6, 0.3, color=WALL))
a.add_patch(Rectangle((4.3, 0), 0.3, 2.5, color=WALL))
a.add_patch(Rectangle((4.3, 0.9), 0.3, 1.2, color=GLASS, ec=MUTED, lw=0.8))
a.add_patch(Rectangle((4.6, 2.1), 1.0, 0.08, color=ORANGE))
a.plot([0.3, 4.3], [0.85, 0.85], color=MUTED, ls=':', lw=1)
a.text(2.3, 0.7, 'daylight plane (sDA300)', ha='center', fontsize=8, color=MUTED, va='top')
a.text(5.1, 2.3, 'overhang\ndepth', ha='center', fontsize=8, color=INK, va='bottom')
a.text(4.2, 1.5, 'glazing\ng, $\\tau_v$', ha='right', fontsize=8, color=INK, va='center')
a.text(2.15, 1.6, '4 m deep, 2.5 m high', ha='center', fontsize=8, color=MUTED)
a.set_xlim(-0.2, 6.0); a.set_ylim(-0.5, 3.4); a.set_title('(a) Section', loc='left', fontsize=9)
# elevation
b.add_patch(Rectangle((0, 0), 4, 2.5, color=WALL))
b.add_patch(Rectangle((0.1, 0.9), 3.8, 1.5, fc='none', ec=INK, lw=0.8, ls='--'))   # largest window
ww, wh = 3.8 * 0.7, 1.5 * 0.7
b.add_patch(Rectangle((2 - ww / 2, 0.9), ww, wh, fc=GLASS, ec=MUTED, lw=0.8))
b.add_patch(Rectangle((2 - ww / 2 - 0.1, 0.9 + wh), ww + 0.2, 0.08, color=ORANGE))
for xf in (2 - ww / 2 - 0.1, 2 + ww / 2 + 0.02):
    b.add_patch(Rectangle((xf, 0.9), 0.08, wh, color=VIOLET))
b.text(2, 0.9 + wh / 2, 'window size\n(width × height,\nsill 0.9 m)', ha='center', va='center', fontsize=8)
b.text(2, 2.28, 'largest window 3.8 × 1.5 m', ha='center', va='center', fontsize=7.5, color=MUTED)
b.annotate('side fins', (2 + ww / 2 + 0.1, 1.3), (4.15, 1.3), va='center', fontsize=8,
           arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
b.annotate('overhang', (2 + ww / 2 + 0.1, 0.94 + wh), (4.15, 2.0), va='center', fontsize=8,
           arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
b.text(2, -0.2, '4 m wide façade, north or south', ha='center', va='top', fontsize=8, color=MUTED)
b.set_xlim(-0.2, 5.4); b.set_ylim(-0.6, 3.0); b.set_title('(b) Elevation', loc='left', fontsize=9)
save(fig, 'design-variables')

# ---------- 4. Pareto concept ----------
rng = np.random.default_rng(3)
size, ctrl = np.meshgrid(np.linspace(0.1, 1, 10), np.linspace(0, 1, 8))      # window size, solar control
size, ctrl = size.ravel(), ctrl.ravel()
cool = (1 + 6 * size * (1 - 0.6 * ctrl)) * rng.uniform(0.95, 1.05, size.size)
heat = (2.2 - 0.8 * size + 0.9 * ctrl) * rng.uniform(0.97, 1.03, size.size)
sda = 25 + 75 * size * (1 - 0.45 * ctrl)
ok = sda >= 50
pts = np.c_[heat[ok], cool[ok]]
front = np.array([p for p in pts if not ((pts[:, 0] <= p[0]) & (pts[:, 1] <= p[1]) & ((pts[:, 0] < p[0]) | (pts[:, 1] < p[1]))).any()])
front = front[np.argsort(front[:, 0])]
fig, ax = plt.subplots(figsize=(6.5, 4.2), facecolor=SURF, layout='constrained')
ax.scatter(heat[~ok], cool[~ok], s=18, fc='none', ec=MUTED, lw=0.8, label='sDA300 < 50 % (infeasible)')
ax.scatter(heat[ok], cool[ok], s=18, color=BLUE, ec=SURF, lw=0.5, label='sDA300 ≥ 50 % (feasible)')
ax.plot(front[:, 0], front[:, 1], color=ORANGE, lw=2, marker='o', ms=5, mec=SURF, label='Pareto front')
pick = front[len(front) // 2]
ax.annotate('chosen design', pick, (pick[0] + 0.45, pick[1] + 1.6), fontsize=8.5,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.set_xlabel('Heating demand →'); ax.set_ylabel('Cooling demand →')
ax.set_xticks([]); ax.set_yticks([]); ax.set_facecolor(SURF)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.legend(frameon=False, loc='upper right', fontsize=8)
save(fig, 'pareto-concept')

# ---------- 5. side fins ----------
D_FIN, PIER = 0.5, 0.3                                     # fin depth, wall between two windows


def fins_figure(name, faz, hours, sides, fin='both', n_win=1):
    """Plan of the window(s) with fins and the sun at two hours on 21 June, and monthly direct radiation.
    faz: façade azimuth from south, west positive; sides: (left, right) labels in the plan;
    fin: 'both', 'left' or 'right' (which side of each window has a fin, as drawn in the plan);
    n_win: the 2.3 m of glass split into n_win equal windows, each with its own fin(s)."""
    wn = W_WIN / n_win                                      # width of each window
    beam, _ = on_vertical(alt, az, faz, ghi, dni, dhi)
    gam = np.angle(np.exp(1j * (az - faz)))                 # horizontal angle sun - façade normal
    gam = np.where(np.cos(gam) > 0, gam, 0.0)
    acts = {'both': gam != 0, 'right': gam > 0, 'left': gam < 0}[fin]       # a fin shades sun from its own side
    beam_fin = beam * (1 - np.clip(D_FIN * np.abs(np.tan(gam)) / wn, 0, 1) * acts)
    m0 = np.array([beam[month == m].sum() / 1000 for m in range(1, 13)])
    m1 = np.array([beam_fin[month == m].sum() / 1000 for m in range(1, 13)])
    print(f'{name} ({n_win} window) beam with {D_FIN} m fins: annual {m0.sum():.0f} -> {m1.sum():.0f} kWh/m2 '
          f'({100 * (1 - m1.sum() / m0.sum()):.0f} %); May-Aug {m0[4:8].sum():.0f} -> {m1[4:8].sum():.0f} '
          f'({100 * (1 - m1[4:8].sum() / m0[4:8].sum()):.0f} %)')
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4.0), facecolor=SURF, layout='constrained',
                               gridspec_kw={'width_ratios': [1, 1.35]})
    a.set_aspect('equal'); a.axis('off')
    x0s = [k * (wn + PIER) for k in range(n_win)]           # left edge of each window
    span = x0s[-1] + wn
    a.add_patch(Rectangle((-0.6, -0.3), span + 1.2, 0.3, color=WALL))          # wall in plan, outside up
    for x0 in x0s:
        a.add_patch(Rectangle((x0, -0.3), wn, 0.3, color=GLASS, ec=MUTED, lw=0.8))
        for xf, sd in ((x0 - 0.06, 'left'), (x0 + wn, 'right')):
            if fin in ('both', sd):
                a.add_patch(Rectangle((xf, 0), 0.06, D_FIN, color=MUTED))      # fins
    a.text(span / 2, -0.4, 'room', ha='center', va='top', fontsize=8, color=MUTED)
    a.text(-0.7, -0.15, sides[0], ha='right', va='center', fontsize=8, color=MUTED)
    a.text(span + 0.7, -0.15, sides[1], ha='left', va='center', fontsize=8, color=MUTED)
    for st, col in zip(hours, (ORANGE, BLUE)):
        wh = np.radians(15 * (st - 12))
        a_sun = np.arctan2(np.sin(wh), np.cos(wh) * np.sin(np.radians(lat)) - np.tan(np.radians(23.44)) * np.cos(np.radians(lat)))
        g = np.angle(np.exp(1j * (a_sun - faz)))
        side = -1 if g < 0 else 1                                                # sun from the left: left fin
        shadow = min(D_FIN * np.tan(abs(g)), wn)                                # shaded strip of each window
        for k, x0 in enumerate(x0s):
            tip = np.array([x0 if side < 0 else x0 + wn, D_FIN])
            hit = tip[0] - side * shadow
            a.add_patch(Rectangle((min(tip[0], hit), -0.3), shadow, 0.3, color=col, alpha=0.35, lw=0))
            start = tip + 1.5 * np.array([side * np.sin(abs(g)), np.cos(abs(g))])
            a.plot([start[0], hit], [start[1], 0], color=col, lw=1.6)
            if k == (0 if side < 0 else n_win - 1):                              # label the outermost ray
                lab_at = start
        a.text(lab_at[0], lab_at[1] + 0.06, f'June 21, {st:02d}:00\n{abs(np.degrees(g)):.0f}° from the normal',
               ha='center', va='bottom', fontsize=8)
    xa = span + 0.25 if fin != 'left' else -0.25
    a.annotate('', (xa, 0), (xa, D_FIN), arrowprops=dict(arrowstyle='<->', color=INK, lw=0.8))
    a.text(xa + (0.05 if fin != 'left' else -0.05), D_FIN / 2, f'{D_FIN} m', ha='left' if fin != 'left' else 'right',
           va='center', fontsize=8)
    glass = f'window {W_WIN} m' if n_win == 1 else f'{n_win} windows × {wn:.2f} m'
    a.text(span / 2, -0.75, f'{glass}, shaded strips coloured', ha='center', va='top', fontsize=8, color=MUTED)
    a.set_xlim(-1.8, span + 1.8); a.set_ylim(-1.1, 2.7)
    n_fins = n_win * (2 if fin == 'both' else 1)
    side_txt = '' if fin == 'both' else f' on the {sides[0 if fin == "left" else 1]} side'
    what = f'side fin{"s" if n_fins > 1 else ""}{side_txt}'
    a.set_title(f'(a) Plan: sun past {D_FIN} m {what}, {name.lower()}', loc='left', fontsize=9)
    b.bar(x - w / 2, m0, w, color=ORANGE, label='Without fins')
    lab = (f'With {D_FIN} m fin' if n_fins == 1 else f'With {n_fins} × {D_FIN} m fins') +         (', both sides' if fin == 'both' else side_txt)
    b.bar(x + w / 2, m1, w, color=VIOLET, label=lab)
    b.set_xticks(x, list(MONTHS)); b.set_ylabel('Direct radiation on window, kWh/m² per month')
    b.legend(frameon=False, loc='upper right'); b.set_ylim(0, 70); b.set_facecolor(SURF)
    b.grid(axis='y', color=GRID); b.set_axisbelow(True)
    for s in ('top', 'right'): b.spines[s].set_visible(False)
    b.set_title(f'(b) Direct sun on the {name.lower()} window{"s" if n_win > 1 else ""}, 2050 TMY', loc='left', fontsize=9)
    save(fig, 'side-fins' + ('' if name == 'South' else '-' + name.lower()) + ('' if n_win == 1 else f'-{n_win}win'))


fins_figure('South', 0.0, (9, 14), ('E', 'W'))
fins_figure('East', -np.pi / 2, (9, 11), ('N', 'S'), fin='right')
fins_figure('West', np.pi / 2, (13, 15), ('S', 'N'), fin='left')
fins_figure('East', -np.pi / 2, (9, 11), ('N', 'S'), fin='right', n_win=2)
fins_figure('West', np.pi / 2, (13, 15), ('S', 'N'), fin='left', n_win=2)
