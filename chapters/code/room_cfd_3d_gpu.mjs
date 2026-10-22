// room_cfd_3d_gpu.mjs: the 3D room model of room_cfd_3d.py, run on the graphics card with WebGPU (test version).
//
// Same physics and numerics as room_cfd_3d.py / room_cfd_3d_numba.py (MAC grid, Chorin projection,
// Boussinesq buoyancy, TVD van Leer advection, k-epsilon with log-law wall functions), but every stage of a
// time step is a WGSL compute shader and the whole time loop stays on the GPU. Differences:
//   - single precision (WGSL has no double); temperature is stored as the deviation from the start value
//   - pressure: conjugate gradients preconditioned by an aggregation multigrid V-cycle whose coarse grids
//     keep a 7-point stencil (2 x 2 x 2 cells per coarse cell, coarse operator = 0.5 P^T A P), weighted
//     Jacobi smoothing and an exact solve on the coarsest grid (<= 128 cells)
//
// Use:   const sim = await createSim(device, caseObj);  await sim.run(onProgress);  const res = await sim.results();
//
// Contact: Christian Hviid, cahv@dtu.dk. Use at own risk; see the disclaimer in room_cfd_3d.py.

export const RHO = 1.2, CP = 1005.0, G = 9.81, NU_AIR = 1.5e-5;
export const WALL = 0, INLET = 1, OUTLET = 2;
const CMU = 0.09, C1 = 1.44, C2 = 1.92, SK = 1.0, SE = 1.3, KAP = 0.41, EWF = 9.0;

export function defaultCase() {
  return {
    L: 5.0, W: 4.0, H: 2.5, nx: 50, ny: 40, nz: 25, ach: 6.0, T_in: 18.0, T_room0: null,
    inlet: { side: "left", start: 0.10, end: 0.30, y0: null, y1: null },
    outlet: { side: "right", start: 2.20, end: 2.40, y0: null, y1: null },
    heat: [], floor_flux: [], turbulence: "k-epsilon", Tu_in: 0.04, nu_t: 2e-3, Pr_t: 0.85,
    advection: "tvd", p_tol: 1e-5, t_end: 900.0, t_avg: 300.0,
  };
}

// ---------------------------------------------------------------------------------------------
// set-up on the CPU (as room_cfd_3d.run)
// ---------------------------------------------------------------------------------------------
function centres(n, h) { return Array.from({ length: n }, (_, i) => (i + 0.5) * h); }

export function boundaries(c) {
  const { nx, ny, nz } = c;
  const xc = centres(nx, c.L / nx), yc = centres(ny, c.W / ny), zc = centres(nz, c.H / nz);
  const b = { L: new Int32Array(ny * nz), R: new Int32Array(ny * nz), B: new Int32Array(nx * nz),
              F: new Int32Array(nx * nz), D: new Int32Array(nx * ny), T: new Int32Array(nx * ny) };
  for (const [op, kind] of [[c.inlet, INLET], [c.outlet, OUTLET]]) {
    const y0 = op.y0 ?? 0.0, y1 = op.y1 ?? c.W;
    let any = false;
    if (op.side === "left" || op.side === "right") {
      const m = op.side === "left" ? b.L : b.R;
      for (let j = 0; j < ny; j++) for (let k = 0; k < nz; k++)
        if (yc[j] > y0 && yc[j] < y1 && zc[k] > op.start && zc[k] < op.end) { m[j * nz + k] = kind; any = true; }
    } else if (op.side === "top") {
      if (kind === INLET) throw new Error("inlets must be in the facade (left) or the back wall (right)");
      for (let i = 0; i < nx; i++) for (let j = 0; j < ny; j++)
        if (xc[i] > op.start && xc[i] < op.end && yc[j] > y0 && yc[j] < y1) { b.T[i * ny + j] = kind; any = true; }
    } else throw new Error(`unknown side ${op.side}`);
    if (!any) throw new Error(`the ${op.side} opening covers no cell faces: refine the mesh`);
  }
  return b;
}

// pressure operator M = -A (SPD) as face coefficients and diagonal; coarse levels by aggregation
function fineOperator(n, d, b) {
  const [a, bb, c] = n, [dx, dy, dz] = d;
  const cx = new Float64Array((a + 1) * bb * c), cy = new Float64Array(a * (bb + 1) * c), cz = new Float64Array(a * bb * (c + 1));
  for (let i = 1; i < a; i++) for (let j = 0; j < bb; j++) for (let k = 0; k < c; k++) cx[(i * bb + j) * c + k] = 1 / dx ** 2;
  for (let i = 0; i < a; i++) for (let j = 1; j < bb; j++) for (let k = 0; k < c; k++) cy[(i * (bb + 1) + j) * c + k] = 1 / dy ** 2;
  for (let i = 0; i < a; i++) for (let j = 0; j < bb; j++) for (let k = 1; k < c; k++) cz[(i * bb + j) * (c + 1) + k] = 1 / dz ** 2;
  const dg = new Float64Array(a * bb * c);
  for (let i = 0; i < a; i++) for (let j = 0; j < bb; j++) for (let k = 0; k < c; k++) {
    let s = cx[(i * bb + j) * c + k] + cx[((i + 1) * bb + j) * c + k] + cy[(i * (bb + 1) + j) * c + k]
          + cy[(i * (bb + 1) + j + 1) * c + k] + cz[(i * bb + j) * (c + 1) + k] + cz[(i * bb + j) * (c + 1) + k + 1];
    if (i === 0 && b.L[j * c + k] === OUTLET) s += 2 / dx ** 2;
    if (i === a - 1 && b.R[j * c + k] === OUTLET) s += 2 / dx ** 2;
    if (k === c - 1 && b.T[i * bb + j] === OUTLET) s += 2 / dz ** 2;
    dg[(i * bb + j) * c + k] = s;
  }
  return { n, cx, cy, cz, dg };
}

function coarsen(op, scale = 0.5) {
  const [a, b, c] = op.n, A = (a + 1) >> 1, B = (b + 1) >> 1, C = (c + 1) >> 1;
  const Cx = new Float64Array((A + 1) * B * C), Cy = new Float64Array(A * (B + 1) * C), Cz = new Float64Array(A * B * (C + 1));
  const D = new Float64Array(A * B * C);
  const cxf = (i, j, k) => op.cx[(i * b + j) * c + k], cyf = (i, j, k) => op.cy[(i * (b + 1) + j) * c + k];
  const czf = (i, j, k) => op.cz[(i * b + j) * (c + 1) + k];
  const rng = (I, n) => (2 * I + 1 < n ? [2 * I, 2 * I + 1] : [2 * I]);
  for (let I = 0; I <= A; I++) for (let J = 0; J < B; J++) for (let K = 0; K < C; K++) {
    const fi = Math.min(2 * I, a); let s = 0;
    for (const j of rng(J, b)) for (const k of rng(K, c)) s += cxf(fi, j, k);
    Cx[(I * B + J) * C + K] = scale * s;
  }
  for (let I = 0; I < A; I++) for (let J = 0; J <= B; J++) for (let K = 0; K < C; K++) {
    const fj = Math.min(2 * J, b); let s = 0;
    for (const i of rng(I, a)) for (const k of rng(K, c)) s += cyf(i, fj, k);
    Cy[(I * (B + 1) + J) * C + K] = scale * s;
  }
  for (let I = 0; I < A; I++) for (let J = 0; J < B; J++) for (let K = 0; K <= C; K++) {
    const fk = Math.min(2 * K, c); let s = 0;
    for (const i of rng(I, a)) for (const j of rng(J, b)) s += czf(i, j, fk);
    Cz[(I * B + J) * (C + 1) + K] = scale * s;
  }
  for (let I = 0; I < A; I++) for (let J = 0; J < B; J++) for (let K = 0; K < C; K++) {
    let s = 0;
    for (const i of rng(I, a)) for (const j of rng(J, b)) for (const k of rng(K, c)) {
      s += op.dg[(i * b + j) * c + k];
      if (i === 2 * I && 2 * I + 1 < a) s -= 2 * cxf(i + 1, j, k);       // couplings inside the aggregate cancel
      if (j === 2 * J && 2 * J + 1 < b) s -= 2 * cyf(i, j + 1, k);
      if (k === 2 * K && 2 * K + 1 < c) s -= 2 * czf(i, j, k + 1);
    }
    D[(I * B + J) * C + K] = scale * s;
  }
  return { n: [A, B, C], cx: Cx, cy: Cy, cz: Cz, dg: D };
}

