#!/usr/bin/env python3
"""slide_022 asset generation — composed-equation pieces + stretched-glyph parens.

Mechanism (certified slide_031 + equations-mathtext-png + delimiters-stretched-glyph
patterns): matplotlib mathtext (STIX serif, matching the deck's serif math look) ->
600dpi tight transparent PNG + sidecar; each piece is font-size-solved (bisection)
against the PIL-measured ink target from the ground-truth frame, then placed in the
build by ink-anchor + math-baseline law (y_top = baseline_px - baseline_frac*h_px).
Parens: delimiters-stretched-glyph pattern (huge '(' glyph, tight-crop, anisotropic
hairline resize, recolor) — spans sized to the measured bracket ink extents.

All measurements in frame px (960x540, 1px = 1pt) from scratch_022/forensics*.
"""
import json
import os
import subprocess
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

DPI = 600
PAD_PX = 8
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
os.makedirs(OUT, exist_ok=True)

matplotlib.rcParams["mathtext.fontset"] = "stix"
BLACK = "#000000"
RED = "#C00000"
NAVY = "#0000CC"


def render_tex(tex, out, fontsize, color):
    """Render one mathtext piece; return sidecar dict (render_eq.py contract)."""
    fig = plt.figure(figsize=(12, 5), dpi=DPI)
    fig.patch.set_alpha(0.0)
    eq = fig.text(0.5, 0.5, f"${tex}$", fontsize=fontsize, color=color,
                  ha="center", va="baseline")
    probe = fig.text(0.15, 0.5, "x", fontsize=fontsize, color=color,
                     ha="center", va="baseline")
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    pb = probe.get_window_extent(renderer=renderer)
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    px0, px1 = max(int(pb.x0) - 2, 0), int(pb.x1) + 2
    baseline_row = int(np.where(ink[:, px0:px1].any(axis=1))[0][-1])
    ink[:, :px1 + 20] = False
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if len(rows) == 0:
        plt.close(fig)
        raise SystemExit(f"no ink for {tex!r}")
    y0, y1 = max(rows[0] - PAD_PX, 0), min(rows[-1] + PAD_PX, buf.shape[0])
    x0, x1 = max(cols[0] - PAD_PX, 0), min(cols[-1] + PAD_PX, buf.shape[1])
    Image.fromarray(buf[y0:y1, x0:x1]).save(out)
    h = y1 - y0
    info = {"path": os.path.basename(out), "w_px": int(x1 - x0), "h_px": int(h),
            "w_in": round(float(x1 - x0) / DPI, 5), "h_in": round(float(h) / DPI, 5),
            "baseline_px": int(baseline_row - y0),
            "baseline_frac": round(float(baseline_row - y0) / float(h), 5),
            "dpi": DPI, "fontsize_pt": fontsize, "color": color.lstrip("#"),
            "mathtext": tex}
    plt.close(fig)
    return info


def solve_fs(tex, color, target_w, target_h, lo=6.0, hi=60.0, iters=16, name="", solve_on_h=False):
    """Bisect fontsize until ink ~= target frame-px (1px=1pt -> 600dpi px = *8.333)."""
    tw = (target_h if solve_on_h else target_w) * DPI / 72.0
    best = None
    for _ in range(iters):
        mid = (lo + hi) / 2
        out = os.path.join(OUT, f"_probe_{name}.png")
        info = render_tex(tex, out, round(mid, 2), color)
        best = (mid, info)
        dim = info["h_px"] if solve_on_h else info["w_px"]
        if dim < tw:
            lo = mid
        else:
            hi = mid
        if abs(dim - tw) <= 8:
            break
    os.remove(os.path.join(OUT, f"_probe_{name}.png"))
    mid, info = best
    # re-render at the chosen size under the final name
    return mid, info


ASSETS = []


