#!/usr/bin/env python3
"""Frame-truth measurement pass for slide 055 (002_transformers_part2).
Frame: unique_slides/slide_055.jpg (960x540, 1px = 1pt).
Part 1: chrome landmarks + mapping fit. Part 2: component census by color.
"""
from PIL import Image
import numpy as np
from scipy import ndimage
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_055.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
A = np.asarray(img).astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]
print("frame", W, "x", H)

# ---------- 1. chrome landmarks ----------
def is_redish(p): r, g, b = p; return r > 120 and g < 100 and b < 100 and (r - max(g, b)) > 50
px = img.load()
col_counts = {x: sum(1 for y in range(H) if is_redish(px[x, y])) for x in range(W)}
row_counts = {y: sum(1 for x in range(W) if is_redish(px[x, y])) for y in range(H)}
weak_cols = [x for x, c in col_counts.items() if c > 60]
weak_rows = [y for y, c in row_counts.items() if c > 60]
print("red border cols(>60):", weak_cols)
print("red border rows(>60):", weak_rows)
print("top border color samples:", [px[x, min(weak_rows)] for x in (100, 300, 500)] if weak_rows else None)
if weak_cols:
    xl = min(weak_cols)
    print("left border color samples:", [px[xl, y] for y in (100, 200, 300)])

# badge: yellow/purple in x 830..935, y 30..110
def is_yellowish(p): r, g, b = p; return r > 200 and g > 200 and b < 180
def is_purple(p): r, g, b = p; return 90 <= r <= 170 and 60 <= g <= 130 and b > 150
pts = [(x, y) for y in range(30, 110) for x in range(830, 935) if is_yellowish(px[x, y]) or is_purple(px[x, y])]
if pts:
    xs = sorted(set(p[0] for p in pts)); ys = sorted(set(p[1] for p in pts))
    print("badge zone bbox:", (min(xs), min(ys), max(xs), max(ys)))

# ---------- mapping fit (landmarks measured in probe_border.txt: L58 R901 T43 B516-517;
# identical to slide_054's template within 1px JPEG noise -> same constants) ----------
X_LEFT = 58.0; X_RIGHT = 901.0; Y_TOP = 43.0; Y_BOT = 516.5
SX = (X_RIGHT - X_LEFT) / (919 - 42)
X0 = X_LEFT - SX * 42
SY = (Y_BOT - Y_TOP) / (540 - 45)
print(f"\nMAPPING FIT: X0={X0:.2f} SX={SX:.5f} SY={SY:.5f}  (landmarks L{X_LEFT} R{X_RIGHT} T{Y_TOP} B{Y_BOT})")

def to_slide(bb):
    x0, y0, x1, y1 = bb
    sx0 = (x0 - X0) / SX; sx1 = (x1 - X0) / SX
    sy0 = y0 / SY; sy1 = y1 / SY
    return [round(sx0, 1), round(sy0, 1), round(sx1, 1), round(sy1, 1), round(sx1 - sx0, 1), round(sy1 - sy0, 1)]

inner = np.zeros((H, W), bool)
inner[int(Y_TOP) + 3:517, int(X_LEFT) + 3:int(X_RIGHT) - 3] = True

# ---------- 2. component census ----------
def comps(mask, min_px, name, topn=40):
    m = mask & inner
    lab, n = ndimage.label(m)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_px: continue
        bb = [int(xs.min()), int(ys.min()), int(xs.max()), int(xs.max() if False else xs.max()), int(ys.max())]
        bb = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
        out.append({"fbox": bb, "w": bb[2] - bb[0] + 1, "h": bb[3] - bb[1] + 1, "npx": int(len(ys)), "slide": to_slide(bb)})
    out.sort(key=lambda c: (c["fbox"][1], c["fbox"][0]))
    print(f"\n== {name}: {len(out)} comps")
    for c in out[:topn]:
        print(f"   f={c['fbox']} {c['w']}x{c['h']} n={c['npx']} slide={c['slide']}")
    return out

# sample the panel color first: center of the diagram area
print("\npanel color samples:", [tuple(A[y, x]) for x, y in [(480, 300), (200, 300), (700, 300), (480, 180)]])

masks = {
    "PEACH-panel ~FCE5C6": (np.abs(R - 252) <= 10) & (np.abs(G - 229) <= 12) & (np.abs(B - 198) <= 14),
    "TAN ~A99E8C/D8C8B9": (np.abs(R - 214) <= 22) & (np.abs(G - 199) <= 22) & (np.abs(B - 180) <= 25),
    "PINK ~FF9C9C (Scaling)": (R >= 240) & (np.abs(G - 156) <= 35) & (np.abs(B - 156) <= 35),
    "VIOLET ~CC99FF (Softmax)": (np.abs(R - 204) <= 30) & (np.abs(G - 153) <= 30) & (B >= 220),
    "LIGHTBLUE ~BFDCEF (Sigma)": (B - R >= 12) & (B - G >= 8) & (B >= 220) & (R >= 170),
    "GREEN fills ~00CC00/00B050": (G - R >= 60) & (G - B >= 60) & (G >= 140),
    "YELLOW ~FFFF00/FFF9C4": (R >= 235) & (G >= 235) & (B <= 190) & (R - B >= 60),
    "RED strong": (R - G >= 70) & (R - B >= 60) & (R >= 150),
    "DARK ink": (R < 110) & (G < 110) & (B < 110),
    "BLUE ~0033CC": (B - R >= 60) & (B >= 120) & (R < 160),
    "MAGENTA/pink-Z ~FF99CC/CC00CC": (R >= 200) & (B >= 150) & (R - G >= 40) & (B - G >= 30),
    "WHITE": (R >= 240) & (G >= 240) & (B >= 240),
    "PALEGREEN ~CCFFCC": (np.abs(R - 204) <= 25) & (G >= 230) & (np.abs(B - 204) <= 25),
    "PALECELL lavender ~EEF0F5": (np.abs(R - 238) <= 12) & (np.abs(G - 240) <= 12) & (np.abs(B - 245) <= 12),
}
for name, m in masks.items():
    comps(m, 150, name)

# ---------- 3. title ink bbox ----------
# title zone: y 55..100, x 80..700 (avoid badge)
sub = A[50:105, 80:700]
lum = 0.299 * sub[..., 0] + 0.299 * sub[..., 1] + 0.114 * sub[..., 2]
dark = lum < 128
ys, xs = np.where(dark)
if len(ys):
    print("\ntitle-zone dark-ink bbox frame:", [80 + xs.min(), 50 + ys.min(), 80 + xs.max(), 50 + ys.max()],
          "slide:", to_slide([80 + int(xs.min()), 50 + int(ys.min()), 80 + int(xs.max()), 50 + int(ys.max())]))
# per-row ink spans to find the two title lines
for yy in range(0, sub.shape[0], 2):
    xs2 = np.where(dark[yy])[0]
    if len(xs2) > 5:
        print(f"   row y={50+yy}: x {80+xs2.min()}..{80+xs2.max()} n={len(xs2)}")