function denseInverse(op) {
  const [a, b, c] = op.n, N = a * b * c, M = new Float64Array(N * N), X = new Float64Array(N * N);
  for (let i = 0; i < a; i++) for (let j = 0; j < b; j++) for (let k = 0; k < c; k++) {
    const r = (i * b + j) * c + k; M[r * N + r] = op.dg[r];
    if (i > 0) M[r * N + r - b * c] = -op.cx[(i * b + j) * c + k];
    if (i < a - 1) M[r * N + r + b * c] = -op.cx[((i + 1) * b + j) * c + k];
    if (j > 0) M[r * N + r - c] = -op.cy[(i * (b + 1) + j) * c + k];
    if (j < b - 1) M[r * N + r + c] = -op.cy[(i * (b + 1) + j + 1) * c + k];
    if (k > 0) M[r * N + r - 1] = -op.cz[(i * b + j) * (c + 1) + k];
    if (k < c - 1) M[r * N + r + 1] = -op.cz[(i * b + j) * (c + 1) + k + 1];
  }
  for (let r = 0; r < N; r++) X[r * N + r] = 1;
  for (let col = 0; col < N; col++) {                      // Gauss-Jordan with partial pivoting
    let piv = col;
    for (let r = col + 1; r < N; r++) if (Math.abs(M[r * N + col]) > Math.abs(M[piv * N + col])) piv = r;
    for (let m = 0; m < N; m++) {
      [M[col * N + m], M[piv * N + m]] = [M[piv * N + m], M[col * N + m]];
      [X[col * N + m], X[piv * N + m]] = [X[piv * N + m], X[col * N + m]];
    }
    const p = M[col * N + col];
    for (let m = 0; m < N; m++) { M[col * N + m] /= p; X[col * N + m] /= p; }
    for (let r = 0; r < N; r++) if (r !== col) {
      const f = M[r * N + col]; if (f === 0) continue;
      for (let m = 0; m < N; m++) { M[r * N + m] -= f * M[col * N + m]; X[r * N + m] -= f * X[col * N + m]; }
    }
  }
  return X;
}

