// Interactive room cool-down model (anywidget module for MyST).
// Same model as room_cooldown.py: one heat store C [J/K] losing heat through UA [W/K].
//   C dT/dt = UA (T_out - T) + Phi   ->   T(t) = T_inf + (T0 - T_inf) exp(-t / tau),  tau = C / UA

export const DEFAULTS = { UA: 25, tau: 10, T0: 21, T_out: 0, gains: 0, hours: 48 };

// Reference rooms of 20 m2 floor (UA and C per m2 of floor times 20), as in room_cooldown.py
const CASES = [
  ["Older house, heavy", 2.5 * 20, 150 * 20e3, "#8a8f94"],
  ["Low-energy house, light", 0.6 * 20, 40 * 20e3, "#d0663a"],
  ["Low-energy house, heavy", 0.6 * 20, 150 * 20e3, "#7b5ea7"],
];

const INPUTS = [
  ["UA", "Heat loss coefficient UA", "W/K", 2, 100, 1, "Transmission and ventilation heat loss of the room per kelvin. A 20 m² room in a low-energy house: about 12 W/K. In an older house: about 50 W/K."],
  ["tau", "Time constant τ", "h", 1, 100, 0.5, "τ = C/UA. The heat capacity C follows from τ and UA and is shown below the sliders."],
  ["T0", "Room temperature when heating stops", "°C", 15, 25, 0.5, "Starting temperature at t = 0."],
  ["T_out", "Outdoor temperature", "°C", -15, 15, 0.5, "Constant outdoor temperature."],
  ["gains", "Internal and solar gains", "W", 0, 600, 10, "Constant heat gain to the room. It sets the temperature the room settles at: T_out + gains/UA."],
  ["hours", "Simulated time", "h", 12, 120, 6, "Length of the time axis."],
];

const CSS = `
:host, .rc { --ink: #1f2328; --muted: #5f6770; --grid: #e3e6e8; --panel: #f6f8fa; --bg: #ffffff; }
@media (prefers-color-scheme: dark) { :host, .rc { --ink: #e6edf3; --muted: #9aa4ae; --grid: #30363d; --panel: #161b22; --bg: #0d1117; } }
.rc { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 14px; color: var(--ink); }
.rc .controls { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 4px 16px; border: 1px solid var(--grid); border-radius: 8px; padding: 8px 12px 10px; background: var(--panel); margin-bottom: 8px; }
.rc label { display: grid; grid-template-columns: 1fr auto; gap: 2px 8px; margin-top: 6px; font-size: 13px; }
.rc label input { grid-column: 1 / 3; width: 100%; accent-color: #2b7bb9; }
.rc .help { color: var(--muted); cursor: help; font-size: 12px; }
.rc .val { font-variant-numeric: tabular-nums; color: var(--muted); }
.rc .bar { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; margin: 4px 0 8px; color: var(--muted); font-size: 13px; }
.rc button { font: inherit; padding: 4px 12px; border-radius: 6px; border: 1px solid var(--grid); background: var(--panel); color: var(--ink); cursor: pointer; }
.rc svg { width: 100%; height: auto; display: block; }
.rc svg text { fill: var(--ink); font-size: 11px; }
.rc svg text.halo { paint-order: stroke; stroke: var(--bg); stroke-width: 4px; stroke-linejoin: round; }
.rc table { border-collapse: collapse; width: 100%; font-size: 13px; font-variant-numeric: tabular-nums; }
.rc th, .rc td { padding: 4px 8px; border-bottom: 1px solid var(--grid); text-align: right; }
.rc th:first-child, .rc td:first-child { text-align: left; }
.rc .tablewrap { overflow-x: auto; margin-top: 8px; }
.rc .chk { display: inline-flex; gap: 6px; align-items: center; white-space: nowrap; }
.rc .swatch { display: inline-block; width: 18px; height: 3px; vertical-align: middle; margin-right: 6px; }
`;

