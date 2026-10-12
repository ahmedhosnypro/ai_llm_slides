#!/usr/bin/env python3
# m12_resume.py — resume-worker forensics for judge-1 findings on 002:51.
# Regions (frame px, 960x540, 1px=1pt):
#   A decoder right edge x770..895 y285..350   (judge BLOCKER-2: "green-ringed Nx circle")
#   B decoder PE cluster  x770..895 y390..440  (judge BLOCKER-1: clock icon + label + dark check)
#   C encoder PE region   x135..215 y385..435  (spec icon? probe says label + tan bar)
#   D decoder badges      x725..835 y190..345  (judge MINOR-7 placements)
#   E encoder norm boxes  x205..285 y260..345  (judge MAJOR-3 "Add & Norm" truncation)
# Compares ORIGINAL vs render_4 (150dpi; render_px = slide_pt*150/72, slide_pt from
# the certified frame->slide mapping in the build header).
import sys
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
orig = Image.open(f"{ROOT}/unique_slides/slide_051.jpg").convert("RGB")
r4 = Image.open(f"{ROOT}/recreated_pptx/qa/slide051/render_4.png").convert("RGB")
OW, OH = orig.size
RW, RH = r4.size
SX = lambda fx: (fx - 18.128) / 0.961235
SY = lambda fy: (fy + 0.045) / 0.956566
K = 150.0 / 72.0  # slide pt -> render px

def px_img(img, x, y):  # x,y in frame px
    return img.getpixel((min(max(int(x), 0), img.size[0] - 1), min(max(int(y), 0), img.size[1] - 1)))

def blob_scan(img, x0, y0, x1, y1, bg_pred, name, min_run=3):
    """Find non-bg pixels; print column/row density profile coarse map."""
    w, h = x1 - x0, y1 - y0
    cols = [0] * w
    rows = [0] * h
    for j in range(h):
        for i in range(w):
            r, g, b = px_img(img, x0 + i, y0 + j)
            if not bg_pred(r, g, b):
                cols[i] += 1
                rows[j] += 1
    print(f"  [{name}] col ink (x:count>=min_run): ", end="")
    runs = []
    i = 0
    while i < w:
        if cols[i] >= min_run:
            j = i
            while j < w and cols[j] >= min_run:
                j += 1
            runs.append((x0 + i, x0 + j - 1, max(cols[i:j])))
            i = j
        else:
            i += 1
    print("; ".join(f"x{a}-{b}(h{c})" for a, b, c in runs))
    print(f"  [{name}] row ink (y:count>=min_run): ", end="")
    runs = []
    j = 0
    while j < h:
        if rows[j] >= min_run:
            k = j
            while k < h and rows[k] >= min_run:
                k += 1
            runs.append((y0 + j, y0 + k - 1, max(rows[j:k])))
            j = k
        else:
            j += 1
    print("; ".join(f"y{a}-{b}(w{c})" for a, b, c in runs))

# --- region A: decoder Nx / navy disc (original) -------------------------------
print("=== A: decoder right edge x770-895 y285-350 — ORIGINAL")
blob_scan(orig, 770, 285, 895, 350, lambda r, g, b: g > 200 and r > 170 and b > 170, "A-orig", 4)
# sample specific candidate circle colors
for (cx, cy, tag) in [(809, 321, "navy?"), (860, 305, "tan?Nx"), (875, 300, "tan2"),
                      (800, 312, "nx-left"), (820, 312, "nx-right")]:
    print(f"  A sample ({cx},{cy}) {tag}: {px_img(orig, cx, cy)}")
print("=== A: same region — RENDER_4")
blob_scan(r4, SX(770) * K, SY(285) * K, SX(895) * K, SY(350) * K,
          lambda r, g, b: g > 200 and r > 170 and b > 170, "A-r4", 4)

# --- region B: decoder PE cluster ----------------------------------------------
print("=== B: decoder PE x770-895 y390-440 — ORIGINAL")
blob_scan(orig, 770, 390, 895, 440, lambda r, g, b: not (g > 190 and r > 150 and b > 150), "B-orig", 4)
for (cx, cy, tag) in [(790, 420, "icon?"), (800, 415, "icon2"), (812, 408, "icon3"),
                      (830, 405, "lbl1"), (830, 420, "lbl2"), (760, 430, "check?")]:
    print(f"  B sample ({cx},{cy}) {tag}: {px_img(orig, cx, cy)}")
