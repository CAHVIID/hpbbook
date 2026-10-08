// Thermal Bridge Lab: draw a construction from rectangles, draw boundary edges on its surfaces,
// and see the 2D steady-state temperature field and heat flux (anywidget module for MyST).
// Same method as thermal_bridge.py, which is the documented reference version; both read the
// same case files. Generated from the standalone page by build_widget.py.

/* 2D steady-state conduction, cell-centred finite differences on a non-uniform structured
   grid, banded Cholesky solve. Every cell face between material and empty space is an
   exposed surface; it takes the condition of the boundary edge drawn on it (last drawn
   wins) and is adiabatic otherwise. */
function gradedSplit(L, hmin, hmax, ratio) {
  if (L <= 2 * hmin) return [L];
  const half = []; let acc = 0, h = hmin;
  while (acc + h <= L / 2 + 1e-15) { half.push(h); acc += h; h = Math.min(h * ratio, hmax); }
  const rest = L - 2 * acc, rev = half.slice().reverse();
  if (rest > 0.5 * half[half.length - 1]) return [...half, rest, ...rev];
  const f = L / (2 * acc);
  return [...half, ...rev].map(v => v * f);
}

function gridLines(coords, hmin, hmax, ratio) {
  const u = [...new Set(coords.map(v => Math.round(v * 1e9) / 1e9))].sort((a, b) => a - b);
  const out = [u[0]];
  for (let k = 0; k < u.length - 1; k++) {
    let x = u[k];
    for (const p of gradedSplit(u[k + 1] - u[k], hmin, hmax, ratio)) { x += p; out.push(x); }
    out[out.length - 1] = u[k + 1];
  }
  return Float64Array.from(out);
}

/* model = {
     rects: [{x0,y0,x1,y1,lambda}]                 later = on top
     bcs:   [{kind:'convective'|'temperature'|'flux'|'adiabatic', T, R, q}]
     segs:  [{orient:'v'|'h', c, a0, a1, bc}]       'v': x=c, y in [a0,a1];  'h': y=c, x in [a0,a1]
     mesh:  {hmin, hmax, ratio} }                   metres */
function solveModel(model) {
  const now = () => (typeof performance !== "undefined" ? performance : Date).now();
  const t0 = now();
  const rects = model.rects, segs = model.segs || [], bcs = model.bcs || [];
  if (!rects.length) return { error: "Draw a rectangle to start." };
  const hmin = Math.max(+model.mesh.hmin || 0.001, 1e-5);
  const hmax = Math.max(+model.mesh.hmax || hmin, hmin);
  const ratio = Math.max(+model.mesh.ratio || 1, 1);

  const xs = rects.flatMap(r => [r.x0, r.x1]), ys = rects.flatMap(r => [r.y0, r.y1]);
  const bx0 = Math.min(...xs), bx1 = Math.max(...xs), by0 = Math.min(...ys), by1 = Math.max(...ys);
  const inb = (v, a, b) => v > a + 1e-9 && v < b - 1e-9;
  for (const s of segs) {   // boundary ends become grid lines so a condition can stop mid-face
    const [cs, as, ca, cb, aa, ab] = s.orient === "v" ? [xs, ys, bx0, bx1, by0, by1] : [ys, xs, by0, by1, bx0, bx1];
    if (inb(s.c, ca, cb)) cs.push(s.c);
    for (const a of [s.a0, s.a1]) if (inb(a, aa, ab)) as.push(a);
  }
  const xl = gridLines(xs, hmin, hmax, ratio), yl = gridLines(ys, hmin, hmax, ratio);
  const nx = xl.length - 1, ny = yl.length - 1, n = nx * ny;
  const res = { xl, yl, nx, ny };
  const rowMajor = nx <= ny, bw = rowMajor ? nx : ny, W = bw + 1;
  if (n > 150000 || (n * bw * bw) / 2 > 4e8) {
    res.error = `Mesh too fine to solve live (${nx} × ${ny} cells). Increase h_min or h_max.`;
    return res;
  }
  const dx = new Float64Array(nx), dy = new Float64Array(ny), xc = new Float64Array(nx), yc = new Float64Array(ny);
  for (let i = 0; i < nx; i++) { dx[i] = xl[i + 1] - xl[i]; xc[i] = 0.5 * (xl[i] + xl[i + 1]); }
  for (let j = 0; j < ny; j++) { dy[j] = yl[j + 1] - yl[j]; yc[j] = 0.5 * (yl[j] + yl[j + 1]); }

  const owner = new Int32Array(n).fill(-1), k = new Float64Array(n).fill(NaN);
  rects.forEach((r, ri) => {
    let i0 = 0; while (i0 < nx && xc[i0] <= r.x0) i0++;
    let j0 = 0; while (j0 < ny && yc[j0] <= r.y0) j0++;
    for (let j = j0; j < ny && yc[j] < r.y1; j++)
      for (let i = i0; i < nx && xc[i] < r.x1; i++) { owner[j * nx + i] = ri; k[j * nx + i] = r.lambda; }
  });
  Object.assign(res, { dx, dy, xc, yc, owner, k });
  const act = c => k[c] === k[c];

  const ord = new Int32Array(n);
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) ord[j * nx + i] = rowMajor ? j * nx + i : i * ny + j;
  const A = new Float64Array(n * W), b = new Float64Array(n);
  const link = (c1, c2, g) => {
    let p = ord[c1], q = ord[c2]; if (p > q) { const t = p; p = q; q = t; }
    A[p * W] += g; A[q * W] += g; A[p * W + (q - p)] -= g;
  };
  const Gx = new Float64Array(ny * Math.max(nx - 1, 0)), Gy = new Float64Array(Math.max(ny - 1, 0) * nx);
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx - 1; i++) {
    const c = j * nx + i;
    if (act(c) && act(c + 1)) {
      const g = dy[j] / (dx[i] / (2 * k[c]) + dx[i + 1] / (2 * k[c + 1]));
      Gx[j * (nx - 1) + i] = g; link(c, c + 1, g);
    }
  }
  for (let j = 0; j < ny - 1; j++) for (let i = 0; i < nx; i++) {
    const c = j * nx + i;
    if (act(c) && act(c + nx)) {
      const g = dx[i] / (dy[j] / (2 * k[c]) + dy[j + 1] / (2 * k[c + nx]));
      Gy[j * nx + i] = g; link(c, c + nx, g);
    }
  }

  // exposed faces
  const tol = 1e-7;
  const findSeg = (orient, coord, along) => {
    for (let s = segs.length - 1; s >= 0; s--) {
      const g = segs[s];
      if (g.orient === orient && Math.abs(g.c - coord) < tol && along > g.a0 - tol && along < g.a1 + tol) return s;
    }
    return -1;
  };
  const faces = [], segFaces = new Int32Array(segs.length);
  let fixed = 0;
  const addFace = (c, dir, x0, y0, x1, y1, area, d) => {
    const orient = x0 === x1 ? "v" : "h";
    const s = orient === "v" ? findSeg("v", x0, (y0 + y1) / 2) : findSeg("h", y0, (x0 + x1) / 2);
    const bi = s >= 0 ? segs[s].bc : -1, bc = bi >= 0 ? bcs[bi] : null;
    const f = { c, dir, x0, y0, x1, y1, area, d, seg: s, bi, G: 0, q: 0 };
    if (s >= 0) segFaces[s]++;
    const p = ord[c];
    if (bc && (bc.kind === "convective" || bc.kind === "temperature")) {
      const R = bc.kind === "temperature" ? 0 : Math.max(+bc.R || 0, 0);
      f.G = area / (d / k[c] + R); A[p * W] += f.G; b[p] += f.G * (+bc.T || 0); fixed++;
    } else if (bc && bc.kind === "flux") {
      f.q = +bc.q || 0; b[p] += f.q * area;
    }
    faces.push(f);
  };
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
    const c = j * nx + i; if (!act(c)) continue;
    if (i === 0 || !act(c - 1)) addFace(c, "left", xl[i], yl[j], xl[i], yl[j + 1], dy[j], dx[i] / 2);
    if (i === nx - 1 || !act(c + 1)) addFace(c, "right", xl[i + 1], yl[j], xl[i + 1], yl[j + 1], dy[j], dx[i] / 2);
    if (j === 0 || !act(c - nx)) addFace(c, "bottom", xl[i], yl[j], xl[i + 1], yl[j], dx[i], dy[j] / 2);
    if (j === ny - 1 || !act(c + nx)) addFace(c, "top", xl[i], yl[j + 1], xl[i + 1], yl[j + 1], dx[i], dy[j] / 2);
  }
  res.faces = faces; res.segFaces = segFaces;
  if (!fixed) {
    res.error = "No surface has a Convective or Temperature condition yet, so the temperature level is undefined. Draw a boundary along a surface.";
    return res;
  }
  for (let c = 0; c < n; c++) if (!act(c)) A[ord[c] * W] = 1;

  // banded Cholesky, L(i,m) stored at L[i*W + (i-m)]
  const L = new Float64Array(n * W);
  for (let i = 0; i < n; i++) {
    const kmin = Math.max(0, i - bw), iW = i * W;
    for (let kk = kmin; kk <= i; kk++) {
      let s = kk === i ? A[iW] : A[kk * W + (i - kk)];
      const kW = kk * W, mmin = Math.max(kmin, kk - bw);
      for (let m = mmin; m < kk; m++) s -= L[iW + (i - m)] * L[kW + (kk - m)];
      if (kk === i) {
        if (!(s > 1e-12 * A[iW])) {
          res.error = "A part of the construction has no Convective or Temperature surface, so its temperature is undefined. Connect it, or draw a boundary on it.";
          return res;
        }
        L[iW] = Math.sqrt(s);
      } else L[iW + (i - kk)] = s / L[kW];
    }
  }
  const y = new Float64Array(n);
  for (let i = 0; i < n; i++) {
    let s = b[i]; const iW = i * W;
    for (let m = Math.max(0, i - bw); m < i; m++) s -= L[iW + (i - m)] * y[m];
    y[i] = s / L[iW];
  }
  for (let i = n - 1; i >= 0; i--) {
    let s = y[i];
    for (let r = i + 1; r <= Math.min(n - 1, i + bw); r++) s -= L[r * W + (r - i)] * y[r];
    y[i] = s / L[i * W];
  }
  const T = new Float64Array(n);
  for (let c = 0; c < n; c++) T[c] = act(c) ? y[ord[c]] : NaN;

  // fluxes
  const fx = new Float64Array(ny * (nx + 1)), fy = new Float64Array((ny + 1) * nx);
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx - 1; i++) {
    const g = Gx[j * (nx - 1) + i], c = j * nx + i;
    if (g) fx[j * (nx + 1) + i + 1] = g * (T[c] - T[c + 1]) / dy[j];
  }
  for (let j = 0; j < ny - 1; j++) for (let i = 0; i < nx; i++) {
    const g = Gy[j * nx + i], c = j * nx + i;
    if (g) fy[(j + 1) * nx + i] = g * (T[c] - T[c + nx]) / dx[i];
  }
  const bcRes = bcs.map(() => ({ Q: 0, tmin: Infinity, tmax: -Infinity, n: 0 }));
  for (const f of faces) {
    if (f.bi < 0) continue;
    const bc = bcs[f.bi], Tc = T[f.c];
    let Q = 0;
    if (bc.kind === "flux") Q = f.q * f.area;
    else if (bc.kind !== "adiabatic") Q = f.G * ((+bc.T || 0) - Tc);
    const qn = Q / f.area, Ts = Tc + qn * f.d / k[f.c];
    f.Q = Q; f.Ts = Ts;
    const br = bcRes[f.bi]; br.Q += Q; br.n++;
    if (Ts < br.tmin) br.tmin = Ts; if (Ts > br.tmax) br.tmax = Ts;
    const j = Math.floor(f.c / nx), i = f.c - j * nx;
    if (f.dir === "left") fx[j * (nx + 1) + i] = qn;
    else if (f.dir === "right") fx[j * (nx + 1) + i + 1] = -qn;
    else if (f.dir === "bottom") fy[j * nx + i] = qn;
    else fy[(j + 1) * nx + i] = -qn;
  }
  const qx = new Float64Array(n), qy = new Float64Array(n), qm = new Float64Array(n);
  let Tmin = Infinity, Tmax = -Infinity, qmax = 0;
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
    const c = j * nx + i;
    if (!act(c)) { qx[c] = qy[c] = qm[c] = NaN; continue; }
    qx[c] = 0.5 * (fx[j * (nx + 1) + i] + fx[j * (nx + 1) + i + 1]);
    qy[c] = 0.5 * (fy[j * nx + i] + fy[(j + 1) * nx + i]);
    qm[c] = Math.hypot(qx[c], qy[c]);
    if (T[c] < Tmin) Tmin = T[c]; if (T[c] > Tmax) Tmax = T[c]; if (qm[c] > qmax) qmax = qm[c];
  }
  const qs = Array.from(qm).filter(v => v > 0).sort((a, b) => a - b);
  const qlo = Math.max(qs.length ? qs[Math.floor(qs.length * 0.02)] : 1e-3, qmax * 1e-5, 1e-6);
  Object.assign(res, { T, qx, qy, qm, Tmin, Tmax, qmax, qlo, bcRes, ms: now() - t0 });
  return res;
}

