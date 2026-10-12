#!/usr/bin/env python3
"""measure_original4 — slide_042 exact geometry forensics (resume worker, 2026-10-12).

Passes (all on unique_slides/slide_042.jpg, 960x540, 1px = 1pt):
  1. slab region ASCII class map + per-row runs for front/light classes + dark outline modal
  2. filter-slices region ASCII map + per-class core modals + per-row runs
  3. output box region ASCII map + per-row runs for front/top/side + edge dark modal
  4. '=' sign region ink map (fit two bars)
  5. stride dots + 's' label clusters on the slab face
  6. diagram label windows: ink bbox + dark modal each
  7. legend: per-line blue/dark bboxes + blue core color + word-width fingerprint data
  8. title dark modal; equation box border rect + color; eq ink left edges re-check
"""
import numpy as np
from PIL import Image

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_042.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
H, W = A.shape[:2]
print(f"frame {W}x{H}")

def lum(a):
    return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]

def modal(pix, label, n=6):
    if len(pix) == 0:
        print(f"{label}: EMPTY")
        return
    vals, counts = np.unique(pix.reshape(-1, 3), axis=0, return_counts=True)
    order = np.argsort(-counts)[:n]
    print(label + ": " + ", ".join('#%02X%02X%02X(%d)' % (tuple(vals[i])) if False else '#%02X%02X%02X(%d)' % (vals[i][0], vals[i][1], vals[i][2], counts[i]) for i in order))

def dark_modal(x0, x1, y0, y1, label, thr=130):
    reg = A[y0:y1, x0:x1]
    L = lum(reg)
    pix = reg[L < thr]
    modal(pix, label, 5)

def dist(a, hexcol):
    c = np.array([int(hexcol[i:i+2], 16) for i in (0, 2, 4)])
    return np.sqrt(((a - c) ** 2).sum(-1))

CL = {  # class -> (hex, tol)
    "F": ("AF6712", 42), "L": ("D98117", 42), "T": ("F2D8B5", 14), "S": ("E0C3A1", 14),
    "A": ("EFCEA3", 14), "C": ("81DDF4", 40), "G": ("51A75E", 45), "R": ("D55F6B", 45),
    "Y": ("E2EB7E", 45), "P": ("BCA3CB", 40),
}

def classify(region):
    L = lum(region)
    out = np.full(region.shape[:2], ".", dtype="<U1")
    out[L > 232] = " "
    out[L < 115] = "K"
    for ch in "FLSCGRYPTA":  # colored classes after K
        if ch in CL:
            hexc, tol = CL[ch]
            m = (dist(region, hexc) < tol) & (out == ".")
            out[m] = ch
    return out