// ---------------------------------------------------------------------------------------------
// the simulation
// ---------------------------------------------------------------------------------------------
export async function createSim(device, c) {
  const nx = c.nx, ny = c.ny, nz = c.nz, n = [nx, ny, nz];
  const d = [c.L / nx, c.W / ny, c.H / nz], [dx, dy, dz] = d;
  const N = nx * ny * nz, Nu = (nx + 1) * ny * nz, Nv = nx * (ny + 1) * nz, Nw = nx * ny * (nz + 1);
  const bnd = boundaries(c);
  const q = c.ach * c.L * c.H * c.W / 3600.0;
  let nIn = 0; for (const m of [bnd.L, bnd.R]) for (const v of m) if (v === INLET) nIn++;
  const A_in = nIn * dy * dz, U_in = q / A_in, h_in = A_in / c.W;
  const Q_tot = c.heat.reduce((s, b) => s + b.power, 0) + c.floor_flux.reduce((s, f) => s + f.power, 0);
  const T_mix = c.T_in + Q_tot / (RHO * CP * q);
  const T0 = c.T_room0 ?? T_mix;
  const beta = 1.0 / (273.15 + T0);
  const ke = c.turbulence === "k-epsilon", tvd = c.advection === "tvd";
  const k_in = 1.5 * (c.Tu_in * U_in) ** 2, e_in = k_in ** 1.5 / (0.1 * h_in);
  const xc = centres(nx, dx), yc = centres(ny, dy), zc = centres(nz, dz);

  // ---- memory layout: one f32 storage buffer, scalars first ----
  const S = { DT: 0, UMAX: 1, NUMAX: 2, RZ: 3, ALPHA: 4, BETA: 5, BB: 6, DONE: 7, STOP: 8, T: 9, WA: 10, AVG: 11,
              ITS: 12, ITS_STEP: 13, ITS_MAX: 14, NOTCONV: 15, STEPS: 16 };
  const NWG = Math.max(1, Math.min(256, Math.ceil(N / 256)));
  let top = 64 + 2 * 256;
  const O = {}, shape = {};
  const alloc = (name, size, shp) => { O[name] = top; shape[name] = shp; top += size + ((64 - (size % 64)) % 64); };
  const su = [nx + 1, ny, nz], sv = [nx, ny + 1, nz], sw = [nx, ny, nz + 1];
  alloc("u", Nu, su); alloc("v", Nv, sv); alloc("w", Nw, sw);        // u, v, w must be contiguous (max |U|)
  O.v = O.u + Nu; O.w = O.v + Nv; top = O.w + Nw; top += (64 - (top % 64)) % 64;
  alloc("us", Nu, su); alloc("vs", Nv, sv); alloc("ws", Nw, sw);
  for (const f of ["T", "Tn", "k", "kn", "e", "en", "nuc", "S", "ypw", "lwall", "P", "p", "b", "r", "dd", "Ad"]) alloc(f, N, n);
  alloc("ne01", (nx + 1) * (ny + 1) * nz); alloc("ne02", (nx + 1) * ny * (nz + 1)); alloc("ne12", nx * (ny + 1) * (nz + 1));
  alloc("wd01", (nx + 1) * (ny + 1) * nz); alloc("wd02", (nx + 1) * ny * (nz + 1)); alloc("wd12", nx * (ny + 1) * (nz + 1));
  alloc("qfl", nx * ny); alloc("bL", ny * nz); alloc("bR", ny * nz); alloc("bT", nx * ny);
  for (const f of ["F0", "Fk0", "Fe0"]) alloc(f, Nu); for (const f of ["F1", "Fk1", "Fe1"]) alloc(f, Nv);
  for (const f of ["F2", "Fk2", "Fe2"]) alloc(f, Nw);
  alloc("au", Nu + Nv + Nw); O.av = O.au + Nu; O.aw = O.av + Nv;           // contiguous like u, v, w
  for (const f of ["aT", "as", "anu", "ak"]) alloc(f, N);

  // multigrid levels
  const ops = [fineOperator(n, d, bnd)];
  while (ops[ops.length - 1].dg.length > 128) ops.push(coarsen(ops[ops.length - 1]));
  const nl = ops.length;
  ops.forEach((op, l) => {
    alloc(`cx${l}`, op.cx.length); alloc(`cy${l}`, op.cy.length); alloc(`cz${l}`, op.cz.length); alloc(`dg${l}`, op.dg.length);
    const m = op.dg.length;
    if (l > 0) alloc(`R${l}`, m);
    if (l < nl - 1) { alloc(`Xa${l}`, m); alloc(`Xb${l}`, m); } else alloc(`Xb${l}`, m);
  });
  O.R0 = O.r;
  const Minv = denseInverse(ops[nl - 1]); alloc("Minv", Minv.length);
  const total = top;
  const maxBytes = device.limits.maxStorageBufferBindingSize;
  if (total * 4 > maxBytes) throw new Error(`mesh too large for this GPU (${(total * 4 / 1e6).toFixed(0)} MB)`);

  // ---- initial data ----
  const init = new Float32Array(total);
  const put = (name, arr) => init.set(arr, O[name]);
  init[S.STOP] = 0;
  const fill = (name, size, v) => init.fill(v, O[name], O[name] + size);
  fill("k", N, k_in); fill("e", N, e_in);
  const yp = new Float64Array(N).fill(Infinity);
  const lw = new Float32Array(N), Sv = new Float32Array(N);
  const id = (i, j, k) => (i * ny + j) * nz + k;
  const setWall = (ax, side, m, dims) => {
    for (let a = 0; a < dims[0]; a++) for (let b2 = 0; b2 < dims[1]; b2++) {
      if (m[a * dims[1] + b2] !== WALL) continue;
      const p = ax === 0 ? [side ? nx - 1 : 0, a, b2] : ax === 1 ? [a, side ? ny - 1 : 0, b2] : [a, b2, side ? nz - 1 : 0];
      const r = id(...p); yp[r] = Math.min(yp[r], d[ax] / 2);
    }
  };
  setWall(0, 0, bnd.L, [ny, nz]); setWall(0, 1, bnd.R, [ny, nz]); setWall(1, 0, bnd.B, [nx, nz]);
  setWall(1, 1, bnd.F, [nx, nz]); setWall(2, 0, bnd.D, [nx, ny]); setWall(2, 1, bnd.T, [nx, ny]);
  const ypw = new Float32Array(N); for (let r = 0; r < N; r++) ypw[r] = isFinite(yp[r]) ? yp[r] : 0;
  for (let i = 0; i < nx; i++) for (let j = 0; j < ny; j++) for (let k = 0; k < nz; k++)
    lw[id(i, j, k)] = Math.min(xc[i], c.L - xc[i], yc[j], c.W - yc[j], zc[k], c.H - zc[k]);
  for (const hb of c.heat) {
    const cells = [];
    for (let i = 0; i < nx; i++) for (let j = 0; j < ny; j++) for (let k = 0; k < nz; k++)
      if (xc[i] > hb.x0 && xc[i] < hb.x1 && yc[j] > hb.y0 && yc[j] < hb.y1 && zc[k] > hb.z0 && zc[k] < hb.z1) cells.push(id(i, j, k));
    for (const r of cells) Sv[r] += hb.power / (cells.length * dx * dy * dz);
  }
  const qf = new Float32Array(nx * ny);
  for (const f of c.floor_flux) {
    const cells = [];
    for (let i = 0; i < nx; i++) for (let j = 0; j < ny; j++)
      if (xc[i] > f.x0 && xc[i] < f.x1 && yc[j] > f.y0 && yc[j] < f.y1) cells.push(i * ny + j);
    for (const r of cells) qf[r] += f.power / (cells.length * dx * dy);
  }
  put("ypw", ypw); put("lwall", lw); put("S", Sv); put("qfl", qf);
  put("bL", Float32Array.from(bnd.L)); put("bR", Float32Array.from(bnd.R)); put("bT", Float32Array.from(bnd.T));
  // wall distance on the edges that get the log-law viscosity (as room_cfd_3d_numba.run)
  const wall2 = { "0,0": [bnd.L, [ny, nz]], "0,1": [bnd.R, [ny, nz]], "1,0": [bnd.B, [nx, nz]], "1,1": [bnd.F, [nx, nz]],
                  "2,0": [bnd.D, [nx, ny]], "2,1": [bnd.T, [nx, ny]] };
  for (const [p, qq] of [[0, 1], [0, 2], [1, 2]]) {
    const es = [0, 1, 2].map((a) => n[a] + (a === p || a === qq ? 1 : 0));
    const wdA = new Float32Array(es[0] * es[1] * es[2]);
    for (const [wa, other] of [[qq, p], [p, qq]]) {
      for (const [side, pos] of [[0, 0], [1, n[wa]]]) {
        const [m, dims] = wall2[`${wa},${side}`];
        const third = [0, 1, 2].find((a) => a !== wa && a !== other);
        const oth = other < wa ? other : other - 1;               // axis of `other` in the wall mask
        for (let eo = 0; eo <= n[other]; eo++) for (let t = 0; t < n[third]; t++) {
          const mi = (o) => { const oc = Math.min(Math.max(o, 0), n[other] - 1); return oth === 0 ? oc * dims[1] + t : t * dims[1] + oc; };
          if (m[mi(eo - 1)] !== WALL || m[mi(eo)] !== WALL) continue;
          const e = [0, 0, 0]; e[wa] = pos; e[other] = eo; e[third] = t;
          wdA[(e[0] * es[1] + e[1]) * es[2] + e[2]] = d[wa] / 2;
        }
      }
    }
    put(`wd${p}${qq}`, wdA);
  }
  // initial velocity: the inlet faces
  for (let j = 0; j < ny; j++) for (let k = 0; k < nz; k++) {
    if (bnd.L[j * nz + k] === INLET) init[O.u + (0 * ny + j) * nz + k] = U_in;
    if (bnd.R[j * nz + k] === INLET) init[O.u + (nx * ny + j) * nz + k] = -U_in;
  }
  ops.forEach((op, l) => { put(`cx${l}`, op.cx); put(`cy${l}`, op.cy); put(`cz${l}`, op.cz); put(`dg${l}`, op.dg); });
  put("Minv", Minv);

  // ---- WGSL ----
  const f = (x) => { const s = Number(x).toExponential(9); return s; };
  const shp = (s) => `vec3<i32>(${s[0]}, ${s[1]}, ${s[2]})`;
  const consts = Object.entries(O).map(([k, v]) => `const O_${k}: i32 = ${v};`).join("\n")
    + "\n" + Object.entries(S).map(([k, v]) => `const S_${k}: i32 = ${v};`).join("\n");
  const cfl = tvd ? 0.25 : 0.4, h = Math.min(dx, dy, dz);
  let code = `
@group(0) @binding(0) var<storage, read_write> F: array<f32>;
const NX: i32 = ${nx}; const NY: i32 = ${ny}; const NZ: i32 = ${nz};
const NC = vec3<i32>(${nx}, ${ny}, ${nz});
const DX: f32 = ${f(dx)}; const DY: f32 = ${f(dy)}; const DZ: f32 = ${f(dz)};
const NU: f32 = ${f(NU_AIR)}; const CMU: f32 = ${f(CMU)}; const KAP: f32 = ${f(KAP)}; const EWF: f32 = ${f(EWF)};
const C1: f32 = ${f(C1)}; const C2: f32 = ${f(C2)}; const SK: f32 = ${f(SK)}; const SE: f32 = ${f(SE)};
const PRT: f32 = ${f(c.Pr_t)}; const RCP: f32 = ${f(RHO * CP)}; const GB: f32 = ${f(G * beta)};
const UIN: f32 = ${f(U_in)}; const KIN: f32 = ${f(k_in)}; const EIN: f32 = ${f(e_in)}; const TIN: f32 = ${f(c.T_in - T0)};
const TOL2: f32 = ${f(c.p_tol ** 2)}; const TEND: f32 = ${f(c.t_end)}; const TAVG0: f32 = ${f(c.t_end - c.t_avg)};
const NUT_C: f32 = ${f(c.nu_t)};
const NWG: i32 = ${NWG}; const N: i32 = ${N};
${consts}
var<workgroup> sa: array<f32, 256>;
var<workgroup> sb: array<f32, 256>;

fn stopped() -> bool { return F[S_STOP] > 0.5; }
fn cgoff() -> bool { return F[S_STOP] > 0.5 || F[S_DONE] > 0.5; }
fn id3(g: u32, s: vec3<i32>) -> vec3<i32> { let m = i32(g); let t = m / s.z; return vec3<i32>(t / s.y, t % s.y, m % s.z); }
fn ix(s: vec3<i32>, p: vec3<i32>) -> i32 { return (p.x * s.y + p.y) * s.z + p.z; }
fn at(o: i32, s: vec3<i32>, p: vec3<i32>) -> f32 { return F[o + ix(s, p)]; }
fn sh(a: i32, s: i32) -> vec3<i32> { if (a == 0) { return vec3<i32>(s, 0, 0); } if (a == 1) { return vec3<i32>(0, s, 0); } return vec3<i32>(0, 0, s); }
fn ushp(c: i32) -> vec3<i32> { return NC + sh(c, 1); }
fn uoff(c: i32) -> i32 { if (c == 0) { return O_u; } if (c == 1) { return O_v; } return O_w; }
fn usoff(c: i32) -> i32 { if (c == 0) { return O_us; } if (c == 1) { return O_vs; } return O_ws; }
fn Uat(c: i32, p: vec3<i32>) -> f32 { return at(uoff(c), ushp(c), p); }
fn cell(o: i32, p: vec3<i32>) -> f32 { return F[o + ix(NC, p)]; }
fn neshp(p: i32, q: i32) -> vec3<i32> { return NC + sh(p, 1) + sh(q, 1); }
fn neoff(p: i32, q: i32) -> i32 { if (p == 0 && q == 1) { return O_ne01; } if (p == 0) { return O_ne02; } return O_ne12; }
fn lim(a: f32, b: f32) -> f32 { return (a * abs(b) + abs(a) * b) / (abs(a) + abs(b) + 1e-30); }
fn ddx(pm2: f32, pm1: f32, p0: f32, pp1: f32, pp2: f32, vel: f32, h: f32) -> f32 {
  let d0 = pm1 - pm2; let d1 = p0 - pm1; let d2 = pp1 - p0; let d3 = pp2 - pp1;
  var l0 = 0.0; var l1 = 0.0; var l2 = 0.0;
  ${tvd ? "l0 = lim(d0, d1); l1 = lim(d1, d2); l2 = lim(d2, d3);" : ""}
  if (vel > 0.0) { return (d1 + 0.5 * l1 - 0.5 * l0) / h; }
  return (d2 - 0.5 * l2 + 0.5 * l1) / h;
}
fn face(em1: f32, e0: f32, e1: f32, e2: f32, vel: f32, tv: bool) -> f32 {
  if (!tv) { if (vel > 0.0) { return e0; } return e1; }
  if (vel > 0.0) { return e0 + 0.5 * lim(e0 - em1, e1 - e0); }
  return e1 - 0.5 * lim(e1 - e0, e2 - e1);
}
fn nu_wall(kw: f32, y: f32) -> f32 {
  let ys = pow(CMU, 0.25) * sqrt(kw) * y / NU;
  if (ys > 11.2) { return KAP * ys * NU / log(EWF * max(ys, 1.0)); }
  return NU;
}
// U_c at p shifted s along a: zero-gradient ends along its own axis, mirrored (no slip) across walls
fn gv(c: i32, a: i32, p: vec3<i32>, s: i32) -> f32 {
  let n = ushp(c); let q = p + sh(a, s);
  let qc = clamp(q, vec3<i32>(0), n - vec3<i32>(1));
  let v = at(uoff(c), n, qc);
  if (a != c && any(q != qc)) { return -v; }
  return v;
}
fn mterm(c: i32, a: i32, p: vec3<i32>, u0: f32, h: f32) -> f32 {
  var vel: f32; var f1: f32; var f0: f32;
  let g1 = gv(c, a, p, 1); let gm1 = gv(c, a, p, -1);
  if (a == c) {
    vel = u0;
    f1 = cell(O_nuc, p) * (Uat(c, p + sh(a, 1)) - u0) / h;
    f0 = cell(O_nuc, p - sh(a, 1)) * (u0 - Uat(c, p - sh(a, 1))) / h;
  } else {
    let sa_ = ushp(a); let oa = uoff(a);
    vel = 0.25 * (at(oa, sa_, p + sh(c, -1)) + at(oa, sa_, p) + at(oa, sa_, p + sh(c, -1) + sh(a, 1)) + at(oa, sa_, p + sh(a, 1)));
    let lo = min(a, c); let hi = max(a, c);
    let ns = neshp(lo, hi); let no = neoff(lo, hi);
    f1 = at(no, ns, p + sh(a, 1)) * (g1 - u0) / h;
    f0 = at(no, ns, p) * (u0 - gm1) / h;
  }
  let der = ddx(gv(c, a, p, -2), gm1, u0, g1, gv(c, a, p, 2), vel, h);
  return -vel * der + (f1 - f0) / h;
}

@compute @workgroup_size(1) fn begin() {
  F[S_STOP] = select(0.0, 1.0, F[S_T] >= TEND);
  F[S_ITS_STEP] = 0.0;
}

@compute @workgroup_size(64) fn nuc(@builtin(global_invocation_id) g: vec3<u32>) {
  if (stopped() || i32(g.x) >= N) { return; }
  let p = id3(g.x, NC); let m = i32(g.x);
  ${ke ? "F[O_nuc + m] = NU + CMU * F[O_k + m] * F[O_k + m] / F[O_e + m];"
       : c.turbulence === "constant" ? "F[O_nuc + m] = NU + NUT_C;"
       : `let uc = 0.5 * (Uat(0, p + sh(0, 1)) + Uat(0, p)); let vc = 0.5 * (Uat(1, p + sh(1, 1)) + Uat(1, p));
          let wc = 0.5 * (Uat(2, p + sh(2, 1)) + Uat(2, p));
          F[O_nuc + m] = NU + 0.03874 * sqrt(uc * uc + vc * vc + wc * wc) * F[O_lwall + m];`}
}

// max |U| and max nu_c: partial maxima per workgroup, then the time step
@compute @workgroup_size(256) fn red1_dt(@builtin(local_invocation_id) l: vec3<u32>, @builtin(workgroup_id) w: vec3<u32>) {
  var a = 0.0; var b = 0.0;
  let t = i32(l.x); let s = i32(w.x) * 256 + t;
  for (var m = s; m < ${Nu + Nv + Nw}; m += NWG * 256) { a = max(a, abs(F[O_u + m])); }
  for (var m = s; m < N; m += NWG * 256) { b = max(b, F[O_nuc + m]); }
  sa[t] = a; sb[t] = b; workgroupBarrier();
  for (var st = 128; st > 0; st >>= 1u) { if (t < st) { sa[t] = max(sa[t], sa[t + st]); sb[t] = max(sb[t], sb[t + st]); } workgroupBarrier(); }
  if (t == 0) { F[64 + i32(w.x)] = sa[0]; F[64 + 256 + i32(w.x)] = sb[0]; }
}
@compute @workgroup_size(256) fn red2_dt(@builtin(local_invocation_id) l: vec3<u32>) {
  let t = i32(l.x);
  sa[t] = select(0.0, F[64 + t], t < NWG); sb[t] = select(0.0, F[64 + 256 + t], t < NWG); workgroupBarrier();
  for (var st = 128; st > 0; st >>= 1u) { if (t < st) { sa[t] = max(sa[t], sa[t + st]); sb[t] = max(sb[t], sb[t + st]); } workgroupBarrier(); }
  if (t == 0 && !stopped()) {
    let um = max(max(sa[0], UIN), 0.05);
    F[S_UMAX] = um; F[S_NUMAX] = sb[0];
    F[S_DT] = min(min(${f(cfl * h)} / um, ${f(0.15 * h * h)} / sb[0]), 0.5);
  }
}
`;
  // edge viscosity, one kernel per pair
  for (const [p, qq] of [[0, 1], [0, 2], [1, 2]]) {
    code += `
@compute @workgroup_size(64) fn edge${p}${qq}(@builtin(global_invocation_id) g: vec3<u32>) {
  let s = neshp(${p}, ${qq});
  if (stopped() || i32(g.x) >= s.x * s.y * s.z) { return; }
  let e = id3(g.x, s);
  let ex = ${p === 0 || qq === 0}; let ey = ${p === 1 || qq === 1}; let ez = ${p === 2 || qq === 2};
  let il = select(e.x, max(e.x - 1, 0), ex); let ih = select(e.x, min(e.x, NX - 1), ex);
  let jl = select(e.y, max(e.y - 1, 0), ey); let jh = select(e.y, min(e.y, NY - 1), ey);
  let kl = select(e.z, max(e.z - 1, 0), ez); let kh = select(e.z, min(e.z, NZ - 1), ez);
  let c0 = vec3<i32>(il, jl, kl); let c3 = vec3<i32>(ih, jh, kh);
  var c1 = c0; c1[${p}] = c3[${p}];          // (p hi, q lo)
  var c2 = c0; c2[${qq}] = c3[${qq}];          // (p lo, q hi)
  var v = 0.25 * (cell(O_nuc, c0) + cell(O_nuc, c1) + cell(O_nuc, c2) + cell(O_nuc, c3));
  ${ke ? `let wdv = F[O_wd${p}${qq} + i32(g.x)];
  if (wdv > 0.0) { v = nu_wall(0.25 * (cell(O_k, c0) + cell(O_k, c1) + cell(O_k, c2) + cell(O_k, c3)), wdv); }` : ""}
  F[O_ne${p}${qq} + i32(g.x)] = v;
}`;
  }
  // momentum predictors
  for (const cc of [0, 1, 2]) {
    code += `
@compute @workgroup_size(64) fn mom${cc}(@builtin(global_invocation_id) g: vec3<u32>) {
  let s = ushp(${cc});
  if (stopped() || i32(g.x) >= s.x * s.y * s.z) { return; }
  let p = id3(g.x, s);
  if (p[${cc}] == 0 || p[${cc}] == s[${cc}] - 1) { return; }
  let u0 = F[uoff(${cc}) + i32(g.x)];
  var rhs = mterm(${cc}, 0, p, u0, DX) + mterm(${cc}, 1, p, u0, DY) + mterm(${cc}, 2, p, u0, DZ);
  ${cc === 2 ? "rhs += GB * 0.5 * (cell(O_T, p - sh(2, 1)) + cell(O_T, p));" : ""}
  F[usoff(${cc}) + i32(g.x)] = u0 + F[S_DT] * rhs;
}`;
  }
  code += `
// boundary values of the predicted velocity
@compute @workgroup_size(64) fn bc(@builtin(global_invocation_id) g: vec3<u32>) {
  if (stopped()) { return; }
  let m = i32(g.x);
  if (m < NY * NZ) {
    let j = m / NZ; let k = m % NZ;
    let bl = F[O_bL + m]; let br = F[O_bR + m];
    var a = 0.0; if (bl == 1.0) { a = UIN; } else if (bl == 2.0) { a = F[O_us + (1 * NY + j) * NZ + k]; }
    F[O_us + (0 * NY + j) * NZ + k] = a;
    var b = 0.0; if (br == 1.0) { b = -UIN; } else if (br == 2.0) { b = F[O_us + ((NX - 1) * NY + j) * NZ + k]; }
    F[O_us + (NX * NY + j) * NZ + k] = b;
  }
  if (m < NX * NZ) {
    let i = m / NZ; let k = m % NZ;
    F[O_vs + (i * (NY + 1) + 0) * NZ + k] = 0.0; F[O_vs + (i * (NY + 1) + NY) * NZ + k] = 0.0;
  }
  if (m < NX * NY) {
    let i = m / NY; let j = m % NY;
    F[O_ws + (i * NY + j) * (NZ + 1)] = 0.0;
    F[O_ws + (i * NY + j) * (NZ + 1) + NZ] = select(0.0, F[O_ws + (i * NY + j) * (NZ + 1) + NZ - 1], F[O_bT + m] == 2.0);
  }
}
// right-hand side of M p = b (M = -A): b = -div(U*) / dt
@compute @workgroup_size(64) fn rhs(@builtin(global_invocation_id) g: vec3<u32>) {
  if (stopped() || i32(g.x) >= N) { return; }
  let p = id3(g.x, NC);
  let dv = (at(O_us, ushp(0), p + sh(0, 1)) - at(O_us, ushp(0), p)) / DX + (at(O_vs, ushp(1), p + sh(1, 1)) - at(O_vs, ushp(1), p)) / DY
         + (at(O_ws, ushp(2), p + sh(2, 1)) - at(O_ws, ushp(2), p)) / DZ;
  F[O_b + i32(g.x)] = -dv / F[S_DT];
}
`;
  // multigrid levels: M x, Jacobi sweeps, restriction, coarse solve
  ops.forEach((op, l) => {
    const [a, b, cz] = op.n, s = shp(op.n);
    code += `
fn xv${l}(ox: i32, oe: i32, p: vec3<i32>) -> f32 {
  var v = F[ox + (p.x * ${b} + p.y) * ${cz} + p.z];
  ${l < nl - 1 ? `if (oe >= 0) { v += F[oe + ((p.x / 2) * ${ops[l + 1].n[1]} + p.y / 2) * ${ops[l + 1].n[2]} + p.z / 2]; }` : ""}
  return v;
}
fn Mx${l}(ox: i32, oe: i32, p: vec3<i32>) -> f32 {
  var y = F[O_dg${l} + (p.x * ${b} + p.y) * ${cz} + p.z] * xv${l}(ox, oe, p);
  if (p.x > 0) { y -= F[O_cx${l} + (p.x * ${b} + p.y) * ${cz} + p.z] * xv${l}(ox, oe, p - vec3<i32>(1, 0, 0)); }
  if (p.x < ${a - 1}) { y -= F[O_cx${l} + ((p.x + 1) * ${b} + p.y) * ${cz} + p.z] * xv${l}(ox, oe, p + vec3<i32>(1, 0, 0)); }
  if (p.y > 0) { y -= F[O_cy${l} + (p.x * ${b + 1} + p.y) * ${cz} + p.z] * xv${l}(ox, oe, p - vec3<i32>(0, 1, 0)); }
  if (p.y < ${b - 1}) { y -= F[O_cy${l} + (p.x * ${b + 1} + p.y + 1) * ${cz} + p.z] * xv${l}(ox, oe, p + vec3<i32>(0, 1, 0)); }
  if (p.z > 0) { y -= F[O_cz${l} + (p.x * ${b} + p.y) * ${cz + 1} + p.z] * xv${l}(ox, oe, p - vec3<i32>(0, 0, 1)); }
  if (p.z < ${cz - 1}) { y -= F[O_cz${l} + (p.x * ${b} + p.y) * ${cz + 1} + p.z + 1] * xv${l}(ox, oe, p + vec3<i32>(0, 0, 1)); }
  return y;
}`;
    if (l < nl - 1) {
      const [A, B, C] = ops[l + 1].n;
      code += `
@compute @workgroup_size(64) fn jac0_${l}(@builtin(global_invocation_id) g: vec3<u32>) {
  let m = i32(g.x); if (cgoff() || m >= ${a * b * cz}) { return; }
  F[O_Xa${l} + m] = 0.8 * F[O_R${l} + m] / F[O_dg${l} + m];
}
@compute @workgroup_size(64) fn jacA_${l}(@builtin(global_invocation_id) g: vec3<u32>) {
  let m = i32(g.x); if (cgoff() || m >= ${a * b * cz}) { return; }
  let p = id3(g.x, ${s});
  F[O_Xb${l} + m] = F[O_Xa${l} + m] + 0.8 * (F[O_R${l} + m] - Mx${l}(O_Xa${l}, -1, p)) / F[O_dg${l} + m];
}
@compute @workgroup_size(64) fn jacC_${l}(@builtin(global_invocation_id) g: vec3<u32>) {
  let m = i32(g.x); if (cgoff() || m >= ${a * b * cz}) { return; }
  let p = id3(g.x, ${s});
  F[O_Xa${l} + m] = xv${l}(O_Xb${l}, O_Xb${l + 1}, p) + 0.8 * (F[O_R${l} + m] - Mx${l}(O_Xb${l}, O_Xb${l + 1}, p)) / F[O_dg${l} + m];
}
@compute @workgroup_size(64) fn restr_${l}(@builtin(global_invocation_id) g: vec3<u32>) {
  let m = i32(g.x); if (cgoff() || m >= ${A * B * C}) { return; }
  let P = id3(g.x, vec3<i32>(${A}, ${B}, ${C}));
  var s = 0.0;
  for (var di = 0; di < 2; di++) { for (var dj = 0; dj < 2; dj++) { for (var dk = 0; dk < 2; dk++) {
    let p = 2 * P + vec3<i32>(di, dj, dk);
    if (p.x < ${a} && p.y < ${b} && p.z < ${cz}) {
      s += F[O_R${l} + (p.x * ${b} + p.y) * ${cz} + p.z] - Mx${l}(O_Xb${l}, -1, p);
    }
  } } }
  F[O_R${l + 1} + m] = s;
}`;
    } else {
      const m = a * b * cz;
      code += `
var<workgroup> rc: array<f32, 128>;
@compute @workgroup_size(128) fn coarse(@builtin(local_invocation_id) li: vec3<u32>) {
  let t = i32(li.x);
  rc[t] = select(0.0, F[O_R${l} + t], t < ${m}); workgroupBarrier();
  if (t < ${m} && !cgoff()) {
    var s = 0.0;
    for (var j = 0; j < ${m}; j++) { s += F[O_Minv + t * ${m} + j] * rc[j]; }
    F[O_Xb${l} + t] = s;
  }
}`;
    }
  });
  // conjugate gradients: dot products in two stages (partial sums, then one workgroup)
  const red1 = (name, body, guard) => `
@compute @workgroup_size(256) fn ${name}(@builtin(local_invocation_id) l: vec3<u32>, @builtin(workgroup_id) w: vec3<u32>) {
  var a = 0.0; var b = 0.0;
  let t = i32(l.x); let off = ${guard ? "cgoff()" : "stopped()"};
  for (var m = i32(w.x) * 256 + t; m < N; m += NWG * 256) { ${body} }
  sa[t] = a; sb[t] = b; workgroupBarrier();
  for (var st = 128; st > 0; st >>= 1u) { if (t < st) { sa[t] += sa[t + st]; sb[t] += sb[t + st]; } workgroupBarrier(); }
  if (t == 0) { F[64 + i32(w.x)] = sa[0]; F[64 + 256 + i32(w.x)] = sb[0]; }
}`;
  const red2 = (name, body, guard) => `
@compute @workgroup_size(256) fn ${name}(@builtin(local_invocation_id) l: vec3<u32>) {
  let t = i32(l.x);
  sa[t] = select(0.0, F[64 + t], t < NWG); sb[t] = select(0.0, F[64 + 256 + t], t < NWG); workgroupBarrier();
  for (var st = 128; st > 0; st >>= 1u) { if (t < st) { sa[t] += sa[t + st]; sb[t] += sb[t + st]; } workgroupBarrier(); }
  if (t == 0 && !${guard ? "cgoff()" : "stopped()"}) { let A = sa[0]; let B = sb[0]; ${body} }
}`;
  code += `
// r = b - M p (warm start from the last pressure)
@compute @workgroup_size(64) fn cg_init(@builtin(global_invocation_id) g: vec3<u32>) {
  let m = i32(g.x); if (stopped() || m >= N) { return; }
  F[O_r + m] = F[O_b + m] - Mx0(O_p, -1, id3(g.x, NC));
}
${red1("cg_bbrr", "a += F[O_b + m] * F[O_b + m]; b += F[O_r + m] * F[O_r + m];", false)}
${red2("cg_bbrr2", "F[S_BB] = A; F[S_DONE] = select(0.0, 1.0, B <= TOL2 * A);", false)}
${red1("cg_rz0", "if (!off) { F[O_dd + m] = F[O_Xb0 + m]; } a += F[O_r + m] * F[O_Xb0 + m];", true)}
${red2("cg_rz02", "F[S_RZ] = A;", true)}
@compute @workgroup_size(64) fn cg_Ad(@builtin(global_invocation_id) g: vec3<u32>) {
  let m = i32(g.x); if (cgoff() || m >= N) { return; }
  F[O_Ad + m] = Mx0(O_dd, -1, id3(g.x, NC));
}
${red1("cg_dAd", "a += F[O_dd + m] * F[O_Ad + m];", true)}
${red2("cg_dAd2", "F[S_ALPHA] = F[S_RZ] / A;", true)}
${red1("cg_upd", "if (!off) { let al = F[S_ALPHA]; F[O_p + m] += al * F[O_dd + m]; F[O_r + m] -= al * F[O_Ad + m]; } a += F[O_r + m] * F[O_r + m];", true)}
${red2("cg_upd2", "F[S_ITS] += 1.0; F[S_ITS_STEP] += 1.0; F[S_DONE] = select(0.0, 1.0, A <= TOL2 * F[S_BB]);", true)}
${red1("cg_rz", "a += F[O_r + m] * F[O_Xb0 + m];", true)}
${red2("cg_rz2", "F[S_BETA] = A / F[S_RZ]; F[S_RZ] = A;", true)}
@compute @workgroup_size(64) fn cg_d(@builtin(global_invocation_id) g: vec3<u32>) {
  let m = i32(g.x); if (cgoff() || m >= N) { return; }
  F[O_dd + m] = F[O_Xb0 + m] + F[S_BETA] * F[O_dd + m];
}

// velocity correction (interior faces and outlet faces), then U = U*
@compute @workgroup_size(64) fn correct(@builtin(global_invocation_id) g: vec3<u32>) {
  let m = i32(g.x); if (stopped() || m >= ${Nu + Nv + Nw}) { return; }
  let dt = F[S_DT];
  if (m < ${Nu}) {
    let p = id3(u32(m), ushp(0)); var u = F[O_us + m];
    if (p.x > 0 && p.x < NX) { u -= dt * (cell(O_p, p) - cell(O_p, p - sh(0, 1))) / DX; }
    else if (p.x == 0 && F[O_bL + p.y * NZ + p.z] == 2.0) { u -= dt * cell(O_p, p) / (0.5 * DX); }
    else if (p.x == NX && F[O_bR + p.y * NZ + p.z] == 2.0) { u -= dt * (-cell(O_p, p - sh(0, 1))) / (0.5 * DX); }
    F[O_u + m] = u;
  } else if (m < ${Nu + Nv}) {
    let mm = m - ${Nu}; let p = id3(u32(mm), ushp(1)); var v = F[O_vs + mm];
    if (p.y > 0 && p.y < NY) { v -= dt * (cell(O_p, p) - cell(O_p, p - sh(1, 1))) / DY; }
    F[O_v + mm] = v;
  } else {
    let mm = m - ${Nu + Nv}; let p = id3(u32(mm), ushp(2)); var w = F[O_ws + mm];
    if (p.z > 0 && p.z < NZ) { w -= dt * (cell(O_p, p) - cell(O_p, p - sh(2, 1))) / DZ; }
    else if (p.z == NZ && F[O_bT + p.x * NY + p.y] == 2.0) { w -= dt * (-cell(O_p, p - sh(2, 1))) / (0.5 * DZ); }
    F[O_w + mm] = w;
  }
}

// face fluxes (advection + diffusion) of a cell-centred scalar
fn flux(o: i32, m: i32, phin: f32, tv: bool, kind: i32) -> f32 {
  var f: f32;
  if (m < ${Nu}) {
    let p = id3(u32(m), ushp(0));
    var e: array<f32, 4>;
    for (var s = 0; s < 4; s++) {
      let ii = p.x - 2 + s;
      if (ii < 0) { e[s] = select(F[o + ix(NC, vec3<i32>(0, p.y, p.z))], phin, F[O_bL + p.y * NZ + p.z] == 1.0); }
      else if (ii > NX - 1) { e[s] = select(F[o + ix(NC, vec3<i32>(NX - 1, p.y, p.z))], phin, F[O_bR + p.y * NZ + p.z] == 1.0); }
      else { e[s] = F[o + ix(NC, vec3<i32>(ii, p.y, p.z))]; }
    }
    let vel = F[O_u + m];
    f = vel * face(e[0], e[1], e[2], e[3], vel, tv);
    if (p.x > 0 && p.x < NX) { let pm = p - sh(0, 1); f -= 0.5 * (D(kind, p) + D(kind, pm)) * (F[o + ix(NC, p)] - F[o + ix(NC, pm)]) / DX; }
  } else if (m < ${Nu + Nv}) {
    let p = id3(u32(m - ${Nu}), ushp(1));
    let vel = F[O_v + m - ${Nu}];
    let a0 = F[o + ix(NC, vec3<i32>(p.x, clamp(p.y - 2, 0, NY - 1), p.z))]; let a1 = F[o + ix(NC, vec3<i32>(p.x, clamp(p.y - 1, 0, NY - 1), p.z))];
    let a2 = F[o + ix(NC, vec3<i32>(p.x, min(p.y, NY - 1), p.z))]; let a3 = F[o + ix(NC, vec3<i32>(p.x, min(p.y + 1, NY - 1), p.z))];
    f = vel * face(a0, a1, a2, a3, vel, tv);
    if (p.y > 0 && p.y < NY) { let pm = p - sh(1, 1); f -= 0.5 * (D(kind, p) + D(kind, pm)) * (F[o + ix(NC, p)] - F[o + ix(NC, pm)]) / DY; }
  } else {
    let p = id3(u32(m - ${Nu + Nv}), ushp(2));
    if (p.z == 0) { return select(0.0, -F[O_qfl + p.x * NY + p.y] / RCP, kind == 0); }
    let vel = F[O_w + m - ${Nu + Nv}];
    let a0 = F[o + ix(NC, vec3<i32>(p.x, p.y, max(p.z - 2, 0)))]; let a1 = F[o + ix(NC, vec3<i32>(p.x, p.y, p.z - 1))];
    let a2 = F[o + ix(NC, vec3<i32>(p.x, p.y, min(p.z, NZ - 1)))]; let a3 = F[o + ix(NC, vec3<i32>(p.x, p.y, min(p.z + 1, NZ - 1)))];
    f = vel * face(a0, a1, a2, a3, vel, tv);
    if (p.z < NZ) { let pm = p - sh(2, 1); f -= 0.5 * (D(kind, p) + D(kind, pm)) * (F[o + ix(NC, p)] - F[o + ix(NC, pm)]) / DZ; }
  }
  return f;
}
fn D(kind: i32, p: vec3<i32>) -> f32 {
  let nu = cell(O_nuc, p);
  if (kind == 0) { return nu / PRT; }
  if (kind == 1) { return NU + (nu - NU) / SK; }
  return NU + (nu - NU) / SE;
}
fn fdiv(o0: i32, o1: i32, o2: i32, p: vec3<i32>) -> f32 {
  return (at(o0, ushp(0), p + sh(0, 1)) - at(o0, ushp(0), p)) / DX + (at(o1, ushp(1), p + sh(1, 1)) - at(o1, ushp(1), p)) / DY
       + (at(o2, ushp(2), p + sh(2, 1)) - at(o2, ushp(2), p)) / DZ;
}
fn fout(o0: i32, o1: i32, o2: i32, m: i32) -> i32 {
  if (m < ${Nu}) { return o0 + m; } if (m < ${Nu + Nv}) { return o1 + m - ${Nu}; } return o2 + m - ${Nu + Nv};
}
@compute @workgroup_size(64) fn fluxT(@builtin(global_invocation_id) g: vec3<u32>) {
  let m = i32(g.x); if (stopped() || m >= ${Nu + Nv + Nw}) { return; }
  F[fout(O_F0, O_F1, O_F2, m)] = flux(O_T, m, TIN, ${tvd}, 0);
}
@compute @workgroup_size(64) fn energy(@builtin(global_invocation_id) g: vec3<u32>) {
  let m = i32(g.x); if (stopped() || m >= N) { return; }
  let p = id3(g.x, NC); let dt = F[S_DT];
  F[O_Tn + m] = F[O_T + m] - dt * fdiv(O_F0, O_F1, O_F2, p) + dt * F[O_S + m] / RCP;
}
`;
  if (ke) code += `
fn ash(p: vec3<i32>, q: vec3<i32>, s: vec3<i32>, o: i32) -> f32 {
  let r = p + q; let rc = clamp(r, vec3<i32>(0), s - vec3<i32>(1));
  let v = F[o + ix(s, rc)];
  if (any(r != rc)) { return -v; }
  return v;
}
// du_p/dx_q + du_q/dx_p on an edge, mirrored at walls
fn shear(p: i32, q: i32, c: vec3<i32>, sp: i32, sq: i32) -> f32 {
  let d = vec3<f32>(DX, DY, DZ);
  let a = (ash(c, sh(p, sp) + sh(q, sq), ushp(p), uoff(p)) - ash(c, sh(p, sp) + sh(q, sq - 1), ushp(p), uoff(p))) / d[q];
  let b = (ash(c, sh(q, sq) + sh(p, sp), ushp(q), uoff(q)) - ash(c, sh(q, sq) + sh(p, sp - 1), ushp(q), uoff(q))) / d[p];
  return a + b;
}
fn shear_c(p: i32, q: i32, c: vec3<i32>) -> f32 {
  return 0.25 * (shear(p, q, c, 0, 0) + shear(p, q, c, 1, 0) + shear(p, q, c, 0, 1) + shear(p, q, c, 1, 1));
}
@compute @workgroup_size(64) fn prod(@builtin(global_invocation_id) g: vec3<u32>) {
  let m = i32(g.x); if (stopped() || m >= N) { return; }
  let p = id3(g.x, NC);
  let e0 = (Uat(0, p + sh(0, 1)) - Uat(0, p)) / DX; let e1 = (Uat(1, p + sh(1, 1)) - Uat(1, p)) / DY;
  let e2 = (Uat(2, p + sh(2, 1)) - Uat(2, p)) / DZ;
  var s = 2.0 * (e0 * e0 + e1 * e1 + e2 * e2);
  let s01 = shear_c(0, 1, p); let s02 = shear_c(0, 2, p); let s12 = shear_c(1, 2, p);
  s += s01 * s01 + s02 * s02 + s12 * s12;
  var val = (F[O_nuc + m] - NU) * s;
  let y = F[O_ypw + m];
  if (y > 0.0) {
    let uc = 0.5 * (Uat(0, p + sh(0, 1)) + Uat(0, p)); let vc = 0.5 * (Uat(1, p + sh(1, 1)) + Uat(1, p));
    let wc = 0.5 * (Uat(2, p + sh(2, 1)) + Uat(2, p));
    let Up = sqrt(uc * uc + vc * vc + wc * wc); let kc = F[O_k + m];
    let tau = nu_wall(kc, y) * Up / y;
    val = tau * pow(CMU, 0.25) * sqrt(kc) / (KAP * y);
  }
  F[O_P + m] = val;
}
@compute @workgroup_size(64) fn fluxKE(@builtin(global_invocation_id) g: vec3<u32>) {
  let m = i32(g.x); if (stopped() || m >= ${Nu + Nv + Nw}) { return; }
  F[fout(O_Fk0, O_Fk1, O_Fk2, m)] = flux(O_k, m, KIN, false, 1);
  F[fout(O_Fe0, O_Fe1, O_Fe2, m)] = flux(O_e, m, EIN, false, 2);
}
@compute @workgroup_size(64) fn keps(@builtin(global_invocation_id) g: vec3<u32>) {
  let m = i32(g.x); if (stopped() || m >= N) { return; }
  let p = id3(g.x, NC); let dt = F[S_DT]; let z = p.z;
  var dT: f32;
  if (z == 0) { dT = (F[O_T + m + 1] - F[O_T + m]) / DZ; }
  else if (z == NZ - 1) { dT = (F[O_T + m] - F[O_T + m - 1]) / DZ; }
  else { dT = (F[O_T + m + 1] - F[O_T + m - 1]) / (2.0 * DZ); }
  let nut = F[O_nuc + m] - NU;
  let Gb = -GB * nut / PRT * dT;
  let Gp = max(Gb, 0.0); let Gm = max(-Gb, 0.0);
  let kc = F[O_k + m]; let ec = F[O_e + m]; let Pc = F[O_P + m];
  let kn = (kc + dt * (-fdiv(O_Fk0, O_Fk1, O_Fk2, p) + Pc + Gp)) / (1.0 + dt * (ec + Gm) / kc);
  let en = (ec + dt * (-fdiv(O_Fe0, O_Fe1, O_Fe2, p) + C1 * ec / kc * (Pc + Gp))) / (1.0 + dt * C2 * ec / kc);
  let kv = max(kn, 1e-10); var ev = max(en, 1e-12);
  let y = F[O_ypw + m];
  if (y > 0.0) { ev = pow(CMU, 0.75) * pow(kv, 1.5) / (KAP * y); }
  F[O_kn + m] = kv; F[O_en + m] = ev;
}
`;
  code += `
@compute @workgroup_size(64) fn copy2(@builtin(global_invocation_id) g: vec3<u32>) {
  let m = i32(g.x); if (stopped() || m >= N) { return; }
  F[O_T + m] = F[O_Tn + m];
  ${ke ? "F[O_k + m] = F[O_kn + m]; F[O_e + m] = F[O_en + m];" : ""}
}
@compute @workgroup_size(1) fn tadv() {
  if (stopped()) { return; }
  F[S_T] += F[S_DT]; F[S_STEPS] += 1.0;
  F[S_ITS_MAX] = max(F[S_ITS_MAX], F[S_ITS_STEP]);
  F[S_NOTCONV] += select(1.0, 0.0, F[S_DONE] > 0.5);
  if (F[S_T] >= TAVG0) { F[S_WA] += F[S_DT]; F[S_AVG] = 1.0; } else { F[S_AVG] = 0.0; }
}
@compute @workgroup_size(64) fn avg(@builtin(global_invocation_id) g: vec3<u32>) {
  let m = i32(g.x); if (stopped() || F[S_AVG] < 0.5 || m >= ${Nu + Nv + Nw}) { return; }
  let dt = F[S_DT];
  F[O_au + m] += dt * F[O_u + m];          // au, av, aw contiguous like u, v, w
  if (m < N) {
    let p = id3(g.x, NC);
    let uc = 0.5 * (Uat(0, p + sh(0, 1)) + Uat(0, p)); let vc = 0.5 * (Uat(1, p + sh(1, 1)) + Uat(1, p));
    let wc = 0.5 * (Uat(2, p + sh(2, 1)) + Uat(2, p));
    F[O_aT + m] += dt * F[O_T + m]; F[O_as + m] += dt * sqrt(uc * uc + vc * vc + wc * wc);
    F[O_anu + m] += dt * F[O_nuc + m]; F[O_ak + m] += dt * F[O_k + m];
  }
}
`;

  // ---- pipelines ----
  device.pushErrorScope("validation");
  const module = device.createShaderModule({ code });
  const info = await module.getCompilationInfo();
  const errs = info.messages.filter((m) => m.type === "error");
  if (errs.length) throw new Error("WGSL: " + errs.map((m) => `${m.lineNum}:${m.linePos} ${m.message}`).join("\n") + "\n");
  const bgl = device.createBindGroupLayout({ entries: [{ binding: 0, visibility: GPUShaderStage.COMPUTE, buffer: { type: "storage" } }] });
  const layout = device.createPipelineLayout({ bindGroupLayouts: [bgl] });
  const names = [...code.matchAll(/@compute[^\n]*? fn (\w+)\(/g)].map((m) => m[1]);
  const pipes = {};
  await Promise.all(names.map(async (nm) => { pipes[nm] = await device.createComputePipelineAsync({ layout, compute: { module, entryPoint: nm } }); }));
  const buf = device.createBuffer({ size: total * 4, usage: GPUBufferUsage.STORAGE | GPUBufferUsage.COPY_SRC | GPUBufferUsage.COPY_DST });
  device.queue.writeBuffer(buf, 0, init);
  const bg = device.createBindGroup({ layout: bgl, entries: [{ binding: 0, resource: { buffer: buf } }] });
  const err = await device.popErrorScope();
  if (err) throw new Error(err.message);

  // ---- encoding a time step ----
  const wg = (cnt) => Math.ceil(cnt / 64);
  const vcycle = (l, seq) => {
    if (l === nl - 1) { seq.push(["coarse", 1]); return; }
    const m = ops[l].dg.length, mc = ops[l + 1].dg.length;
    seq.push([`jac0_${l}`, wg(m)], [`jacA_${l}`, wg(m)], [`restr_${l}`, wg(mc)]);
    vcycle(l + 1, seq);
    seq.push([`jacC_${l}`, wg(m)], [`jacA_${l}`, wg(m)]);
  };
  const vc = []; vcycle(0, vc);
  const stepSeq = (K) => {
    const s = [["begin", 1], ["nuc", wg(N)], ["red1_dt", NWG], ["red2_dt", 1],
               ["edge01", wg((nx + 1) * (ny + 1) * nz)], ["edge02", wg((nx + 1) * ny * (nz + 1))], ["edge12", wg(nx * (ny + 1) * (nz + 1))],
               ["mom0", wg(Nu)], ["mom1", wg(Nv)], ["mom2", wg(Nw)], ["bc", wg(Math.max(ny * nz, nx * nz, nx * ny))], ["rhs", wg(N)],
               ["cg_init", wg(N)], ["cg_bbrr", NWG], ["cg_bbrr2", 1], ...vc, ["cg_rz0", NWG], ["cg_rz02", 1]];
    for (let it = 0; it < K; it++)
      s.push(["cg_Ad", wg(N)], ["cg_dAd", NWG], ["cg_dAd2", 1], ["cg_upd", NWG], ["cg_upd2", 1], ...vc,
             ["cg_rz", NWG], ["cg_rz2", 1], ["cg_d", wg(N)]);
    s.push(["correct", wg(Nu + Nv + Nw)], ["fluxT", wg(Nu + Nv + Nw)], ["energy", wg(N)]);
    if (ke) s.push(["prod", wg(N)], ["fluxKE", wg(Nu + Nv + Nw)], ["keps", wg(N)]);
    s.push(["copy2", wg(N)], ["tadv", 1], ["avg", wg(Nu + Nv + Nw)]);
    return s;
  };

  const staging = device.createBuffer({ size: 256, usage: GPUBufferUsage.MAP_READ | GPUBufferUsage.COPY_DST });
  async function scalars() {
    const enc = device.createCommandEncoder(); enc.copyBufferToBuffer(buf, 0, staging, 0, 256);
    device.queue.submit([enc.finish()]);
    await staging.mapAsync(GPUMapMode.READ); const a = new Float32Array(staging.getMappedRange().slice(0)); staging.unmap();
    return a;
  }
  async function readField(name, size) {
    const st = device.createBuffer({ size: size * 4, usage: GPUBufferUsage.MAP_READ | GPUBufferUsage.COPY_DST });
    const enc = device.createCommandEncoder(); enc.copyBufferToBuffer(buf, O[name] * 4, st, 0, size * 4);
    device.queue.submit([enc.finish()]);
    await st.mapAsync(GPUMapMode.READ); const a = new Float32Array(st.getMappedRange().slice(0)); st.unmap(); st.destroy();
    return a;
  }

  let K = 30;                       // CG iterations encoded per step (adapted to what the steps use)
  // run to t_end in batches of steps; the batch size adapts so one batch takes about `target` ms
  async function run(onProgress, { batch = 10, target = 150, stopFlag = () => false } = {}) {
    const t0 = performance.now();
    for (;;) {
      const tb = performance.now();
      const enc = device.createCommandEncoder();
      const pass = enc.beginComputePass(); pass.setBindGroup(0, bg);
      const seq = stepSeq(K);
      for (let b = 0; b < batch; b++) for (const [nm, cnt] of seq) { pass.setPipeline(pipes[nm]); pass.dispatchWorkgroups(cnt); }
      pass.end(); device.queue.submit([enc.finish()]);
      const sc = await scalars();
      const used = sc[S.ITS_MAX], notconv = sc[S.NOTCONV];
      K = notconv > 0 ? Math.min(K + 10, 200) : Math.max(Math.min(K, used + 3), 4);
      device.queue.writeBuffer(buf, S.ITS_MAX * 4, new Float32Array([0, 0]));   // ITS_MAX, NOTCONV
      const took = performance.now() - tb;
      batch = Math.max(1, Math.min(200, Math.round(batch * Math.min(Math.max(target / Math.max(took, 1), 0.5), 2))));
      if (onProgress) await onProgress({ t: sc[S.T], dt: sc[S.DT], steps: sc[S.STEPS], cg: sc[S.ITS] / Math.max(sc[S.STEPS], 1),
                                   K, notconv, umax: sc[S.UMAX], elapsed: (performance.now() - t0) / 1000 });
      if (sc[S.T] >= c.t_end || stopFlag()) return sc;
    }
  }

  async function results() {
    const sc = await scalars(), wa = sc[S.WA];
    const r = { case: c, nx, ny, nz, dx, dy, dz, U_in, h_in, T_mix, T0, steps: sc[S.STEPS], cg_iters: sc[S.ITS], t: sc[S.T],
                levels: ops.map((o) => o.n) };
    const sc_ = (a, s, add = 0) => { const o = new Float64Array(a.length); for (let m = 0; m < a.length; m++) o[m] = a[m] / s + add; return o; };
    r.u = sc_(await readField("au", Nu), wa); r.v = sc_(await readField("av", Nv), wa); r.w = sc_(await readField("aw", Nw), wa);
    r.T = sc_(await readField("aT", N), wa, T0); r.speed = sc_(await readField("as", N), wa);
    r.nu_t = sc_(await readField("anu", N), wa); r.k = sc_(await readField("ak", N), wa);
    return r;
  }
  async function snapshot() {         // instantaneous fields (for live plots)
    const T = await readField("T", N), u = await readField("u", Nu + Nv + Nw);
    return { T: T.map((x) => x + T0), u: u.subarray(0, Nu), v: u.subarray(Nu, Nu + Nv), w: u.subarray(Nu + Nv) };
  }
  return { run, results, snapshot, scalars, info: { N, levels: ops.map((o) => o.n), bytes: total * 4, U_in, T_mix, dispatchesPerStep: stepSeq(K).length },
           destroy: () => { buf.destroy(); staging.destroy(); } };
}
