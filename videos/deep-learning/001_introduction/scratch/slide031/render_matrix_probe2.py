#!/usr/bin/env python3
"""Matrix probe v2 (working genfrac syntax). Fit: ink 200x99pt, ratio 2.020."""
import json, os, importlib.util
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["mathtext.fontset"] = "stix"
import numpy as np
from PIL import Image

spec = importlib.util.spec_from_file_location("render_eq", "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

HERE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide031"

def ink_bbox(png):
    al = np.asarray(Image.open(png))[:, :, 3]
    ys, xs = np.where(al > 8)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())

def try_render(tag, latex, fs):
    out = os.path.join(HERE, f"probe_{tag}.png")
    info = mod.render(latex, out, fs, "000000")
    x0, y0, x1, y1 = ink_bbox(out)
    w = (x1 - x0 + 1) / 600 * 72
    h = (y1 - y0 + 1) / 600 * 72
    print(f"{tag}: fs {fs} ink {x1-x0+1}x{y1-y0+1}px -> {w:.1f}x{h:.1f}pt ratio {w/h:.3f} (t 2.020) ink_off ({x0},{y0})")
    return w, h

G = r"\genfrac{}{}{0}{0}"
variants = [
    ("v_semi",  rf"\left[\;{G}{{\theta_1\;\;\theta_2\;\;\theta_3}}{{{G}{{\theta_4\;\;\theta_5\;\;\theta_6}}{{\theta_7\;\;\theta_8\;\;\theta_9}}}}\;\right]"),
    ("v_thin",  rf"\left[\ {G}{{\theta_1\ \ \theta_2\ \ \theta_3}}{{{G}{{\theta_4\ \ \theta_5\ \ \theta_6}}{{\theta_7\ \ \theta_8\ \ \theta_9}}}}\ \right]"),
    ("v_quad",  rf"\left[\ {G}{{\theta_1\quad\theta_2\quad\theta_3}}{{{G}{{\theta_4\quad\theta_5\quad\theta_6}}{{\theta_7\quad\theta_8\quad\theta_9}}}}\ \right]"),
]
for tag, latex in variants:
    try_render(tag, latex, 40.0)
