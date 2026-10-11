"""Build the stand-alone page room-cfd.html from room-cfd.mjs.

The page inlines the anywidget module, so it is one file that runs offline in any
browser and starts the simulation at once. Run this again after changing room-cfd.mjs:

    python build_room_cfd_html.py
"""
from pathlib import Path

HERE = Path(__file__).parent
module = (HERE / "room-cfd.mjs").read_text(encoding="utf-8")

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Room Section CFD</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
html, body {{ margin: 0; background: #f3f5f7; color: #17212b; font-family: "IBM Plex Sans", system-ui, sans-serif; }}
@media (prefers-color-scheme: dark) {{ html, body {{ background: #11161b; color: #e5ebf0; }} }}
main {{ max-width: 1240px; margin: 0 auto; padding: 16px; }}
h1 {{ font-size: 22px; font-weight: 600; margin: 4px 0 4px; }}
p.sub {{ margin: 0 0 12px; font-size: 14px; opacity: .75; max-width: 70ch; }}
</style>
</head><body><main>
<h1>Room Section CFD</h1>
<p class="sub">A 2D section through a 5 m deep, 2.5 m high office (4 m wide) cooled by outdoor air through one opening in the facade. The air leaves through an exhaust in the back wall. Watch the cold air enter, fall and spread, then read the draught at ankle height.</p>
<div id="app"></div>
</main>
<script type="module">
{module}
render({{ model: {{ get: k => (k === "autorun" ? true : null), set() {{}}, on() {{}}, save_changes() {{}} }}, el: document.getElementById("app") }});
</script></body></html>
"""
(HERE / "room-cfd.html").write_text(page, encoding="utf-8")
print("wrote", HERE / "room-cfd.html")