export { solveModel, gradedSplit, gridLines };

// One HTML file that runs the app on its own: this module inlined, plus a model to start from.
export function standaloneHtml(moduleSource, caseJson) {
  const safe = s => s.replace(/<\/(script)/gi, "<\\/$1");
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Thermal Bridge Lab</title>
<style>html,body{margin:0;height:100%;background:#fff}@media (prefers-color-scheme: dark){html,body{background:#0d1117}}</style>
</head><body><div id="app"></div>
<script type="module">
${safe(moduleSource)}
const START_CASE = ${caseJson ? safe(caseJson) : "null"};
render({ model: { get: k => (k === "case" ? START_CASE : null), on() {}, set() {} }, el: document.getElementById("app"), standalone: true });
</` + `script></body></html>
`;
}

const CSS = `
:host, .tb {
  --bg: #ffffff; --panel: #f6f8fa; --ink: #1f2328; --muted: #5f6770; --line: #d6dbe0;
  --accent: #b5461d; --accent-soft: #f3ddd2; --board: #fbfcfd; --grid: #e8ecf0; --grid-major: #cfd6dd;
  --ok: #2f7d4f; --bad: #b3261e;
  --f-body: system-ui, -apple-system, "Segoe UI", sans-serif;
  --f-mono: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark) {
  :host, .tb {
    --bg: #0d1117; --panel: #161b22; --ink: #e6edf3; --muted: #9aa4ae; --line: #30363d;
    --accent: #ee7b48; --accent-soft: #3a2419; --board: #0d1117; --grid: #171e27; --grid-major: #263240;
    --ok: #5cc28a; --bad: #f2867c;
  }
}
.tb { font-family: var(--f-body); font-size: 14px; color: var(--ink); display: flex; flex-direction: column; gap: 8px; }
.tb *, .tb *::before, .tb *::after { box-sizing: border-box; }
.tb h2 { font-size: 0.72rem; font-weight: 650; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted);
  margin: 0; display: flex; align-items: center; gap: 8px; border: 0; padding: 0; }
.tb h2 .tail { margin-left: auto; text-transform: none; letter-spacing: 0; font-weight: 500; }
.tb section { display: flex; flex-direction: column; gap: 8px; min-width: 0; }
.tb .hint { color: var(--muted); font-size: 0.8rem; margin: 0; line-height: 1.4; }
.tb button, .tb select, .tb input, .tb textarea { font: inherit; color: var(--ink); }
.tb .btn { border: 1px solid var(--line); background: var(--board); border-radius: 6px; padding: 4px 10px; cursor: pointer; font-size: 0.84rem; }
.tb .btn:hover { border-color: var(--muted); }
.tb .btn.primary { background: var(--accent); border-color: var(--accent); color: #fff; }
.tb .btn:disabled { opacity: 0.45; cursor: default; }
.tb button:focus-visible, .tb select:focus-visible, .tb input:focus-visible, .tb .row:focus-visible, .tb canvas:focus-visible, .tb .bc-card:focus-visible {
  outline: 2px solid var(--accent); outline-offset: 1px; }
.tb .seg { display: inline-flex; flex-wrap: wrap; border: 1px solid var(--line); border-radius: 7px; overflow: hidden; background: var(--board); }
.tb .seg button { border: 0; background: transparent; padding: 5px 9px; cursor: pointer; font-size: 0.82rem; border-right: 1px solid var(--line); color: var(--muted); }
.tb .seg button:last-child { border-right: 0; }
.tb .seg button[aria-pressed="true"] { background: var(--accent-soft); color: var(--ink); font-weight: 600; }
.tb input[type="number"], .tb input[type="text"], .tb select { background: var(--board); border: 1px solid var(--line); border-radius: 5px;
  padding: 3px 6px; min-width: 0; width: 100%; font-size: 0.84rem; }
.tb .toolbar select { width: auto; }
.tb input[type="number"] { font-family: var(--f-mono); font-variant-numeric: tabular-nums; }
.tb input[type="color"] { width: 22px; height: 22px; border: 1px solid var(--line); border-radius: 4px; padding: 0; background: none; cursor: pointer; flex: none; }
.tb label.field { display: flex; flex-direction: column; gap: 3px; font-size: 0.74rem; color: var(--muted); min-width: 0; }
.tb .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.tb .grid3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
.tb .check { display: inline-flex; align-items: center; gap: 5px; font-size: 0.84rem; cursor: pointer; white-space: nowrap; }
.tb .list { display: flex; flex-direction: column; gap: 2px; }
.tb .row { display: grid; align-items: center; gap: 6px; padding: 3px 6px; border-radius: 6px; border: 1px solid transparent; cursor: pointer; min-width: 0; }
.tb .row:hover { background: var(--board); }
.tb .row[aria-selected="true"] { border-color: var(--accent); background: var(--board); }
.tb .mat-row { grid-template-columns: 22px minmax(0, 1fr) 74px 16px; gap: 4px; }
.tb .layer-row, .tb .edge-row { grid-template-columns: 14px minmax(0, 1fr) auto; }
.tb .swatch { width: 14px; height: 14px; border-radius: 3px; border: 1px solid rgba(0,0,0,.25); }
.tb .swatch.line { height: 5px; border-radius: 3px; border: 0; }
.tb .row .name { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 0.84rem; }
.tb .row .dim { font-family: var(--f-mono); font-size: 0.7rem; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.tb .row .dim.warn { color: var(--bad); }
.tb .row input[type="text"] { border-color: transparent; background: transparent; padding: 2px 4px; }
.tb .row input[type="text"]:focus { border-color: var(--line); background: var(--board); }
.tb .icon-btn { border: 0; background: transparent; cursor: pointer; color: var(--muted); padding: 0 3px; font-size: 0.9rem; line-height: 1; }
.tb .icon-btn:hover { color: var(--ink); }
.tb .layer-tools { display: inline-flex; gap: 2px; }
.tb .unit { font-family: var(--f-mono); font-size: 0.7rem; color: var(--muted); }
.tb .bc-card { border: 1px solid var(--line); border-radius: 7px; padding: 6px 8px; display: grid; gap: 6px; background: var(--panel); cursor: pointer; }
.tb .bc-card[aria-selected="true"] { border-color: var(--accent); background: var(--board); }
.tb .bc-card .head { display: grid; grid-template-columns: 22px minmax(0, 1fr) 16px; gap: 6px; align-items: center; }
.tb .bc-card .params { display: grid; grid-template-columns: 1.3fr 1fr 1fr; gap: 6px; }
.tb .bc-card .params.two { grid-template-columns: 1.3fr 2fr; }
.tb .bc-card .params.one { grid-template-columns: 1fr; }
.tb .toolbar { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }
.tb .toolbar .spacer { flex: 1; }
.tb .board { position: relative; height: 520px; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; background: var(--board); }
.tb canvas { position: absolute; inset: 0; width: 100%; height: 100%; touch-action: none; display: block; }
.tb .status { position: absolute; left: 10px; top: 10px; font-size: 0.76rem; padding: 2px 8px; border-radius: 99px; background: var(--panel);
  border: 1px solid var(--line); color: var(--muted); font-family: var(--f-mono); pointer-events: none; }
.tb .status.err { color: var(--bad); border-color: var(--bad); white-space: normal; max-width: calc(100% - 20px); font-family: var(--f-body); border-radius: 8px; }
.tb .status.stale { color: var(--accent); border-color: var(--accent); }
.tb .tip { position: absolute; right: 10px; top: 10px; max-width: 260px; font-size: 0.76rem; padding: 6px 9px; border-radius: 8px; background: var(--panel);
  border: 1px solid var(--line); color: var(--muted); pointer-events: none; line-height: 1.4; }
.tb .footer-bar { display: flex; flex-wrap: wrap; gap: 6px 18px; align-items: center; min-height: 24px; }
.tb .legend { display: flex; align-items: center; gap: 8px; font-family: var(--f-mono); font-size: 0.74rem; color: var(--muted); flex-wrap: wrap; }
.tb .legend .bar { width: 160px; height: 10px; border-radius: 3px; border: 1px solid var(--line); }
.tb .readout { font-family: var(--f-mono); font-size: 0.74rem; color: var(--muted); font-variant-numeric: tabular-nums; }
.tb .panels { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 10px; }
.tb .card { border: 1px solid var(--line); border-radius: 8px; background: var(--panel); padding: 10px; display: flex; flex-direction: column; gap: 16px; min-width: 0; }
.tb .kpis { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
.tb .kpi { border: 1px solid var(--line); border-radius: 6px; padding: 6px 8px; background: var(--board); min-width: 0; }
.tb .kpi .k { font-size: 0.68rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }
.tb .kpi .v { font-family: var(--f-mono); font-size: 1rem; font-variant-numeric: tabular-nums; margin-top: 2px; }
.tb .kpi .v small { font-size: 0.68rem; color: var(--muted); }
.tb table.flows { width: 100%; border-collapse: collapse; font-size: 0.78rem; margin: 0; }
.tb table.flows th { text-align: left; font-weight: 500; color: var(--muted); font-size: 0.68rem; padding: 3px 4px; border-bottom: 1px solid var(--line); background: none; }
.tb table.flows td { padding: 3px 4px; border-bottom: 1px solid var(--line); font-family: var(--f-mono); font-variant-numeric: tabular-nums; }
.tb table.flows td:first-child { font-family: var(--f-body); }
.tb table.flows td.num, .tb table.flows th.num { text-align: right; }
.tb .balance { font-size: 0.72rem; color: var(--muted); font-family: var(--f-mono); }
.tb textarea { width: 100%; min-height: 110px; font-family: var(--f-mono); font-size: 0.7rem; background: var(--board); border: 1px solid var(--line); border-radius: 6px; padding: 6px; resize: vertical; }
.tb details summary { cursor: pointer; font-size: 0.8rem; color: var(--muted); }
.tb .btns { display: flex; gap: 6px; flex-wrap: wrap; }
.tb .msg { font-size: 0.78rem; color: var(--muted); }
.tb .msg.err { color: var(--bad); }
.tb [hidden] { display: none !important; }
@media (max-width: 600px) { .tb .board { height: 420px; } .tb .tip { display: none; } }
.tb.full { position: fixed; inset: 0; z-index: 2147483000; background: var(--bg); padding: 12px 16px;
  display: grid; grid-template-columns: minmax(0, 1fr) 360px; grid-template-rows: auto auto minmax(0, 1fr) auto;
  gap: 8px 14px; overflow: hidden; }
.tb.full > .toolbar, .tb.full > .board, .tb.full > .footer-bar { grid-column: 1; }
.tb.full > .sa-head { grid-column: 1 / -1; display: flex; align-items: baseline; gap: 6px 16px; flex-wrap: wrap; padding-bottom: 2px; }
.tb.full:has(> .sa-head) { grid-template-rows: auto auto auto minmax(0, 1fr) auto; }
.tb.full:has(> .sa-head) > .panels { grid-row: 2 / -1; }
.tb .sa-head h1 { margin: 0; font-size: 1.6rem; font-weight: 700; letter-spacing: 0.01em; font-stretch: 80%; line-height: 1.2; }
.tb .sa-head h1 span { color: var(--accent); }
.tb .sa-head .sub { margin: 0; color: var(--muted); font-size: 0.92rem; }
.tb .sa-head .keys { margin: 0 0 0 auto; color: var(--muted); font-size: 0.78rem; font-family: var(--f-mono); }
.tb kbd { font-family: var(--f-mono); font-size: 0.72rem; border: 1px solid var(--line); border-bottom-width: 2px; border-radius: 4px; padding: 0 4px; background: var(--panel); color: var(--ink); }
.tb.full > .board { height: auto; min-height: 0; }
.tb.full > .panels { grid-column: 2; grid-row: 1 / -1; grid-template-columns: 1fr; overflow: auto; align-content: start; min-height: 0; }
@media (max-width: 900px) {
  .tb.full { display: flex; flex-direction: column; overflow: auto; }
  .tb .sa-head .keys { display: none; }
  .tb.full > .board { height: 70vh; flex: none; }
}
`;

const MARKUP = `
<div class="toolbar">
  <div class="seg" role="group" aria-label="Tool">
    <button id="tool-select" type="button" aria-pressed="true" title="Select and move (V)">Select</button>
    <button id="tool-draw" type="button" aria-pressed="false" title="Draw rectangles (D)">Draw</button>
    <button id="tool-edge" type="button" aria-pressed="false" title="Draw boundary (B)">Boundary</button>
  </div>
  <label class="check">Snap
    <select id="snap" aria-label="Snap to grid">
      <option value="0">edges only</option>
      <option value="0.0005">0.5 mm</option>
      <option value="0.001">1 mm</option>
      <option value="0.005">5 mm</option>
      <option value="0.01">10 mm</option>
      <option value="0.05">50 mm</option>
    </select>
  </label>
  <span class="spacer"></span>
  <label class="check"><input type="checkbox" id="live" checked> Live</label>
  <button class="btn primary" id="solve-btn" type="button" disabled>Solve</button>
  <button class="btn" id="fit-btn" type="button">Fit view</button>
  <button class="btn" id="app-btn" type="button" title="Download the app as one HTML file that runs on its own, with the current model">Download stand-alone app</button>
</div>
<div class="toolbar">
  <div class="seg" role="group" aria-label="Show">
    <button type="button" data-disp="geometry" aria-pressed="false">Geometry</button>
    <button type="button" data-disp="mesh" aria-pressed="false">Mesh</button>
    <button type="button" data-disp="temperature" aria-pressed="true">Temperature</button>
    <button type="button" data-disp="flux" aria-pressed="false">Heat flux</button>
  </div>
  <label class="check"><input type="checkbox" id="iso" checked> Isotherms</label>
</div>
<div class="board" id="board">
  <canvas id="cv" tabindex="0" aria-label="Drawing board: rectangles of material, boundary edges and the computed field"></canvas>
  <div class="status" id="status">–</div>
  <div class="tip" id="tip" hidden></div>
</div>
<div class="footer-bar">
  <div class="legend" id="legend"></div>
  <div class="readout" id="readout">Hover the board to read values.</div>
</div>
<div class="panels">
  <div class="card">
    <section>
      <h2>Results <span class="tail unit" id="solve-time"></span></h2>
      <div class="kpis">
        <div class="kpi"><div class="k">Heat flow Φ</div><div class="v" id="k-phi">–</div></div>
        <div class="kpi"><div class="k">L<sub>2D</sub></div><div class="v" id="k-l2d">–</div></div>
        <div class="kpi"><div class="k">Min. inside surface</div><div class="v" id="k-tsi">–</div></div>
        <div class="kpi"><div class="k">f<sub>Rsi</sub></div><div class="v" id="k-frsi">–</div></div>
      </div>
      <table class="flows">
        <thead><tr><th>Boundary</th><th class="num">Φ in [W/m]</th><th class="num">T<sub>s</sub> min…max [°C]</th></tr></thead>
        <tbody id="flow-body"></tbody>
      </table>
      <div class="balance" id="balance"></div>
    </section>
  </div>
  <div class="card">
    <section>
      <h2>Boundary conditions</h2>
      <p class="hint">Pick one, then use <b>Boundary</b>: click a surface to assign the whole straight face, or drag along it to assign part. Surfaces without a boundary are adiabatic.</p>
      <div id="bc-list" style="display:flex;flex-direction:column;gap:6px"></div>
      <div class="btns"><button class="btn" id="bc-add" type="button">Add boundary condition</button></div>
    </section>
    <section>
      <h2>Boundary edges <span class="tail unit" id="edge-count"></span></h2>
      <div class="list" id="edge-list"></div>
      <div id="edge-fields" hidden>
        <div class="grid3">
          <label class="field"><span id="ef-c-label">x [mm]</span><input id="ef-c" type="number" step="any"></label>
          <label class="field"><span id="ef-a0-label">from y [mm]</span><input id="ef-a0" type="number" step="any"></label>
          <label class="field"><span id="ef-a1-label">to y [mm]</span><input id="ef-a1" type="number" step="any"></label>
        </div>
        <label class="field" style="margin-top:8px">Boundary condition<select id="ef-bc"></select></label>
        <div class="btns" style="margin-top:8px"><button class="btn" id="ef-del" type="button">Delete edge</button></div>
      </div>
    </section>
  </div>
  <div class="card">
    <section>
      <h2>Materials <span class="tail unit">λ in W/(m·K)</span></h2>
      <p class="hint">Pick the material to draw with. Edit names and λ directly.</p>
      <div class="list" id="mat-list"></div>
      <label class="field">Add from library<select id="mat-add"><option value="">Choose a material…</option></select></label>
    </section>
    <section>
      <h2>Layers <span class="tail unit">front on top</span></h2>
      <div class="list" id="layer-list"></div>
    </section>
    <section>
      <h2>Selected rectangle</h2>
      <p class="hint" id="sel-empty">Click a rectangle on the board or in the layer list.</p>
      <div id="sel-fields" hidden>
        <div class="grid2">
          <label class="field">x [mm]<input id="sel-x" type="number" step="any"></label>
          <label class="field">y [mm]<input id="sel-y" type="number" step="any"></label>
          <label class="field">width [mm]<input id="sel-w" type="number" step="any" min="0"></label>
          <label class="field">height [mm]<input id="sel-h" type="number" step="any" min="0"></label>
        </div>
        <label class="field" style="margin-top:8px">Material<select id="sel-mat"></select></label>
        <div class="btns" style="margin-top:8px">
          <button class="btn" id="sel-front" type="button">Bring to front</button>
          <button class="btn" id="sel-dup" type="button">Duplicate</button>
          <button class="btn" id="sel-del" type="button">Delete</button>
        </div>
      </div>
    </section>
  </div>
  <div class="card">
    <section>
      <h2>Mesh <span class="tail unit" id="mesh-count"></span></h2>
      <p class="hint">Grid lines follow every rectangle edge and boundary end. Cells start at the minimum size next to each line and grow by the ratio towards the middle, up to the maximum.</p>
      <div class="grid3">
        <label class="field">Min. cell [mm]<input id="m-hmin" type="number" step="any" min="0.01"></label>
        <label class="field">Max. cell [mm]<input id="m-hmax" type="number" step="any" min="0.01"></label>
        <label class="field">Growth ratio<input id="m-ratio" type="number" step="0.05" min="1"></label>
      </div>
    </section>
  </div>
  <div class="card">
    <section>
      <h2>Examples and case files</h2>
      <div class="btns">
        <button class="btn" id="ex-corner" type="button">Wall corner</button>
        <button class="btn" id="ex-stud" type="button">Steel stud in wall</button>
      </div>
      <div class="btns">
        <button class="btn" id="save-btn" type="button">Save case file</button>
        <button class="btn" id="open-btn" type="button">Open case file</button>
        <input id="file-in" type="file" accept=".json,application/json" hidden>
      </div>
      <details>
        <summary>Show or paste the case as JSON</summary>
        <div class="btns" style="margin:6px 0">
          <button class="btn" id="exp-btn" type="button">Show JSON</button>
          <button class="btn" id="copy-btn" type="button">Copy</button>
          <button class="btn" id="imp-btn" type="button">Load pasted JSON</button>
        </div>
        <textarea id="json" spellcheck="false" aria-label="Case JSON" placeholder="Paste a case here, then Load pasted JSON."></textarea>
      </details>
      <div class="msg" id="json-msg"></div>
    </section>
  </div>
</div>
`;

function render({ model, el: host, standalone = false }) {
  const style = document.createElement("style"); style.textContent = CSS;
  const root = document.createElement("div"); root.className = "tb"; root.innerHTML = MARKUP;
  host.appendChild(style); host.appendChild(root);
  if (standalone) {
    root.classList.add("full");
    const head = document.createElement("header"); head.className = "sa-head";
    head.innerHTML = `<h1>Thermal Bridge <span>Lab</span></h1>
      <p class="sub">Draw a construction from rectangles, mark its surfaces, watch heat find its way through.</p>
      <p class="keys"><kbd>V</kbd> select · <kbd>D</kbd> draw · <kbd>B</kbd> boundary · <kbd>Del</kbd> remove · wheel zoom · drag empty space to pan</p>`;
    root.prepend(head);
  }
  const PRESETS = [
    ["Concrete", 1.7, "#a6a49b"], ["Brick", 0.6, "#c06a4f"], ["Aerated concrete", 0.12, "#d7d1c0"],
    ["Mineral wool", 0.037, "#efc451"], ["EPS", 0.035, "#dde6ee"], ["PIR", 0.022, "#e6d48a"],
    ["Timber", 0.13, "#cf9b62"], ["Wood fibre board", 0.05, "#a97b55"], ["Gypsum board", 0.25, "#e8e1cf"],
    ["Steel", 50, "#566779"], ["Stainless steel", 17, "#7d8c9b"], ["Aluminium", 160, "#9cb1c6"],
    ["Glass", 1.0, "#9fd0d6"], ["Screed", 1.3, "#b9b6ab"], ["XPS", 0.034, "#8fc1e3"],
  ];
  const KIND_LABEL = { convective: "Convective", temperature: "Temperature", flux: "Heat flux", adiabatic: "Adiabatic" };
  const BC_COLORS = ["#d2452f", "#2f6fc4", "#8a52c9", "#2f9a6a", "#d18a1c", "#c43f8b"];

  let uid = 1;
  const nid = () => uid++;
  const preset = name => PRESETS.find(p => p[0] === name);
  const mkMat = name => { const p = preset(name); return { id: nid(), name: p[0], lambda: p[1], color: p[2] }; };
  const mkRect = (x0, y0, x1, y1, m) => ({ id: nid(), x0, y0, x1, y1, mat: m.id });
  const mkEdge = (bc, x0, y0, x1, y1) => x0 === x1
    ? { id: nid(), bc: bc.id, orient: "v", c: x0, a0: Math.min(y0, y1), a1: Math.max(y0, y1) }
    : { id: nid(), bc: bc.id, orient: "h", c: y0, a0: Math.min(x0, x1), a1: Math.max(x0, x1) };
  const defaultBCs = () => [
    { id: nid(), name: "Inside", kind: "convective", T: 20, R: 0.13, q: 0, color: BC_COLORS[0] },
    { id: nid(), name: "Outside", kind: "convective", T: 0, R: 0.04, q: 0, color: BC_COLORS[1] },
  ];
  const baseUI = () => ({ selected: null, selEdge: null, tool: "select", display: "temperature", iso: true, live: true, snap: 0.005 });

  function cornerExample() {
    // External wall corner in plan: 200 mm concrete, 200 mm insulation outside, room in the
    // inner corner. Flanking walls cut off 1 m from the inside corner (adiabatic cut planes).
    const con = mkMat("Concrete"), ins = mkMat("Mineral wool");
    const [bin, bout] = defaultBCs();
    return {
      materials: [con, ins], bcTypes: [bin, bout],
      rects: [
        mkRect(0, 0, 0.2, 1.4, ins), mkRect(0, 0, 1.4, 0.2, ins),
        mkRect(0.2, 0.2, 0.4, 1.4, con), mkRect(0.2, 0.2, 1.4, 0.4, con),
      ],
      edges: [
        mkEdge(bout, 0, 0, 0, 1.4), mkEdge(bout, 0, 0, 1.4, 0),
        mkEdge(bin, 0.4, 0.4, 0.4, 1.4), mkEdge(bin, 0.4, 0.4, 1.4, 0.4),
      ],
      mesh: { hmin: 0.002, hmax: 0.025, ratio: 1.3 },
      activeMat: con.id, activeBC: bin.id, ...baseUI(),
    };
  }
  function studExample() {
    const gyp = mkMat("Gypsum board"), mw = mkMat("Mineral wool"), wf = mkMat("Wood fibre board"), st = mkMat("Steel");
    const [bin, bout] = defaultBCs();
    return {
      materials: [gyp, mw, wf, st], bcTypes: [bin, bout],
      rects: [
        mkRect(0, 0, 0.013, 0.6, gyp), mkRect(0.013, 0, 0.213, 0.6, mw), mkRect(0.213, 0, 0.235, 0.6, wf),
        mkRect(0.013, 0.2995, 0.213, 0.3005, st), mkRect(0.013, 0.275, 0.014, 0.325, st), mkRect(0.212, 0.275, 0.213, 0.325, st),
      ],
      edges: [mkEdge(bin, 0, 0, 0, 0.6), mkEdge(bout, 0.235, 0, 0.235, 0.6)],
      mesh: { hmin: 0.0005, hmax: 0.01, ratio: 1.25 },
      activeMat: mw.id, activeBC: bin.id, ...baseUI(), snap: 0.001,
    };
  }

  // ------------------------------------------------------------------ state + persistence
  let S = cornerExample();
  function persist() { /* the book widget keeps no state between visits */ }

  let version = 1, R = null, needSolve = true, needRender = true;
  const matById = id => S.materials.find(m => m.id === id);
  const bcById = id => S.bcTypes.find(b => b.id === id);
  function changed(structure) {
    version++; needSolve = true; needRender = true; persist();
    if (structure) { buildLayers(); buildEdges(); }
    syncSelected(); syncEdgeFields();
    tick();
  }

  // ------------------------------------------------------------------ DOM helpers
  const $ = id => root.querySelector("#" + id);
  const activeEl = () => { const r = root.getRootNode(); return (r && r.activeElement) || document.activeElement; };
  const cv = $("cv"), ctx = cv.getContext("2d"), board = $("board");
  const view = { scale: 1000, ox: 60, oy: 400, w: 600, h: 400, fitted: false };
  const fmt = (v, d = 2) => (v === undefined || !isFinite(v)) ? "–" : v.toFixed(d);
  const mm = v => +(v * 1000).toFixed(3);
  const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; };
  const iconBtn = (txt, title, fn) => { const b = el("button", "icon-btn", txt); b.type = "button"; b.title = title; b.setAttribute("aria-label", title); b.addEventListener("click", e => { e.stopPropagation(); fn(); }); return b; };
  function flash(t, err) { const m = $("json-msg"); m.textContent = t; m.className = "msg" + (err ? " err" : ""); }

  // ---- materials
  function buildMaterials() {
    const list = $("mat-list"); list.innerHTML = "";
    for (const m of S.materials) {
      const row = el("div", "row mat-row"); row.tabIndex = 0;
      row.setAttribute("aria-selected", String(m.id === S.activeMat));
      row.title = "Draw with " + m.name;
      const color = el("input"); color.type = "color"; color.value = m.color; color.id = "mc-" + m.id;
      color.setAttribute("aria-label", "Colour of " + m.name);
      color.addEventListener("input", () => { m.color = color.value; needRender = true; persist(); buildLayers(); tick(); });
      const name = el("input"); name.type = "text"; name.value = m.name; name.id = "mn-" + m.id;
      name.setAttribute("aria-label", "Material name");
      name.addEventListener("input", () => { m.name = name.value || "Unnamed"; persist(); buildLayers(); fillMatSelect(); });
      const lam = el("input"); lam.type = "number"; lam.step = "any"; lam.min = "0"; lam.value = m.lambda; lam.id = "ml-" + m.id;
      lam.setAttribute("aria-label", "Thermal conductivity of " + m.name);
      lam.addEventListener("input", () => { const v = parseFloat(lam.value); if (v > 0) { m.lambda = v; changed(false); } });
      const del = iconBtn("×", "Remove material", () => {
        if (S.rects.some(r => r.mat === m.id)) { flashTip("That material is still used by a rectangle."); return; }
        S.materials = S.materials.filter(x => x !== m);
        if (S.activeMat === m.id) S.activeMat = S.materials[0]?.id ?? null;
        buildMaterials(); fillMatSelect(); persist();
      });
      row.append(color, name, lam, del);
      const pick = () => { S.activeMat = m.id; buildMaterials(); persist(); setTool("draw"); };
      row.addEventListener("click", e => { if (e.target === row) pick(); });
      row.addEventListener("keydown", e => { if (e.key === "Enter" && e.target === row) pick(); });
      list.append(row);
    }
  }
  const addSel = $("mat-add");
  for (const p of PRESETS) { const o = el("option", "", `${p[0]} · ${p[1]}`); o.value = p[0]; addSel.append(o); }
  { const o = el("option", "", "Custom material"); o.value = "__custom"; addSel.append(o); }
  addSel.addEventListener("change", () => {
    const v = addSel.value; addSel.value = ""; if (!v) return;
    const p = v === "__custom" ? ["Custom", 1.0, "#8aa39b"] : preset(v);
    let name = p[0], n = 2; while (S.materials.some(m => m.name === name)) name = `${p[0]} ${n++}`;
    const m = { id: nid(), name, lambda: p[1], color: p[2] };
    S.materials.push(m); S.activeMat = m.id; buildMaterials(); fillMatSelect(); persist(); setTool("draw");
  });

  // ---- layers
  function buildLayers() {
    const list = $("layer-list"); list.innerHTML = "";
    if (!S.rects.length) { list.append(el("p", "hint", "No rectangles yet. Choose Draw rectangle and drag on the board.")); return; }
    for (let idx = S.rects.length - 1; idx >= 0; idx--) {
      const r = S.rects[idx], m = matById(r.mat);
      const row = el("div", "row layer-row"); row.tabIndex = 0;
      row.setAttribute("aria-selected", String(r.id === S.selected));
      const sw = el("span", "swatch"); sw.style.background = m ? m.color : "transparent";
      const nm = el("div"); nm.style.minWidth = "0";
      nm.append(el("div", "name", m ? m.name : "(missing material)"), el("div", "dim", `${mm(r.x1 - r.x0)} × ${mm(r.y1 - r.y0)} mm`));
      const tools = el("span", "layer-tools");
      tools.append(iconBtn("↑", "Move forward", () => moveLayer(r.id, +1)), iconBtn("↓", "Move backward", () => moveLayer(r.id, -1)), iconBtn("×", "Delete rectangle", () => removeRect(r.id)));
      row.append(sw, nm, tools);
      row.addEventListener("click", () => select(r.id));
      row.addEventListener("keydown", e => { if (e.key === "Enter") select(r.id); });
      list.append(row);
    }
  }
  function moveLayer(id, dir) {
    const i = S.rects.findIndex(r => r.id === id), j = i + dir;
    if (i < 0 || j < 0 || j >= S.rects.length) return;
    [S.rects[i], S.rects[j]] = [S.rects[j], S.rects[i]]; changed(true);
  }
  function removeRect(id) { S.rects = S.rects.filter(r => r.id !== id); if (S.selected === id) S.selected = null; changed(true); }
  function select(id) {
    S.selected = id; if (id !== null) S.selEdge = null;
    buildLayers(); buildEdges(); syncSelected(); syncEdgeFields(); needRender = true; tick();
  }

  // ---- selected rectangle
  function fillMatSelect() {
    const s = $("sel-mat"), cur = s.value; s.innerHTML = "";
    for (const m of S.materials) { const o = el("option", "", `${m.name} (λ ${m.lambda})`); o.value = m.id; s.append(o); }
    s.value = cur;
  }
  function syncSelected() {
    const r = S.rects.find(x => x.id === S.selected);
    $("sel-empty").hidden = !!r; $("sel-fields").hidden = !r;
    if (!r) return;
    const set = (id, v) => { const e = $(id); if (activeEl() !== e) e.value = v; };
    set("sel-x", mm(r.x0)); set("sel-y", mm(r.y0)); set("sel-w", mm(r.x1 - r.x0)); set("sel-h", mm(r.y1 - r.y0));
    if (activeEl() !== $("sel-mat")) { fillMatSelect(); $("sel-mat").value = r.mat; }
  }
  ["sel-x", "sel-y", "sel-w", "sel-h"].forEach(id => $(id).addEventListener("input", () => {
    const r = S.rects.find(x => x.id === S.selected); if (!r) return;
    const x = parseFloat($("sel-x").value), y = parseFloat($("sel-y").value), w = parseFloat($("sel-w").value), h = parseFloat($("sel-h").value);
    if (![x, y, w, h].every(isFinite) || w <= 0 || h <= 0) return;
    r.x0 = x / 1000; r.y0 = y / 1000; r.x1 = (x + w) / 1000; r.y1 = (y + h) / 1000; changed(true);
  }));
  $("sel-mat").addEventListener("change", () => { const r = S.rects.find(x => x.id === S.selected); if (r) { r.mat = +$("sel-mat").value; changed(true); } });
  $("sel-del").addEventListener("click", () => S.selected && removeRect(S.selected));
  $("sel-front").addEventListener("click", () => { const i = S.rects.findIndex(r => r.id === S.selected); if (i >= 0) { S.rects.push(S.rects.splice(i, 1)[0]); changed(true); } });
  $("sel-dup").addEventListener("click", () => {
    const r = S.rects.find(x => x.id === S.selected); if (!r) return;
    const off = (r.x1 - r.x0) < 0.02 ? 0.01 : 0.02, c = { ...r, id: nid(), x0: r.x0 + off, x1: r.x1 + off };
    S.rects.push(c); S.selected = c.id; changed(true);
  });

  // ---- boundary conditions (types)
  function buildBCs() {
    const box = $("bc-list"); box.innerHTML = "";
    for (const bc of S.bcTypes) {
      const card = el("div", "bc-card"); card.tabIndex = 0;
      card.setAttribute("aria-selected", String(bc.id === S.activeBC));
      card.title = "Draw edges with " + bc.name;
      const head = el("div", "head");
      const color = el("input"); color.type = "color"; color.value = bc.color; color.id = "bcc-" + bc.id;
      color.setAttribute("aria-label", "Colour of " + bc.name);
      color.addEventListener("input", () => { bc.color = color.value; needRender = true; persist(); buildEdges(); tick(); });
      const name = el("input"); name.type = "text"; name.value = bc.name; name.id = "bcn-" + bc.id;
      name.setAttribute("aria-label", "Boundary condition name");
      name.addEventListener("input", () => { bc.name = name.value || "Unnamed"; persist(); buildEdges(); fillBCSelect(); showResults(); needRender = true; tick(); });
      const del = iconBtn("×", "Remove boundary condition", () => {
        if (S.edges.some(e => e.bc === bc.id)) { flashTip("Delete the edges that use this condition first."); return; }
        S.bcTypes = S.bcTypes.filter(x => x !== bc);
        if (S.activeBC === bc.id) S.activeBC = S.bcTypes[0]?.id ?? null;
        buildBCs(); fillBCSelect(); persist();
      });
      head.append(color, name, del);
      const params = el("div", "params");
      const kind = el("select"); kind.id = "bck-" + bc.id; kind.setAttribute("aria-label", "Type of " + bc.name);
      for (const kk of Object.keys(KIND_LABEL)) { const o = el("option", "", KIND_LABEL[kk]); o.value = kk; kind.append(o); }
      kind.value = bc.kind;
      kind.addEventListener("change", () => { bc.kind = kind.value; buildBCs(); changed(false); });
      const kindWrap = el("label", "field"); kindWrap.append(el("span", "", "type"), kind);
      params.append(kindWrap);
      const num = (key, label, unit) => {
        const inp = el("input"); inp.type = "number"; inp.step = "any"; inp.value = bc[key]; inp.id = `bc${key}-${bc.id}`;
        inp.title = label; inp.setAttribute("aria-label", `${label} of ${bc.name}`);
        inp.addEventListener("input", () => { const v = parseFloat(inp.value); if (isFinite(v)) { bc[key] = v; changed(false); } });
        const l = el("label", "field"); l.append(el("span", "", unit), inp); return l;
      };
      if (bc.kind === "convective") params.append(num("T", "Air temperature", "T [°C]"), num("R", "Surface resistance", "R [m²K/W]"));
      else if (bc.kind === "temperature") { params.className = "params two"; params.append(num("T", "Surface temperature", "T [°C]")); }
      else if (bc.kind === "flux") { params.className = "params two"; params.append(num("q", "Heat flux into the construction", "q [W/m²]")); }
      else params.className = "params one";
      card.append(head, params);
      const pick = () => { S.activeBC = bc.id; buildBCs(); persist(); setTool("edge"); };
      card.addEventListener("click", e => { if (e.target === card || e.target === head) pick(); });
      card.addEventListener("keydown", e => { if (e.key === "Enter" && e.target === card) pick(); });
      box.append(card);
    }
  }
  $("bc-add").addEventListener("click", () => {
    const n = S.bcTypes.length;
    const bc = { id: nid(), name: `Boundary ${n + 1}`, kind: "convective", T: 20, R: 0.13, q: 0, color: BC_COLORS[n % BC_COLORS.length] };
    S.bcTypes.push(bc); S.activeBC = bc.id; buildBCs(); fillBCSelect(); persist(); setTool("edge");
  });
  function fillBCSelect() {
    const s = $("ef-bc"), cur = s.value; s.innerHTML = "";
    for (const b of S.bcTypes) { const o = el("option", "", b.name); o.value = b.id; s.append(o); }
    s.value = cur;
  }

  // ---- boundary edges
  function edgeText(e) {
    return e.orient === "v" ? `x = ${mm(e.c)}, y ${mm(e.a0)}…${mm(e.a1)} mm` : `y = ${mm(e.c)}, x ${mm(e.a0)}…${mm(e.a1)} mm`;
  }
  function buildEdges() {
    const list = $("edge-list"); list.innerHTML = "";
    $("edge-count").textContent = S.edges.length ? `${S.edges.length} drawn` : "";
    if (!S.edges.length) { list.append(el("p", "hint", "No boundary edges yet. Every surface is adiabatic.")); return; }
    const fresh = R && R.version === version && R.segFaces;
    S.edges.forEach((e, idx) => {
      const b = bcById(e.bc);
      const row = el("div", "row edge-row"); row.tabIndex = 0;
      row.setAttribute("aria-selected", String(e.id === S.selEdge));
      const sw = el("span", "swatch line"); sw.style.background = b ? b.color : "transparent";
      const nm = el("div"); nm.style.minWidth = "0";
      const none = fresh && R.segFaces[idx] === 0;
      nm.append(el("div", "name", b ? b.name : "(missing)"), el("div", "dim" + (none ? " warn" : ""), none ? "Not on a surface: no effect" : edgeText(e)));
      row.append(sw, nm, iconBtn("×", "Delete edge", () => removeEdge(e.id)));
      row.addEventListener("click", () => selectEdge(e.id));
      row.addEventListener("keydown", ev => { if (ev.key === "Enter") selectEdge(e.id); });
      list.append(row);
    });
  }
  function removeEdge(id) { S.edges = S.edges.filter(e => e.id !== id); if (S.selEdge === id) S.selEdge = null; changed(true); }
  function selectEdge(id) {
    S.selEdge = id; if (id !== null) S.selected = null;
    buildLayers(); buildEdges(); syncSelected(); syncEdgeFields(); needRender = true; tick();
  }
  function syncEdgeFields() {
    const e = S.edges.find(x => x.id === S.selEdge);
    $("edge-fields").hidden = !e; if (!e) return;
    const [c, a] = e.orient === "v" ? ["x", "y"] : ["y", "x"];
    $("ef-c-label").textContent = `${c} [mm]`; $("ef-a0-label").textContent = `from ${a} [mm]`; $("ef-a1-label").textContent = `to ${a} [mm]`;
    const set = (id, v) => { const x = $(id); if (activeEl() !== x) x.value = v; };
    set("ef-c", mm(e.c)); set("ef-a0", mm(e.a0)); set("ef-a1", mm(e.a1));
    if (activeEl() !== $("ef-bc")) { fillBCSelect(); $("ef-bc").value = e.bc; }
  }
  ["ef-c", "ef-a0", "ef-a1"].forEach(id => $(id).addEventListener("input", () => {
    const e = S.edges.find(x => x.id === S.selEdge); if (!e) return;
    const c = parseFloat($("ef-c").value), a0 = parseFloat($("ef-a0").value), a1 = parseFloat($("ef-a1").value);
    if (![c, a0, a1].every(isFinite) || a1 <= a0) return;
    e.c = c / 1000; e.a0 = a0 / 1000; e.a1 = a1 / 1000; changed(true);
  }));
  $("ef-bc").addEventListener("change", () => { const e = S.edges.find(x => x.id === S.selEdge); if (e) { e.bc = +$("ef-bc").value; changed(true); } });
  $("ef-del").addEventListener("click", () => S.selEdge && removeEdge(S.selEdge));

  // ---- tools / display
  const TIPS = {
    select: "",
    draw: "Drag to draw a rectangle of the selected material. Later rectangles cover earlier ones.",
    edge: "Click a surface to assign the whole straight face, or drag along a surface to assign part of it.",
  };
  function setTool(t) {
    S.tool = t;
    $("tool-select").setAttribute("aria-pressed", String(t === "select"));
    $("tool-draw").setAttribute("aria-pressed", String(t === "draw"));
    $("tool-edge").setAttribute("aria-pressed", String(t === "edge"));
    cv.style.cursor = t === "select" ? "default" : "crosshair";
    const b = bcById(S.activeBC), m = matById(S.activeMat);
    const tip = $("tip");
    tip.hidden = !TIPS[t];
    tip.textContent = t === "edge" ? `${TIPS.edge} Condition: ${b ? b.name : "none"}.` : t === "draw" ? `${TIPS.draw} Material: ${m ? m.name : "none"}.` : "";
  }
  $("tool-select").addEventListener("click", () => setTool("select"));
  $("tool-draw").addEventListener("click", () => setTool("draw"));
  $("tool-edge").addEventListener("click", () => setTool("edge"));
  function syncSnap() { $("snap").value = String(S.snap); if ($("snap").value === "") { $("snap").value = "0.005"; S.snap = 0.005; } }
  $("snap").addEventListener("change", () => { S.snap = +$("snap").value; persist(); });

  function setDisplay(d) {
    S.display = d;
    root.querySelectorAll("[data-disp]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.disp === d)));
    needRender = true; persist(); tick();
  }
  root.querySelectorAll("[data-disp]").forEach(b => b.addEventListener("click", () => setDisplay(b.dataset.disp)));
  $("iso").addEventListener("change", () => { S.iso = $("iso").checked; needRender = true; persist(); tick(); });
  $("live").addEventListener("change", () => { S.live = $("live").checked; persist(); tick(); });
  $("solve-btn").addEventListener("click", () => { runSolve(); needRender = true; tick(); });
  $("fit-btn").addEventListener("click", () => { fitView(); needRender = true; tick(); });
  function updateSolveBtn() { $("solve-btn").disabled = S.live || !!(R && R.version === version); }

  // ---- mesh settings
  const meshInput = () => {
    const a = parseFloat($("m-hmin").value), b = parseFloat($("m-hmax").value), c = parseFloat($("m-ratio").value);
    if (a > 0) S.mesh.hmin = a / 1000; if (b > 0) S.mesh.hmax = b / 1000; if (c >= 1) S.mesh.ratio = c;
    changed(false);
  };
  ["m-hmin", "m-hmax", "m-ratio"].forEach(id => $(id).addEventListener("input", meshInput));

  // ---- case JSON
  function toCase() {
    const materials = {}; S.materials.forEach(m => materials[m.name] = m.lambda);
    const r6 = v => +v.toFixed(6);
    return {
      materials,
      rectangles: S.rects.map(r => ({ x0: r6(r.x0), y0: r6(r.y0), x1: r6(r.x1), y1: r6(r.y1), material: matById(r.mat)?.name })),
      boundaries: S.bcTypes.map(b => {
        const o = { name: b.name, kind: b.kind };
        if (b.kind === "convective" || b.kind === "temperature") o.T = b.T;
        if (b.kind === "convective") o.R = b.R;
        if (b.kind === "flux") o.q = b.q;
        return o;
      }),
      edges: S.edges.map(e => {
        const name = bcById(e.bc)?.name;
        return e.orient === "v"
          ? { boundary: name, x0: r6(e.c), y0: r6(e.a0), x1: r6(e.c), y1: r6(e.a1) }
          : { boundary: name, x0: r6(e.a0), y0: r6(e.c), x1: r6(e.a1), y1: r6(e.c) };
      }),
      mesh: { h_min: S.mesh.hmin, h_max: S.mesh.hmax, ratio: S.mesh.ratio },
    };
  }
  function fromCase(c) {
    if (!c || typeof c.materials !== "object" || !Array.isArray(c.rectangles)) throw new Error("Expected keys 'materials' and 'rectangles'.");
    const mats = Object.entries(c.materials).map(([name, lambda], i) => {
      if (!(+lambda > 0)) throw new Error(`Material '${name}' needs a positive λ.`);
      const p = preset(name);
      return { id: nid(), name, lambda: +lambda, color: p ? p[2] : ["#8aa39b", "#c9a46b", "#7f9cc0", "#b87f8f", "#9bbf7a", "#c7b8a0"][i % 6] };
    });
    const byName = Object.fromEntries(mats.map(m => [m.name, m]));
    const rects = c.rectangles.map(r => {
      if (!byName[r.material]) throw new Error(`Rectangle uses unknown material '${r.material}'.`);
      const x0 = Math.min(r.x0, r.x1), x1 = Math.max(r.x0, r.x1), y0 = Math.min(r.y0, r.y1), y1 = Math.max(r.y0, r.y1);
      if (!(x1 > x0 && y1 > y0)) throw new Error("A rectangle has zero width or height.");
      return { id: nid(), x0, y0, x1, y1, mat: byName[r.material].id };
    });
    const bcTypes = [], edges = [];
    const bcList = c.boundaries || [];
    if (bcList.some(b => b.side)) {
      // older side-based format: turn each side into an edge along the bounding box
      const bx0 = Math.min(...rects.map(r => r.x0)), bx1 = Math.max(...rects.map(r => r.x1));
      const by0 = Math.min(...rects.map(r => r.y0)), by1 = Math.max(...rects.map(r => r.y1));
      bcList.forEach((b, i) => {
        if (!b.kind || b.kind === "adiabatic") return;
        const bc = { id: nid(), name: b.name || b.side, kind: b.kind, T: +b.T || 0, R: b.R ?? 0.13, q: +b.q || 0, color: BC_COLORS[i % BC_COLORS.length] };
        bcTypes.push(bc);
        const lo = b.start ?? -Infinity, hi = b.end ?? Infinity;
        if (b.side === "left") edges.push(mkEdge(bc, bx0, Math.max(by0, lo), bx0, Math.min(by1, hi)));
        if (b.side === "right") edges.push(mkEdge(bc, bx1, Math.max(by0, lo), bx1, Math.min(by1, hi)));
        if (b.side === "bottom") edges.push(mkEdge(bc, Math.max(bx0, lo), by0, Math.min(bx1, hi), by0));
        if (b.side === "top") edges.push(mkEdge(bc, Math.max(bx0, lo), by1, Math.min(bx1, hi), by1));
      });
    } else {
      bcList.forEach((b, i) => bcTypes.push({ id: nid(), name: b.name || `Boundary ${i + 1}`, kind: b.kind || "convective", T: +b.T || 0, R: b.R ?? 0.13, q: +b.q || 0, color: BC_COLORS[i % BC_COLORS.length] }));
      const bcByName = Object.fromEntries(bcTypes.map(b => [b.name, b]));
      (c.edges || []).forEach(e => {
        const bc = bcByName[e.boundary];
        if (!bc) throw new Error(`Edge uses unknown boundary '${e.boundary}'.`);
        if (e.x0 !== e.x1 && e.y0 !== e.y1) throw new Error("Edges must be horizontal or vertical.");
        edges.push(mkEdge(bc, e.x0, e.y0, e.x1, e.y1));
      });
    }
    if (!bcTypes.length) bcTypes.push(...defaultBCs());
    const m = c.mesh || {};
    S = Object.assign({}, S, {
      materials: mats, rects, bcTypes, edges, selected: null, selEdge: null,
      mesh: { hmin: m.h_min ?? S.mesh.hmin, hmax: m.h_max ?? S.mesh.hmax, ratio: m.ratio ?? S.mesh.ratio },
      activeMat: mats[0]?.id ?? null, activeBC: bcTypes[0].id,
    });
  }
  $("exp-btn").addEventListener("click", () => { $("json").value = JSON.stringify(toCase(), null, 2); flash("Case shown below."); });
  $("copy-btn").addEventListener("click", () => {
    const txt = JSON.stringify(toCase(), null, 2); $("json").value = txt;
    const fallback = () => { $("json").select(); flash("Select the text below and copy it."); };
    try { navigator.clipboard.writeText(txt).then(() => flash("Copied to clipboard."), fallback); } catch (e) { fallback(); }
  });
  // ---- stand-alone app: one HTML file with this module and the current model inside
  const appBtn = $("app-btn");
  if (standalone) appBtn.hidden = true;
  appBtn.addEventListener("click", async () => {
    try {
      const src = await (await fetch(import.meta.url)).text();
      const blob = new Blob([standaloneHtml(src, JSON.stringify(toCase()))], { type: "text/html" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob); a.download = "thermal-bridge-lab.html";
      root.append(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(a.href), 2000);
      flashTip("Saved thermal-bridge-lab.html. Double-click it to run the app on its own, also offline.");
    } catch (e) { flashTip("Could not make the stand-alone file: " + e.message); }
  });

  $("save-btn").addEventListener("click", () => {
    const blob = new Blob([JSON.stringify(toCase(), null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = "thermal-bridge-case.json";
    root.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
    flash("Saved thermal-bridge-case.json to your downloads.");
  });
  $("open-btn").addEventListener("click", () => $("file-in").click());
  $("file-in").addEventListener("change", () => {
    const f = $("file-in").files[0]; if (!f) return;
    const rd = new FileReader();
    rd.onload = () => {
      try { fromCase(JSON.parse(rd.result)); afterLoad(); flash(`Opened ${f.name}.`); $("json").value = ""; }
      catch (e) { flash(`Could not open ${f.name}: ${e.message}`, true); }
      $("file-in").value = "";
    };
    rd.readAsText(f);
  });
  $("imp-btn").addEventListener("click", () => {
    try { fromCase(JSON.parse($("json").value)); afterLoad(); flash("Case loaded."); }
    catch (e) { flash("Could not load: " + e.message, true); }
  });
  function loadExample(fn, msg) {
    const keep = { live: S.live, display: S.display, iso: S.iso };
    S = Object.assign(fn(), keep); afterLoad(); flash(msg);
  }
  $("ex-corner").addEventListener("click", () => loadExample(cornerExample, "Example loaded: external wall corner with outside insulation."));
  $("ex-stud").addEventListener("click", () => loadExample(studExample, "Example loaded: steel C-stud through a 200 mm insulated wall."));
  function afterLoad() {
    $("m-hmin").value = mm(S.mesh.hmin); $("m-hmax").value = mm(S.mesh.hmax); $("m-ratio").value = S.mesh.ratio;
    $("iso").checked = S.iso; $("live").checked = S.live; syncSnap();
    buildMaterials(); buildBCs(); fillMatSelect(); fillBCSelect(); setTool(S.tool); setDisplay(S.display);
    fitView(); changed(true);
  }

  // ------------------------------------------------------------------ solve + results
  function runSolve() {
    const bcIndex = new Map(S.bcTypes.map((b, i) => [b.id, i]));
    const model = {
      rects: S.rects.map(r => ({ x0: r.x0, y0: r.y0, x1: r.x1, y1: r.y1, lambda: matById(r.mat)?.lambda ?? NaN })),
      bcs: S.bcTypes.map(b => ({ kind: b.kind, T: b.T, R: b.R, q: b.q })),
      segs: S.edges.map(e => ({ orient: e.orient, c: e.c, a0: e.a0, a1: e.a1, bc: bcIndex.get(e.bc) ?? -1 })),
      mesh: S.mesh,
    };
    R = solveModel(model);
    R.version = version; R.rectIds = S.rects.map(r => r.id); R.bcIds = S.bcTypes.map(b => b.id);
    needSolve = false; showResults(); buildEdges(); updateSolveBtn();
  }
  function showResults() {
    const set = (id, html) => $(id).innerHTML = html;
    const body = $("flow-body"); body.innerHTML = "";
    $("mesh-count").textContent = R && R.nx ? `${R.nx} × ${R.ny} = ${(R.nx * R.ny).toLocaleString("en")} cells` : "";
    if (!R || R.error || !R.T) {
      ["k-phi", "k-l2d", "k-tsi", "k-frsi"].forEach(id => set(id, "–"));
      $("balance").textContent = ""; $("solve-time").textContent = ""; return;
    }
    $("solve-time").textContent = `solved in ${R.ms.toFixed(0)} ms`;
    let sum = 0; const used = [];
    R.bcIds.forEach((id, i) => {
      const br = R.bcRes[i], b = bcById(id);
      if (!b || !br.n || b.kind === "adiabatic") return;
      used.push({ b, br }); sum += br.Q;
      const tr = el("tr");
      const td0 = el("td"); const sw = el("span", "swatch line"); sw.style.cssText = `display:inline-block;width:12px;margin-right:6px;vertical-align:middle;background:${b.color}`;
      td0.append(sw, document.createTextNode(b.name));
      tr.append(td0, el("td", "num", fmt(br.Q, 3)), el("td", "num", `${fmt(br.tmin, 2)} … ${fmt(br.tmax, 2)}`));
      body.append(tr);
    });
    $("balance").textContent = `Energy balance ${sum.toExponential(1)} W/m (should be ≈ 0)`;
    const fixedUsed = used.filter(u => u.b.kind === "convective" || u.b.kind === "temperature");
    const Ti = Math.max(...fixedUsed.map(u => +u.b.T)), Te = Math.min(...fixedUsed.map(u => +u.b.T));
    const warm = fixedUsed.filter(u => +u.b.T === Ti);
    const phi = warm.reduce((a, u) => a + u.br.Q, 0), tsi = Math.min(...warm.map(u => u.br.tmin));
    set("k-phi", `${fmt(phi, 3)} <small>W/m</small>`);
    set("k-tsi", `${fmt(tsi, 2)} <small>°C</small>`);
    if (Ti > Te) {
      set("k-l2d", `${fmt(phi / (Ti - Te), 4)} <small>W/(m·K)</small>`);
      set("k-frsi", fmt((tsi - Te) / (Ti - Te), 3));
    } else { set("k-l2d", "–"); set("k-frsi", "–"); }
  }

  // ------------------------------------------------------------------ colour maps
  const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
  function makeLUT(stops) {
    const c = stops.map(hex), out = [];
    for (let i = 0; i < 256; i++) {
      const t = i / 255 * (c.length - 1), a = Math.min(Math.floor(t), c.length - 2), f = t - a;
      out.push(`rgb(${c[a].map((v, k) => Math.round(v + (c[a + 1][k] - v) * f)).join(",")})`);
    }
    return { lut: out, css: `linear-gradient(90deg, ${stops.join(",")})` };
  }
  const CM_T = makeLUT(["#3b4cc0", "#6788ee", "#9abbff", "#c9d7f0", "#edd1c2", "#f7a889", "#e26952", "#b40426"]);
  const CM_Q = makeLUT(["#440154", "#46327e", "#365c8d", "#277f8e", "#1fa187", "#4ac16d", "#a0da39", "#fde725"]);

  // ------------------------------------------------------------------ view
  const W2S = (x, y) => [view.ox + x * view.scale, view.oy - y * view.scale];
  const S2W = (sx, sy) => [(sx - view.ox) / view.scale, (view.oy - sy) / view.scale];
  function bounds() {
    if (!S.rects.length) return { x0: 0, y0: 0, x1: 0.3, y1: 0.3 };
    return { x0: Math.min(...S.rects.map(r => r.x0)), y0: Math.min(...S.rects.map(r => r.y0)), x1: Math.max(...S.rects.map(r => r.x1)), y1: Math.max(...S.rects.map(r => r.y1)) };
  }
  function fitView() {
    const b = bounds(), pad = 64;
    const bw = Math.max(b.x1 - b.x0, 1e-4), bh = Math.max(b.y1 - b.y0, 1e-4);
    view.scale = Math.min((view.w - 2 * pad) / bw, (view.h - 2 * pad) / bh);
    view.ox = (view.w - bw * view.scale) / 2 - b.x0 * view.scale;
    view.oy = view.h - (view.h - bh * view.scale) / 2 + b.y0 * view.scale;
    view.fitted = true;
  }
  function resize() {
    const r = board.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
    view.w = r.width; view.h = r.height;
    cv.width = Math.round(r.width * dpr); cv.height = Math.round(r.height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (!view.fitted) fitView();
    needRender = true; tick();
  }
  new ResizeObserver(resize).observe(board);

  // ------------------------------------------------------------------ render
  const cssVar = n => getComputedStyle(root).getPropertyValue(n).trim();
  function render() {
    needRender = false;
    const w = view.w, h = view.h;
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = cssVar("--board"); ctx.fillRect(0, 0, w, h);
    drawGrid();
    const fresh = R && R.version === version;
    const hasField = fresh && !R.error && R.T;
    const hasMesh = fresh && R.owner;
    const d = S.display;
    if (d === "geometry" || (d === "mesh" && !hasMesh) || ((d === "temperature" || d === "flux") && !hasField)) drawGeometry();
    else if (d === "mesh") drawMesh();
    else if (d === "temperature") { drawField(R.T, R.Tmin, R.Tmax, CM_T, false); if (S.iso) drawIsotherms(); }
    else { drawField(R.qm, R.qlo, R.qmax, CM_Q, true); drawArrows(); }
    drawOutlines();
    if (fresh && R.faces) drawFreeSurfaces();
    drawEdges();
    drawDraft();
    drawScaleBar();
    updateStatus(!fresh);
    updateLegend(hasField);
  }
  function drawGrid() {
    const steps = [0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5];
    const minor = steps.find(s => s * view.scale >= 10) || 5;
    const major = steps.find(s => s * view.scale >= 70 && s > minor) || minor * 10;
    const [x0, y1] = S2W(0, 0), [x1, y0] = S2W(view.w, view.h);
    for (const [step, col] of [[minor, cssVar("--grid")], [major, cssVar("--grid-major")]]) {
      ctx.strokeStyle = col; ctx.lineWidth = 1; ctx.beginPath();
      for (let x = Math.ceil(x0 / step) * step; x <= x1; x += step) { const sx = Math.round(W2S(x, 0)[0]) + 0.5; ctx.moveTo(sx, 0); ctx.lineTo(sx, view.h); }
      for (let y = Math.ceil(y0 / step) * step; y <= y1; y += step) { const sy = Math.round(W2S(0, y)[1]) + 0.5; ctx.moveTo(0, sy); ctx.lineTo(view.w, sy); }
      ctx.stroke();
    }
  }
  function drawGeometry() {
    for (const r of S.rects) {
      const m = matById(r.mat); if (!m) continue;
      const [a, b] = W2S(r.x0, r.y1), [cx, cy] = W2S(r.x1, r.y0);
      ctx.fillStyle = m.color; ctx.fillRect(a, b, Math.max(cx - a, 1), Math.max(cy - b, 1));
    }
  }
  function screenLines() {
    const sx = new Float64Array(R.xl.length), sy = new Float64Array(R.yl.length);
    for (let i = 0; i < sx.length; i++) sx[i] = view.ox + R.xl[i] * view.scale;
    for (let j = 0; j < sy.length; j++) sy[j] = view.oy - R.yl[j] * view.scale;
    return [sx, sy];
  }
  function cellLoop(fn) {
    const [sx, sy] = screenLines(), { nx, ny } = R;
    for (let j = 0; j < ny; j++) {
      const top = sy[j + 1], bot = sy[j];
      if (bot < 0 || top > view.h) continue;
      for (let i = 0; i < nx; i++) {
        const l = sx[i], rr = sx[i + 1];
        if (rr < 0 || l > view.w) continue;
        fn(j * nx + i, l, top, rr - l, bot - top);
      }
    }
  }
  function drawMesh() {
    const cols = R.rectIds.map(id => { const r = S.rects.find(x => x.id === id); const m = r && matById(r.mat); return m ? m.color : null; });
    cellLoop((c, x, y, w, h) => { const o = R.owner[c]; if (o >= 0 && cols[o]) { ctx.fillStyle = cols[o]; ctx.fillRect(x, y, w + 0.5, h + 0.5); } });
    ctx.strokeStyle = "rgba(20,25,30,0.45)"; ctx.lineWidth = 0.6; ctx.beginPath();
    cellLoop((c, x, y, w, h) => { if (R.owner[c] >= 0) ctx.rect(x, y, w, h); });
    ctx.stroke();
  }
  function drawField(arr, lo, hi, cm, log) {
    const a = log ? Math.log(lo) : lo, span = (log ? Math.log(hi) : hi) - a || 1;
    cellLoop((c, x, y, w, h) => {
      const v = arr[c]; if (v !== v) return;
      let t = ((log ? Math.log(Math.max(v, lo)) : v) - a) / span;
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      ctx.fillStyle = cm.lut[(t * 255) | 0]; ctx.fillRect(x, y, w + 0.5, h + 0.5);
    });
  }
  function isoStep() {
    const span = R.Tmax - R.Tmin; if (!(span > 0)) return 0;
    const raw = span / 14, p = Math.pow(10, Math.floor(Math.log10(raw)));
    return [1, 2, 2.5, 5, 10].map(f => f * p).find(s => s >= raw);
  }
  function drawIsotherms() {
    const step = isoStep(); if (!step) return;
    const { nx, ny, xc, yc, T } = R;
    ctx.strokeStyle = "rgba(15,18,22,0.55)"; ctx.lineWidth = 0.8; ctx.beginPath();
    for (let L = Math.ceil(R.Tmin / step) * step; L < R.Tmax; L += step) {
      for (let j = 0; j < ny - 1; j++) for (let i = 0; i < nx - 1; i++) {
        const c = j * nx + i, v0 = T[c], v1 = T[c + 1], v2 = T[c + nx + 1], v3 = T[c + nx];
        if (v0 !== v0 || v1 !== v1 || v2 !== v2 || v3 !== v3) continue;
        const code = (v0 > L) | ((v1 > L) << 1) | ((v2 > L) << 2) | ((v3 > L) << 3);
        if (code === 0 || code === 15) continue;
        const E = e => {
          if (e === 0) { const t = (L - v0) / (v1 - v0); return W2S(xc[i] + t * (xc[i + 1] - xc[i]), yc[j]); }
          if (e === 1) { const t = (L - v1) / (v2 - v1); return W2S(xc[i + 1], yc[j] + t * (yc[j + 1] - yc[j])); }
          if (e === 2) { const t = (L - v3) / (v2 - v3); return W2S(xc[i] + t * (xc[i + 1] - xc[i]), yc[j + 1]); }
          const t = (L - v0) / (v3 - v0); return W2S(xc[i], yc[j] + t * (yc[j + 1] - yc[j]));
        };
        const seg = (e1, e2) => { const p = E(e1), q = E(e2); ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]); };
        switch (code) {
          case 1: case 14: seg(3, 0); break;
          case 2: case 13: seg(0, 1); break;
          case 3: case 12: seg(3, 1); break;
          case 4: case 11: seg(1, 2); break;
          case 5: seg(3, 2); seg(0, 1); break;
          case 6: case 9: seg(0, 2); break;
          case 7: case 8: seg(3, 2); break;
          case 10: seg(3, 0); seg(1, 2); break;
        }
      }
    }
    ctx.stroke();
  }
  const bsearch = (arr, v) => { let lo = 0, hi = arr.length - 1; if (v < arr[0] || v > arr[hi]) return -1; while (hi - lo > 1) { const m = (lo + hi) >> 1; if (arr[m] <= v) lo = m; else hi = m; } return lo; };
  function cellAt(x, y) {
    if (!R || !R.xl) return -1;
    const i = bsearch(R.xl, x), j = bsearch(R.yl, y);
    return i < 0 || j < 0 ? -1 : j * R.nx + i;
  }
  function drawArrows() {
    const gap = 26; ctx.strokeStyle = "rgba(255,255,255,0.85)"; ctx.lineWidth = 1.1; ctx.beginPath();
    for (let sy = gap / 2; sy < view.h; sy += gap) for (let sx = gap / 2; sx < view.w; sx += gap) {
      const [x, y] = S2W(sx, sy), c = cellAt(x, y);
      if (c < 0 || !(R.qm[c] > 0)) continue;
      const ux = R.qx[c] / R.qm[c], uy = -R.qy[c] / R.qm[c], L = 8;
      const ax = sx - ux * L / 2, ay = sy - uy * L / 2, bx = sx + ux * L / 2, by = sy + uy * L / 2;
      ctx.moveTo(ax, ay); ctx.lineTo(bx, by);
      ctx.moveTo(bx, by); ctx.lineTo(bx - ux * 3.5 - uy * 2.5, by - uy * 3.5 + ux * 2.5);
      ctx.moveTo(bx, by); ctx.lineTo(bx - ux * 3.5 + uy * 2.5, by - uy * 3.5 - ux * 2.5);
    }
    ctx.stroke();
  }
  function drawOutlines() {
    const solid = S.display === "geometry";
    ctx.lineWidth = 1;
    for (const r of S.rects) {
      const [a, b] = W2S(r.x0, r.y1), [c, d] = W2S(r.x1, r.y0);
      ctx.strokeStyle = solid ? "rgba(20,25,30,0.5)" : "rgba(20,25,30,0.3)";
      ctx.setLineDash(solid ? [] : [3, 3]);
      ctx.strokeRect(Math.round(a) + 0.5, Math.round(b) + 0.5, Math.max(Math.round(c - a), 1), Math.max(Math.round(d - b), 1));
    }
    ctx.setLineDash([]);
    const sel = S.rects.find(r => r.id === S.selected);
    if (sel) {
      const acc = cssVar("--accent");
      const [a, b] = W2S(sel.x0, sel.y1), [c, d] = W2S(sel.x1, sel.y0);
      ctx.strokeStyle = acc; ctx.lineWidth = 2; ctx.strokeRect(a, b, Math.max(c - a, 1), Math.max(d - b, 1));
      ctx.fillStyle = acc;
      for (const [x, y] of [[a, b], [c, b], [a, d], [c, d]]) ctx.fillRect(x - 4, y - 4, 8, 8);
      chip(`${mm(sel.x1 - sel.x0)} × ${mm(sel.y1 - sel.y0)} mm`, (a + c) / 2, b - 8, acc, "center");
    }
  }
  function chip(txt, x, y, col, align) {
    ctx.font = `500 11px ${cssVar("--f-mono")}`;
    const tw = ctx.measureText(txt).width;
    let tx = align === "center" ? x - tw / 2 : align === "right" ? x - tw : x;
    tx = Math.min(Math.max(tx, 4), view.w - tw - 6); const ty = Math.min(Math.max(y, 13), view.h - 4);
    ctx.fillStyle = cssVar("--panel"); ctx.fillRect(tx - 4, ty - 11, tw + 8, 15);
    ctx.strokeStyle = col; ctx.lineWidth = 1; ctx.strokeRect(tx - 4 + 0.5, ty - 11 + 0.5, tw + 7, 14);
    ctx.fillStyle = col; ctx.fillText(txt, tx, ty);
  }
  function drawFreeSurfaces() {
    // exposed surfaces with no drawn condition: thin dashed line = adiabatic
    ctx.strokeStyle = cssVar("--muted"); ctx.lineWidth = 1.5; ctx.setLineDash([4, 3]); ctx.beginPath();
    for (const f of R.faces) {
      if (f.seg >= 0) continue;
      const [a, b] = W2S(f.x0, f.y0), [c, d] = W2S(f.x1, f.y1);
      ctx.moveTo(a, b); ctx.lineTo(c, d);
    }
    ctx.stroke(); ctx.setLineDash([]);
  }
  function edgeEnds(e) { return e.orient === "v" ? [e.c, e.a0, e.c, e.a1] : [e.a0, e.c, e.a1, e.c]; }
  function outwardSide(e) {
    // which side of the edge is empty space: label goes there
    const [x0, y0, x1, y1] = edgeEnds(e), mx = (x0 + x1) / 2, my = (y0 + y1) / 2, eps = 3 / view.scale;
    if (e.orient === "v") return hitRect(mx + eps, my) && !hitRect(mx - eps, my) ? -1 : 1;
    return hitRect(mx, my + eps) && !hitRect(mx, my - eps) ? -1 : 1;
  }
  function drawEdges() {
    const fresh = R && R.version === version && R.segFaces;
    S.edges.forEach((e, idx) => {
      const b = bcById(e.bc); if (!b) return;
      const [x0, y0, x1, y1] = edgeEnds(e), [a, bb] = W2S(x0, y0), [c, d] = W2S(x1, y1);
      const sel = e.id === S.selEdge, dead = fresh && R.segFaces[idx] === 0;
      ctx.lineCap = "round";
      if (sel) { ctx.strokeStyle = cssVar("--accent"); ctx.lineWidth = 10; ctx.globalAlpha = 0.35; ctx.beginPath(); ctx.moveTo(a, bb); ctx.lineTo(c, d); ctx.stroke(); ctx.globalAlpha = 1; }
      ctx.strokeStyle = b.color; ctx.lineWidth = 5; ctx.setLineDash(dead ? [6, 5] : []);
      ctx.beginPath(); ctx.moveTo(a, bb); ctx.lineTo(c, d); ctx.stroke(); ctx.setLineDash([]);
      ctx.fillStyle = b.color;
      for (const [px, py] of [[a, bb], [c, d]]) { ctx.beginPath(); ctx.arc(px, py, 3.5, 0, Math.PI * 2); ctx.fill(); }
      ctx.lineCap = "butt";
      const len = Math.hypot(c - a, d - bb);
      if (len > 70 || sel) {
        const side = outwardSide(e), mx = (a + c) / 2, my = (bb + d) / 2;
        const txt = b.kind === "convective" ? `${b.name} · ${b.T} °C · R ${b.R}` : b.kind === "temperature" ? `${b.name} · ${b.T} °C` : b.kind === "flux" ? `${b.name} · ${b.q} W/m²` : b.name;
        if (e.orient === "v") chip(txt, mx + side * 10, my + 4, b.color, side > 0 ? "left" : "right");
        else chip(txt, mx, my - side * 12 + (side < 0 ? 4 : 0), b.color, "center");
      }
    });
  }
  function drawDraft() {
    if (!drag) return;
    const acc = cssVar("--accent");
    if (drag.type === "draw") {
      const m = matById(S.activeMat), r = normRect(drag.x0, drag.y0, drag.x1, drag.y1);
      const [a, b] = W2S(r.x0, r.y1), [c, d] = W2S(r.x1, r.y0);
      ctx.globalAlpha = 0.7; ctx.fillStyle = m ? m.color : "#888"; ctx.fillRect(a, b, c - a, d - b); ctx.globalAlpha = 1;
      ctx.strokeStyle = acc; ctx.setLineDash([4, 3]); ctx.lineWidth = 1.5; ctx.strokeRect(a, b, c - a, d - b); ctx.setLineDash([]);
      chip(`${mm(r.x1 - r.x0)} × ${mm(r.y1 - r.y0)} mm`, (a + c) / 2, b - 8, acc, "center");
    }
    if (drag.type === "edge" && drag.moved) {
      const b = bcById(S.activeBC), e = draftEdge(); if (!e) return;
      const [x0, y0, x1, y1] = edgeEnds(e), [a, bb] = W2S(x0, y0), [c, d] = W2S(x1, y1);
      ctx.strokeStyle = b ? b.color : acc; ctx.lineWidth = 5; ctx.lineCap = "round"; ctx.globalAlpha = 0.75;
      ctx.beginPath(); ctx.moveTo(a, bb); ctx.lineTo(c, d); ctx.stroke(); ctx.globalAlpha = 1; ctx.lineCap = "butt";
      chip(`${mm(e.a1 - e.a0)} mm`, (a + c) / 2 + 10, (bb + d) / 2 - 8, b ? b.color : acc, "left");
    }
  }
  function drawScaleBar() {
    const opts = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2];
    const L = opts.find(v => v * view.scale >= 60) || 2, px = L * view.scale;
    const x = 14, y = view.h - 14, ink = cssVar("--ink");
    ctx.strokeStyle = ink; ctx.lineWidth = 2; ctx.beginPath();
    ctx.moveTo(x, y - 5); ctx.lineTo(x, y); ctx.lineTo(x + px, y); ctx.lineTo(x + px, y - 5); ctx.stroke();
    ctx.fillStyle = ink; ctx.font = `500 11px ${cssVar("--f-mono")}`;
    ctx.fillText(`${mm(L)} mm`, x + px + 6, y);
  }
  function updateStatus(stale) {
    const st = $("status");
    if (R && R.error && !stale) { st.className = "status err"; st.textContent = R.error; return; }
    if (stale || !R) { st.className = "status stale"; st.textContent = S.live ? "Solving…" : "Results out of date. Press Solve."; return; }
    st.className = "status"; st.textContent = `${R.nx} × ${R.ny} cells · ${R.ms.toFixed(0)} ms`;
  }
  function updateLegend(hasField) {
    const lg = $("legend");
    if (S.display === "mesh") {
      lg.textContent = R && R.nx && R.version === version ? `Mesh: ${R.nx} × ${R.ny} cells, smallest ${fmt(Math.min(...R.dx, ...R.dy) * 1000, 2)} mm` : "";
      return;
    }
    if (!hasField || S.display === "geometry") { lg.textContent = "Dashed grey surfaces have no boundary drawn and are adiabatic."; return; }
    if (S.display === "temperature") {
      const st = isoStep();
      lg.innerHTML = `<span>${fmt(R.Tmin, 1)} °C</span><span class="bar" style="background:${CM_T.css}"></span><span>${fmt(R.Tmax, 1)} °C</span>${S.iso && st ? `<span>· isotherms every ${st} K</span>` : ""}`;
    } else {
      const f = v => v >= 100 ? v.toFixed(0) : v >= 1 ? v.toFixed(1) : v.toPrecision(2);
      lg.innerHTML = `<span>${f(R.qlo)}</span><span class="bar" style="background:${CM_Q.css}"></span><span>${f(R.qmax)} W/m² (log)</span>`;
    }
  }
  let tipTimer = 0;
  function flashTip(t) {
    const tip = $("tip"); tip.hidden = false; tip.textContent = t;
    clearTimeout(tipTimer); tipTimer = setTimeout(() => setTool(S.tool), 2600);
  }

  // ------------------------------------------------------------------ interaction
  let drag = null, spaceDown = false;
  const normRect = (x0, y0, x1, y1) => ({ x0: Math.min(x0, x1), x1: Math.max(x0, x1), y0: Math.min(y0, y1), y1: Math.max(y0, y1) });
  function snap(v, axis, exclude) {
    const tol = 7 / view.scale; let best = null, bd = tol;
    for (const r of S.rects) {
      if (r.id === exclude) continue;
      for (const e of axis === "x" ? [r.x0, r.x1] : [r.y0, r.y1]) { const d = Math.abs(e - v); if (d < bd) { bd = d; best = e; } }
    }
    for (const e of S.edges) {
      const [x0, y0, x1, y1] = edgeEnds(e);
      for (const v2 of axis === "x" ? [x0, x1] : [y0, y1]) { const d = Math.abs(v2 - v); if (d < bd) { bd = d; best = v2; } }
    }
    if (best !== null) return { v: best, hit: true };
    return { v: S.snap > 0 ? Math.round(v / S.snap) * S.snap : v, hit: false };
  }
  const localXY = e => { const r = cv.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; };
  function hitRect(x, y) {
    for (let i = S.rects.length - 1; i >= 0; i--) { const r = S.rects[i]; if (x >= r.x0 && x <= r.x1 && y >= r.y0 && y <= r.y1) return r; }
    return null;
  }
  function hitCorner(sx, sy) {
    const r = S.rects.find(x => x.id === S.selected); if (!r) return null;
    for (const cx of ["x0", "x1"]) for (const cy of ["y0", "y1"]) {
      const [px, py] = W2S(r[cx], r[cy]);
      if (Math.abs(px - sx) <= 7 && Math.abs(py - sy) <= 7) return { r, cx, cy };
    }
    return null;
  }
  function hitEdge(sx, sy) {
    for (let i = S.edges.length - 1; i >= 0; i--) {
      const e = S.edges[i], [x0, y0, x1, y1] = edgeEnds(e), [a, b] = W2S(x0, y0), [c, d] = W2S(x1, y1);
      const inside = e.orient === "v" ? (sy >= Math.min(b, d) - 4 && sy <= Math.max(b, d) + 4 && Math.abs(sx - a) <= 6)
                                      : (sx >= Math.min(a, c) - 4 && sx <= Math.max(a, c) + 4 && Math.abs(sy - b) <= 6);
      if (inside) return e;
    }
    return null;
  }
  function draftEdge() {
    const dxs = Math.abs(drag.sx1 - drag.sx0), dys = Math.abs(drag.sy1 - drag.sy0);
    if (dxs < 3 && dys < 3) return null;
    if (dys >= dxs) {   // vertical: x fixed from the start point
      const c = snap(drag.x0, "x").v, a0 = snap(drag.y0, "y").v, a1 = snap(drag.y1, "y").v;
      return a1 === a0 ? null : { orient: "v", c, a0: Math.min(a0, a1), a1: Math.max(a0, a1) };
    }
    const c = snap(drag.y0, "y").v, a0 = snap(drag.x0, "x").v, a1 = snap(drag.x1, "x").v;
    return a1 === a0 ? null : { orient: "h", c, a0: Math.min(a0, a1), a1: Math.max(a0, a1) };
  }
  // click on a surface: find the straight exposed face under the pointer, corner to corner
  function surfaceRunAt(sx, sy) {
    if (!R || !R.owner || R.version !== version) return null;
    const { xl, yl, nx, ny, owner } = R;
    const solid = (i, j) => i >= 0 && j >= 0 && i < nx && j < ny && owner[j * nx + i] >= 0;
    const [x, y] = S2W(sx, sy), tol = 8 / view.scale;
    let best = null;
    // vertical lines
    const j = bsearch(yl, y);
    if (j >= 0) for (let i = 0; i <= nx; i++) {
      const d = Math.abs(xl[i] - x); if (d > tol || (best && d >= best.d)) continue;
      const side = solid(i - 1, j) - solid(i, j); if (!side) continue;
      let j0 = j, j1 = j;
      while (j0 > 0 && solid(i - 1, j0 - 1) - solid(i, j0 - 1) === side) j0--;
      while (j1 < ny - 1 && solid(i - 1, j1 + 1) - solid(i, j1 + 1) === side) j1++;
      best = { d, orient: "v", c: xl[i], a0: yl[j0], a1: yl[j1 + 1] };
    }
    const i = bsearch(xl, x);
    if (i >= 0) for (let jj = 0; jj <= ny; jj++) {
      const d = Math.abs(yl[jj] - y); if (d > tol || (best && d >= best.d)) continue;
      const side = solid(i, jj - 1) - solid(i, jj); if (!side) continue;
      let i0 = i, i1 = i;
      while (i0 > 0 && solid(i0 - 1, jj - 1) - solid(i0 - 1, jj) === side) i0--;
      while (i1 < nx - 1 && solid(i1 + 1, jj - 1) - solid(i1 + 1, jj) === side) i1++;
      best = { d, orient: "h", c: yl[jj], a0: xl[i0], a1: xl[i1 + 1] };
    }
    return best;
  }

  cv.addEventListener("pointerdown", e => {
    cv.focus();
    const [sx, sy] = localXY(e), [x, y] = S2W(sx, sy);
    cv.setPointerCapture(e.pointerId);
    if (e.button === 1 || e.button === 2 || spaceDown) { drag = { type: "pan", sx, sy, ox: view.ox, oy: view.oy }; return; }
    if (S.tool === "draw") {
      if (!matById(S.activeMat)) { flashTip("Add a material first."); return; }
      const px = snap(x, "x").v, py = snap(y, "y").v;
      drag = { type: "draw", x0: px, y0: py, x1: px, y1: py };
      return;
    }
    if (S.tool === "edge") {
      if (!bcById(S.activeBC)) { flashTip("Add a boundary condition first."); return; }
      drag = { type: "edge", x0: x, y0: y, x1: x, y1: y, sx0: sx, sy0: sy, sx1: sx, sy1: sy, moved: false };
      return;
    }
    const corner = hitCorner(sx, sy);
    if (corner) { drag = { type: "resize", ...corner }; return; }
    const ed = hitEdge(sx, sy);
    if (ed) { selectEdge(ed.id); drag = null; return; }
    const r = hitRect(x, y);
    if (r) { select(r.id); drag = { type: "move", r, x, y, orig: { ...r } }; return; }
    select(null); selectEdge(null);
    drag = { type: "pan", sx, sy, ox: view.ox, oy: view.oy };
  });
  cv.addEventListener("pointermove", e => {
    const [sx, sy] = localXY(e), [x, y] = S2W(sx, sy);
    readout(x, y);
    if (!drag) {
      if (S.tool === "select") cv.style.cursor = hitCorner(sx, sy) ? "nwse-resize" : hitEdge(sx, sy) ? "pointer" : hitRect(x, y) ? "move" : "default";
      return;
    }
    if (drag.type === "pan") { view.ox = drag.ox + sx - drag.sx; view.oy = drag.oy + sy - drag.sy; needRender = true; tick(); return; }
    if (drag.type === "draw") { drag.x1 = snap(x, "x").v; drag.y1 = snap(y, "y").v; needRender = true; tick(); return; }
    if (drag.type === "edge") {
      drag.x1 = x; drag.y1 = y; drag.sx1 = sx; drag.sy1 = sy;
      if (Math.hypot(sx - drag.sx0, sy - drag.sy0) > 4) drag.moved = true;
      needRender = true; tick(); return;
    }
    if (drag.type === "resize") {
      const r = drag.r; r[drag.cx] = snap(x, "x", r.id).v; r[drag.cy] = snap(y, "y", r.id).v;
      const n = normRect(r.x0, r.y0, r.x1, r.y1);
      if (n.x1 - n.x0 > 1e-6 && n.y1 - n.y0 > 1e-6) {
        if (r.x0 > r.x1) drag.cx = drag.cx === "x0" ? "x1" : "x0";
        if (r.y0 > r.y1) drag.cy = drag.cy === "y0" ? "y1" : "y0";
        Object.assign(r, n);
      }
      changed(false); return;
    }
    if (drag.type === "move") {
      const o = drag.orig, r = drag.r, ddx = x - drag.x, ddy = y - drag.y;
      const shift = (a, b, axis) => {
        const sa = snap(a, axis, r.id), sb = snap(b, axis, r.id);
        if (sa.hit) return sa.v - a; if (sb.hit) return sb.v - b;
        return S.snap > 0 ? Math.round(a / S.snap) * S.snap - a : 0;
      };
      const nx0 = o.x0 + ddx, nx1 = o.x1 + ddx, ny0 = o.y0 + ddy, ny1 = o.y1 + ddy;
      const fx = shift(nx0, nx1, "x"), fy = shift(ny0, ny1, "y");
      r.x0 = nx0 + fx; r.x1 = nx1 + fx; r.y0 = ny0 + fy; r.y1 = ny1 + fy;
      changed(false);
    }
  });
  const endDrag = () => {
    if (!drag) return;
    const d = drag; drag = null;
    if (d.type === "draw") {
      const n = normRect(d.x0, d.y0, d.x1, d.y1);
      if (n.x1 - n.x0 > 1e-6 && n.y1 - n.y0 > 1e-6) {
        const r = { id: nid(), ...n, mat: S.activeMat };
        S.rects.push(r); S.selected = r.id; S.selEdge = null; changed(true); return;
      }
    }
    if (d.type === "edge") {
      drag = d; let e = d.moved ? draftEdge() : surfaceRunAt(d.sx0, d.sy0); drag = null;
      if (!d.moved && !e) flashTip(R && R.version === version ? "No surface here. Click on the edge between material and empty space." : "Waiting for the mesh. Try again in a moment.");
      if (e) {
        const ne = { id: nid(), bc: S.activeBC, orient: e.orient, c: e.c, a0: e.a0, a1: e.a1 };
        S.edges.push(ne); S.selEdge = ne.id; S.selected = null; changed(true); return;
      }
    }
    if (d.type === "move" || d.type === "resize") { changed(true); return; }
    needRender = true; tick();
  };
  cv.addEventListener("pointerup", endDrag);
  cv.addEventListener("pointercancel", endDrag);
  cv.addEventListener("pointerleave", () => { if (!drag) $("readout").textContent = "Hover the board to read values."; });
  cv.addEventListener("contextmenu", e => e.preventDefault());
  cv.addEventListener("wheel", e => {
    e.preventDefault();
    const [sx, sy] = localXY(e), f = Math.exp(-e.deltaY * 0.0015);
    const ns = Math.min(Math.max(view.scale * f, 20), 5e6), g = ns / view.scale;
    view.ox = sx - (sx - view.ox) * g; view.oy = sy - (sy - view.oy) * g; view.scale = ns;
    needRender = true; tick();
  }, { passive: false });

  function readout(x, y) {
    let txt = `x ${fmt(x * 1000, 1)}  y ${fmt(y * 1000, 1)} mm`;
    const r = hitRect(x, y), m = r && matById(r.mat);
    if (m) txt += `  ·  ${m.name}, λ ${m.lambda}`;
    if (R && R.T && R.version === version) {
      const c = cellAt(x, y);
      if (c >= 0 && R.T[c] === R.T[c]) txt += `  ·  T ${fmt(R.T[c], 2)} °C  ·  |q| ${fmt(R.qm[c], 2)} W/m²`;
    }
    $("readout").textContent = txt;
  }

  let pointerInside = false;
  root.addEventListener("pointerenter", () => { pointerInside = true; });
  root.addEventListener("pointerleave", () => { pointerInside = false; });
  const keysForUs = () => standalone || pointerInside || root.contains(activeEl());
  document.addEventListener("keydown", e => {
    if (!keysForUs() || e.ctrlKey || e.metaKey || e.altKey) return;
    const t = (e.composedPath && e.composedPath()[0]) || e.target;
    const tag = ((t && t.tagName) || "").toLowerCase();
    if (tag === "input" || tag === "textarea" || tag === "select" || (t && t.isContentEditable)) return;
    if (e.key === " ") { spaceDown = true; e.preventDefault(); }
    else if (e.key === "v" || e.key === "V") setTool("select");
    else if (e.key === "r" || e.key === "R" || e.key === "d" || e.key === "D") setTool("draw");
    else if (e.key === "b" || e.key === "B") setTool("edge");
    else if (e.key === "Delete" || e.key === "Backspace") {
      if (S.selEdge) { e.preventDefault(); removeEdge(S.selEdge); }
      else if (S.selected) { e.preventDefault(); removeRect(S.selected); }
    }
    else if (e.key === "Escape") { drag = null; select(null); selectEdge(null); }
  });
  document.addEventListener("keyup", e => { if (e.key === " ") spaceDown = false; });

  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => { needRender = true; tick(); });

  // ------------------------------------------------------------------ frame loop
  let frameQueued = false;
  function tick() {
    if (frameQueued) return;
    frameQueued = true;
    requestAnimationFrame(() => {
      frameQueued = false;
      if (needSolve && S.live) { runSolve(); needRender = true; }
      updateSolveBtn();
      if (needRender) render();
    });
  }

  // ------------------------------------------------------------------ boot
  { const c = model && model.get ? model.get("case") : null;
    if (c) { try { fromCase(typeof c === "string" ? JSON.parse(c) : c); } catch (e) { /* keep the example */ } } }
  $("m-hmin").value = mm(S.mesh.hmin); $("m-hmax").value = mm(S.mesh.hmax); $("m-ratio").value = S.mesh.ratio;
  $("iso").checked = S.iso; $("live").checked = S.live; syncSnap();
  buildMaterials(); buildLayers(); buildBCs(); buildEdges(); fillMatSelect(); fillBCSelect();
  syncSelected(); syncEdgeFields(); setTool(S.tool); setDisplay(S.display);
  resize();
  if (!S.live) runSolve();
  tick();
}

export default { render };
