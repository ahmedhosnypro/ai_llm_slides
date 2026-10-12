#!/usr/bin/env python3
"""Sweep eq3 mathtext variants; report (w_pt, h_pt) vs targets w~118.7..121, h~49.2."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides"
VID = f"{ROOT}/videos/deep-learning/002_transformers_part2"
SCR = f"{VID}/scratch/slide040"
ENV = dict(os.environ)
ENV["MATPLOTLIBRC"] = f"{SCR}/matplotlibrc"
ENV["MPLCONFIGDIR"] = SCR
ENV["TMPDIR"] = SCR

ARROW_LONG = r"\widehat{x}_i \longleftarrow \frac{x_i - \mu_{\mathcal{B}}}{\sqrt{\sigma_{\mathcal{B}}^2 + \epsilon}}"
ARROW_SHORT = r"\widehat{x}_i \leftarrow \frac{x_i - \mu_{\mathcal{B}}}{\sqrt{\sigma_{\mathcal{B}}^2 + \epsilon}}"

CANDS = [
    ("A long fs21.4", ARROW_LONG, 21.4),
    ("B short fs24.5", ARROW_SHORT, 24.5),
    ("C short fs26.0", ARROW_SHORT, 26.0),
    ("D long fs22.5", ARROW_LONG, 22.5),
    ("E short fs25.0", ARROW_SHORT, 25.0),
]
print(f"{'cand':16s} {'w_pt':>7s} {'h_pt':>7s} {'dw%':>7s} {'dh%':>7s}  (targets w 118.7-121, h 49.2)")
for name, latex, fs in CANDS:
    out = f"{SCR}/cand_eq3.png"
    r = subprocess.run([sys.executable, f"{ROOT}/scripts/render_eq.py", latex, out, str(fs), "000000"],
                       capture_output=True, text=True, env=ENV, cwd=SCR)
    if r.returncode != 0:
        print(name, "FAIL", r.stderr[-200:]); continue
    info = json.loads(r.stdout)
    w, h = info["w_in"]*72, info["h_in"]*72
    print(f"{name:16s} {w:7.1f} {h:7.1f} {(w/119.5-1)*100:+7.1f} {(h/49.2-1)*100:+7.1f}")