def add(name, tex, color, target_w, target_h, anchor, baseline, note="", fs_override=None, solve_on_h=False):
    if fs_override:
        fs = fs_override
    else:
        fs, _ = solve_fs(tex, color, target_w, target_h, name=name, solve_on_h=solve_on_h)
    out = os.path.join(OUT, f"eq_022_{name}.png")
    info = render_tex(tex, out, round(fs, 2), color)
    info["anchor"] = anchor          # {"mode": "left"|"center", "x_px": ...}
    info["baseline_px"] = baseline   # frame-px baseline for placement law
    info["target_w"] = target_w
    info["target_h"] = target_h
    info["note"] = note
    ASSETS.append(info)
    print(f"{name}: fs={fs:.2f} ink {info['w_px']}x{info['h_px']} (target {target_w}x{target_h}) "
          f"bl_frac={info['baseline_frac']}")
    return info


# ---- augmented-vector box ----
# X̲ =  : ink x88..117 (w 30), X cap y159..173 -> baseline 171.5
add("augX1", r"\underline{\mathbf{X}}\ =", BLACK, 30, 15, {"mode": "left", "x": 88}, 171.5)
# vector-1 entries centered ~129.5; baselines [130, 153, 176, 197.5, 220]
FS_X = add("v1_x1", r"x_1", BLACK, 15, 12, {"mode": "center", "x": 129.5}, 130) or None
add("v1_x2", r"x_2", BLACK, 15, 12, {"mode": "center", "x": 129.5}, 153, fs_override=FS_X["fontsize_pt"])
add("v1_d1", r"\cdots", BLACK, 14, 4, {"mode": "center", "x": 129.5}, 176)
add("v1_d2", r"\cdots", BLACK, 14, 4, {"mode": "center", "x": 129.5}, 197.5)
add("v1_xn", r"x_n", BLACK, 15, 12, {"mode": "center", "x": 129.5}, 220, fs_override=FS_X["fontsize_pt"])
# red arrow between vectors: x180..193 (w 14), y162..169 center-y 165.5
add("aug_arr", r"\Rightarrow", RED, 14, 10, {"mode": "center", "x": 186.5}, 168.5)
# X̲ = (2nd): ink x222..250 (w 29), baseline 171.5
add("augX2", r"\underline{\mathbf{X}}\ =", BLACK, 29, 15, {"mode": "left", "x": 222}, 171.5)
# vector-2 entries centered ~268.5; baselines [118.5, 141, 165.5, 187.5, 208, 229.5]
add("v2_1", r"1", RED, 8, 12, {"mode": "center", "x": 260.5}, 118.5)
add("v2_x1", r"x_1", BLACK, 15, 12, {"mode": "center", "x": 260.5}, 141, fs_override=FS_X["fontsize_pt"])
add("v2_x2", r"x_2", BLACK, 15, 12, {"mode": "center", "x": 260.5}, 165.5, fs_override=FS_X["fontsize_pt"])
add("v2_d1", r"\cdots", BLACK, 14, 4, {"mode": "center", "x": 260.5}, 187.5)
add("v2_d2", r"\cdots", BLACK, 14, 4, {"mode": "center", "x": 260.5}, 208)
add("v2_xn", r"x_n", BLACK, 15, 12, {"mode": "center", "x": 260.5}, 229.5, fs_override=FS_X["fontsize_pt"])

# ---- weights box ----
# W̲ (RED): ink x561..578 (w 18), baseline 171.5
add("wtsW", r"\underline{\mathbf{W}}", RED, 18, 15, {"mode": "left", "x": 561}, 171.5)
# '=' black: x581..597 (w 16), axis y163..169 -> baseline ~169.5
add("wtsEq", r"=", BLACK, 15, 7, {"mode": "center", "x": 589}, 169.5)
# vector entries centered ~607.5; baselines [117.5, 140.5, 165.5, 187.5, 208, 229.5]
add("wv_b", r"b", RED, 12, 14, {"mode": "center", "x": 607.5}, 117.5)
FS_W = add("wv_w1", r"w_1", BLACK, 13, 12, {"mode": "center", "x": 607.5}, 140.5) or None
add("wv_w2", r"w_2", BLACK, 13, 12, {"mode": "center", "x": 607.5}, 165.5, fs_override=FS_W["fontsize_pt"])
add("wv_d1", r"\cdots", BLACK, 13, 4, {"mode": "center", "x": 607.5}, 187.5)
add("wv_d2", r"\cdots", BLACK, 13, 4, {"mode": "center", "x": 607.5}, 208)
add("wv_wn", r"w_n", BLACK, 13, 12, {"mode": "center", "x": 607.5}, 229.5, fs_override=FS_W["fontsize_pt"])

