#!/usr/bin/env python3
"""Generate remaining slide-024 equation PNGs (600 dpi mathtext, transparent).

Companion to gen_slide_024_eq.py, which only emits eq_s024_sigmoid.png.
slide_024_recreated.js expects: eq_s024_remember.png, eq_s024_step1.png,
eq_s024_step2a.png, eq_s024_step2b.png, eq_s024_step3.png, eq_s024_final.png.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
from PIL import Image

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DPI = 600
FONT_SIZE = 22
BLACK = "#000000"
RED = "#c00000"


def render(spec, name, color=BLACK):
    fig, ax = plt.subplots(figsize=(1, 1), dpi=DPI)
    ax.text(0.5, 0.5, spec, ha="center", va="center",
            fontsize=FONT_SIZE, color=color, fontfamily="DejaVu Sans")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    out = os.path.join(OUT_DIR, name)
    fig.savefig(out, dpi=DPI, transparent=True, bbox_inches="tight", pad_inches=0.01)
    plt.close(fig)
    img = Image.open(out)
    w, h = img.size
    print(f"{name}: {w}x{h} px = {w/DPI:.3f}x{h/DPI:.3f} in")
    return img


render(r"$\mathrm{Remember:}\ \frac{\partial}{\partial x}\left(\frac{1}{x}\right) = -\frac{1}{x^{2}}$",
       "eq_s024_remember.png", "#333333")
render(r"$f'(x) = \frac{e^{-x}}{(1+e^{-x})(1+e^{-x})} = \frac{1*(1+e^{-x}-1)}{(1+e^{-x})(1+e^{-x})}$",
       "eq_s024_step1.png", "#333333")
render(r"$= \frac{1}{(1+e^{-x})}\left|\frac{(1+e^{-x}-1)}{(1+e^{-x})}\right|$",
       "eq_s024_step2a.png", "#333333")
render(r"$= \frac{1}{(1+e^{-x})}\left|\frac{(1+e^{-x})}{(1+e^{-x})}\frac{-1}{(1+e^{-x})}\right|$",
       "eq_s024_step2b.png", "#333333")
render(r"$f'(x) = \frac{1}{(1+e^{-x})}\left|1 - \frac{1}{(1+e^{-x})}\right|$",
       "eq_s024_step3.png", "#333333")
render(r"$\Rightarrow\ f'(x) = f(x)\,[1 - f(x)]$",
       "eq_s024_final.png", RED)
print("done slide 024 remaining eqs")
