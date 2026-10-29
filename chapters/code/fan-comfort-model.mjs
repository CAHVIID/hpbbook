// Comfort models for the ceiling fan app (fan-comfort.html).
// Ported from pythermalcomfort 4.6 so the app gives the same numbers as fan_comfort.py:
//   setCE       = set_tmp(..., calculate_ce=True, limit_inputs=False).set (two-node Gagge model, standing)
//   coolingEffect = cooling_effect(...).ce (ASHRAE 55)
//   pmvAshrae   = pmv_ppd_ashrae(...).pmv (elevated air speed method)

const MET_W = 58.15;          // W/m2 per met (pythermalcomfort met_to_w_m2)
const BODY_AREA = 1.8258;     // m2
const P_ATM = 101325;         // Pa
const V_STILL = 0.1;          // m/s

const pSatTorr = (t) => Math.exp(18.6686 - 4030.183 / (t + 235.0));

// Standard Effective Temperature from the two-node model, as used for the cooling effect
// (no activity-driven convection, standing radiation area factor 0.73).
export function setCE(tdb, tr, v, rh, met, clo, wme = 0) {
  const vp = rh * pSatTorr(tdb) / 100.0;
  const airSpeed = Math.max(v, 0.1);
  const kClo = 0.25, bodyWeight = 70, metFactor = 58.2, sbc = 0.000000056697;
  const cSw = 170, cDil = 120, cStr = 0.5;
  const tSkN = 33.7, tCrN = 36.8;
  let alfa = 0.1;
  const tBN = alfa * tSkN + (1 - alfa) * tCrN;
  const sbfN = 6.3;
  let tSk = tSkN, tCr = tCrN, mBl = sbfN;
  let eSk = 0.1 * met, qSens = 0, w = 0, eRsw = 0, eDiff = 0, eMax = 0, mRsw = 0;
  const pAtm = P_ATM / 101325;
  const rClo = 0.155 * clo, faCl = 1.0 + 0.15 * clo, lr = 2.2 / pAtm;
  const rm = (met - wme) * metFactor;
  let m = met * metFactor;
  const iCl = clo > 0 ? 0.45 : 1.0;
  const wMax = clo > 0 ? 0.59 * Math.pow(airSpeed, -0.08) : 0.38 * Math.pow(airSpeed, -0.29);
  let hCc = 3.0 * Math.pow(pAtm, 0.53);
  const hFc = 8.600001 * Math.pow(airSpeed * pAtm, 0.53);
  hCc = Math.max(hCc, hFc);
  let hR = 4.7, hT = hR + hCc, rA = 1.0 / (faCl * hT), tOp = (hR * tr + hCc * tdb) / hT;
  let tBody;
  const qRes = 0.0023 * m * (44.0 - vp);
  const cRes = 0.0014 * m * (34.0 - tdb);
  let rEa = 0, rEcl = 0;
  for (let n = 1; n < 60; n++) {
    let tCl = (rA * tSk + rClo * tOp) / (rA + rClo);
    for (let it = 0; ; it++) {
      hR = 4.0 * 0.95 * sbc * Math.pow((tCl + tr) / 2.0 + 273.15, 3.0) * 0.73;
      hT = hR + hCc;
      rA = 1.0 / (faCl * hT);
      tOp = (hR * tr + hCc * tdb) / hT;
      const tClNew = (rA * tSk + rClo * tOp) / (rA + rClo);
      const done = Math.abs(tClNew - tCl) <= 0.01;
      tCl = tClNew;
      if (done) break;
      if (it > 150) throw new Error("Max iterations exceeded");
    }
    qSens = (tSk - tOp) / (rA + rClo);
    const hfCs = (tCr - tSk) * (5.28 + 1.163 * mBl);
    const sCore = m - hfCs - qRes - cRes - wme;
    const sSkin = hfCs - qSens - eSk;
    const tcSk = 0.97 * alfa * bodyWeight, tcCr = 0.97 * (1 - alfa) * bodyWeight;
    tSk += (sSkin * BODY_AREA) / (tcSk * 60.0);
    tCr += (sCore * BODY_AREA) / (tcCr * 60.0);
    tBody = alfa * tSk + (1 - alfa) * tCr;
    const skSig = tSk - tSkN;
    const warmSk = skSig > 0 ? skSig : 0;
    const colds = -skSig > 0 ? -skSig : 0;
    const cRegSig = tCr - tCrN;
    const cWarm = cRegSig > 0 ? cRegSig : 0;
    const cCold = -cRegSig > 0 ? -cRegSig : 0;
    const bdSig = tBody - tBN;
    const warmB = bdSig > 0 ? bdSig : 0;
    mBl = (sbfN + cDil * cWarm) / (1 + cStr * colds);
    mBl = Math.max(Math.min(mBl, 90), 0.5);
    mRsw = Math.min(cSw * warmB * Math.exp(warmSk / 10.7), 500);
    eRsw = 0.68 * mRsw;
    rEa = 1.0 / (lr * faCl * hCc);
    rEcl = rClo / (lr * iCl);
    eMax = (pSatTorr(tSk) - vp) / (rEa + rEcl);
    if (eMax === 0) eMax = 0.001;
    let pRsw = eRsw / eMax;
    w = 0.06 + 0.94 * pRsw;
    eDiff = w * eMax - eRsw;
    if (w > wMax) {
      w = wMax;
      pRsw = wMax / 0.94;
      eRsw = pRsw * eMax;
      eDiff = 0.06 * (1.0 - pRsw) * eMax;
    }
    if (eMax < 0) { eDiff = 0; eRsw = 0; w = wMax; }
    eSk = eRsw + eDiff;
    m = rm + 19.4 * colds * cCold;
    alfa = 0.0417737 + 0.7451833 / (mBl + 0.585417);
  }
  const qSkin = qSens + eSk;
  const pSSk = pSatTorr(tSk);
  const hRS = hR;
  const hCS = Math.max(3.0 * Math.pow(pAtm, 0.53), 3.0);
  const hTS = hCS + hRS;
  const rCloS = 1.52 / ((met - wme / metFactor) + 0.6944) - 0.1835;
  const rClS = 0.155 * rCloS;
  const faClS = 1.0 + kClo * rCloS;
  const fClS = 1.0 / (1.0 + 0.155 * faClS * hTS * rCloS);
  const iMS = 0.45;
  const iClS = iMS * hCS / hTS * (1 - fClS) / (hCS / hTS - fClS * iMS);
  const rAS = 1.0 / (faClS * hTS);
  const rEaS = 1.0 / (lr * faClS * hCS);
  const rEclS = rClS / (lr * iClS);
  const hDS = 1.0 / (rAS + rClS);
  const hES = 1.0 / (rEaS + rEclS);
  const delta = 0.0001;
  let dx = 100.0;
  let setOld = Math.round((tSk - qSkin / hDS) * 100) / 100;
  let set = setOld;
  while (Math.abs(dx) > 0.01) {
    const e1 = qSkin - hDS * (tSk - setOld) - w * hES * (pSSk - 0.5 * pSatTorr(setOld));
    const e2 = qSkin - hDS * (tSk - (setOld + delta)) - w * hES * (pSSk - 0.5 * pSatTorr(setOld + delta));
    set = setOld - delta * e1 / (e2 - e1);
    dx = set - setOld;
    setOld = set;
  }
  return set;
}