export function temperature(UA, C, t_h, p) {
  const tau = C / UA, Tinf = p.T_out + p.gains / UA;
  return Tinf + (p.T0 - Tinf) * Math.exp(-t_h * 3600 / tau);
}

function hoursTo(UA, C, target, p) {
  // time until the room reaches `target`, or null if it never does
  const Tinf = p.T_out + p.gains / UA, tau = C / UA;
  const r = (target - Tinf) / (p.T0 - Tinf);
  return r > 0 && r < 1 ? -Math.log(r) * tau / 3600 : null;
}

function axis(lo, hi) {
  if (hi - lo < 1e-6) { lo -= 0.5; hi += 0.5; }
  const raw = (hi - lo) / 5, mag = 10 ** Math.floor(Math.log10(raw));
  const step = [1, 2, 2.5, 5, 10].map(f => f * mag).find(st => st >= raw);
  const ymin = Math.floor(lo / step) * step, ymax = Math.ceil(hi / step) * step;
  const ticks = []; for (let v = ymin; v <= ymax + step / 2; v += step) ticks.push(+v.toFixed(6));
  return { ymin, ymax, ticks };
}

function chart(series, p, mark) {
  const W = 900, H = 340, L = 46, R = 12, Tm = 14, B = 34;
  const all = series.flatMap(s => s.y).concat([p.T_out, p.T0]);
  const ax = axis(Math.min(...all), Math.max(...all));
  const X = t => L + t / p.hours * (W - L - R), Y = v => Tm + (ax.ymax - v) / (ax.ymax - ax.ymin) * (H - Tm - B);
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Room temperature after the heating stops">`;
  for (const v of ax.ticks) s += `<line x1="${L}" x2="${W - R}" y1="${Y(v)}" y2="${Y(v)}" stroke="var(--grid)"/><text x="${L - 6}" y="${Y(v) + 4}" text-anchor="end">${v}</text>`;
  const xs = p.hours <= 48 ? 6 : 12;
  for (let t = 0; t <= p.hours + 1e-9; t += xs) s += `<line x1="${X(t)}" x2="${X(t)}" y1="${Tm}" y2="${H - B}" stroke="var(--grid)"/><text x="${X(t)}" y="${H - B + 14}" text-anchor="middle">${t}</text>`;
  s += `<line x1="${L}" x2="${W - R}" y1="${Y(p.T_out)}" y2="${Y(p.T_out)}" stroke="var(--muted)" stroke-dasharray="4 4"/>`;
  s += `<text x="${W - R - 4}" y="${Y(p.T_out) - 4}" text-anchor="end" fill="var(--muted)">outdoor</text>`;
  for (const sr of series) {
    let d = "";
    sr.t.forEach((t, i) => { d += `${i ? "L" : "M"}${X(t).toFixed(1)} ${Y(sr.y[i]).toFixed(1)}`; });
    s += `<path d="${d}" fill="none" stroke="${sr.color}" stroke-width="${sr.width}" ${sr.dash ? `stroke-dasharray="${sr.dash}"` : ""}/>`;
  }
  if (mark.t <= p.hours) {
    s += `<line x1="${X(mark.t)}" x2="${X(mark.t)}" y1="${Y(mark.T)}" y2="${H - B}" stroke="#2b7bb9" stroke-dasharray="2 3"/>`;
    s += `<circle cx="${X(mark.t)}" cy="${Y(mark.T)}" r="5" fill="#2b7bb9" stroke="#fff" stroke-width="2"/>`;
    s += `<text class="halo" x="${X(mark.t) + 8}" y="${Y(mark.T) - 8}">t = τ: 63 % of the drop</text>`;
  }
  s += `<text x="${(L + W - R) / 2}" y="${H - 4}" text-anchor="middle">Time after the heating stops [h]</text>`;
  s += `<text transform="translate(11 ${(Tm + H - B) / 2}) rotate(-90)" text-anchor="middle">Room temperature [°C]</text>`;
  return s + "</svg>";
}

