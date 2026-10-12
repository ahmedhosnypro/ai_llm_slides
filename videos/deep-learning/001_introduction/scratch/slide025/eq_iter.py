#!/usr/bin/env python3
"""Iterate equation PNGs to match the original's measured ink (frame px = pt).
Targets (ink bboxes, baseline):
  eq1: x90..232, y472..490, baseline 486.5  'Net_j = sum_i ( w_ji O_i )'
  eq2: x297..484, y463..494, baseline 482.5 'O_j = f ( Net_j ) = 1/(1+e^-Net_j)'
  eq3: x546..703, y461..495, baseline 480.5 'E = 1/2 sum_j ( t_j - O_j )^2'
"""
import json, subprocess, sys
from PIL import Image
import numpy as np

A = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"

CANDIDATES = {
    "eq1": [
        (15, r"Net_j\,=\,\sum_{i}\,(\,w_{ji}O_{i}\,)"),
        (15, r"Net_j\;=\;\sum_{i}\;(\;w_{ji}O_{i}\;)"),
        (16, r"Net_j\;=\;\sum_{i}\;(\;w_{ji}O_{i}\;)"),
    ],
    "eq2": [
        (15, r"O_j\,=\,f\,(\,\mathit{Net}_j\,)\,=\,\frac{1}{1+e^{-\mathit{Net}_j}}"),
        (15, r"O_j\;=\;f\;(\,\mathit{Net}_j\,)\;=\;\frac{1}{1+e^{-\mathit{Net}_j}}"),
        (16, r"O_j\;=\;f\;(\,\mathit{Net}_j\,)\;=\;\frac{1}{1+e^{-\mathit{Net}_j}}"),
    ],
    "eq3": [
        (15, r"E\,=\,\frac{1}{2}\,\sum_{j}\,(\,t_j - O_j\,)^{2}"),
        (15, r"E\;=\;\frac{1}{2}\;\sum_{j}\;(\,t_j - O_j\,)^{2}"),
        (16, r"E\;=\;\frac{1}{2}\;\sum_{j}\;(\,t_j - O_j\,)^{2}"),
    ],
}
TARGET = {"eq1": (142, 19), "eq2": (187, 32), "eq3": (157, 35)}

def ink_bbox(png):
    im = np.asarray(Image.open(png).convert("RGBA")).astype(int)
    ink = im[:, :, 3] > 8
    ys, xs = np.where(ink)
    return xs.min(), ys.min(), xs.max(), ys.max()

for name, cands in CANDIDATES.items():
    tw, th = TARGET[name]
    for fs, tex in cands:
        out = f"{A}/{name}_trial.png"
        r = subprocess.run([sys.executable, "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py",
                            tex, out, str(fs), "000000"], capture_output=True, text=True)
        if r.returncode != 0:
            print(name, fs, "RENDER FAIL", r.stderr[-300:]); continue
        d = json.loads(r.stdout)
        wpt, hpt = d["w_px"] / 600 * 72, d["h_px"] / 600 * 72
        x0, y0, x1, y1 = ink_bbox(out)
        inkw, inkh = (x1 - x0 + 1) / 600 * 72, (y1 - y0 + 1) / 600 * 72
        print(f"{name} F{fs}: ink {inkw:.1f}x{inkh:.1f}pt (target {tw}x{th})  dw={inkw-tw:+.1f} dh={inkh-th:+.1f}  tex={tex[:50]}")