// Brent's method root finder (as scipy.optimize.brentq, xtol 2e-12).
function brentq(f, a, b, xtol = 2e-12, rtol = 8.9e-16, maxiter = 100) {
  let fa = f(a), fb = f(b);
  if (fa * fb > 0) return null;
  if (fa === 0) return a;
  if (fb === 0) return b;
  let c = a, fc = fa, d = b - a, e = d;
  for (let i = 0; i < maxiter; i++) {
    if (fb * fc > 0) { c = a; fc = fa; d = b - a; e = d; }
    if (Math.abs(fc) < Math.abs(fb)) { a = b; b = c; c = a; fa = fb; fb = fc; fc = fa; }
    const tol = 2 * rtol * Math.abs(b) + 0.5 * xtol;
    const mid = 0.5 * (c - b);
    if (Math.abs(mid) <= tol || fb === 0) return b;
    if (Math.abs(e) >= tol && Math.abs(fa) > Math.abs(fb)) {
      let p, q, r;
      const s = fb / fa;
      if (a === c) { p = 2 * mid * s; q = 1 - s; }
      else { q = fa / fc; r = fb / fc; p = s * (2 * mid * q * (q - r) - (b - a) * (r - 1)); q = (q - 1) * (r - 1) * (s - 1); }
      if (p > 0) q = -q; else p = -p;
      if (2 * p < Math.min(3 * mid * q - Math.abs(tol * q), Math.abs(e * q))) { e = d; d = p / q; }
      else { d = mid; e = d; }
    } else { d = mid; e = d; }
    a = b; fa = fb;
    b += Math.abs(d) > tol ? d : (mid > 0 ? tol : -tol);
    fb = f(b);
  }
  return b;
}

