#!/usr/bin/env python3
"""generate_diagrams — slide_042 volume diagrams (resume worker, 2026-10-12).

Vector-traces the three 3D volume groups (input slab, filter stack, output box) from
the ground-truth frame into clean polygon fills rendered at 600 dpi (the certified
mechanism for shapes the native pptxgenjs engine cannot draw: parallelogram-face
oblique boxes with occlusions). Also renders the 11 diagram labels and the 4 box
equations as STIX mathtext PNGs with sidecars.

Outputs (banked under recreated_pptx/build/assets/):
  slide042_slab.png / slide042_slices.png / slide042_output.png   (600dpi, 1px=1/600in)
  eq42_1..4.png + .json                                           (equations, native pptx embed)
  labels/*.png + slide042_labels.json                             (label placements)
Prints: palettes, per-label calibration, equation calibration.
"""
import json
import os
import subprocess
import sys

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

ROOT = "/home/ahmed/Projects/ai_llm_slides"
VID = f"{ROOT}/videos/deep-learning/001_introduction"
ASSETS = f"{VID}/recreated_pptx/build/assets"
QADIR = f"{VID}/recreated_pptx/qa/slide042"
STIX = f"{ROOT}/.agents/skills/slide-recreation/scripts/render_eq_stix.py"
os.makedirs(ASSETS, exist_ok=True)
os.makedirs(f"{ASSETS}/labels42", exist_ok=True)

A = np.asarray(Image.open(f"{VID}/unique_slides/slide_042.jpg").convert("RGB")).astype(int)
DPI = 600.0
S = DPI / 72.0  # render px per frame px (8.3333)


def dist(img, hexcol):
    c = np.array([int(hexcol[i:i + 2], 16) for i in (0, 2, 4)])
    return np.sqrt(((img - c) ** 2).sum(-1))


def lum(img):
    return 0.299 * img[..., 0] + 0.587 * img[..., 1] + 0.114 * img[..., 2]


REGIONS = {
    "slab": (112, 192, 268, 366),
    "slices": (262, 210, 470, 325),
    "output": (545, 158, 880, 366),
}
EXCL = {
    "slab": [(167, 213, 197, 232), (117, 291, 145, 310), (151, 341, 181, 363),
             (200, 243, 212, 256), (176, 257, 205, 292)],
    "slices": [(286, 238, 306, 252), (364, 217, 384, 233), (270, 269, 288, 288),
               (293, 295, 319, 324)],
    "output": [(598, 177, 637, 195), (549, 268, 584, 285), (683, 342, 719, 359)],
}

palette_report = {}

