#!/usr/bin/env python3
# measure9.py — pixel ASCII maps + color cores for slide_012's ambiguous zones.
from PIL import Image
import numpy as np

IM = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_012.jpg'
a = np.asarray(Image.open(IM).convert('RGB')).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

def cls(x, y):
    rr, gg, bb = a[y, x]
    if rr - max(gg, bb) > 45 and rr > 120: return 'R'      # red ink
    if bb - rr > 40 and bb > 110: return 'B'               # blue ink
    if rr - (gg + bb) / 2 > 25 and rr > 115: return 'r'    # loose red (orange/soft)
    if rr > 130 and bb > 130 and gg < 110: return 'M'      # magenta
    if rr > 243 and gg > 243 and bb > 243: return ' '      # white
    if rr > 235 and gg > 235 and bb < 232 and rr - bb > 25: return 'y'  # yellow cell
    if abs(rr - 206) < 25 and gg > 230: return 'g'         # green panel
    if rr > 225 and abs(gg - 222) < 28 and abs(bb - 190) < 32: return 'o'  # orange panel
    if abs(rr - 213) < 22 and abs(gg - 211) < 22 and bb > 226: return 'l'  # lavender
    if rr - gg > 8 and rr > 235 and bb - gg > 2: return 'p'  # pink
    if rr < 100 and gg < 100 and bb < 100: return 'k'      # black
    return '.'

def amap(x0, x1, y0, y1, xstep=1, ystep=1, label=""):
    print(f"--- {label} fx {x0}..{x1} (step {xstep}) fy {y0}..{y1} (step {ystep}) ---")
    hdr = "     " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(x0, x1 + 1, xstep))
    print(hdr)
    for y in range(y0, y1 + 1, ystep):
        row = "".join(cls(x, y) for x in range(x0, x1 + 1, xstep))
        print(f"fy {y:3d} {row}")

def core(x0, x1, y0, y1, mask_fn, label):
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    m = mask_fn(sub)
    if m.sum() == 0:
        print(f"{label}: none")
        return
    med = np.median(sub[m], axis=0).astype(int)
    print(f"{label}: core {tuple(med)} n={int(m.sum())}")

red_fn   = lambda s: (s[:, 0] - np.maximum(s[:, 1], s[:, 2]) > 45) & (s[:, 0] > 120)
sat_fn   = lambda s: (s.max(axis=1) - s.min(axis=1) > 60) & (s.max(axis=1) < 170)

# 1. embedding block
amap(95, 345, 122, 165, 2, 1, "EMBED labels")
amap(95, 345, 165, 262, 2, 2, "EMBED box+circles")
# 2. brace after H1 (clean zone)
amap(404, 436, 156, 336, 1, 6, "BRACE after H1")
# 3. after H2
amap(548, 600, 156, 336, 1, 6, "AFTER H2 (brace?)")
# 4. after H3
amap(700, 780, 148, 344, 2, 6, "AFTER H3 (brace? panel edge)")
# 5. '=' region, red only
amap(185, 255, 345, 395, 1, 1, "EQUALS region")
# 6. magenta
amap(505, 548, 265, 300, 1, 1, "MAGENTA annotation")
# 7. one cell H1 r1c1
amap(252, 282, 170, 200, 1, 1, "CELL H1 r1c1")
# 8. strip1 y1 box
amap(254, 292, 353, 390, 1, 1, "STRIP1 y1 box")
# 9. short brace
amap(710, 736, 345, 395, 1, 1, "SHORT BRACE")
# 10. Y result 1
amap(312, 344, 418, 448, 1, 1, "Y2^(1) result")
# 11. header H1
amap(240, 368, 134, 162, 1, 1, "HEADER H1")
# 12. panel tops/bottoms: vertical strip through each panel center
amap(310, 316, 128, 172, 1, 1, "H1 panel top zone fx 310")
amap(310, 316, 322, 344, 1, 1, "H1 panel bottom zone")

# color cores
core(414, 420, 200, 260, red_fn, "brace-H1 stroke core")
core(556, 572, 200, 260, red_fn, "after-H2 red core")
core(716, 726, 200, 260, red_fn, "after-H3 red core")
core(204, 218, 367, 377, red_fn, "equals core")
core(722, 730, 355, 385, red_fn, "short-brace core")
core(240, 368, 136, 156, red_fn, "header H1 core")
core(260, 710, 390, 414, red_fn, "caption core")
core(318, 334, 422, 440, sat_fn, "Y-result blue core")
core(518, 532, 274, 290, sat_fn, "magenta core")
core(100, 345, 150, 262, lambda s: (s[:, 0] - s[:, 1] > 8) & (s[:, 0] > 235) & (s[:, 2] - s[:, 1] > 2), "pink box fill core")
# H2 / H3 yellow cell col groups (same as H1 method)
yel = (r > 235) & (g > 235) & (b < 232) & (r - b > 25)
for nm, (x0, x1) in [("H2", (405, 565)), ("H3", (566, 730))]:
    sub = yel[160:340, x0:x1]
    colc = sub.sum(axis=0)
    groups = []
    s = None
    for x in range(x1 - x0):
        if colc[x] > 4:
            if s is None: s = x
            p = x
        else:
            if s is not None: groups.append((s + x0, p + x0)); s = None
    if s is not None: groups.append((s + x0, p + x0))
    print(f"{nm} yellow-cell col groups:", groups)