// Cooling effect (K): the drop in air and radiant temperature that gives the same SET in still air.
export function coolingEffect(tdb, tr, vr, rh, met, clo, wme = 0) {
  if (vr <= V_STILL) return 0;
  const set0 = setCE(tdb, tr, vr, rh, met, clo, wme);
  const ce = brentq((x) => setCE(tdb - x, tr - x, V_STILL, rh, met, clo, wme) - set0, 0.0, 40);
  return ce === null ? 0 : ce;
}

// Fanger PMV (ISO 7730 / ASHRAE 55 still-air core).
export function pmvFanger(tdb, tr, vr, rh, met, clo, wme = 0) {
  const pa = rh * 10 * Math.exp(16.6536 - 4030.183 / (tdb + 235));
  const icl = 0.155 * clo, m = met * MET_W, wW = wme * MET_W, mw = m - wW;
  const fCl = icl <= 0.078 ? 1 + 1.29 * icl : 1.05 + 0.645 * icl;
  const hcf = 12.1 * Math.sqrt(vr);
  let hc = hcf;
  const taa = tdb + 273, tra = tr + 273;
  const tCla = taa + (35.5 - tdb) / (3.5 * (6.45 * icl + 0.1));
  const p1 = icl * fCl, p2 = p1 * 3.96, p3 = p1 * 100, p4 = p1 * taa;
  const p5 = (308.7 - 0.028 * mw) + p2 * Math.pow(tra / 100.0, 4);
  let xn = tCla / 100, xf = tCla / 50;
  for (let n = 0; Math.abs(xn - xf) > 0.00015; n++) {
    xf = (xf + xn) / 2;
    const hcn = 2.38 * Math.pow(Math.abs(100.0 * xf - taa), 0.25);
    hc = Math.max(hcn, hcf);
    xn = (p5 + p4 * hc - p2 * Math.pow(xf, 4)) / (100 + p3 * hc);
    if (n > 150) throw new Error("Max iterations exceeded");
  }
  const tcl = 100 * xn - 273;
  const hl1 = 3.05 * 0.001 * (5733 - 6.99 * mw - pa);
  const hl2 = mw > MET_W ? 0.42 * (mw - MET_W) : 0;
  const hl3 = 1.7 * 0.00001 * m * (5867 - pa);
  const hl4 = 0.0014 * m * (34 - tdb);
  const hl5 = 3.96 * fCl * (Math.pow(xn, 4) - Math.pow(tra / 100.0, 4));
  const hl6 = fCl * hc * (tcl - tdb);
  return (0.303 * Math.exp(-0.036 * m) + 0.028) * (mw - hl1 - hl2 - hl3 - hl4 - hl5 - hl6);
}

// PMV by the ASHRAE 55 elevated air speed method. Returns {pmv, ce}.
export function pmvAshrae(tdb, tr, vr, rh, met, clo, wme = 0) {
  const ce = vr > V_STILL ? Math.round(coolingEffect(tdb, tr, vr, rh, met, clo, wme) * 100) / 100 : 0;
  const v = ce > 0 ? V_STILL : vr;
  return { pmv: pmvFanger(tdb - ce, tr - ce, v, rh, met, clo, wme), ce };
}

// Fan air speed S_F and room-average speed for seated occupants S_O,avg (Raftery et al. 2019).
export function airSpeed(qM3h, D, R, C) {
  const sF = 4 * qM3h / 3600 / (Math.PI * D * D);
  return { sF, sO: sF * (0.25 + 0.99 * D / R - 0.06 * C / D + 0.11 * D / 1.7 + 0.024) };
}