print("=== B: same — RENDER_4")
blob_scan(r4, SX(770) * K, SY(390) * K, SX(895) * K, SY(440) * K,
          lambda r, g, b: not (g > 190 and r > 150 and b > 150), "B-r4", 4)

# --- region C: encoder PE region ------------------------------------------------
print("=== C: encoder PE x135-215 y385-435 — ORIGINAL")
blob_scan(orig, 135, 385, 215, 435, lambda r, g, b: not (r > 235 and g > 220 and b > 200), "C-orig", 3)
for (cx, cy, tag) in [(150, 410, "icon?"), (165, 412, "icon2"), (180, 410, "lbl"),
                      (150, 393, "up?"), (222, 420, "emb-box")]:
    print(f"  C sample ({cx},{cy}) {tag}: {px_img(orig, cx, cy)}")

# --- region D: decoder badge census (navy discs) --------------------------------
print("=== D: navy-disc census x725-835 y185-345 — ORIGINAL")
def navy_discs(img, x0, y0, x1, y1, scale=1.0, ox=0.0, oy=0.0):
    """Scan for dark-navy blobs; report connected rough bboxes (grid-based)."""
    step = 2
    hits = []
    for j in range(y0, y1, step):
        for i in range(x0, x1, step):
            x = ox + i * scale
            y = oy + j * scale
            r, g, b = px_img(img, x, y)
            if b > 110 and b < 200 and r < 80 and g < 80:
                hits.append((i, j))
    # cluster
    clusters = []
    for (i, j) in hits:
        placed = False
        for c in clusters:
            if abs(c[0] - i) < 14 and abs(c[1] - j) < 14:
                c[0] = (c[0] * c[2] + i) / (c[2] + 1)
                c[1] = (c[1] * c[2] + j) / (c[2] + 1)
                c[2] += 1
                placed = True
                break
        if not placed:
            clusters.append([i, j, 1])
    return [(round(c[0]), round(c[1]), c[2]) for c in clusters if c[2] >= 4]

discs = navy_discs(orig, 725, 185, 835, 345)
print(f"  D-orig navy clusters (cx,cy,n): {discs}")
discs4 = navy_discs(r4, int(SX(725) * K), int(SY(185) * K), int(SX(835) * K), int(SY(345) * K),
                    scale=1 / (K / 0.961235), ox=18.128, oy=-0.045)
# simpler: rerun in render space then convert back to frame px
def navy_discs_render(img, fx0, fy0, fx1, fy1):
    x0, y0 = SX(fx0) * K, SY(fy0) * K
    x1, y1 = SX(fx1) * K, SY(fy1) * K
    hits = []
    for j in range(int(y0), int(y1), 2):
        for i in range(int(x0), int(x1), 2):
            r, g, b = img.getpixel((i, j))
            if b > 110 and b < 200 and r < 80 and g < 80:
                fx = (i / K) * 0.961235 + 18.128
                fy = (j / K) * 0.956566 - 0.045
                hits.append((fx, fy))
    clusters = []
    for (i, j) in hits:
        placed = False
        for c in clusters:
            if abs(c[0] - i) < 14 and abs(c[1] - j) < 14:
                c[0] = (c[0] * c[2] + i) / (c[2] + 1)
                c[1] = (c[1] * c[2] + j) / (c[2] + 1)
                c[2] += 1
                placed = True
                break
        if not placed:
            clusters.append([i, j, 1])
    return [(round(c[0]), round(c[1]), c[2]) for c in clusters if c[2] >= 4]

print(f"  D-r4   navy clusters (frame px): {navy_discs_render(r4, 725, 185, 835, 345)}")

# --- region E: encoder norm boxes: ink extent of text rows ----------------------
print("=== E: encoder norm boxes — ORIGINAL ink rows in box1 (213..276, 266..276)")
blob_scan(orig, 205, 262, 285, 280, lambda r, g, b: not (abs(r - 109) < 45 and abs(g - 153) < 45 and abs(b - 180) < 45), "E-box1-orig", 2)
print("=== E: same — RENDER_4")
blob_scan(r4, SX(205) * K, SY(262) * K, SX(285) * K, SY(280) * K,
          lambda r, g, b: not (abs(r - 109) < 45 and abs(g - 153) < 45 and abs(b - 180) < 45), "E-box1-r4", 2)
