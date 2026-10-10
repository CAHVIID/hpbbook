// Interactive exhaust-air heat pump charging a hot water tank (anywidget module for MyST).
// Same model as heatpump_model.py, which is the documented reference version.

export const DEFAULTS = {
  T_out: 7, T_supply: 55, T_return: 15,
  T_room: 20, eta_hx: 0.85, dt_evap: 5, dt_cond: 5, eta_lorenz: 0.32,
};

// PHI certificate, DHW tank heating, Compact P @ 92 m3/h
const T_OUT_PTS = [-6.9, 1.9, 7.2, 20.2];   // outdoor, C
const P_DHW_PTS = [0.51, 0.72, 0.89, 1.02];  // heat output, kW

export function capacity(tOut) {
  // linear interpolation, held constant beyond the test range (as numpy.interp)
  const x = T_OUT_PTS, y = P_DHW_PTS;
  if (tOut <= x[0]) return y[0];
  if (tOut >= x[x.length - 1]) return y[y.length - 1];
  let i = 0; while (tOut > x[i + 1]) i++;
  return y[i] + (y[i + 1] - y[i]) * (tOut - x[i]) / (x[i + 1] - x[i]);
}

export function exhaustTemp(tOut, p) { return p.T_room - p.eta_hx * (p.T_room - tOut); }
export function evaporatorTemp(tOut, p) { return exhaustTemp(tOut, p) - p.dt_evap; }

function logMean(tHi, tLo) {
  const a = tHi + 273.15, b = tLo + 273.15;
  return Math.abs(a - b) < 1e-6 ? a : (a - b) / Math.log(a / b);
}

export function cop(tOut, tSupply, tReturn, p) {
  const tHot = logMean(tSupply, tReturn) + p.dt_cond;
  const tCold = evaporatorTemp(tOut, p) + 273.15;
  return p.eta_lorenz * tHot / (tHot - tCold);
}

export function hour(tOut, tSupply, tReturn, p) {
  const q = capacity(tOut), c = cop(tOut, tSupply, tReturn, p);
  return { q, el: q / c, cop: c };
}

// ---------------------------------------------------------------- user interface

const INPUTS = [
  ["Operating point", [
    ["T_out", "Outdoor temperature", "°C", -15, 25, 1, "Outdoor air temperature. It sets the temperature of the exhaust air after the ventilation heat exchanger, and through it the evaporating temperature, the COP and the heat output."],
    ["T_supply", "Supply temperature", "°C", 35, 65, 1, "Water leaving the condenser to the tank. A higher supply temperature raises the condensing temperature and lowers the COP. About 55 °C is typical for hot water."],
    ["T_return", "Return temperature", "°C", 5, 60, 1, "Water entering the condenser from the bottom of the tank: cold at the start of a charge, close to the supply temperature at the end. The COP uses the log-mean of supply and return, so a cold, well-stratified tank bottom gives a higher COP. Cannot exceed the supply temperature."]]],
  ["Model parameters", [
    ["T_room", "Extract air temperature", "°C", 18, 24, 0.5, "Temperature of the room air extracted from kitchen and bathrooms. It is the warm side of the ventilation heat exchanger."],
    ["eta_hx", "Heat exchanger efficiency", "–", 0.6, 0.95, 0.01, "Temperature efficiency of the counterflow ventilation heat exchanger, (T_room − T_exhaust) / (T_room − T_out). A better heat exchanger leaves colder exhaust air for the heat pump and so lowers its COP."],
    ["dt_evap", "Evaporator approach", "K", 2, 10, 0.5, "Temperature difference between the exhaust air and the evaporating refrigerant. A larger evaporator gives a smaller approach and a higher COP."],
    ["dt_cond", "Condenser approach", "K", 2, 10, 0.5, "Temperature difference between the condensing refrigerant and the mean water temperature in the condenser. A larger condenser gives a smaller approach and a higher COP."],
    ["eta_lorenz", "Fraction of Lorenz COP", "–", 0.2, 0.6, 0.01, "Real COP as a fraction of the ideal Lorenz COP. It covers compressor, fan and other losses. 0.32 is tuned so the COP is 2.8 at 7 °C outdoors, as in the PHI certificate."]]],
];

