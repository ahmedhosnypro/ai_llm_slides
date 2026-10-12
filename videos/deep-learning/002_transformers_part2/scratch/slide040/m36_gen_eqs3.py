#!/usr/bin/env python3
"""Regenerate eq3 (short arrow, fs 23.0) and eq4 (fs 18.6) calibrated to the original's
measured ink extents (eq3: frame 173..281 bar inside rect edge 287; eq4: frame 175..371)."""
import json, os, subprocess, sys

ROOT = "/home/ahmed/Projects/ai_llm_slides"
VID = f"{ROOT}/videos/deep-learning/002_transformers_part2"
ASSETS = f"{VID}/recreated_pptx/build/assets"
SCR = f"{VID}/scratch/slide040"

ENV = dict(os.environ)
ENV["MATPLOTLIBRC"] = f"{SCR}/matplotlibrc"
ENV["MPLCONFIGDIR"] = SCR
ENV["TMPDIR"] = SCR

EQS = [
    ("eq3", r"\widehat{x}_i \leftarrow \frac{x_i - \mu_{\mathcal{B}}}{\sqrt{\sigma_{\mathcal{B}}^2 + \epsilon}}", "000000", 23.0),
    ("eq4", r"y_i \leftarrow \gamma\, \widehat{x}_i + \beta \equiv \mathrm{BN}_{\gamma,\beta}(x_i)", "000000", 18.6),
]
for name, latex, color, fs in EQS:
    out = f"{ASSETS}/slide040_{name}.png"
    r = subprocess.run([sys.executable, f"{ROOT}/scripts/render_eq.py", latex, out, str(fs), color],
                       capture_output=True, text=True, env=ENV, cwd=SCR)
    if r.returncode != 0:
        print("RENDER FAIL:", name, r.stderr[-300:]); continue
    info = json.loads(r.stdout)
    with open(f"{ASSETS}/slide040_{name}_eq.json", "w") as f:
        json.dump(info, f, indent=1)
    print(f"{name}: fs {fs} -> w {info['w_in']*72:.1f}pt h {info['h_in']*72:.1f}pt baseline_frac {info['baseline_frac']:.4f}")
