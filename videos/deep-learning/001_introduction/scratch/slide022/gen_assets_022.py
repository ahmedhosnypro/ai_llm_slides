#!/usr/bin/env python3
"""Generate all equation/delimiter PNGs for slide 022 + manifest.
STIX serif mathtext @600dpi (certified mechanism); stretched-glyph delimiters.
Every token placed later at MEASURED ink-left + baseline (see MEASUREMENTS.md)."""
import json, os, sys, importlib.util
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["mathtext.fontset"] = "stix"
import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides"
ASSETS = f"{ROOT}/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
os.makedirs(ASSETS, exist_ok=True)

spec = importlib.util.spec_from_file_location(
    "render_eq", f"{ROOT}/scripts/render_eq.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

BLACK, RED, BLUE = "#000000", "#FF0000", "#0000CC"
DPI = 600
manifest = []

from PIL import ImageDraw, ImageFont
LIB = "/usr/share/fonts/liberation/LiberationSerif-Regular.ttf"
def pilglyph(name, ch, fs, color, x_pt, baseline_pt):
    """Serif text glyph (TNR-substitute) at 600dpi, tight crop NO pad, baseline-anchored."""
    out = f"{ASSETS}/eq022_{name}.png"
    size = int(round(fs * DPI / 72))
    font = ImageFont.truetype(LIB, size)
    cw, chh = size * 2, size * 2
    img = Image.new("RGBA", (cw, chh), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    ox, oy = size // 2, size  # baseline at oy
    dr.text((ox, oy), ch, font=font, fill=(int(color[1:3],16), int(color[3:5],16), int(color[5:7],16), 255), anchor="ls")
    a = np.asarray(img)
    ink = a[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]; cols = np.where(ink.any(axis=0))[0]
    crop = a[rows[0]:rows[-1]+1, cols[0]:cols[-1]+1]
    Image.fromarray(crop).save(out)
    h_px = rows[-1] - rows[0] + 1; w_px = cols[-1] - cols[0] + 1
    baseline_frac = (oy - rows[0]) / h_px
    manifest.append({"image": f"eq022_{name}.png", "x_pt": x_pt, "baseline_pt": baseline_pt,
                     "w_in": round(w_px/DPI,5), "h_in": round(h_px/DPI,5),
                     "baseline_frac": round(baseline_frac,5), "kind": "token", "pad": False, "role": name})
    print(f"{name:10s} {w_px}x{h_px}px (serif) x={x_pt} b={baseline_pt} bf={baseline_frac:.3f}")

def tok(name, latex, fs, color, x_pt, baseline_pt):
    out = f"{ASSETS}/eq022_{name}.png"
    info = mod.render(latex, out, fs, color)
    manifest.append({"image": f"eq022_{name}.png", "x_pt": x_pt, "baseline_pt": baseline_pt,
                     "w_in": info["w_in"], "h_in": info["h_in"],
                     "baseline_frac": info["baseline_frac"], "kind": "token", "role": name})
    print(f"{name:10s} {info['w_px']}x{info['h_px']}px  w={info['w_in']} h={info['h_in']} bf={info['baseline_frac']}")
    return info

def delim(name, glyph, fs, color, x_pt, y_pt, w_pt, h_pt):
    """huge glyph -> tight crop (NO pad) -> anisotropic resize to (w_pt,h_pt) at 600dpi, recolor."""
    out = f"{ASSETS}/eq022_{name}.png"
    fig = plt.figure(figsize=(10, 6), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.4, glyph, fontsize=fs, color="#000000", ha="center", va="center")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]; cols = np.where(ink.any(axis=0))[0]
    crop = buf[rows[0]:rows[-1]+1, cols[0]:cols[-1]+1]
    im = Image.fromarray(crop)
    W, H = int(round(w_pt * DPI / 72)), int(round(h_pt * DPI / 72))
    im = im.resize((W, H), Image.LANCZOS)
    a = np.asarray(im).copy()
    a[:, :, 0], a[:, :, 1], a[:, :, 2] = (
        int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16))
    Image.fromarray(a).save(out)
    w_in, h_in = W / DPI, H / DPI
    manifest.append({"image": f"eq022_{name}.png", "x_pt": x_pt, "y_pt": y_pt,
                     "w_in": round(w_in, 5), "h_in": round(h_in, 5), "kind": "delim", "role": name})
    print(f"{name:10s} {W}x{H}px (stretched)  x={x_pt} y={y_pt}")
    plt.close(fig)