const OUTPUT_HELP = {
  q: "Heat delivered to the tank. Interpolated between the PHI certificate test points (DHW tank heating, 92 m³/h) and held constant outside −6.9 to 20.2 °C. It depends only on the outdoor temperature.",
  el: "Electric power of the heat pump: heat output divided by COP.",
  cop: "Coefficient of performance, the heat delivered per unit of electricity. COP = η_L · T_hot / (T_hot − T_cold), with T_hot the log-mean of supply and return plus the condenser approach, and T_cold the evaporating temperature, both in kelvin.",
  tex: "Exhaust air after the ventilation heat exchanger, T_room − η_hx · (T_room − T_out). This is the heat source of the heat pump.",
  tev: "Evaporating temperature of the refrigerant: the exhaust air temperature minus the evaporator approach.",
};

const CSS = `
.hp { --ink: #1f2328; --muted: #5f6770; --grid: #e3e6e8; --panel: #f6f8fa; --c1: #2b7bb9; --c2: #d0663a; --c3: #5aa02c;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 14px; color: var(--ink); }
@media (prefers-color-scheme: dark) { :root:not([data-theme=light]) .hp { --ink: #e6edf3; --muted: #9aa4ae; --grid: #30363d; --panel: #161b22; } }
:root[data-theme=dark] .hp { --ink: #e6edf3; --muted: #9aa4ae; --grid: #30363d; --panel: #161b22; }
.hp .controls { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin-bottom: 12px; }
.hp fieldset { min-width: 0; border: 1px solid var(--grid); border-radius: 8px; padding: 8px 12px 10px; margin: 0; background: var(--panel); }
.hp legend { font-weight: 600; padding: 0 4px; }
.hp label { display: grid; grid-template-columns: 1fr auto; gap: 2px 8px; margin-top: 6px; font-size: 13px; }
.hp .tip { display: inline-block; margin-left: 4px; color: var(--muted); font-size: 12px; cursor: help; border-radius: 50%; }
.hp .tip:hover, .hp .tip:focus-visible { color: var(--c1); outline: none; }
.hp .tipbox { position: fixed; z-index: 1000; max-width: 280px; padding: 7px 10px; border-radius: 6px; font-size: 12px; line-height: 1.45;
  background: var(--ink); color: var(--panel); box-shadow: 0 2px 8px rgba(0,0,0,.25); pointer-events: none; }
.hp label input { grid-column: 1 / 3; width: 100%; accent-color: var(--c1); }
.hp .val { font-variant-numeric: tabular-nums; color: var(--muted); }
.hp .reset { font: inherit; font-size: 12px; margin-top: 8px; padding: 2px 10px; border-radius: 6px; border: 1px solid var(--grid); background: transparent; color: var(--ink); cursor: pointer; }
.hp .tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 8px; margin-bottom: 12px; }
.hp .tile { border: 1px solid var(--grid); border-radius: 8px; padding: 8px 10px; }
.hp .tile b { display: block; font-size: 20px; font-variant-numeric: tabular-nums; }
.hp .tile span { color: var(--muted); font-size: 12px; }
.hp .charts { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; }
.hp svg { width: 100%; height: auto; display: block; }
.hp svg text { fill: var(--ink); font-size: 11px; }
.hp svg .mut { fill: var(--muted); }
.hp .note { color: var(--muted); font-size: 12px; margin-top: 8px; }
`;

const esc = t => String(t).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
const tip = text => `<span class="tip" tabindex="0" data-tip="${esc(text)}" aria-label="${esc(text)}">ⓘ</span>`;

function ticks(lo, hi, n = 5) {
  const raw = (hi - lo) / n, mag = 10 ** Math.floor(Math.log10(raw));
  const step = [1, 2, 2.5, 5, 10].map(f => f * mag).find(s => s >= raw);
  const out = []; for (let v = Math.ceil(lo / step) * step; v <= hi + 1e-9; v += step) out.push(+v.toFixed(6));
  return out;
}

