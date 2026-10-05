// Interactive floor heating control model (anywidget module for MyST).
// Same model as floor_control.py, which is the documented reference version.

export const DEFAULTS = {
  T_set: 21, T_vent: 24, H_loss: 0.6, C_room: 40e3, Q_int: 3,
  solar_cloudy: 8, solar_sunny: 40, curve_slope: 0.6, T_supply_max: 35, flow_design: 6,
  hyst: 0.25, p_band: 2, Ti_min: 90, pwm_min: 15,
  dead_open_min: 3, stroke_open_min: 4, dead_close_min: 2, stroke_close_min: 5,
  warmup_days: 4,
};

export const FLOORS = {
  "Light floor": { R_pipe: 0.10, layers: [
    ["pine boards", 0.022, 0.13, 500, 1600], "PIPE", ["EPS", 0.030, 0.035, 20, 1450],
    ["plywood", 0.018, 0.13, 500, 1600], ["mineral wool", 0.250, 0.037, 30, 850]] },
  "Heavy floor": { R_pipe: 0.03, layers: [
    ["oak parquet", 0.014, 0.18, 700, 1700], ["concrete", 0.050, 1.7, 2300, 900], "PIPE",
    ["concrete", 0.050, 1.7, 2300, 900], ["EPS", 0.300, 0.037, 20, 1450]] },
};
const H_SURF = 10.8, DT = 60, DX = 0.002, CP_WATER = 4186;

function discretize(floor) {
  const k = [], C = [], dz = []; let pipe = null;
  for (const L of floor.layers) {
    if (L === "PIPE") { pipe = k.length; continue; }
    const [, d, lam, rho, c] = L; const n = Math.max(2, Math.round(d / DX));
    for (let i = 0; i < n; i++) { k.push(lam); C.push(rho * c * d / n); dz.push(d / n); }
  }
  return { k, C, dz, pipe };
}

function climate(th, p) {
  const day = Math.floor(th / 24), h = th % 24;
  const tOut = 7 - 5 * Math.cos(2 * Math.PI * (h - 3) / 24);
  const peak = day === p.warmup_days + 1 ? p.solar_sunny : p.solar_cloudy;
  return [tOut, peak * Math.max(0, Math.sin(Math.PI * (h - 7) / 12))];
}

function thomas(a, b, c, d, x, cp, dp) {
  const n = b.length;
  cp[0] = c[0] / b[0]; dp[0] = d[0] / b[0];
  for (let i = 1; i < n; i++) {
    const m = b[i] - a[i] * cp[i - 1];
    cp[i] = i < n - 1 ? c[i] / m : 0;
    dp[i] = (d[i] - a[i] * dp[i - 1]) / m;
  }
  x[n - 1] = dp[n - 1];
  for (let i = n - 2; i >= 0; i--) x[i] = dp[i] - cp[i] * x[i + 1];
}