# ---- decision box (per-token pinning; measured clusters, baseline 299) ----
add("dec_d", r"d(", BLACK, 16, 15, {"mode": "left", "x": 87}, 299)
add("dec_X", r"\mathbf{X}", RED, 13, 14.5, {"mode": "left", "x": 110}, 299.5, solve_on_h=True)
add("dec_rp", r")", BLACK, 5, 18, {"mode": "left", "x": 123}, 299, solve_on_h=True)
add("dec_e1", r"=", BLACK, 9, 6, {"mode": "left", "x": 138}, 299)
add("dec_WT", r"\underline{\mathbf{W}}^T", BLACK, 26, 21, {"mode": "left", "x": 156}, 299)
add("dec_X2", r"\underline{\mathbf{X}}", BLACK, 14, 16, {"mode": "left", "x": 193}, 299)
add("dec_e2", r"=", BLACK, 9, 6, {"mode": "left", "x": 216}, 299)
add("dec_w1", r"w_1x_1", BLACK, 29, 14, {"mode": "left", "x": 233}, 299)
add("dec_p1", r"+", BLACK, 10, 9, {"mode": "left", "x": 272}, 299)
add("dec_w2", r"w_2x_2", BLACK, 29, 14, {"mode": "left", "x": 285}, 299)
add("dec_p2", r"+", BLACK, 10, 9, {"mode": "left", "x": 324}, 299)
add("dec_dots", r".....", BLACK, 22, 3, {"mode": "left", "x": 337}, 299.5)
add("dec_p3", r"+", BLACK, 10, 9, {"mode": "left", "x": 362}, 299)
add("dec_wn", r"w_nx_n", BLACK, 29, 14, {"mode": "left", "x": 375}, 299)
add("dec_p4", r"+", BLACK, 10, 9, {"mode": "left", "x": 414}, 299)
add("dec_b1", r"b*1", RED, 29, 13, {"mode": "left", "x": 427}, 299)
add("dec_arr", r"\Longrightarrow", RED, 22, 12, {"mode": "left", "x": 500}, 297.5)
# three navy case lines: x555.., baselines ~281 / 303 / 325
add("case1", r">0\ \Rightarrow\ \mathrm{Class\ I}", NAVY, 116, 15, {"mode": "left", "x": 555}, 281)
add("case2", r"<0\ \Rightarrow\ \mathrm{Class\ II}", NAVY, 116, 15, {"mode": "left", "x": 555}, 303)
add("case3", r"=0\ \Rightarrow\ \mathrm{Undefined\ Class}", NAVY, 185, 15, {"mode": "left", "x": 555}, 325)

# ---- diagram ----
# Sigma: ink x422..438 (w 16), y411..430 (h 19); circle center (432.5,420.5)
add("sigma", r"\Sigma", BLACK, 16, 19, {"mode": "center", "x": 429.5}, 430)
# input labels (black) x252..264; red 1; rows y-bands (357,366)(379,388)(402,410)(430,431)(452,454)(470,479)(490,498)
add("d_x1", r"x_1", BLACK, 12, 10, {"mode": "left", "x": 252}, 363)
add("d_x2", r"x_2", BLACK, 12, 10, {"mode": "left", "x": 252}, 385)
add("d_x3", r"x_3", BLACK, 12, 10, {"mode": "left", "x": 252}, 407)
add("d_d1", r"\cdots", BLACK, 12, 3, {"mode": "center", "x": 258}, 431)
add("d_d2", r"\cdots", BLACK, 12, 3, {"mode": "center", "x": 258}, 453)
add("d_xn", r"x_n", BLACK, 12, 10, {"mode": "left", "x": 252}, 476)
add("d_1", r"1", RED, 7, 9, {"mode": "left", "x": 255}, 497.5)
# weight labels (navy) x289..305; rows (358,368)(376,385)(398,407)(449,459)(488,498)
FS_DW = add("d_w1", r"w_1", NAVY, 16, 10, {"mode": "left", "x": 289}, 365.5) or None
add("d_w2", r"w_2", NAVY, 16, 10, {"mode": "left", "x": 289}, 383, fs_override=FS_DW["fontsize_pt"])
add("d_w3", r"w_3", NAVY, 16, 10, {"mode": "left", "x": 289}, 404.5, fs_override=FS_DW["fontsize_pt"])
add("d_wn", r"w_n", NAVY, 16, 10, {"mode": "left", "x": 289}, 456.5, fs_override=FS_DW["fontsize_pt"])
add("d_b", r"b", NAVY, 10, 10, {"mode": "left", "x": 292}, 495.5)