# ============ EQ1 (left box) — line baseline 171.5 ============
tok("X",   r"X", 21, BLACK, 86, 171.5)
tok("E1",  r"=", 21, BLACK, 101, 171.5)
tok("arr", r"\Rightarrow", 21, RED, 178, 170.5)
tok("X2",  r"X", 21, BLACK, 218, 171.5)          # same glyphs as X, own file for provenance
tok("E2",  r"=", 21, BLACK, 234, 171.5)
# vector entries fs21
tok("x1",  r"x_1", 21, BLACK, 121, 131)
tok("x2",  r"x_2", 21, BLACK, 121, 154.5)
tok("dt",  r"\dots", 21, BLACK, 121, 178)
tok("dt2", r"\dots", 21, BLACK, 121, 199)
tok("xn",  r"x_n", 21, BLACK, 121, 220)
pilglyph("one", "1", 19, RED, 258, 120)   # orig 7x13 wide serif — TNR-style, not STIX math
tok("x1b", r"x_1", 21, BLACK, 253, 141)
tok("x2b", r"x_2", 21, BLACK, 253, 165)
tok("dtb", r"\dots", 21, BLACK, 253, 188)
tok("dtc", r"\dots", 21, BLACK, 253, 209)
tok("xnb", r"x_n", 21, BLACK, 253, 230)
# ============ EQ2 (right box) — baseline 172.5 ============
tok("W",   r"W", 21, RED, 559, 172.5)
tok("E3",  r"=", 21, BLACK, 578, 172.5)
pilglyph("wb", "b", 20, RED, 602, 120)    # orig 10x14 — TNR-style
tok("w1",  r"w_1", 21, BLACK, 597, 141)
tok("w2",  r"w_2", 21, BLACK, 597, 165)
tok("wd1", r"\dots", 21, BLACK, 597, 189)
tok("wd2", r"\dots", 21, BLACK, 597, 209)
tok("wn",  r"w_n", 21, BLACK, 597, 230)
# ============ EQ3 (decision box) — main baseline 301 ============
tok("dp",  r"d(", 21, BLACK, 87, 301)
tok("Xr",  r"X", 21, RED, 108, 301)
tok("rp",  r")", 21, BLACK, 126, 301)
tok("e1",  r"=", 21, BLACK, 137, 301)
tok("WT",  r"W^T", 21, BLACK, 156, 301)
tok("Xm",  r"X", 21, BLACK, 192, 301)
tok("e2",  r"=", 21, BLACK, 215, 301)
tok("w1x1", r"w_1x_1", 21, BLACK, 233, 301)
tok("p1",  r"+", 21, BLACK, 272, 301)
tok("w2x2", r"w_2x_2", 21, BLACK, 285, 301)
tok("p2",  r"+", 21, BLACK, 324, 301)
tok("d5",  r".....", 21, BLACK, 337, 301)  # replaced below by PIL dots
tok("p3",  r"+", 21, BLACK, 362, 301)
tok("wnxn", r"w_nx_n", 21, BLACK, 375, 301)
tok("p4",  r"+", 21, BLACK, 414, 301)
pilglyph("cb", "b", 20, RED, 426, 301)    # orig 10x14 — TNR-style
tok("ca",  r"*", 21, RED, 438.5, 301)
tok("c1",  r"1", 21, RED, 451.5, 301)
tok("ar3", r"\Rightarrow", 21, RED, 502, 299)
# cases (BLUE incl arrows — PIL)
tok("gt",  r">", 21, BLUE, 554, 282)
tok("z1",  r"0", 21, BLUE, 565, 282)
tok("ka1", r"\Rightarrow", 14.5, BLUE, 586, 279.5)
tok("lt",  r"<", 21, BLUE, 554, 304)
tok("z2",  r"0", 21, BLUE, 565, 304)
tok("ka2", r"\Rightarrow", 14.5, BLUE, 586, 301.5)
tok("eqq", r"=", 21, BLUE, 554, 326)
tok("z3",  r"0", 21, BLUE, 566, 326)
tok("ka3", r"\Rightarrow", 14.5, BLUE, 586, 323.5)
# ============ DIAGRAM — fs 17.5 ============
tok("dx1",  r"x_1", 17.5, BLACK, 250, 364.5)
tok("dx2",  r"x_2", 17.5, BLACK, 250, 387.5)
tok("dx3",  r"x_3", 17.5, BLACK, 250, 409.5)
tok("ddt",  r"\dots", 17.5, BLACK, 250, 432)
tok("ddt2", r"\dots", 17.5, BLACK, 250, 455)
tok("dxn",  r"x_n", 17.5, BLACK, 250, 478)
tok("d1",   r"1", 17.5, RED, 252, 500)
tok("dw1",  r"w_1", 17.5, BLUE, 288, 367)
tok("dw2",  r"w_2", 17.5, BLUE, 288, 384.5)
tok("dw3",  r"w_3", 17.5, BLUE, 288, 405.5)
tok("dwn",  r"w_n", 17.5, BLUE, 288, 457)
tok("db",   r"b", 17.5, BLUE, 288, 499)
tok("sig",  r"\Sigma", 30, BLACK, 415, 429.5)