export function simulate(floor, mode, p = DEFAULTS) {
  const { k, C, dz, pipe } = discretize(floor);
  const n = k.length + 1;
  const Gtop = 1 / (1 / H_SURF + dz[0] / (2 * k[0]));
  const Cv = [p.C_room, ...C];
  const b0 = new Float64Array(n), a = new Float64Array(n), c = new Float64Array(n);
  b0[0] = Cv[0] / DT + Gtop + p.H_loss; c[0] = -Gtop; b0[1] += Gtop; a[1] = -Gtop;
  for (let i = 0; i < k.length - 1; i++) {
    const g = 1 / (dz[i] / (2 * k[i]) + dz[i + 1] / (2 * k[i + 1])), j = i + 1;
    b0[j] += g; b0[j + 1] += g; c[j] = -g; a[j + 1] = -g;
  }
  for (let j = 1; j < n; j++) b0[j] += Cv[j] / DT;
  const pipeNodes = [pipe, pipe + 1];
  let T = new Float64Array(n).fill(p.T_set);
  const b = new Float64Array(n), d = new Float64Array(n), x = new Float64Array(n),
        cp = new Float64Array(n), dp = new Float64Array(n);
  let pos = 0, cmd = false, timer = 0, integ = 0.4, duty = 0, gp = 0, tSup = 0, mcp = 0;
  const cycleSteps = Math.max(1, Math.round(p.pwm_min * 60 / DT));
  const Kp = 1 / p.p_band, Ti = p.Ti_min * 60;
  const steps = Math.floor((p.warmup_days + 2) * 24 * 3600 / DT), tShow = p.warmup_days * 24;
  const out = { t: [], room: [], q_floor: [], heat: [], vent: [], solar: [], t_out: [], t_sup: [], surface: [], t_ret: [], flow: [] };
  for (let s = 0; s < steps; s++) {
    const th = s * DT / 3600;
    const [tOut, sol] = climate(th, p);
    b.set(b0);
    for (let j = 0; j < n; j++) d[j] = Cv[j] / DT * T[j];
    d[0] += p.H_loss * tOut + p.Q_int + sol;
    let heat = 0;
    mcp = 0;
    tSup = Math.min(p.T_supply_max, 20 + p.curve_slope * (20 - tOut));
    if (mode === "ideal") {
      heat = Math.max(0, p.H_loss * (p.T_set - tOut) - p.Q_int - sol + p.C_room * (p.T_set - T[0]) / 600);
      d[0] += heat;
    } else {
      let nw = cmd;
      if (mode === "onoff") {
        if (T[0] < p.T_set - p.hyst) nw = true; else if (T[0] > p.T_set + p.hyst) nw = false;
      } else {
        if (s % cycleSteps === 0) {
          const e = p.T_set - T[0], u = Kp * e + integ;
          if ((u > 0 && u < 1) || (u >= 1 && e < 0) || (u <= 0 && e > 0))
            integ = Math.min(1, Math.max(0, integ + Kp / Ti * e * cycleSteps * DT));
          duty = Math.min(1, Math.max(0, Kp * e + integ));
        }
        nw = (s % cycleSteps) < duty * cycleSteps;
      }
      if (nw !== cmd) { cmd = nw; timer = 0; }
      timer += DT;
      if (cmd && timer > p.dead_open_min * 60) pos = Math.min(1, pos + DT / (p.stroke_open_min * 60));
      if (!cmd && timer > p.dead_close_min * 60) pos = Math.max(0, pos - DT / (p.stroke_close_min * 60));
      if (pos < 1e-9) pos = 0;   // avoid a tiny floating-point flow when closed
      // loop mass flow follows the valve position; heat transfer from water to the pipe plane
      // with an effectiveness (NTU) model: UA = 1/R_pipe per m2 floor
      mcp = pos * p.flow_design / 3600 * CP_WATER;
      gp = mcp > 0 ? mcp * (1 - Math.exp(-1 / floor.R_pipe / mcp)) / 2 : 0;
      for (const j of pipeNodes) { b[j] += gp; d[j] += gp * tSup; }
    }
    thomas(a, b, c, d, x, cp, dp);
    T.set(x);
    if (mode !== "ideal") heat = pipeNodes.reduce((acc, j) => acc + gp * (tSup - T[j]), 0);
    let vent = 0;
    if (T[0] > p.T_vent) { vent = (T[0] - p.T_vent) * p.C_room / DT; T[0] = p.T_vent; }
    if (th >= tShow) {
      out.t.push(th - tShow); out.room.push(T[0]);
      out.q_floor.push(mode !== "ideal" ? Gtop * (T[1] - T[0]) : heat);
      out.heat.push(heat); out.vent.push(vent); out.solar.push(sol);
      out.t_out.push(tOut); out.t_sup.push(tSup);
      out.surface.push(T[0] + Gtop * (T[1] - T[0]) / H_SURF);   // floor surface temperature
      out.flow.push(mcp / CP_WATER * 3600);                       // kg/(h m2)
      out.t_ret.push(mcp > 0 ? tSup - heat / mcp : NaN);
    }
  }
  const h = DT / 3600, sum = (arr, f) => arr.reduce((acc, v) => acc + f(v), 0) * h;
  out.summary = {
    heating_Wh: sum(out.heat, v => v), vented_Wh: sum(out.vent, v => v),
    below_Kh: sum(out.room, v => Math.max(0, p.T_set - v)),
    above_Kh: sum(out.room, v => Math.max(0, v - p.T_set)),
  };
  let mSum = 0, mtSum = 0;
  out.flow.forEach((m, i) => { if (m > 0) { mSum += m; mtSum += m * out.t_ret[i]; } });
  out.summary.return_mw = mSum > 0 ? mtSum / mSum : NaN;     // mass-flow-weighted return temperature
  out.summary.flow_kg = mSum * h;                             // kg/m2 over the two days
  return out;
}