def ascii_map(x0, x1, y0, y1, cell, classes, label):
    print(f"==== {label} ASCII (cell={cell}px, x{x0}..{x1} y{y0}..{y1}) ====")
    print("     " + "".join(str((x0 + i * cell) // 100 % 10) if (x0 + i * cell) % (cell * 5) < cell else " " for i in range((x1 - x0) // cell)))
    reg = A[y0:y1, x0:x1]
    cls = classify(reg)
    for cy in range(0, reg.shape[0] - cell + 1, cell):
        row = []
        for cx in range(0, reg.shape[1] - cell + 1, cell):
            blk = cls[cy:cy + cell, cx:cx + cell].ravel()
            counts = {c: (blk == c).sum() for c in set(blk)}
            if counts.get("K", 0) >= 0.4 * len(blk) and counts["K"] >= 1:
                row.append("K")
            else:
                best = max(counts.items(), key=lambda kv: (kv[1], kv[0] in classes))
                row.append(best[0] if best[1] >= 1 else "?")
        print(f"y{y0+cy:3d} " + "".join(row))

def row_runs(x0, x1, y0, y1, ch, label, step=1):
    print(f"---- {label}: per-row [min,max] for class {ch} ----")
    reg = A[y0:y1, x0:x1]
    cls = classify(reg)
    for ry in range(0, reg.shape[0], step):
        xs = np.where(cls[ry] == ch)[0]
        if len(xs):
            print(f"  y{y0+ry}: x {x0+xs.min()}..{x0+xs.max()} n={len(xs)}")

# ---------- 1. slab ----------
ascii_map(145, 268, 190, 352, 2, "FL", "SLAB")
row_runs(145, 268, 192, 352, "F", "slab front")
row_runs(145, 268, 192, 352, "L", "slab light")
dark_modal(145, 268, 192, 352, "slab dark outline modal (excl labels approx)", 115)

# ---------- 2. slices ----------
ascii_map(290, 470, 228, 312, 2, "CGRYP", "SLICES")
for ch in "CGRYP":
    row_runs(290, 470, 230, 312, ch, f"slice {ch}")
# core modals: only saturated pixels
reg = A[228:312, 290:470].reshape(-1, 3)
mx = reg.max(1); mn = reg.min(1)
sat = reg[(mx - mn) > 45]
vals, counts = np.unique(sat, axis=0, return_counts=True)
order = np.argsort(-counts)[:18]
print("slices saturated modals: " + ", ".join('#%02X%02X%02X(%d)' % (vals[i][0], vals[i][1], vals[i][2], counts[i]) for i in order))
dark_modal(290, 470, 230, 312, "slices outline dark modal", 100)

# ---------- 3. output box ----------
ascii_map(580, 895, 120, 350, 3, "ATS", "OUTPUT")
row_runs(580, 895, 122, 350, "A", "output front", 2)
row_runs(580, 895, 122, 350, "T", "output top", 2)
row_runs(580, 895, 122, 350, "S", "output side", 2)
dark_modal(580, 895, 122, 350, "output edge dark modal", 115)

# ---------- 4. equals ----------
print("==== EQUALS ink map (thr lum<150), x485..580 y250..295 ====")
reg = A[250:295, 485:580]
L = lum(reg)
for ry in range(reg.shape[0]):
    xs = np.where(L[ry] < 150)[0]
    if len(xs):
        runs = []
        s = p = xs[0]
        for x in xs[1:]:
            if x == p + 1:
                p = x
            else:
                runs.append((485 + s, 485 + p)); s = p = x
        runs.append((485 + s, 485 + p))
        print(f"  y{250+ry}: " + " ".join(f"{a}..{b}" for a, b in runs))

# ---------- 5. stride dots ----------
print("==== STRIDE region dark clusters (lum<120), x168..215 y236..295 ====")
reg = A[236:295, 168:215]
L = lum(reg)
ys, xs = np.where(L < 120)
if len(xs):
    for yy in range(236, 295):
        r = xs[ys == (yy - 236)]
        if len(r):
            runs = []
            s = p = r[0]
            for x in r[1:]:
                if x == p + 1:
                    p = x
                else:
                    runs.append((168 + s, 168 + p)); s = p = x
            runs.append((168 + s, 168 + p))
            print(f"  y{yy}: " + " ".join(f"{a}..{b}" for a, b in runs))

# ---------- 6. label windows ----------
LABELS = [
    ("w_in", 158, 212, 203, 237), ("h_in", 108, 152, 268, 320), ("d_in", 143, 192, 338, 366),
    ("s_lab", 194, 216, 236, 258), ("w_f", 278, 312, 234, 258), ("n_f", 352, 396, 208, 236),
    ("h_f", 262, 296, 256, 298), ("d_f", 284, 326, 298, 332),
    ("w_out", 588, 646, 168, 196), ("h_out", 542, 592, 262, 302), ("d_out", 676, 728, 338, 366),
]
print("==== LABEL windows (ink lum<140) ====")
for name, x0, x1, y0, y1 in LABELS:
    reg = A[y0:y1, x0:x1]
    L = lum(reg)
    ys, xs = np.where(L < 140)
    if len(xs) == 0:
        print(f"  {name}: EMPTY in window")
        continue
    print(f"  {name}: ink x {x0+xs.min()}..{x0+xs.max()}  y {y0+ys.min()}..{y0+ys.max()}  n={len(xs)}")
    modal(reg[L < 140], f"    {name} ink modal", 3)

# ---------- 7. legend ----------
print("==== LEGEND per-line blue/dark ====")
bands = [(372, 392), (393, 413), (414, 434), (434, 454), (455, 475), (476, 496)]
for i, (y0, y1) in enumerate(bands):
    reg = A[y0:y1, 95:320]
    r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
    L = lum(reg)
    ink = L < 200
    blue = ink & ((b - r) > 30) & (b > 90)
    dark = ink & ~blue
    if blue.any():
        ys, xs = np.where(blue)
        print(f"  L{i+1} y{y0}..{y1}: BLUE x {95+xs.min()}..{95+xs.max()} y {y0+ys.min()}..{y0+ys.max()} n={len(xs)}")
        bpix = reg[blue]
        Lb = 0.299 * bpix[:, 0] + 0.587 * bpix[:, 1] + 0.114 * bpix[:, 2]
        core = bpix[Lb <= np.percentile(Lb, 12)]
        modal(core, f"    L{i+1} blue core(12% darkest)", 4)
    if dark.any():
        ys, xs = np.where(dark)
        print(f"  L{i+1} y{y0}..{y1}: dark x {95+xs.min()}..{95+xs.max()} y {y0+ys.min()}..{y0+ys.max()} n={len(xs)}")

# word ink widths for font fingerprint (blue+dark, per line, x>126 to skip symbol)
print("==== LEGEND word widths (ink right of x=126) ====")
words = ["hight", "Width", "Depth", "Filter", "Filters Count", "Stride"]
for i, (y0, y1) in enumerate(bands):
    reg = A[y0:y1, 95:320]
    L = lum(reg)
    ink = L < 190
    ink[:, : (126 - 95)] = False
    ys, xs = np.where(ink)
    if len(xs):
        print(f"  '{words[i]}': x {95+xs.min()}..{95+xs.max()} (w {xs.max()-xs.min()+1})  y {y0+ys.min()}..{y0+ys.max()}")

# ---------- 8. title + eq box ----------
dark_modal(186, 779, 78, 117, "title ink modal", 130)
print("==== EQ BOX border ====")
reg = A[328:470, 310:530]
L = lum(reg)
for ry in range(reg.shape[0]):
    xs = np.where(L[ry] < 120)[0]
    if len(xs) > 120:
        print(f"  long row y{328+ry}: x {310+xs.min()}..{310+xs.max()} n={len(xs)}")
for cx in range(reg.shape[1]):
    ys = np.where(L[:, cx] < 120)[0]
    if len(ys) > 80:
        print(f"  long col x{310+cx}: y {328+ys.min()}..{328+ys.max()} n={len(ys)}")
dark_modal(310, 530, 328, 470, "eqbox ink modal", 110)
