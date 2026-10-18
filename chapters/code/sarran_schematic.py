# Writes sarran-schematic.svg/.png: the apartment floor heating installation in Sarran et al. (2022),
# with the measured and the virtually sensed variables. Redrawn from their Fig. 3 (CC BY 4.0).
import math, sys
from pathlib import Path
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "figures" / "c1"
W, H = 1180, 600
RED, BLUE, INK, GR, PUR = "#d0663a", "#2b7bb9", "#222", "#777", "#7d5ba6"
MEAS_IN, MEAS_OUT, VIRT = "#c4302a", "#1f5fbf", "#1b8a8a"
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Helvetica, Arial, sans-serif">',
     f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
def t(x, y, s, size=13, a="start", w="normal", f=INK):
    o.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{a}" font-weight="{w}" fill="{f}">{s}</text>')
def line(pts, col, wdt=4, dash=None, halo=False):
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    if halo: o.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{wdt+8}"/>')
    o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{wdt}" stroke-linejoin="round"' + (f' stroke-dasharray="{dash}"' if dash else "") + '/>')
def flow(x, y, ang, col):
    a = math.radians(ang); p = [(x + 9 * math.cos(a), y + 9 * math.sin(a))]
    for s in (2.5, -2.5): p.append((x + 9 * math.cos(a + s), y + 9 * math.sin(a + s)))
    o.append('<path d="M' + " L".join(f"{u:.1f} {v:.1f}" for u, v in p) + f' Z" fill="{col}"/>')
def pump(x, y, ang=0):
    o.append(f'<circle cx="{x}" cy="{y}" r="15" fill="#fff" stroke="{INK}" stroke-width="1.6"/>')
    p = [(x + 15 * math.cos(math.radians(ang + d)), y + 15 * math.sin(math.radians(ang + d))) for d in (0, 120, 240)]
    o.append('<path d="M' + " L".join(f"{u:.1f} {v:.1f}" for u, v in p) + f' Z" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')
def check(x, y):
    o.append(f'<path d="M{x-10} {y+12} L{x+10} {y+12} L{x} {y} Z" fill="#fff" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')
    o.append(f'<path d="M{x-10} {y-12} L{x+10} {y-12} L{x} {y} Z" fill="{INK}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')
def mvalve(x, y):           # 2-way valve with a motor actuator
    o.append(f'<path d="M{x-12} {y-10} L{x+12} {y+10} L{x+12} {y-10} L{x-12} {y+10} Z" fill="#fff" stroke="{INK}" stroke-width="1.6"/>')
    o.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y-20}" stroke="{INK}" stroke-width="1.6"/>')
    o.append(f'<circle cx="{x}" cy="{y-31}" r="11" fill="#fff" stroke="{INK}" stroke-width="1.6"/>'); t(x, y - 26, "M", 12, "middle", "bold")
def onoff(x, y):            # on/off valve with wax actuator on a vertical return outlet
    o.append(f'<rect x="{x-8}" y="{y-8}" width="16" height="16" fill="#fff" stroke="{INK}" stroke-width="1.4"/>'); t(x, y + 4, "T", 10, "middle", "bold")
def dot(x, y, kind):        # kind: "in" measured model input, "out" measured model output, "virt" virtually sensed
    if kind == "virt": o.append(f'<circle cx="{x}" cy="{y}" r="6.5" fill="#fff" stroke="{VIRT}" stroke-width="2.6"/>')
    else: o.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{MEAS_IN if kind == "in" else MEAS_OUT}" stroke="#fff" stroke-width="1.5"/>')
def lead(x0, y0, x1, y1): o.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="#999" stroke-width="1"/>')
COL = {"in": MEAS_IN, "out": MEAS_OUT, "virt": VIRT}

XR, XS, YS, YR = 50, 95, 175, 330
XM, XV = 375, 290
# risers
line([(XS, 50), (XS, 470)], RED); line([(XR, 50), (XR, 470)], BLUE)
flow(XS, 110, -90, RED); flow(XR, 110, 90, BLUE)
t(XS - 5, 40, "district heating risers", 13, "start", "bold", GR)
# apartment box
o.append(f'<rect x="125" y="95" width="1040" height="400" rx="10" fill="none" stroke="#bbb" stroke-width="1.2" stroke-dasharray="6 5"/>')
t(1155, 485, "apartment", 13, "end", "bold", GR)
# supply branch and return branch (crossing the supply riser)
line([(XS, YS), (660, YS)], RED)
line([(660, YR), (XR, YR)], BLUE, halo=True); line([(XS, YR - 12), (XS, YR + 12)], RED)
flow(280, YS, 0, RED); flow(560, YR, 180, BLUE)
# bypass with check valve and motorized valve on the return
line([(XM, YR), (XM, YS)], PUR, 3); check(XM, (YS + YR) / 2); flow(XM, 215, -90, PUR)
t(XM - 16, (YS + YR) / 2 + 12, "bypass with", 12, "end", f=GR); t(XM - 16, (YS + YR) / 2 + 27, "check valve", 12, "end", f=GR)
mvalve(XV, YR); t(XV, YR + 32, "motorized valve", 12, "middle", f=GR)
# control of the mixed supply temperature
line([(440, YS + 8), (440, 225), (XV, 225), (XV, YR - 42)], GR, 1.2, "4 4")
# pump
pump(505, YS, 0); t(505, YS + 34, "pump", 12, "middle", f=GR)
# heat meter
o.append('<rect x="140" y="395" width="110" height="38" rx="5" fill="#f4f6f8" stroke="#555" stroke-width="1.3"/>'); t(195, 419, "heat meter", 12, "middle", "bold")
line([(160, YR), (160, 395)], GR, 1.2, "4 4"); line([(230, YR), (230, 395)], GR, 1.2, "4 4")
# measured and virtual points on the main circuit
dot(205, YS, "in"); t(205, YS - 22, "supply riser temperature", 12, "middle", f=MEAS_IN)
dot(230, YR, "out"); dot(160, YR, "out")
t(160, 455, "metered flow and return", 12, "start", f=MEAS_OUT); t(160, 470, "riser temperature", 12, "start", f=MEAS_OUT)
dot(440, YS, "virt"); t(452, YS - 16, "mixed supply temperature", 12, "end", f=VIRT)
dot(505, YS - 15, "out"); t(515, YS - 16, "pump current", 12, "start", f=MEAS_OUT)
dot(600, YS, "virt"); t(600, YS + 30, "total flow", 12, "middle", f=VIRT)