// ---------------------------------------------------------------- user interface
const INPUTS = [
  ["Room and climate", [
    ["T_set", "Setpoint", "°C", 18, 24, 0.5,
      "Room temperature the controllers aim for. The ideal heater holds it exactly whenever heat is needed."],
    ["T_vent", "Windows opened above", "°C", 22, 28, 0.5,
      "Occupants open windows when the room exceeds this temperature. The heat removed is reported as heat vented."],
    ["H_loss", "Heat loss coefficient", "W/(m²·K)", 0.3, 1.5, 0.05,
      "Transmission and ventilation loss per m² floor and per K indoor–outdoor difference. Around 0.6 for a new low-energy house, 1–1.5 for an older house."],
    ["solar_cloudy", "Peak solar gain, cloudy day", "W/m²", 0, 40, 1,
      "Solar gain through the windows at noon on the first day, per m² floor. It follows a half sine from 07 to 19. The warm-up days use the same value."],
    ["solar_sunny", "Peak solar gain, sunny day", "W/m²", 0, 80, 1,
      "Solar gain through the windows at noon on the second day, per m² floor. 40 W/m² is a clear spring day in a room with south-facing windows."]]],
  ["Supply water", [
    ["curve_slope", "Heating curve slope", "K/K", 0.2, 1.2, 0.05,
      "Supply temperature = 20 °C + slope × (20 °C − outdoor temperature). A steeper curve gives warmer water and more heat stored in the floor."],
    ["T_supply_max", "Max supply temperature", "°C", 25, 45, 1,
      "Upper limit of the supply temperature. Set it below the curve to get a constant supply temperature."],
    ["flow_design", "Design mass flow", "kg/(h·m²)", 2, 20, 0.5,
      "Water flow per m² floor when the wax thermostat is fully open (set by hydronic balancing). 6 kg/(h·m²) gives about 5 K cooling of the water at 35 W/m²."]]],
  ["Room control", [
    ["hyst", "On/off hysteresis, ±", "K", 0.1, 1, 0.05,
      "On/off thermostat: opens the loop below setpoint − hysteresis and closes it above setpoint + hysteresis."],
    ["p_band", "PI proportional band", "K", 0.5, 5, 0.25,
      "Temperature error that gives 100 % output from the proportional part. A narrow band reacts strongly to small errors."],
    ["Ti_min", "PI integral time", "min", 15, 360, 15,
      "Time for the integral part to add as much output as the proportional part, at a constant error. Long times give slow but stable control."],
    ["pwm_min", "PWM cycle time", "min", 5, 60, 5,
      "The PI output is sent as a duty cycle: the loop is open for that fraction of each cycle. Short cycles are smoother but wear the actuator."]]],
  ["Wax thermostat", [
    ["dead_open_min", "Dead time, opening", "min", 0, 10, 0.5,
      "Time for the wax to heat up before the valve starts to move after it is switched on."],
    ["stroke_open_min", "Stroke time, opening", "min", 1, 10, 0.5,
      "Time from the valve starting to move until it is fully open. Closing uses 2 min dead time and 5 min stroke."]]],
];
const MODES = [["ideal", "Ideal heater, no delay", "#8a8f94", "6 4"],
               ["onoff", "On/off thermostat", "#d0663a", ""],
               ["pi", "PI controller with PWM", "#2b7bb9", ""]];

