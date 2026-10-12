#!/usr/bin/env python3
"""Final equation PNG set for slide_040 (long arrows per frame, width+height reported)."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides"
VID = f"{ROOT}/videos/deep-learning/002_transformers_part2"
ASSETS = f"{VID}/recreated_pptx/build/assets"
SCR = f"{VID}/scratch/slide040"

ENV = dict(os.environ)
ENV["MATPLOTLIBRC"] = f"{SCR}/matplotlibrc"
ENV["MPLCONFIGDIR"] = SCR
ENV["TMPDIR"] = SCR

# (name, latex, color, fontsize, target_w_pt, target_h_pt)
EQS = [
    ("h1", r"\mathbf{Input:}\ \ \mathrm{Values\ of}\ x\ \mathrm{over\ a\ mini-batch:}\ \mathcal{B}=\{x_{1\ldots m}\};", "000000", 15.75, 382.1, 16.7),
    ("h2", r"\mathrm{Parameters\ to\ be\ learned:}\ \gamma,\ \beta", "#008000", 16.3, 217.3, 13.6),
    ("h3", r"\mathbf{Output:}\ \ \{y_i=\mathrm{BN}_{\gamma,\beta}(x_i)\}", "000000", 16.95, 201.7, 15.7),
    ("eq1", r"\mu_{\mathcal{B}} \longleftarrow \frac{1}{m} \sum_{i=1}^{m} x_i", "000000", 19.5, 124.8, 49.2),
    ("eq2", r"\sigma_{\mathcal{B}}^{2} \longleftarrow \frac{1}{m} \sum_{i=1}^{m} (x_i - \mu_{\mathcal{B}})^2", "000000", 19.5, 183.6, 51.3),
    ("eq3", r"\widehat{x}_i \longleftarrow \frac{x_i - \mu_{\mathcal{B}}}{\sqrt{\sigma_{\mathcal{B}}^2 + \epsilon}}", "000000", 24.5, 121.0, 49.2),
    ("eq4", r"y_i \leftarrow \gamma\, \widehat{x}_i + \beta \equiv \mathrm{BN}_{\gamma,\beta}(x_i)", "000000", 19.9, 207.6, 24.1),
]

def render(latex, out, fs, color):
    r = subprocess.run(
        [sys.executable, f"{ROOT}/scripts/render_eq.py", latex, out, str(fs), color],
        capture_output=True, text=True, env=ENV, cwd=SCR)
    if r.returncode != 0:
        print("RENDER FAIL:", latex[:44], "|", r.stdout[-200:], r.stderr[-300:])
        return None
    return json.loads(r.stdout)

report = {}
for name, latex, color, fs, tw, th in EQS:
    out = f"{ASSETS}/slide040_{name}.png"
    info = render(latex, out, fs, color)
    if info is None:
        report[name] = "FAILED"
        continue
    im = np.asarray(Image.open(out))
    alpha = im[:, :, 3]
    ys, xs = np.where(alpha > 40)
    report[name] = {
        "fs": fs, "w_pt": round(info["w_in"]*72, 1), "h_pt": round(info["h_in"]*72, 1),
        "target_w": tw, "target_h": th,
        "dw%": round((info["w_in"]*72/tw - 1)*100, 1), "dh%": round((info["h_in"]*72/th - 1)*100, 1),
        "baseline_frac": info["baseline_frac"],
        "n_ink": int((alpha > 40).sum()),
    }
    with open(f"{ASSETS}/slide040_{name}_eq.json", "w") as f:
        json.dump(info, f, indent=1)

print(json.dumps(report, indent=1))