function chart({ title, xlabel, ylabel, xmin, xmax, ymin, ymax, series, marker, ylabel2, y2max, series2 }) {
  const W = 460, H = 280, L = 44, R = series2 ? 56 : 14, T = 26, B = 36;
  const X = v => L + (v - xmin) / (xmax - xmin) * (W - L - R);
  const Y = v => T + (ymax - v) / (ymax - ymin) * (H - T - B);
  const Y2 = v => T + (y2max - v) / y2max * (H - T - B);
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${title}"><text x="${L}" y="14" font-weight="600" style="font-size:12px">${title}</text>`;
  for (const v of ticks(xmin, xmax)) s += `<line x1="${X(v)}" x2="${X(v)}" y1="${T}" y2="${H - B}" stroke="var(--grid)"/><text x="${X(v)}" y="${H - B + 14}" text-anchor="middle" class="mut">${v}</text>`;
  for (const v of ticks(ymin, ymax)) s += `<line x1="${L}" x2="${W - R}" y1="${Y(v)}" y2="${Y(v)}" stroke="var(--grid)"/><text x="${L - 6}" y="${Y(v) + 4}" text-anchor="end" class="mut">${v}</text>`;
  if (series2) for (const v of ticks(0, y2max)) s += `<text x="${W - R + 6}" y="${Y2(v) + 4}" class="mut">${v}</text>`;
  s += `<text x="${(L + W - R) / 2}" y="${H - 4}" text-anchor="middle" class="mut">${xlabel}</text>`;
  s += `<text transform="translate(11 ${(T + H - B) / 2}) rotate(-90)" text-anchor="middle" class="mut">${ylabel}</text>`;
  if (series2) s += `<text transform="translate(${W - 6} ${(T + H - B) / 2}) rotate(90)" text-anchor="middle" class="mut">${ylabel2}</text>`;
  const path = (pts, y) => pts.map(([x, v], i) => `${i ? "L" : "M"}${X(x).toFixed(1)} ${y(v).toFixed(1)}`).join("");
  let lx = L + 8;
  for (const sr of series) {
    s += `<path d="${path(sr.pts, Y)}" fill="none" stroke="${sr.color}" stroke-width="2" ${sr.dash ? `stroke-dasharray="${sr.dash}"` : ""}/>`;
  }
  for (const sr of series2 || []) s += `<path d="${path(sr.pts, Y2)}" fill="none" stroke="${sr.color}" stroke-width="2" ${sr.dash ? `stroke-dasharray="${sr.dash}"` : ""}/>`;
  for (const sr of [...series, ...(series2 || [])]) {
    s += `<line x1="${lx}" x2="${lx + 16}" y1="${T + 8}" y2="${T + 8}" stroke="${sr.color}" stroke-width="2" ${sr.dash ? `stroke-dasharray="${sr.dash}"` : ""}/><text x="${lx + 20}" y="${T + 12}">${sr.label}</text>`;
    lx += 26 + sr.label.length * 6;
  }
  if (marker) s += `<circle cx="${X(marker[0])}" cy="${Y(marker[1])}" r="4.5" fill="var(--ink)"/>`;
  return s + "</svg>";
}