const C_SUP = "#7b5ea7";

const CSS = `
:host, .fc { --ink: #1f2328; --muted: #5f6770; --grid: #e3e6e8; --panel: #f6f8fa; --sun: #f2c14e; --day: #fff4d6; }
@media (prefers-color-scheme: dark) { :host, .fc { --ink: #e6edf3; --muted: #9aa4ae; --grid: #30363d; --panel: #161b22; --sun: #b8892a; --day: #2b2410; } }
.fc { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 14px; color: var(--ink); }
.fc .controls { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 12px; margin-bottom: 12px; }
.fc fieldset { min-width: 0; border: 1px solid var(--grid); border-radius: 8px; padding: 8px 12px 10px; margin: 0; background: var(--panel); }
.fc legend { font-weight: 600; padding: 0 4px; }
.fc label { display: grid; grid-template-columns: 1fr auto; gap: 2px 8px; margin-top: 6px; font-size: 13px; }
.fc label input { grid-column: 1 / 3; width: 100%; accent-color: #2b7bb9; }
.fc .help { color: var(--muted); cursor: help; font-size: 12px; }
.fc .val { font-variant-numeric: tabular-nums; color: var(--muted); }
.fc .bar { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; margin: 4px 0 8px; color: var(--muted); font-size: 13px; }
.fc button { font: inherit; padding: 4px 12px; border-radius: 6px; border: 1px solid var(--grid); background: var(--panel); color: var(--ink); cursor: pointer; }
.fc .charts { display: grid; gap: 6px; }
.fc [hidden] { display: none !important; }
.fc .tabs { display: flex; gap: 4px; border-bottom: 1px solid var(--grid); margin-bottom: 10px; }
.fc .tabs button { border: 1px solid var(--grid); border-bottom: 0; border-radius: 6px 6px 0 0; padding: 6px 14px; }
.fc .tabs button.on { background: #2b7bb9; color: #fff; font-weight: 600; }
.fc .extra { display: grid; grid-template-columns: minmax(0, 1fr); gap: 12px; margin-bottom: 12px; }
.fc .extra .note { grid-column: 1 / -1; margin: 0; color: var(--muted); font-size: 13px; }
.fc table.mat input { width: 80px; max-width: 100%; font: inherit; padding: 2px 4px; background: transparent; color: var(--ink); border: 1px solid var(--grid); border-radius: 4px; text-align: right; }
.fc table.mat tr.pipe td { color: #d0663a; text-align: left; }
.fc .cap { margin: 6px 0 0; font-size: 13px; color: var(--muted); }
.fc .toggle { display: inline-flex; border: 1px solid var(--grid); border-radius: 8px; overflow: hidden; }
.fc .toggle button { border: 0; border-radius: 0; padding: 6px 16px; }
.fc .toggle button.on { background: #2b7bb9; color: #fff; font-weight: 600; }
.fc svg { width: 100%; height: auto; display: block; }
.fc svg text { fill: var(--ink); font-size: 11px; }
.fc .legend { display: flex; gap: 16px; flex-wrap: wrap; font-size: 13px; margin: 6px 0 10px; }
.fc .legend span { display: inline-flex; align-items: center; gap: 6px; }
.fc .legend svg { width: auto; flex: none; }
.fc table { border-collapse: collapse; width: 100%; font-size: 13px; font-variant-numeric: tabular-nums; }
.fc th, .fc td { padding: 4px 8px; border-bottom: 1px solid var(--grid); text-align: right; }
.fc th:first-child, .fc td:first-child { text-align: left; }
.fc .tablewrap { overflow-x: auto; }
`;

