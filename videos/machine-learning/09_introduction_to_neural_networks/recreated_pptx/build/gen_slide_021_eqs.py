#!/usr/bin/env python3
"""Render slide 021's four color-coded formulas as transparent 600 dpi PNGs.

Coordinates are original-frame pixels (960x540, 1 px = 1 pt). Each formula is
composed from measured text tokens, with a stretched brace and explicit super/
subscript tokens for the two-dimensional math layout.
"""
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import PathPatch, Ellipse
from matplotlib.textpath import TextPath
from matplotlib.transforms import Affine2D
import numpy as np
from PIL import Image

BUILD = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
DPI = 600
FONT = "DejaVu Serif"
RED = "#D00000"
BLUE = "#0000CC"
BLACK = "#000000"
GREEN = "#008000"


def tok(text, color, left, top, width, size=18, weight="normal", style="normal"):
    return dict(text=text, color=color, left=left, top=top, width=width,
                size=size, weight=weight, style=style)


def draw_token(ax, t):
    prop = FontProperties(family=FONT, weight=t["weight"], style=t["style"], size=t["size"])
    path = TextPath((0, 0), t["text"], prop=prop)
    bb = path.get_extents()
    if bb.width <= 0:
        return
    sx = t["width"] / bb.width
    baseline = t["top"] + bb.y1
    trans = Affine2D.from_values(sx, 0.0, 0.0, -1.0,
                                 t["left"] - sx * bb.x0, baseline)
    ax.add_patch(PathPatch(path, facecolor=t["color"], edgecolor="none",
                           transform=trans + ax.transData))


def draw_brace(ax, x0, x1, y0, y1, color=RED):
    prop = FontProperties(family=FONT, weight="normal", size=40)
    path = TextPath((0, 0), "{", prop=prop)
    bb = path.get_extents()
    sx = (x1 - x0) / bb.width
    sy = (y1 - y0) / bb.height
    trans = Affine2D.from_values(sx, 0.0, 0.0, -sy,
                                 x0 - sx * bb.x0, y1 + sy * bb.y0)
    ax.add_patch(PathPatch(path, facecolor=color, edgecolor="none",
                           transform=trans + ax.transData))


def render(name, region, tokens, brace=None, dot=None):
    x0, y0, x1, y1 = region
    w, h = x1 - x0, y1 - y0
    dev_w, dev_h = int(round(w * DPI / 72)), int(round(h * DPI / 72))
    fig = plt.figure(figsize=(dev_w / DPI, dev_h / DPI), dpi=DPI)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0, x1)
    ax.set_ylim(y1, y0)
    ax.axis("off")
    for t in tokens:
        draw_token(ax, t)
    if brace:
        draw_brace(ax, *brace)
    if dot:
        dx0, dy0, dx1, dy1, color = dot
        ax.add_patch(Ellipse(((dx0 + dx1) / 2, (dy0 + dy1) / 2),
                             dx1 - dx0, dy1 - dy0, facecolor=color, edgecolor="none"))
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    plt.close(fig)
    path = os.path.join(BUILD, name + ".png")
    Image.fromarray(buf).save(path)
    return {"path": path, "region_px": list(region), "dev_w_px": dev_w,
            "dev_h_px": dev_h, "w_in": dev_w / DPI, "h_in": dev_h / DPI, "dpi": DPI}


def fx(x, y, color=BLACK):
    return [tok("F", color, x, y, 11, style="italic"),
            tok("(", color, x + 12, y, 5),
            tok("x", color, x + 19, y + 3, 9, style="italic"),
            tok(")", color, x + 30, y, 5),
            tok("=", color, x + 40, y + 3, 11)]


def conditions(x, y, color, second=False):
    return [tok("for", color, x, y, 20, size=14, weight="bold", style="italic"),
            tok("x", color, x + 23, y + 3, 8, size=14, weight="bold", style="italic"),
            tok("≥" if second else "<", color, x + 33, y + 2, 10, size=14, weight="bold", style="italic"),
            tok("0", color, x + 45, y, 8, size=14, weight="bold", style="italic")]


def main():
    manifest = {}
    tl = fx(123, 64) + [
        tok("Re", RED, 174, 64, 18, weight="bold"),
        tok("ctified Linear Unit", RED, 193, 64, 105),
        tok("=", BLACK, 303, 67, 11),
        tok("0", RED, 337, 64, 9),
        tok("x", RED, 337, 82, 9, style="italic"),
    ] + conditions(359, 64, BLACK) + conditions(359, 82, GREEN, True)
    manifest["eq_021_relu"] = render("eq_021_relu", (113, 54, 414, 105), tl,
                                      brace=(329, 334, 58, 99))

    tr = fx(554, 64) + [
        tok("P", BLUE, 603, 64, 9, weight="bold"),
        tok("arametric ReLU", RED, 615, 64, 103),
        tok("=", BLACK, 720, 67, 11),
        tok("x", RED, 743, 82, 9, style="italic"),
    ] + conditions(774, 64, BLACK) + conditions(774, 82, GREEN, True)
    manifest["eq_021_prelu"] = render("eq_021_prelu", (550, 54, 851, 105), tr,
                                       brace=(733, 738, 58, 99),
                                       dot=(742, 65, 756, 79, RED))

    bl = fx(100, 302) + [
        tok("E", BLUE, 148, 302, 9, weight="bold"),
        tok("xponential LU", RED, 160, 302, 91),
        tok("=", BLACK, 253, 305, 11),
        tok("α", BLUE, 275, 302, 10, style="italic"),
        tok("(", BLUE, 288, 302, 5),
        tok("e", BLUE, 295, 302, 8, style="italic"),
        tok("x", BLUE, 304, 296, 6, size=12, style="italic"),
        tok("−", BLUE, 312, 305, 8),
        tok("1", BLUE, 321, 302, 8),
        tok(")", BLUE, 330, 302, 5),
        tok("x", RED, 275, 321, 9, style="italic"),
    ] + conditions(343, 302, BLACK) + conditions(343, 321, GREEN, True)
    manifest["eq_021_elu"] = render("eq_021_elu", (94, 283, 431, 341), bl,
                                     brace=(266, 271, 288, 335))

    br = fx(607, 302) + [
        tok("SoftPlus", RED, 654, 302, 56, weight="bold"),
        tok("=", BLACK, 716, 305, 11),
        tok("log", BLACK, 725, 302, 18),
        tok("e", BLACK, 745, 316, 6, size=12, style="italic"),
        tok("(", RED, 758, 302, 5),
        tok("1", RED, 765, 302, 8),
        tok("+", RED, 775, 305, 8),
        tok("e", RED, 785, 302, 8, style="italic"),
        tok("x", RED, 794, 296, 6, size=12, style="italic"),
        tok(")", RED, 801, 302, 5),
    ]
    manifest["eq_021_softplus"] = render("eq_021_softplus", (584, 286, 816, 339), br)

    with open(os.path.join(BUILD, "eq_021_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
