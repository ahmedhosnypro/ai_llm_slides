#!/usr/bin/env python3
"""Generate slide_040 equation PNGs via the certified scripts/render_eq.py (600dpi,
tight transparent, sidecar JSON). Fontset cm (playlist panel is LaTeX Computer Modern).
Width-fit: render at 19pt, rescale fontsize so ink width matches the original frame's
measured ink width (frame px -> slide pt: /0.96123), re-render. PIL-probe every PNG."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides"
VID = f"{ROOT}/videos/deep-learning/002_transformers_part2"
ASSETS = f"{VID}/recreated_pptx/build/assets"
SCR = f"{VID}/scratch/slide040"
os.makedirs(ASSETS, exist_ok=True)

ENV = dict(os.environ)
ENV["MATPLOTLIBRC"] = f"{SCR}/matplotlibrc"
ENV["MPLCONFIGDIR"] = SCR
ENV["TMPDIR"] = SCR

# name, mathtext, color, target_ink_w_pt (from PIL frame measurements /0.96123)
EQS = [
    ("h1", r"\mathbf{Input:}\ \ \mathrm{Values\ of}\ x\ \mathrm{over\ a\ mini-batch:}\ \mathcal{B}=\{x_{1\ldots m}\};", "000000", 382.1),
    ("h2", r"\mathrm{Parameters\ to\ be\ learned:}\ \gamma,\ \beta", "008000", 217.3),
    ("h3", r"\mathbf{Output:}\ \ \{y_i=\mathrm{BN}_{\gamma,\beta}(x_i)\}", "000000", 201.7),
    ("eq1", r"\mu_{\mathcal{B}} \leftarrow \frac{1}{m} \sum_{i=1}^{m} x_i", "000000", 124.8),
    ("eq2", r"\sigma_{\mathcal{B}}^{2} \leftarrow \frac{1}{m} \sum_{i=1}^{m} (x_i - \mu_{\mathcal{B}})^2", "000000", 183.6),
    ("eq3", r"\widehat{x}_i \leftarrow \frac{x_i - \mu_{\mathcal{B}}}{\sqrt{\sigma_{\mathcal{B}}^2 + \epsilon}}", "000000", 121.0),
    ("eq4", r"y_i \leftarrow \gamma\, \widehat{x}_i + \beta \equiv \mathrm{BN}_{\gamma,\beta}(x_i)", "000000", 207.6),
]

def render(latex, out, fs, color):
    r = subprocess.run(
        [sys.executable, f"{ROOT}/scripts/render_eq.py", latex, out, str(fs), color],
        capture_output=True, text=True, env=ENV, cwd=SCR)
    if r.returncode != 0:
        print("RENDER FAIL:", latex[:40], r.stdout[-400:], r.stderr[-400:])
        return None
    return json.loads(r.stdout)

report = {}
for name, latex, color, target_w in EQS:
    out = f"{ASSETS}/slide040_{name}.png"
    info = render(latex, out, 19.0, color)
    if info is None:
        report[name] = "FAILED"
        continue
    w_pt = info["w_in"] * 72
    fs2 = round(19.0 * target_w / w_pt, 2)
    info2 = render(latex, out, fs2, color)
    w_pt2 = info2["w_in"] * 72
    # PIL probe: ink present? ink bbox + mean ink color
    im = np.asarray(Image.open(out))
    alpha = im[:, :, 3]
    ys, xs = np.where(alpha > 40)
    ink = im[alpha > 120][:, :3]
    mean_ink = ink.mean(axis=0).astype(int) if len(ink) else [0, 0, 0]
    report[name] = {
        "fontsize": fs2, "w_pt": round(w_pt2, 1), "target_w_pt": target_w,
        "h_pt": round(info2["h_in"] * 72, 1),
        "baseline_frac": info2["baseline_frac"],
        "px": [info2["w_px"], info2["h_px"]],
        "ink_bbox_frac": [round(xs.min()/info2["w_px"], 3), round(ys.min()/info2["h_px"], 3),
                          round(xs.max()/info2["w_px"], 3), round(ys.max()/info2["h_px"], 3)],
        "mean_ink_rgb": mean_ink.tolist(),
        "n_ink_px": int((alpha > 40).sum()),
    }
    with open(f"{ASSETS}/slide040_{name}_eq.json", "w") as f:
        json.dump(info2, f, indent=1)

print(json.dumps(report, indent=1))
