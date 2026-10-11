#!/usr/bin/env python3
"""Slide 033 pass 8: borders, arrows, circles, fine maps, core colors."""
from PIL import Image
import numpy as np
from collections import Counter, deque

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
H, W = A.shape[:2]
R, G, B = A[:,:,0], A[:,:,1], A[:,:,2]

def comps(m, x0, y0, min_area=4, max_n=3000):
    h, w = m.shape
    seen = np.zeros((h, w), bool)
    out = []
    idx = np.argwhere(m)
    for (y, x) in idx:
        if seen[y, x]: continue
        q = deque([(y, x)]); seen[y, x] = True
        ys, xs, n = [y], [x], 0
        while q:
            cy, cx = q.popleft(); n += 1
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = cy+dy, cx+dx
                    if 0 <= ny < h and 0 <= nx < w and not seen[ny, nx] and m[ny, nx]:
                        seen[ny, nx] = True; q.append((ny, nx)); ys.append(ny); xs.append(nx)
                if n > max_n: break
            if n > max_n: break
        if n >= min_area:
            out.append((n, x0+min(xs), x0+max(xs), y0+min(ys), y0+max(ys)))
    out.sort(key=lambda b: (b[3], b[1]))
    return out

def show(title, rows, k=40):
    print(f"--- {title} ---")
    for n, x0, x1, y0, y1 in rows[:k]:
        print(f"  n={n:4d} x {x0:3d}..{x1:3d} y {y0:3d}..{y1:3d} (w={x1-x0+1:3d} h={y1-y0+1:3d})")

def core(name, x0, y0, x1, y1, thr=110):
    sub = A[y0:y1+1, x0:x1+1].reshape(-1, 3)
    dk = sub[sub.max(axis=1) < thr]
    if len(dk) == 0:
        print(f"{name}: none <{thr}"); return
    c = Counter(map(tuple, dk)).most_common(3)
    print(f"{name}: {[(f'#{r:02X}{g:02X}{b:02X}', n) for (r, g, b), n in c]} n={len(dk)}")

# 1) sensitive red (arrows/lines incl. blends)
sred = (R - G > 50) & (R - B > 35) & (R > 150)
show("SENSITIVE-RED comps x40..930 y100..540", comps(sred[100:540, 40:930], 40, 100, 6), 70)

# 2) orange W-box borders
orange = (R > 170) & (G > 80) & (G < 175) & (B < 110) & (R - B > 90)
show("ORANGE comps", comps(orange[180:480, 130:340], 130, 180, 4), 30)
show("ORANGE comps right (W_v)", comps(orange[180:480, 690:760], 690, 180, 4), 30)

# 3) green full list
green = (G > 110) & (G - R > 40) & (G - B > 25) & (R < 130)
show("GREEN comps FULL", comps(green[100:540, 40:930], 40, 100, 4), 60)

# 4) X2 pink box bbox
pink = (R > 195) & (B > 140) & (G < 175) & (R - G > 45) & (B - G > 15)
show("PINK comps (X2 box)", comps(pink[460:530, 250:345], 250, 460, 60), 8)
core("X2-box X glyph", 288, 483, 312, 502, 130)
core("X2 box fill", 270, 478, 290, 486, 255)

# 5) circles: red-ring vertical extent per row
for cy, name in [(246, "c1"), (288, "c2"), (328, "c3"), (372, "c4")]:
    win = sred[cy-22:cy+23, 500:600]
    ys, xs = np.where(win)
    if len(ys):
        print(f"circle {name}: x {500+xs.min()}..{500+xs.max()} y {cy-22+ys.min()}..{cy-22+ys.max()} n={len(ys)}")

# 6) output box fine map (non-peach) x530..640 y100..180
sub = A[100:181, 530:641]
np_mask = (np.abs(sub - np.array([247, 226, 205])) > 22).any(axis=2)
print("--- OUTPUT BOX non-peach map (x530..640, y100..180), 2px ---")
for yy in range(0, 81, 2):
    row = ""
    for xx in range(0, 111, 2):
        blk = np_mask[yy:yy+2, xx:xx+2]
        row += "#" if blk.mean() > 0.5 else ("+" if blk.mean() > 0.15 else " ")
    print(f"{100+yy:3d} {row}")

# 7) legend fine map x730..910 y462..536 (non-peach)
sub = A[462:537, 730:911]
np2 = (np.abs(sub - np.array([247, 226, 205])) > 22).any(axis=2)
print("--- LEGEND non-peach map (x730..910, y462..536), 2px ---")
for yy in range(0, 75, 2):
    row = ""
    for xx in range(0, 181, 2):
        blk = np2[yy:yy+2, xx:xx+2]
        row += "#" if blk.mean() > 0.5 else ("+" if blk.mean() > 0.15 else " ")
    print(f"{462+yy:3d} {row}")

# 8) q region fine map x255..340 y395..475
sub = A[395:476, 255:341]
np3 = (np.abs(sub - np.array([247, 226, 205])) > 22).any(axis=2)
print("--- Q-REGION non-peach map (x255..340, y395..475), 2px ---")
for yy in range(0, 81, 2):
    row = ""
    for xx in range(0, 86, 2):
        blk = np3[yy:yy+2, xx:xx+2]
        row += "#" if blk.mean() > 0.5 else ("+" if blk.mean() > 0.15 else " ")
    print(f"{395+yy:3d} {row}")

# 9) core colors (low threshold)
core("DP 'Dot'", 270, 198, 322, 228, 120)
core("DP 'K2q'", 344, 196, 370, 214, 120)
core("Soft max", 466, 262, 482, 336, 130)
core("Sigma glyph", 576, 197, 590, 215, 120)
core("W box text r1", 158, 233, 195, 260, 130)
core("caption 'd: Embedding'", 765, 512, 880, 530, 120)
core("pill S text", 260, 166, 340, 186, 170)
core("pill P text", 438, 166, 506, 186, 170)
core("pill W text", 600, 164, 684, 182, 170)
core("K label r1", 234, 226, 252, 244, 120)
core("V label r2", 636, 270, 660, 292, 120)
core("title blue '(' 490", 488, 58, 495, 77, 140)
core("title blue mid", 616, 60, 662, 73, 120)
core("title black 'M' x395", 395, 58, 406, 73, 120)
core("Y glyph in box", 576, 120, 592, 142, 140)
core("Y cells green", 596, 120, 616, 142, 200)
core("legend '1^d' left", 774, 476, 798, 500, 150)
core("legend W black", 804, 480, 822, 496, 120)
core("legend right '1^d'", 843, 478, 862, 500, 150)
core("legend 'd*d'", 800, 500, 826, 514, 150)
core("legend '='", 828, 480, 842, 500, 150)
core("arrow q-DP", 295, 403, 303, 414, 150)
core("sent X1 red", 216, 484, 232, 502, 140)
