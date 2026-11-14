#!/usr/bin/env python3
"""Color-aware 600-dpi equation assets for slide 024.

Renders each mathtext expression glyph-by-glyph from matplotlib's vector parse,
so individual glyphs can carry the original's red/blue/black/orange ink. Writes
one transparent PNG plus a JSON sidecar per equation and a combined manifest.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.ft2font import LoadFlags
from matplotlib.mathtext import MathTextParser
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from PIL import Image

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DPI = 600
PARSER = MathTextParser("path")
PAD_PT = 4.0
BLACK = "#000000"
RED = "#CC0000"
BLUE = "#0000CC"
ORANGE = "#E36C0A"

EXPRESSIONS = {
    "sigmoid": (r"$f(x)=\mathbf{Sigmoid}(x)=\frac{1}{1+e^{-x}}$", 19, {20: RED, 21: RED}),
    "remember": (r"$\mathit{\mathbf{Remember:}}\ \frac{\partial}{\partial x}\left(\frac{1}{x}\right)=-\frac{1}{x^{2}}$", 18,
                 {**{i: BLUE for i in range(0, 9)}, **{i: RED for i in range(12, 16)}, **{i: BLUE for i in range(17, 21)}}),
    "step1": (r"$f'(x)=\frac{e^{-x}}{(1+e^{-x})(1+e^{-x})}=\frac{1*(1+e^{-x}-1)}{(1+e^{-x})(1+e^{-x})}$", 28,
              {7: RED, 8: RED, 13: RED, 14: RED, 20: RED, 21: RED, 24: RED,
               30: RED, 31: RED, 39: RED, 40: RED, 46: RED, 47: RED,
               **{i: BLUE for i in range(26, 35)}}),
    "step2a": (r"$f'(x)=\frac{1}{(1+e^{-x})}\left(\frac{(1+e^{-x}-1)}{(1+e^{-x})}\right)$", 24,
               {11: RED, 12: RED, 19: RED, 20: RED, 28: RED, 29: RED,
                **{i: BLUE for i in range(15, 24)}}),
    "step2b": (r"$=\frac{1}{(1+e^{-x})}\left(\frac{(1+e^{-x})}{(1+e^{-x})}\frac{-1}{(1+e^{-x})}\right)$", 24,
               {6: RED, 7: RED, 14: RED, 15: RED, 21: RED, 22: RED, 30: RED, 31: RED,
                **{i: BLUE for i in range(10, 17)}, 24: BLUE, 25: BLUE}),
    "step3": (r"$f'(x)=\frac{1}{(1+e^{-x})}\left|1-\frac{1}{(1+e^{-x})}\right|$", 26,
              {11: RED, 12: RED, 22: RED, 23: RED}),
    "final": (r"$\Rightarrow\ f'(x)=f(x)\,[1-f(x)]$", 28,
              {0: ORANGE, **{i: RED for i in range(7, 19)}}),
}


def render_color_math(spec, font_size_pt, color_by_index, out_png):
    prop = font_manager.FontProperties(size=100)
    width, height, descent, glyphs, rects = PARSER.parse(spec, dpi=72, prop=prop)
    scale = font_size_pt / 100.0
    total_w = (width + 2 * PAD_PT) * scale
    total_h = (height + descent + 2 * PAD_PT) * scale
    fig = plt.figure(figsize=(total_w / 72.0, total_h / 72.0), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, total_w)
    ax.set_ylim(0, total_h)
    ax.axis("off")
    for i, (font, glyph_fs, ccode, glyph_index, ox, oy) in enumerate(glyphs):
        font.clear()
        font.set_size(100, 72)
        font.load_glyph(glyph_index, flags=LoadFlags.NO_HINTING)
        verts, codes = font.get_path()
        s = (glyph_fs / 100.0) * scale
        x = (ox * scale) + PAD_PT * scale
        y = (oy * scale) + (descent + PAD_PT) * scale
        path = Path(verts * s + [x, y], codes)
        ax.add_patch(PathPatch(path, facecolor=color_by_index.get(i, BLACK), edgecolor="none"))
    for ox, oy, w, h in rects:
        x = ox * scale + PAD_PT * scale
        y = oy * scale + (descent + PAD_PT) * scale
        ww = w * scale
        hh = h * scale
        verts = [(x, y), (x, y + hh), (x + ww, y + hh), (x + ww, y), (x, y)]
        codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(verts, codes), facecolor=BLACK, edgecolor="none"))
    fig.savefig(out_png, dpi=DPI, transparent=True)
    plt.close(fig)
    im = Image.open(out_png).convert("RGBA")
    arr = np.array(im)
    alpha = arr[:, :, 3] > 100
    ys, xs = np.where(alpha)
    ink = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
    return im.size, ink


def main():
    manifest = {"pad_pt": PAD_PT, "dpi": DPI, "equations": {}}
    for name, (spec, font_size_pt, colors) in EXPRESSIONS.items():
        png = os.path.join(OUT_DIR, f"eq_s024_{name}.png")
        (w_px, h_px), ink = render_color_math(spec, font_size_pt, colors, png)
        sidecar = {
            "image": os.path.basename(png),
            "ink_bbox_px": ink,
            "mathtext": spec,
            "font_size_pt": font_size_pt,
            "color": BLACK,
            "width_px": w_px,
            "height_px": h_px,
            "width_in": w_px / DPI,
            "height_in": h_px / DPI,
            "pad_pt": PAD_PT,
            "baseline_frac": (font_size_pt * 0 + (PARSER.parse(spec, dpi=72, prop=font_manager.FontProperties(size=100))[1] + PAD_PT) * (font_size_pt / 100.0)) / (h_px / DPI),
        }
        with open(os.path.join(OUT_DIR, f"eq_s024_{name}.json"), "w", encoding="utf-8") as f:
            json.dump(sidecar, f, indent=2)
        manifest["equations"][name] = sidecar
        print(name, w_px, h_px, round(w_px / DPI, 3), round(h_px / DPI, 3))
    with open(os.path.join(OUT_DIR, "eq_s024_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)


if __name__ == "__main__":
    main()
