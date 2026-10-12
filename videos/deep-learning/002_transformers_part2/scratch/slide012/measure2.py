#!/usr/bin/env python3
# measure2.py — finer: title/subtitle rows, panels, matrices, braces, outputs
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]
mx = np.maximum(np.maximum(r, g), b)
mn = np.minimum(np.minimum(r, g), b)
sat = mx - mn
dark = mx < 140
ink = (sat > 60) | dark

def red_ink(y0, y1, x0=20, x1=940):
    m = (r > 120) & (r < 230) & (g < 90) & (b < 90)
    return m

def blue_ink():
    m = (b > 120) & (b - r > 50) & (b - g > 40)
    return m

def spans_from_mask(m, axis=0, base=0, minlen=2):
    v = m.any(axis=axis)
    out = []
    s = None
    for i, v in enumerate(v):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s >= minlen: out.append((base + s, base + i - 1))
            s = None
    if s is not None: out.append((base + s, base + len(v) - 1))
    return out

RED = red_ink(0, H)
BLUE = blue_ink()

print("--- RED text rows fy 50..140 (x 100..860, excluding badge x>840) ---")
rm = RED.copy(); rm[:, 840:] = False; rm[:50] = False; rm[140:] = False
for s in spans_from_mask(rm[:, 100:860], axis=1, base=50):
    cols = spans_from_mask(rm[s[0]:s[1]+1, :840], axis=0)
    print(f"red band fy {s}, fx {cols[0][0]}..{cols[-1][1]}" if cols else f"red band fy {s}")

print("--- BLUE text rows fy 50..150 (x 100..860) ---")
bm = BLUE.copy(); bm[:, 840:] = False; bm[:50] = False; bm[150:] = False
for s in spans_from_mask(bm[:, 100:860], axis=1, base=50):
    cols = spans_from_mask(bm[s[0]:s[1]+1, :840], axis=0)
    print(f"blue band fy {s}, fx {cols[0][0]}..{cols[-1][1]}" if cols else f"blue band fy {s}")

def mode_color(x0, y0, x1, y1, q=8):
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    qq = (sub // q) * q
    uniq, cnt = np.unique(qq, axis=0, return_counts=True)
    k = int(cnt.argmax())
    return tuple(int(v) for v in uniq[k]), int(cnt[k])

# find pastel panels: green C9EFC9, orange F5DFC0, lavender C9C9F2
green = (np.abs(r - 201) < 30) & (np.abs(g - 239) < 25) & (np.abs(b - 201) < 30)
orange = (np.abs(r - 245) < 25) & (np.abs(g - 223) < 30) & (np.abs(b - 192) < 35)
lav = (np.abs(r - 201) < 30) & (np.abs(g - 201) < 30) & (np.abs(b - 242) < 25)
pink = (np.abs(r - 248) < 25) & (np.abs(g - 215) < 30) & (np.abs(b - 232) < 30)

for name, m in [("green", green), ("orange", orange), ("lavender", lav), ("pink", pink)]:
    ys, xs = np.where(m)
    if len(ys) < 50:
        print(f"{name}: n={len(ys)} (too few)")
        continue
    print(f"{name}: n={len(ys)} fx {xs.min()}..{xs.max()} fy {ys.min()}..{ys.max()}")

# white canvas: bright rows/cols
white = (r > 235) & (g > 235) & (b > 235)
wcols = white[200:460, :].any(axis=0)
wspans = spans_from_mask(wcols[:, None].T, axis=1, base=0, minlen=5)
print("white canvas fx spans (y 200..460):", wspans[:6], "..." if len(wspans) > 6 else "")
wrows = white[:, 100:850].any(axis=1)
rsp = spans_from_mask(wrows[:, None].T, axis=1, base=0, minlen=5)
print("white canvas fy spans (x 100..850):", rsp[:8])

# dark red braces: C00000-ish saturated red right of x=800? tall braces after matrices
br = (r > 150) & (g < 70) & (b < 70)
print("\n--- deep-red brace columns (tall) x 300..940, fy 120..330 ---")
brm = br.copy(); brm[:120] = False; brm[340:] = False
cols = spans_from_mask(brm[:, :], axis=0, minlen=1)
print("red col spans:", cols)

print("\n--- red bands fy 340..470 (output row: =, strips, short brace) ---")
brm2 = br.copy(); brm2[:335] = False; brm2[480:] = False
rows = spans_from_mask(brm2[:, :], axis=1, base=0)
print("red row spans fy:", rows)

# magenta annotation
mag = (r > 140) & (b > 140) & (g < 110)
ys, xs = np.where(mag)
if len(ys) > 10:
    print(f"magenta: n={len(ys)} fx {xs.min()}..{xs.max()} fy {ys.min()}..{ys.max()}")

print("\n--- sampled colors ---")
print("chrome bg (30,300):", a[300, 30].tolist())
print("title px sample (200,75):", a[75, 200].tolist())
