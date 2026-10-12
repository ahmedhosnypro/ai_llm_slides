#!/usr/bin/env python3
"""Render the 3x3 theta bracket matrix via certified render_eq.py + STIX serif fontset.
Target (original frame ink): brackets x 634..833 (w 200pt), y 396..494 (h 99pt).
Knobs: fontsize (absolute scale), column separation (w/h ratio).
"""
import json, os, sys, importlib.util
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["mathtext.fontset"] = "stix"  # serif italic theta — matches original
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("render_eq", "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
os.makedirs(ASSETS, exist_ok=True)

def ink_bbox(png):
    im = Image.open(png)
    al = np.asarray(im)[:, :, 3]
    ys, xs = np.where(al > 8)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())

def try_render(tag, latex, fs, out):
    info = mod.render(latex, out, fs, "000000")
    x0, y0, x1, y1 = ink_bbox(out)
    w_ink_pt = (x1 - x0 + 1) / 600 * 72
    h_ink_pt = (y1 - y0 + 1) / 600 * 72
    print(f"{tag}: fs {fs} ink {x1-x0+1}x{y1-y0+1}px -> {w_ink_pt:.1f}x{h_ink_pt:.1f}pt (target 200x99, ratio {w_ink_pt/h_ink_pt:.3f} t 2.020) ink_off ({x0},{y0})")
    return {"tag": tag, "latex": latex, "fs": fs, "info": info, "ink_off": [x0, y0],
            "w_ink_pt": w_ink_pt, "h_ink_pt": h_ink_pt}

results = []
# spacing variants between columns and around brackets (fontsize probe at 40)
for tag, latex in [
    ("semicol", r"\left[\;\genfrac{}{}{0pt}{0}{\theta_1\;\;\theta_2\;\;\theta_3}{\genfrac{}{}{0pt}{0}{\theta_4\;\;\theta_5\;\;\theta_6}{\theta_7\;\;\theta_8\;\;\theta_9}}\;\right]"),
    ("thinsp",  r"\left[\ \genfrac{}{}{0pt}{0}{\theta_1\ \ \theta_2\ \ \theta_3}{\genfrac{}{}{0pt}{0}{\theta_4\ \ \theta_5\ \ \theta_6}{\theta_7\ \ \theta_8\ \ \theta_9}}\ \right]"),
    ("nospace", r"\left[\genfrac{}{}{0pt}{0}{\theta_1\ \theta_2\ \theta_3}{\genfrac{}{}{0pt}{0}{\theta_4\ \theta_5\ \theta_6}{\theta_7\ \theta_8\ \theta_9}}\right]"),
]:
    out = os.path.join(HERE, f"probe_{tag}.png")
    results.append(try_render(tag, latex, 40.0, out))

json.dump(results, open(os.path.join(HERE, "probe_results.json"), "w"), indent=1)
print("saved probe_results.json")
