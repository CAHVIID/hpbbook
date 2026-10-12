"""Build the stand-alone page dhw-tank.html from dhw-tank.mjs.

The page inlines the anywidget module, so it is one file that runs offline in any
browser. Run this again after changing dhw-tank.mjs:

    python build_dhw_tank_html.py
"""
from pathlib import Path

HERE = Path(__file__).parent
module = (HERE / "dhw-tank.mjs").read_text(encoding="utf-8")

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Stratified hot water tank simulator</title>
<style>
html, body {{ margin: 0; background: #fff; color: #1f2328; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }}
@media (prefers-color-scheme: dark) {{ html, body {{ background: #0d1117; color: #e6edf3; }} }}
main {{ max-width: 1200px; margin: 0 auto; padding: 16px; }}
h1 {{ font-size: 20px; margin: 4px 0 4px; }}
p.sub {{ margin: 0 0 12px; font-size: 14px; opacity: .75; }}
</style>
</head><body><main>
<h1>Stratified hot water tank simulator</h1>
<p class="sub">One day in a domestic hot water tank split into horizontal layers, charged by a heat pump in the hours you allow and emptied by a tapping profile.</p>
<div id="app"></div>
</main>
<script type="module">
{module}
render({{ model: {{ get: () => null, set() {{}}, on() {{}}, save_changes() {{}} }}, el: document.getElementById("app") }});
</script></body></html>
"""
(HERE / "dhw-tank.html").write_text(page, encoding="utf-8")
print("wrote", HERE / "dhw-tank.html")