# ============ stretched delimiters ============
delim("pv1L", "(", 120, BLACK, 115, 116, 3.6, 112)
delim("pv1R", ")", 120, BLACK, 138.5, 116, 3.6, 112)
delim("pv2L", "(", 120, BLACK, 248, 104, 3.6, 132)
delim("pv2R", ")", 120, BLACK, 271, 104, 3.6, 132)
delim("pwL",  "(", 120, BLACK, 592, 103, 3.6, 132)
delim("pwR",  ")", 120, BLACK, 618, 103, 3.6, 132)
delim("brace", "{", 60, RED, 543, 267, 14, 59)

# --- five literal dots (mathtext '.....' too wide: 42pt vs measured 22pt) ---
out = f"{ASSETS}/eq022_d5dots.png"
W, H = int(24*DPI/72), int(6*DPI/72)
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
from PIL import ImageDraw
dr = ImageDraw.Draw(img)
# measured: x337..359 (22px), dot d~4px, bottoms ~301 -> dot centers y ~ baseline-2.2
d_px = int(3.8 * DPI / 72); cy = H - d_px // 2 - 1  # dot bottoms at PNG bottom -> baseline 301
x0 = int(1.0 * DPI / 72); pitch = int(4.55 * DPI / 72)
for i in range(5):
    cx = x0 + i * pitch
    dr.ellipse([cx, cy, cx + d_px, cy + d_px], fill=(0, 0, 0, 255))
img.save(out)
manifest.append({"image": "eq022_d5dots.png", "x_pt": 337, "baseline_pt": 301,
                 "w_in": round(W/DPI, 5), "h_in": round(H/DPI, 5), "baseline_frac": 1.0,
                 "kind": "token", "role": "d5dots"})
print(f"d5dots     {W}x{H}px (PIL)")
# drop the unused mathtext d5 token
manifest[:] = [m for m in manifest if not (m["role"] == "d5" and m.get("baseline_frac") != 1.0)]

with open(f"{ASSETS}/eq022_manifest.json", "w") as f:
    json.dump({"slide": 22, "assets": manifest}, f, indent=1)
print(f"\nmanifest: {len(manifest)} entries -> eq022_manifest.json")