function axis(arrays) {
  // y-axis range and "nice" ticks that fit all finite values in the given arrays
  let lo = Infinity, hi = -Infinity;
  for (const arr of arrays) for (const v of arr) if (Number.isFinite(v)) { if (v < lo) lo = v; if (v > hi) hi = v; }
  if (!Number.isFinite(lo)) { lo = 0; hi = 1; }
  if (hi - lo < 1e-6) { lo -= 0.5; hi += 0.5; }
  const pad = 0.03 * (hi - lo);            // keep lines off the frame; 0 stays the bottom for flows
  if (lo !== 0) lo -= pad;
  hi += pad;
  const raw = (hi - lo) / 5, mag = 10 ** Math.floor(Math.log10(raw));
  const step = [1, 2, 2.5, 5, 10].map(f => f * mag).find(st => st >= raw);
  const ymin = Math.floor(lo / step + 1e-9) * step, ymax = Math.ceil(hi / step - 1e-9) * step;
  const yticks = []; for (let v = ymin; v <= ymax + step / 2; v += step) yticks.push(+v.toFixed(6));
  return { ymin, ymax, yticks };
}

function chart(series, opts) {
  // series: [{x, y, color, dash}], opts: {title, ylabel, ymin, ymax, yticks, fill, hline}
  const W = opts.W || 900, H = opts.H || 220, L = 46, R = opts.y2 ? 50 : 10, Tm = 22, B = 30;
  const X = v => L + v / 48 * (W - L - R), Y = v => Tm + (opts.ymax - v) / (opts.ymax - opts.ymin) * (H - Tm - B);
  const clampY = v => Y(Math.min(opts.ymax, Math.max(opts.ymin, v)));
  const y2 = opts.y2, Y2 = v => Tm + (y2.max - Math.min(y2.max, Math.max(y2.min, v))) / (y2.max - y2.min) * (H - Tm - B);
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${opts.title}">`;
  s += `<rect x="${X(24)}" y="${Tm}" width="${X(48) - X(24)}" height="${H - Tm - B}" fill="var(--day)"/>`;
  if (opts.fill) {
    const f = opts.fill; let d = `M${X(f.x[0])} ${Y(0)}`;
    for (let i = 0; i < f.x.length; i += 5) d += ` L${X(f.x[i]).toFixed(1)} ${clampY(f.y[i]).toFixed(1)}`;
    d += ` L${X(f.x[f.x.length - 1])} ${Y(0)} Z`;
    s += `<path d="${d}" fill="var(--sun)" opacity="0.45"/>`;
  }
  for (const v of opts.yticks) s += `<line x1="${L}" x2="${W - R}" y1="${Y(v)}" y2="${Y(v)}" stroke="var(--grid)"/><text x="${L - 6}" y="${Y(v) + 4}" text-anchor="end">${v}</text>`;
  for (let v = 0; v <= 48; v += 6) s += `<line x1="${X(v)}" x2="${X(v)}" y1="${Tm}" y2="${H - B}" stroke="var(--grid)"/><text x="${X(v)}" y="${H - B + 14}" text-anchor="middle">${v}</text>`;
  if (opts.hline !== undefined) s += `<line x1="${L}" x2="${W - R}" y1="${Y(opts.hline)}" y2="${Y(opts.hline)}" stroke="#5aa02c" stroke-dasharray="2 3"/>`;
  if (opts.zero) s += `<line x1="${L}" x2="${W - R}" y1="${Y(0)}" y2="${Y(0)}" stroke="var(--muted)"/>`;
  for (const sr of series) {
    let d = "", pen = false;
    const fy = sr.axis === 2 ? Y2 : clampY, step = sr.step || 5;
    for (let i = 0; i < sr.x.length; i += step) {
      if (!Number.isFinite(sr.y[i])) { pen = false; continue; }
      d += `${pen ? "L" : "M"}${X(sr.x[i]).toFixed(1)} ${fy(sr.y[i]).toFixed(1)}`; pen = true;
    }
    s += `<path d="${d}" fill="none" stroke="${sr.color}" stroke-width="${sr.width || 1.8}" ${sr.opacity ? `opacity="${sr.opacity}"` : ""} ${sr.dash ? `stroke-dasharray="${sr.dash}"` : ""}/>`;
  }
  s += `<text x="${L}" y="14" font-weight="600" style="font-size:12px">${opts.title}</text>`;
  s += `<text x="${X(12)}" y="${Tm + 12}" text-anchor="middle" fill="var(--muted)">cloudy day</text><text x="${X(36)}" y="${Tm + 12}" text-anchor="middle">sunny day</text>`;
  s += `<text x="${(L + W - R) / 2}" y="${H - 4}" text-anchor="middle">Time [h]</text>`;
  s += `<text transform="translate(11 ${(Tm + H - B) / 2}) rotate(-90)" text-anchor="middle">${opts.ylabel}</text>`;
  if (y2) {
    for (const v of y2.ticks) s += `<text x="${W - R + 6}" y="${Y2(v) + 4}">${v}</text>`;
    s += `<text transform="translate(${W - 8} ${(Tm + H - B) / 2}) rotate(90)" text-anchor="middle">${y2.label}</text>`;
  }
  return s + "</svg>";
}