function render({ model, el }) {
  const p = { ...DEFAULTS };
  for (const key of Object.keys(DEFAULTS)) { const v = model.get(key); if (typeof v === "number") p[key] = v; }
  const root = document.createElement("div"); root.className = "rc";
  const style = document.createElement("style"); style.textContent = CSS;
  el.appendChild(style); el.appendChild(root);

  const controls = document.createElement("div"); controls.className = "controls";
  const sliders = {};
  for (const [key, label, unit, min, max, step, help] of INPUTS) {
    const lab = document.createElement("label");
    lab.title = help;
    lab.innerHTML = `<span>${label} <span class="help" aria-label="${help}">ⓘ</span></span><span class="val"></span><input type="range" min="${min}" max="${max}" step="${step}" value="${p[key]}">`;
    const input = lab.querySelector("input"), val = lab.querySelector(".val");
    const show = () => { val.textContent = `${(+input.value).toLocaleString("en", { maximumFractionDigits: 1 })} ${unit}`; };
    input.addEventListener("input", () => { p[key] = +input.value; show(); draw(); });
    show(); sliders[key] = { input, show };
    controls.appendChild(lab);
  }
  root.appendChild(controls);

  const bar = document.createElement("div"); bar.className = "bar";
  bar.innerHTML = `<span class="derived"></span><span class="chk"><input type="checkbox" checked id="rc-ref"><span>show reference rooms</span></span><button type="button">Reset</button>`;
  root.appendChild(bar);
  const derived = bar.querySelector(".derived"), refBox = bar.querySelector("input");
  refBox.addEventListener("change", draw);
  bar.querySelector("button").addEventListener("click", () => {
    Object.assign(p, DEFAULTS);
    for (const [key, s] of Object.entries(sliders)) { s.input.value = p[key]; s.show(); }
    draw();
  });
  const plot = document.createElement("div"); root.appendChild(plot);
  const tableWrap = document.createElement("div"); tableWrap.className = "tablewrap"; root.appendChild(tableWrap);

  function curve(UA, C) {
    const n = 240, t = [], y = [];
    for (let i = 0; i <= n; i++) { const th = p.hours * i / n; t.push(th); y.push(temperature(UA, C, th, p)); }
    return { t, y };
  }

  function draw() {
    const C = p.tau * 3600 * p.UA;
    derived.textContent = `Heat capacity C = τ·UA = ${(C / 1e3).toLocaleString("en", { maximumFractionDigits: 0 })} kJ/K`;
    const rows = [["Your room", p.UA, C, "#2b7bb9"]];
    const series = [];
    if (refBox.checked) for (const [name, UA, Cr, color] of CASES) {
      series.push({ ...curve(UA, Cr), color, width: 1.4, dash: "6 4" }); rows.push([name, UA, Cr, color]);
    }
    series.push({ ...curve(p.UA, C), color: "#2b7bb9", width: 2.6 });
    plot.innerHTML = chart(series, p, { t: p.tau, T: temperature(p.UA, C, p.tau, p) });

    const f = v => v === null ? "never" : v.toFixed(1);
    let h = `<table><thead><tr><th>Room</th><th>UA [W/K]</th><th>C [kJ/K]</th><th>τ [h]</th><th>Settles at [°C]</th><th>After 8 h [°C]</th><th>After 24 h [°C]</th><th>Hours to 18 °C</th></tr></thead><tbody>`;
    for (const [name, UA, Cr, color] of rows) {
      h += `<tr><td><span class="swatch" style="background:${color}"></span>${name}</td><td>${UA.toFixed(0)}</td><td>${(Cr / 1e3).toFixed(0)}</td><td>${(Cr / UA / 3600).toFixed(1)}</td>`
        + `<td>${(p.T_out + p.gains / UA).toFixed(1)}</td><td>${temperature(UA, Cr, 8, p).toFixed(1)}</td><td>${temperature(UA, Cr, 24, p).toFixed(1)}</td><td>${f(hoursTo(UA, Cr, 18, p))}</td></tr>`;
    }
    tableWrap.innerHTML = h + "</tbody></table>";
  }
  draw();
}

export default { render };
