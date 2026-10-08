"""Build the stand-alone page floor-control.html from floor-control.mjs.

The page inlines the anywidget module, so it is one file that runs offline in any
browser. Run this again after changing floor-control.mjs:

    python build_floor_control_html.py
"""
from pathlib import Path

HERE = Path(__file__).parent
module = (HERE / "floor-control.mjs").read_text(encoding="utf-8")

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Floor heating control model</title>
<style>
html, body {{ margin: 0; background: #fff; color: #1f2328; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }}
@media (prefers-color-scheme: dark) {{ html, body {{ background: #0d1117; color: #e6edf3; }} }}
main {{ max-width: 1200px; margin: 0 auto; padding: 16px; }}
h1 {{ font-size: 20px; margin: 4px 0 4px; }}
p.sub {{ margin: 0 0 12px; font-size: 14px; opacity: .75; }}
</style>
</head><body><main>
<h1>Floor heating control model</h1>
<p class="sub">One room in a low-energy house with a light and a heavy floor over a cloudy and a sunny spring day. On/off thermostat, PI control with PWM to the wax thermostat, and an ideal heater for reference.</p>
<div id="app"></div>
</main>
<script type="module">
{module}
render({{ model: {{ get: () => null, set() {{}}, on() {{}}, save_changes() {{}} }}, el: document.getElementById("app") }});
</script></body></html>
"""
(HERE / "floor-control.html").write_text(page, encoding="utf-8")
print("wrote", HERE / "floor-control.html")