# manifolds and loops
o.append(f'<rect x="640" y="115" width="345" height="275" rx="8" fill="#faf6ef" stroke="#c9b48a" stroke-width="1.2"/>')
line([(650, YS), (760, YS)], RED, 9); line([(650, YR), (760, YR)], BLUE, 9)
MX = (680, 710, 740)
for x in MX[:2]:
    o.append(f'<line x1="{x}" y1="{YS+4}" x2="{x}" y2="{YS+40}" stroke="{RED}" stroke-width="2.2" stroke-dasharray="5 4"/>')
    o.append(f'<line x1="{x}" y1="{YR-4}" x2="{x}" y2="{YR-40}" stroke="{BLUE}" stroke-width="2.2" stroke-dasharray="5 4"/>')
    onoff(x, YR - 16)
t(695, YS + 60, "loops", 11, "middle", f=GR); t(695, YS + 74, "2 to 5", 11, "middle", f=GR)
yt, yb = YS + 20, YR - 52
pts = [(MX[2], YS), (MX[2], yt), (800, yt)]
for i, x in enumerate(range(800, 960, 26)):
    y0, y1 = (yt, yb) if i % 2 == 0 else (yb, yt)
    pts += [(x, y0), (x, y1)]
xe = pts[-1][0]
o.append('<path d="M' + " L".join(f"{x} {y}" for x, y in pts) + '" fill="none" stroke="#c46a3a" stroke-width="2.2" stroke-linejoin="round"/>')
line([(xe, pts[-1][1]), (xe, YR - 32), (MX[2], YR - 32), (MX[2], YR)], BLUE, 2.2)
onoff(MX[2], YR - 16)
t(870, 135, "loop 1, one room", 12, "middle", "bold", GR)
# points in the loop
dot(860, YR - 32, "virt"); dot(800, YR - 32, "virt"); dot(MX[2] + 14, YR - 16, "in")
dot(878, (yt + yb) / 2, "virt"); dot(965, 150, "in"); dot(974, 235, "virt")
# labels: right column
for (y, s, k, px, py) in ((150, "room temperature", "in", 965, 150), (270, "room heat output", "virt", 974, 235),
                          (220, "floor surface temperature", "virt", 878, (yt + yb) / 2)):
    lead(px + 7 if px > 960 else px + 7, py, 1000, y); t(1004, y + 4, s, 12, f=COL[k])
# labels below the manifold box
for (x, s, k, px, py) in ((690, "loop flow", "virt", MX[2], YS + 12), (800, "loop return temperature", "virt", 800, YR - 32),
                          (690, "valve status (on/off)", "in", MX[2] + 14, YR - 16)):
    pass
lead(860, YR - 26, 935, 420); t(935, 434, "loop flow", 12, "middle", f=VIRT)
lead(MX[2] + 14, YR - 9, 720, 420); t(720, 434, "valve status", 12, "middle", f=MEAS_IN); t(720, 449, "(open/closed)", 12, "middle", f=MEAS_IN)
lead(800, YR - 26, 825, 420); t(825, 434, "loop return", 12, "middle", f=VIRT); t(825, 449, "temperature", 12, "middle", f=VIRT)

# legend
ly = 545
for i, (k, s) in enumerate((("in", "measured, model input"), ("out", "measured, fitted output"), ("virt", "virtually sensed by the model"))):
    x = 140 + i * 260; dot(x, ly, k); t(x + 14, ly + 4, s, 12.5)
line([(930, ly - 8), (970, ly - 8)], RED, 3); t(976, ly - 4, "supply", 12)
line([(930, ly + 10), (970, ly + 10)], BLUE, 3); t(976, ly + 14, "return", 12)
o.append("</svg>")
svg = "\n".join(o)
(OUT / "sarran-schematic.svg").write_text(svg)
import cairosvg; cairosvg.svg2png(bytestring=svg.encode(), write_to=str(OUT / "sarran-schematic.png"), output_width=2000)
print("ok")
