"""Build the stand-alone page room-cfd-3d.html from room-cfd-3d.template.html and room_cfd_3d_gpu.mjs.

The page inlines the WebGPU solver, so it is one file that runs from disk without a web server
(double-click it). Run this again after changing either source file:

    python build_room_cfd_3d_html.py
"""
from pathlib import Path

HERE = Path(__file__).parent
solver = (HERE / "room_cfd_3d_gpu.mjs").read_text(encoding="utf-8").replace("\nexport ", "\n")
page = (HERE / "room-cfd-3d.template.html").read_text(encoding="utf-8")
assert page.count("/*SOLVER*/") == 1
(HERE / "room-cfd-3d.html").write_text(page.replace("/*SOLVER*/", solver), encoding="utf-8")
print("wrote", HERE / "room-cfd-3d.html")