export function render({ model, el }) {
  const p = { ...DEFAULTS };
  for (const key of Object.keys(DEFAULTS)) { const v = model.get(key); if (typeof v === "number") p[key] = v; }
  const root = document.createElement("div"); root.className = "hp";
  const style = document.createElement("style"); style.textContent = CSS;
  el.append(style, root);

  // one floating tooltip for all ⓘ icons; shown on hover and keyboard focus, kept inside the window
  const box = document.createElement("div"); box.className = "tipbox"; box.hidden = true; box.setAttribute("role", "tooltip");
  root.appendChild(box);
  const showTip = t => {
    box.textContent = t.dataset.tip; box.hidden = false;
    const r = t.getBoundingClientRect(), w = box.offsetWidth, h = box.offsetHeight;
    const x = Math.max(8, Math.min(r.left + r.width / 2 - w / 2, window.innerWidth - w - 8));
    const y = r.bottom + 6 + h > window.innerHeight ? r.top - h - 6 : r.bottom + 6;
    box.style.left = `${x}px`; box.style.top = `${y}px`;
  };
  const hideTip = () => { box.hidden = true; };
  root.addEventListener("mouseover", e => { const t = e.target.closest(".tip"); if (t) showTip(t); });
  root.addEventListener("mouseout", e => { if (e.target.closest(".tip")) hideTip(); });
  root.addEventListener("focusin", e => { const t = e.target.closest(".tip"); if (t) showTip(t); });
  root.addEventListener("focusout", hideTip);

  const controls = document.createElement("div"); controls.className = "controls";
  const tiles = document.createElement("div"); tiles.className = "tiles";
  const charts = document.createElement("div"); charts.className = "charts";
  const note = document.createElement("p"); note.className = "note";
  note.textContent = "Heat output from the PHI certificate test points (DHW tank heating, 92 m³/h), held constant outside −6.9 to 20.2 °C. COP from a Lorenz model: the water is heated over a glide from return to supply, the evaporator works at the exhaust air temperature minus the approach.";
  root.append(controls, tiles, charts, note);

  const sliders = [];
  for (const [group, items] of INPUTS) {
    const fs = document.createElement("fieldset"); fs.innerHTML = `<legend>${group}</legend>`;
    for (const [key, label, unit, min, max, step, help] of items) {
      const lab = document.createElement("label");
      lab.innerHTML = `<span>${label}${tip(help)}</span><span class="val"></span><input type="range" min="${min}" max="${max}" step="${step}" aria-label="${label}">`;
      const input = lab.querySelector("input"), val = lab.querySelector(".val");
      const show = () => { input.value = p[key]; val.textContent = `${(+p[key]).toLocaleString("en", { maximumFractionDigits: 2 })} ${unit}`; };
      input.addEventListener("input", () => {
        p[key] = +input.value;
        if (p.T_return > p.T_supply) { p.T_return = p.T_supply; sliders.forEach(f => f()); }   // return cannot exceed supply
        show(); update();
      });
      show(); sliders.push(show); fs.appendChild(lab);
    }
    if (group === "Model parameters") {
      const b = document.createElement("button"); b.type = "button"; b.className = "reset"; b.textContent = "Reset all";
      b.addEventListener("click", () => { Object.assign(p, DEFAULTS); sliders.forEach(f => f()); update(); });
      fs.appendChild(b);
    }
    controls.appendChild(fs);
  }

  function update() {
    if (!box.hidden && !box.isConnected) box.hidden = true;
    const r = hour(p.T_out, p.T_supply, p.T_return, p);
    const tile = (v, u, label, help) => `<div class="tile"><b>${v} ${u}</b><span>${label}${tip(help)}</span></div>`;
    tiles.innerHTML = tile(r.q.toFixed(2), "kW", "heat output", OUTPUT_HELP.q) + tile(r.el.toFixed(2), "kW", "electricity", OUTPUT_HELP.el)
      + tile(r.cop.toFixed(2), "", "COP", OUTPUT_HELP.cop) + tile(exhaustTemp(p.T_out, p).toFixed(1), "°C", "exhaust air to evaporator", OUTPUT_HELP.tex)
      + tile(evaporatorTemp(p.T_out, p).toFixed(1), "°C", "evaporating temperature", OUTPUT_HELP.tev);

    const tOuts = []; for (let t = -15; t <= 25; t += 0.5) tOuts.push(t);
    const copPts = tr => tOuts.map(t => [t, cop(t, p.T_supply, tr, p)]);
    const c1 = chart({
      title: `COP and heat output vs outdoor temperature, supply ${p.T_supply} °C`, xlabel: "Outdoor temperature [°C]", ylabel: "COP [–]",
      xmin: -15, xmax: 25, ymin: 0, ymax: 6,
      series: [{ label: `COP, return ${p.T_return} °C`, color: "var(--c1)", pts: copPts(p.T_return) },
               { label: "return 50 °C", color: "var(--c1)", dash: "4 3", pts: copPts(Math.min(50, p.T_supply)) }],
      ylabel2: "Heat output [kW]", y2max: 1.5,
      series2: [{ label: "heat output", color: "var(--c2)", pts: tOuts.map(t => [t, capacity(t)]) }],
      marker: [p.T_out, r.cop],
    });
    const trs = []; for (let t = 5; t <= p.T_supply; t += 0.5) trs.push(t);
    const trs65 = []; for (let t = 5; t <= 65; t += 0.5) trs65.push(t);
    const c2 = chart({
      title: `COP vs return temperature, outdoor ${p.T_out} °C`, xlabel: "Return temperature [°C]", ylabel: "COP [–]",
      xmin: 5, xmax: 65, ymin: 0, ymax: 6,
      series: [{ label: `supply ${p.T_supply} °C`, color: "var(--c1)", pts: trs.map(t => [t, cop(p.T_out, p.T_supply, t, p)]) },
               { label: "supply 65 °C", color: "var(--c3)", dash: "4 3", pts: trs65.map(t => [t, cop(p.T_out, 65, t, p)]) }],
      marker: [p.T_return, r.cop],
    });
    charts.innerHTML = c1 + c2;
  }
  update();
}

export default { render };
