"""Build the stand-alone app fan-comfort.html from fan-comfort.src.html and fan-comfort-model.mjs.

The comfort model is inlined, so the app is one file. It needs internet only for the fonts
and the chart library. Run this again after changing either source file:

    python build_fan_comfort_html.py
"""
from pathlib import Path

HERE = Path(__file__).parent
model = (HERE / "fan-comfort-model.mjs").read_text(encoding="utf-8").replace("export function", "function")
body = (HERE / "fan-comfort.src.html").read_text(encoding="utf-8").replace("/*MODEL*/", model)
page = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<style>body{margin:0} [hidden]{display:none!important}</style>\n'
        f'</head><body>\n{body}\n</body></html>\n')
(HERE / "fan-comfort.html").write_text(page, encoding="utf-8")
print("wrote", HERE / "fan-comfort.html")
