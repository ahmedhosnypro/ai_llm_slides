#!/usr/bin/env python3
"""048 right-digit ruling: compare its visible 2-row top against the deck's
real '8' glyphs (slides 008/018/028/038/058) and real '9' glyphs (009/019/029/
039/049/059), position-anchored (no shift freedom) plus shift diagnostics."""
from PIL import Image
import numpy as np
from scipy import ndimage
import os, collections

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
US = os.path.join(ROOT, "unique_slides")
HINT = (877.0, 70.0)


def find_blob(a):
    r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
    ym = (r > 215) & (g > 205) & (b < 215) & ((r - b) > 35) & ((g - b) > 35)
    region = np.zeros(ym.shape, bool); region[:170, 830:] = True
    ym &= region
    lab, n = ndimage.label(ym)
    best, best_area = None, 0
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() > best_area:
            ys, xs = np.where(m)
            cy, cx = ys.mean(), xs.mean()
            if ((cx - HINT[0]) ** 2 + (cy - HINT[1]) ** 2) ** 0.5 <= 60:
                best, best_area = m, m.sum()
    return best


def glyphs_of(name):
    a = np.array(Image.open(os.path.join(US, f"{name}.jpg")).convert("RGB"))
    blob = find_blob(a)
    fill = np.median(a[blob].reshape(-1, 3), axis=0)
    rch, gch, bch = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
    lum = 0.299 * rch + 0.587 * gch + 0.114 * bch
    region = (ndimage.binary_fill_holes(blob) |
              ndimage.binary_closing(blob, structure=np.ones((3, 3), bool), iterations=3))
    dist = np.sqrt(((a.astype(int) - fill.astype(int)) ** 2).sum(axis=2))
    guards = (lum < 185) & ((rch - gch) > -60) & ((bch - rch) < 20)
    ink = (dist > 70) & region & guards
    lab, n = ndimage.label(ink)
    out = []
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() < 5:
            continue
        ys, xs = np.where(m)
        out.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), m[ys.min():ys.max()+1, xs.min():xs.max()+1]))
    out.sort(key=lambda t: t[0])
    return out


def ascii_of(m):
    return "\n".join("".join("#" if v else "." for v in row) for row in m)


def iou_natural(obs, tpl):
    """IoU with both pinned at their bbox top-left (no shift freedom)."""
    H = max(obs.shape[0], tpl.shape[0]) + 2
    W = max(obs.shape[1], tpl.shape[1]) + 2
    A = np.zeros((H, W), bool); B = np.zeros((H, W), bool)
    A[1:1+obs.shape[0], 1:1+obs.shape[1]] = obs
    B[1:1+tpl.shape[0], 1:1+tpl.shape[1]] = tpl
    u = (A | B).sum()
    return round(float((A & B).sum()) / u, 3) if u else 0.0


def iou_shift(obs, tpl, dxs=(-2, -1, 0, 1, 2)):
    best, bestdx = 0.0, None
    for dx in dxs:
        H = max(obs.shape[0], tpl.shape[0]) + 2
        W = max(obs.shape[0], tpl.shape[1]) + 8
        A = np.zeros((H, W), bool); B = np.zeros((H, W), bool)
        A[1:1+obs.shape[0], 4:4+obs.shape[1]] = obs
        x2 = 4 + dx
        if x2 < 0:
            continue
        B[1:1+tpl.shape[0], x2:x2+tpl.shape[1]] = tpl
        u = (A | B).sum()
        v = float((A & B).sum()) / u if u else 0.0
        if v > best:
            best, bestdx = v, dx
    return round(best, 3), bestdx


# ---- collect 8 and 9 templates with absolute x positions ----
eights, nines = [], []
for name in ["slide_008", "slide_018", "slide_028", "slide_038", "slide_058"]:
    gs = glyphs_of(name)
    print(f"--- {name} glyphs:", [(g[0], g[1], g[2], g[3]) for g in gs])
    for g in gs:
        print(ascii_of(g[4]))
    if name == "slide_008":
        eights.extend(gs)
    else:
        eights.append(gs[-1])   # units digit = 8
for name in ["slide_009", "slide_019", "slide_029", "slide_039", "slide_049", "slide_059"]:
    gs = glyphs_of(name)
    if name in ("slide_009",):
        nines.extend(gs)
    else:
        nines.append(gs[-1])

print("\n=== 8 templates (x0,y0,x1,y1) + top-2-rows ===")
for x0, y0, x1, y1, m in eights:
    print(f"x0={x0} x1={x1} w={x1-x0+1} rows01={[''.join('#' if v else '.' for v in r) for r in m[:2]]}")
print("=== 9 templates ===")
for x0, y0, x1, y1, m in nines:
    print(f"x0={x0} x1={x1} w={x1-x0+1} rows01={[''.join('#' if v else '.' for v in r) for r in m[:2]]}")

# ---- the observed 048 right glyph ----
obs = glyphs_of("slide_048")[-1]
print(f"\n048 right glyph bbox x0={obs[0]} x1={obs[2]} rows={obs[3]-obs[1]+1}")
print(ascii_of(obs[4]))
obs2 = obs[4][:2, :]   # its 2 visible rows

print("\n=== ruling: natural-position IoU (left edges pinned) and best-shift ===")
for label, tlist in (("8", eights), ("9", nines)):
    for x0, y0, x1, y1, m in tlist:
        nat = iou_natural(obs2, m[:2, :])
        sh, dx = iou_shift(obs2, m[:2, :])
        print(f"  vs {label} (x0={x0}): natural={nat}  best_shift={sh} at dx={dx}")