# ---- stretched-glyph parens (delimiters-stretched-glyph pattern) ----
GEN = "/home/ahmed/Projects/ai_llm_slides/.agents/skills/slide-recreation/patterns/delimiters-stretched-glyph/gen_delimiter.py"
PARENS = [
    # name, glyph, span_pt (ink extent), stroke_px@600dpi, color, x_px (stroke left), y0_px, y1_px
    ("par_v1L", "(", 115, 16, "000000", 117.0, 112, 227),
    ("par_v1R", ")", 115, 16, "000000", 139.5, 112, 227),
    ("par_v2L", "(", 136, 16, "000000", 248.5, 102, 238),
    ("par_v2R", ")", 136, 16, "000000", 271.5, 102, 238),
    ("par_wL", "(", 139, 16, "000000", 597.0, 100, 239),
    ("par_wR", ")", 139, 16, "000000", 617.0, 100, 239),
    # case-group delimiters: hairline curved parens, washed lavender-blue
    # (judge dec-crop MAJOR: the original encloses the 3-case group on BOTH sides;
    #  spine reads x543..545 / x748..750, lum ~176-183 over the yellow fill)
    ("par_caseL", "(", 66, 9, "A9A5D0", 542.8, 261, 327),
    ("par_caseR", ")", 66, 9, "A9A5D0", 747.8, 261, 327),
]
parens_meta = []
for name, glyph, span, stroke, col, x_px, y0, y1 in PARENS:
    out = os.path.join(OUT, f"eq_022_{name}.png")
    r = subprocess.run([sys.executable, GEN, glyph, str(span), str(stroke), col, out],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"gen_delimiter failed for {name}: {r.stderr}")
    img = Image.open(out)
    w_px, h_px = img.size
    parens_meta.append({"name": name, "image": f"eq_022_{name}.png",
                        "w_px": w_px, "h_px": h_px,
                        "w_in": round(w_px / DPI, 5), "h_in": round(h_px / DPI, 5),
                        "x_px": x_px, "y0_px": y0, "y1_px": y1, "glyph": glyph})
    print(f"{name}: {w_px}x{h_px}px span {span}pt at x={x_px} y{y0}..{y1}")

manifest = {"slide": 22, "video": "deep-learning/001_introduction",
            "dpi": DPI, "equations": ASSETS, "parens": parens_meta,
            "text": {
                "title": {"text": "Visualization of Single Perceptron", "font": "Arial",
                          "bold": True, "size": 30.4, "color": "C00000",
                          "ink_left": 228, "ink_right": 718, "baseline": 81.6},
                "aug_label": {"text": "Ugmented Vector", "font": "Arial", "italic": True,
                              "size": 15.5, "color": "000080", "ink_left": 300,
                              "baseline": 172, "underline": [300, 405, 172.5]},
                "wts_label": {"text": "Model Weights", "font": "Arial", "italic": True,
                              "size": 15.5, "color": "000080", "ink_left": 670,
                              "baseline": 172, "underline": [670, 762, 172.5]},
                "op": {"text": "O/P", "font": "Arial", "bold": True, "size": 17,
                       "color": "000000", "ink_left": 575, "baseline": 428},
                "callout_l1": {"text": "Binary Classification", "font": "Arial",
                               "bold": True, "italic": True, "color": "604820",
                               "ink_left": 649, "baseline": 420, "size": 15.0},
                "callout_l2": {"text": "(2 Classes)", "font": "Arial", "bold": True,
                               "italic": True, "color": "604820", "ink_left": 684,
                               "baseline": 436, "size": 15.0},
            }}
mpath = os.path.join(OUT, "eq_022_manifest.json")
with open(mpath, "w") as f:
    json.dump(manifest, f, indent=1)
print("manifest ->", mpath)