function render({ model, el }) {
  const p = { ...DEFAULTS };
  for (const key of Object.keys(DEFAULTS)) { const v = model.get(key); if (typeof v === "number") p[key] = v; }
  const root = document.createElement("div"); root.className = "fc";
  const style = document.createElement("style"); style.textContent = CSS;
  el.appendChild(style); el.appendChild(root);

  const floors = structuredClone(FLOORS);
  const tabs = document.createElement("div"); tabs.className = "tabs"; tabs.setAttribute("role", "tablist");
  root.appendChild(tabs);
  const controls = document.createElement("div"); controls.className = "controls";
  const sliders = {};
  for (const [group, items] of INPUTS) {
    const fs = document.createElement("fieldset");
    fs.innerHTML = `<legend>${group}</legend>`;
    for (const [key, label, unit, min, max, step, help] of items) {
      const lab = document.createElement("label");
      lab.title = help;
      lab.innerHTML = `<span>${label} <span class="help" aria-label="${help}">ⓘ</span></span><span class="val"></span><input type="range" min="${min}" max="${max}" step="${step}" value="${p[key]}">`;
      const input = lab.querySelector("input"), val = lab.querySelector(".val");
      const show = () => { val.textContent = `${(+input.value).toLocaleString("en", { maximumFractionDigits: 2 })} ${unit}`; };
      input.addEventListener("input", () => { p[key] = +input.value; show(); schedule(); });
      show(); sliders[key] = { input, show };
      fs.appendChild(lab);
    }
    controls.appendChild(fs);
  }
  root.appendChild(controls);
  const extra = document.createElement("div"); extra.className = "extra"; extra.hidden = true;
  root.appendChild(extra);
  const COLS = [[1, "Thickness", "mm", 1000, 1], [2, "Conductivity λ", "W/(m·K)", 1, 0.005], [3, "Density ρ", "kg/m³", 1, 10], [4, "Specific heat c", "J/(kg·K)", 1, 10]];
  function buildExtra() {
    extra.innerHTML = `<p class="note">Material properties of the floor layers, from the top surface down. Heat capacity above the pipes controls how fast the floor responds;
      the pipe resistance R<sub>pipe</sub> covers heat spreading from the pipe into the pipe plane (lower with concrete or aluminium plates). Changes apply immediately.</p>`;
    for (const [name, fl] of Object.entries(floors)) {
      const fs = document.createElement("fieldset");
      let html = `<legend>${name}</legend><div class="tablewrap"><table class="mat"><thead><tr><th>Layer</th>${COLS.map(([, l, u]) => `<th>${l}<br>[${u}]</th>`).join("")}</tr></thead><tbody>`;
      fl.layers.forEach((L, i) => {
        if (L === "PIPE") { html += `<tr class="pipe"><td>pipe plane</td><td colspan="4">R<sub>pipe</sub> <input type="number" step="0.005" min="0.005" data-rpipe="1" value="${fl.R_pipe}"> m²·K/W</td></tr>`; return; }
        html += `<tr><td>${L[0]}</td>${COLS.map(([j, , , f, st]) => `<td><input type="number" min="0" step="${st}" data-i="${i}" data-j="${j}" value="${+(L[j] * f).toFixed(4)}"></td>`).join("")}</tr>`;
      });
      html += `</tbody></table></div><p class="cap"></p>`;
      fs.innerHTML = html;
      const cap = fs.querySelector(".cap");
      const showCap = () => {
        let above = 0, total = 0, seen = false;
        for (const L of fl.layers) { if (L === "PIPE") { seen = true; continue; } const c = L[1] * L[3] * L[4] / 1000; total += c; if (!seen) above += c; }
        cap.textContent = `Heat capacity above the pipes ${above.toFixed(0)} kJ/(m²·K), whole floor ${total.toFixed(0)} kJ/(m²·K).`;
      };
      fs.querySelectorAll("input").forEach(inp => inp.addEventListener("input", () => {
        const v = parseFloat(inp.value);
        if (!(v > 0)) return;
        if (inp.dataset.rpipe) fl.R_pipe = v;
        else { const col = COLS.find(c => c[0] === +inp.dataset.j); fl.layers[+inp.dataset.i][+inp.dataset.j] = v / col[3]; }
        showCap(); schedule();
      }));
      showCap();
      extra.appendChild(fs);
    }
  }
  buildExtra();
  for (const [label, panel] of [["Inputs", controls], ["Extra: floor materials", extra]]) {
    const b = document.createElement("button"); b.textContent = label; b.setAttribute("role", "tab");
    b.addEventListener("click", () => {
      controls.hidden = panel !== controls; extra.hidden = panel !== extra;
      tabs.querySelectorAll("button").forEach(x => { x.classList.toggle("on", x === b); x.setAttribute("aria-selected", x === b); });
    });
    tabs.appendChild(b);
  }
  tabs.firstChild.classList.add("on");
  const bar = document.createElement("div"); bar.className = "bar";
  let floorName = Object.keys(FLOORS)[0];
  const toggle = document.createElement("div"); toggle.className = "toggle"; toggle.setAttribute("role", "group");
  const floorButtons = Object.keys(FLOORS).map(name => {
    const btn = document.createElement("button"); btn.textContent = name;
    btn.addEventListener("click", () => { floorName = name; mark(); schedule(); });
    toggle.appendChild(btn); return btn;
  });
  const mark = () => floorButtons.forEach(btn => { const on = btn.textContent === floorName; btn.classList.toggle("on", on); btn.setAttribute("aria-pressed", on); });
  mark();
  bar.appendChild(toggle);
  const reset = document.createElement("button"); reset.textContent = "Reset to defaults";
  const status = document.createElement("span");
  bar.append(reset, status); root.appendChild(bar);
  reset.addEventListener("click", () => {
    Object.assign(p, DEFAULTS);
    for (const [key, s] of Object.entries(sliders)) { s.input.value = p[key]; s.show(); }
    Object.assign(floors, structuredClone(FLOORS)); buildExtra();
    schedule();
  });
  const legend = document.createElement("div"); legend.className = "legend";
  legend.innerHTML = MODES.map(([, lab, col, dash]) =>
    `<span><svg width="26" height="10"><line x1="0" x2="26" y1="5" y2="5" stroke="${col}" stroke-width="2.2" ${dash ? `stroke-dasharray="${dash}"` : ""}/></svg>${lab}</span>`).join("")
    + `<span><svg width="18" height="10"><rect width="18" height="10" fill="var(--sun)" opacity="0.6"/></svg>Solar gain</span>`
    + `<span><svg width="26" height="10"><line x1="0" x2="26" y1="5" y2="5" stroke="${C_SUP}" stroke-width="2.2"/></svg>Supply temperature</span>`
    + `<span><svg width="26" height="10"><line x1="0" x2="26" y1="5" y2="5" stroke="var(--muted)" stroke-width="1"/></svg>Return temperature (thin)</span>`
    ;
  const charts = document.createElement("div"); charts.className = "charts";
  const tableWrap = document.createElement("div"); tableWrap.className = "tablewrap";
  root.append(legend, charts, tableWrap);

  let timerId = null;
  function schedule() { clearTimeout(timerId); status.textContent = "calculating…"; timerId = setTimeout(run, 120); }
  function run() {
    const t0 = performance.now();
    const floor = floors[floorName];
    const r = Object.fromEntries(MODES.map(([m]) => [m, simulate(floor, m, p)]));
    const water = MODES.filter(([m]) => m !== "ideal");
    const roomS = MODES.map(([m, , color, dash]) => ({ x: r[m].t, y: r[m].room, color, dash }));
    let html = chart(roomS, { title: `${floorName}: room temperature [°C]`, ylabel: "°C", hline: p.T_vent,
      ...axis([...roomS.map(sr => sr.y), [p.T_set, p.T_vent]]) });
    const fluxS = MODES.map(([m, , color, dash]) => ({ x: r[m].t, y: r[m].q_floor, color, dash }));
    html += chart(fluxS, { title: `${floorName}: heat flux floor surface [W/m²] (ideal heater: its own output)`, ylabel: "W/m²",
      zero: true, fill: { x: r.ideal.t, y: r.ideal.solar }, ...axis([...fluxS.map(sr => sr.y), r.ideal.solar, [0]]) });
    const tSeries = [{ x: r.ideal.t, y: r.ideal.t_sup, color: C_SUP },
        ...MODES.map(([m, , color, dash]) => ({ x: r[m].t, y: r[m].surface, color, dash })),
        ...water.map(([m, , color]) => ({ x: r[m].t, y: r[m].t_ret, color, width: 1, step: 1 }))];
    html += chart(tSeries, { title: `${floorName}: supply, return (thin) and floor surface temperature [°C]`, ylabel: "°C",
      ...axis(tSeries.map(sr => sr.y)) });
    const flowS = water.map(([m, , color]) => ({ x: r[m].t, y: r[m].flow, color, width: 1.2, step: 1 }));
    html += chart(flowS, { title: `${floorName}: mass flow in the loop [kg/(h·m²)]`, ylabel: "kg/(h·m²)", H: 170,
      ...axis([...flowS.map(sr => sr.y), [0, p.flow_design]]) });
    charts.innerHTML = html;
    let rows = "";
    for (const [m, lab] of MODES) {
      const s = r[m].summary, tr = Number.isFinite(s.return_mw) ? s.return_mw.toFixed(1) : "–";
      rows += `<tr><td>${lab}</td><td>${s.heating_Wh.toFixed(0)}</td><td>${s.vented_Wh.toFixed(0)}</td>
        <td>${s.below_Kh.toFixed(1)}</td><td>${s.above_Kh.toFixed(1)}</td><td>${(s.below_Kh + s.above_Kh).toFixed(1)}</td><td>${tr}</td></tr>`;
    }
    tableWrap.innerHTML = `<table><thead><tr><th>${floorName}</th><th title="Heat supplied by the water (or the ideal heater) over the two days">Heating energy<br>[Wh/m²]</th>
      <th title="Heat removed by opening windows above the venting temperature">Heat vented<br>[Wh/m²]</th>
      <th title="Time integral of how far the room is below the setpoint">Below setpoint<br>[K·h]</th>
      <th title="Time integral of how far the room is above the setpoint">Above setpoint<br>[K·h]</th><th>Total deviation<br>[K·h]</th>
      <th title="Average return temperature weighted by the mass flow, i.e. the temperature the heat source actually receives">Return temp., flow-weighted<br>[°C]</th></tr></thead>
      <tbody>${rows}</tbody></table>`;
    status.textContent = `Two days shown, after ${p.warmup_days} cloudy warm-up days. Calculated in ${Math.round(performance.now() - t0)} ms.`;
  }
  run();
  return () => clearTimeout(timerId);
}

export default { render };