for name, (X0, Y0, X1, Y1) in REGIONS.items():
    reg = A[Y0:Y1, X0:X1]
    H, W = reg.shape[:2]
    white = dist(reg, "FFFFFF") < 26
    excl = np.zeros((H, W), bool)
    for (a, b, c, d) in EXCL[name]:
        excl[max(0, b - Y0):max(0, d - Y0), max(0, a - X0):max(0, c - X0)] = True
    cand = ~white & ~excl
    pix = reg[cand]

    # ---- palette: quantized modals, merged ----
    q = (pix // 12).astype(int)
    keys, counts = np.unique(q, axis=0, return_counts=True)
    order = np.argsort(-counts)
    centers = []
    for i in order:
        c = keys[i] * 12 + 6
        if counts[i] < 12:
            break
        if all(np.sqrt(((c - np.array(m)) ** 2).sum()) > 22 for m in centers):
            centers.append(list(c))
        if len(centers) >= 10:
            break
    centers_arr = np.array(centers)
    # classify + refine centers (2 rounds)
    lab = np.full((H, W), -1, int)
    d = np.stack([dist(reg, None) if False else np.sqrt(((reg - centers_arr[k]) ** 2).sum(-1)) for k in range(len(centers_arr))])
    lab[cand] = np.argmin(d[:, cand], axis=0)
    for _ in range(2):
        for k in range(len(centers_arr)):
            m = lab == k
            if m.sum() > 8:
                centers_arr[k] = reg[m].mean(0).round().astype(int)
        d = np.stack([np.sqrt(((reg - centers_arr[k]) ** 2).sum(-1)) for k in range(len(centers_arr))])
        lab[cand] = np.argmin(d[:, cand], axis=0)
    sizes = [(lab == k).sum() for k in range(len(centers_arr))]
    keep = [k for k in range(len(centers_arr)) if sizes[k] >= 25]
    palette_report[name] = [
        ("#%02X%02X%02X" % tuple(centers_arr[k]), int(sizes[k]),
         round(float(lum(centers_arr[k][None, None])[0, 0]), 1)) for k in keep]
    # merge tiny clusters into nearest kept center by color
    for k in range(len(centers_arr)):
        if sizes[k] < 25:
            near = min(keep, key=lambda j: np.sqrt(((centers_arr[k] - centers_arr[j]) ** 2).sum()))
            lab[lab == k] = near
    keep_centers = {k: centers_arr[k] for k in keep}

    # ---- trace each class ----
    L = lum(reg)
    dark_last, light_first = [], []
    for k in keep:
        (dark_last if lum(keep_centers[k]) < 105 else light_first).append(k)
    light_first.sort(key=lambda k: -sizes[k])
    dark_last.sort(key=lambda k: -sizes[k])

    fig = plt.figure(figsize=(W / 72.0, H / 72.0), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(H, 0)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    def polys_of(k):
        mask = ((lab == k).astype(np.uint8)) * 255
        cs, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        out = []
        for c in cs:
            if cv2.contourArea(c) < 16:
                continue
            ap = cv2.approxPolyDP(c, 1.3, True)
            out.append(ap[:, 0, :].astype(float))
        return out

    for k in light_first + dark_last:
        col = tuple(int(v) for v in keep_centers[k])
        for pts in polys_of(k):
            ax.add_patch(plt.Polygon(pts, closed=True, facecolor=np.array(col) / 255.0, edgecolor="none", linewidth=0))

    # ---- stride marker (slab only) ----
    if name == "slab":
        for (dx, dy) in [(205.6, 249), (193.5, 259), (179.8, 267)]:
            ax.add_patch(plt.Circle((dx, dy), 2.1, color="black"))
        ax.annotate("", xy=(198.2, 264.8), xytext=(179.6, 278.6),
                    arrowprops=dict(arrowstyle="<->", color="black", lw=1.1, shrinkA=0, shrinkB=0))
        ax.plot([178.7, 178.7], [274.8, 282.2], color="black", lw=1.1)
        ax.plot([198.6, 198.6], [259.6, 267.2], color="black", lw=1.1)

    fig.savefig(f"{ASSETS}/slide042_{name}.png", dpi=DPI, facecolor="white")
    plt.close(fig)
    print(f"[{name}] region x{X0}..{X1} y{Y0}..{Y1}  palette:")
    for c, n, l in palette_report[name]:
        print(f"    {c}  n={n}  lum={l}")

# ---- diagram labels: mathtext, uniform size calibrated to measured ink widths ----
LABELS = {
    "w_in":  ("w_{in}",  170, 216, 25),
    "h_in":  ("h_{in}",  120, 294, 23),
    "d_in":  ("d_{in}",  154, 344, 25),
    "w_f":   ("w_{f}",   288, 240, 16),
    "n_f":   ("n_{f}",   367, 220, 15),
    "h_f":   ("h_{f}",   273, 272, 13),
    "d_f":   ("d_{f}",   296, 301, 21),
    "w_out": ("w_{out}", 601, 180, 34),
    "h_out": ("h_{out}", 552, 271, 30),
    "d_out": ("d_{out}", 686, 345, 31),
}

def render_label(tex, size, out):
    r = subprocess.run([sys.executable, STIX, tex, out, str(size), "#000000"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr)
    return json.loads(r.stdout)

# calibration round at 20pt
cal = {}
for k, (tex, x, y, tw) in LABELS.items():
    sc = render_label(tex, 20.0, f"{ASSETS}/labels42/{k}_c.png")
    cal[k] = 20.0 * tw * S / sc["w_px"]
size = round(float(np.median(list(cal.values()))), 2)
print(f"[labels] per-label size from width: " +
      ", ".join(f"{k}:{v:.1f}" for k, v in cal.items()) + f"  -> uniform {size}pt")

placements = {}
for k, (tex, x, y, tw) in LABELS.items():
    out = f"{ASSETS}/labels42/{k}.png"
    sc = render_label(tex, size, out)
    im = Image.open(out)
    # paste centered on measured ink-left/top with measured width anchor
    placements[k] = {"png": out, "ink_left": x, "ink_top": y, "w_px": sc["w_px"], "h_px": sc["h_px"],
                     "target_w": tw, "w_err": round(sc["w_px"] - tw * S, 1)}
    print(f"[label {k}] size {size} target w{tw} ({tw*S:.0f}px600) -> rendered w{sc['w_px']} h{sc['h_px']} (err {sc['w_px']-tw*S:+.0f})")

# paste labels into the region PNGs
LABEL_REGION = {"w_in": "slab", "h_in": "slab", "d_in": "slab", "s_lab": "slab",
                "w_f": "slices", "n_f": "slices", "h_f": "slices", "d_f": "slices",
                "w_out": "output", "h_out": "output", "d_out": "output"}
# 's' label (stride) — small, calibrated to w9
sc_s = render_label('s', 20.0, f"{ASSETS}/labels42/s_c.png")
s_size = round(20.0 * 9.0 * S / sc_s["w_px"], 2)
sc_s = render_label('s', s_size, f"{ASSETS}/labels42/s_lab.png")
placements["s_lab"] = {"png": f"{ASSETS}/labels42/s_lab.png", "ink_left": 188, "ink_top": 281,
                       "w_px": sc_s["w_px"], "h_px": sc_s["h_px"], "target_w": 9, "w_err": round(sc_s["w_px"] - 9 * S, 1)}
print(f"[label s_lab] size {s_size} -> w{sc_s['w_px']} h{sc_s['h_px']} (target {9*S:.0f})")

for k, p in placements.items():
    rname = LABEL_REGION[k]
    X0, Y0, X1, Y1 = REGIONS[rname]
    canvas = Image.open(f"{ASSETS}/slide042_{rname}.png").convert("RGBA")
    lab_im = Image.open(p["png"]).convert("RGBA")
    px_x = (p["ink_left"] - X0) * S
    px_y = (p["ink_top"] - Y0) * S
    canvas.alpha_composite(lab_im, (int(round(px_x)), int(round(px_y))))
    canvas.convert("RGB").save(f"{ASSETS}/slide042_{rname}.png")
    print(f"[paste {k}] into {rname} at frame ({p['ink_left']},{p['ink_top']})")

json.dump({"regions": REGIONS, "labels": placements, "label_size_pt": size, "s_size_pt": s_size,
           "palette": palette_report},
          open(f"{ASSETS}/slide042_diagram_constants.json", "w"), indent=1)

# ---- equations (native pptx embeds; calibrated to measured ink boxes) ----
EQS = {
    1: (r'h_{out}=\dfrac{h_{in}-h_f}{s}+1', 343, 341, 152),
    2: (r'w_{out}=\dfrac{w_{in}-w_f}{s}+1', 341, 378, 160),
    3: (r'd_{out}=n_f', 343, 417, 72),
    4: (r'd_f=d_{in}', 359, 440, 65),
}
eq_out = {}
for n, (tex, x, y, tw) in EQS.items():
    sc20 = render_label(tex, 14.0, f"{ASSETS}/eq42_{n}_c.png")
    fs = round(14.0 * tw * S / sc20["w_px"], 2)
    sc = render_label(tex, fs, f"{ASSETS}/eq42_{n}.png")
    json.dump(sc, open(f"{ASSETS}/eq42_{n}.json", "w"))
    eq_out[n] = {"png": f"{ASSETS}/eq42_{n}.png", "mathtext": tex, "ink_left": x, "ink_top": y,
                 "font_size_pt": fs, "w_px": sc["w_px"], "h_px": sc["h_px"],
                 "target_w": tw, "w_err": round(sc["w_px"] - tw * S, 1)}
    print(f"[eq {n}] fs {fs} -> w{sc['w_px']} h{sc['h_px']} (target w{tw}, err {sc['w_px']-tw:+d})")
json.dump(eq_out, open(f"{ASSETS}/slide042_eq_constants.json", "w"), indent=1)
print("DONE")
