#!/usr/bin/env python3
"""Slide 033 build-time measurement pass W1: full-slide family maps + box edges."""
from PIL import Image
import numpy as np
from collections import Counter, deque

IM = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg').convert('RGB')
A = np.asarray(IM).astype(int)
H, W = A.shape[:2]
R, G, B = A[:, :, 0], A[:, :, 1], A[:, :, 2]

# ---- peach panel edges: peach fill columns/rows --------------------------------
peach = (np.abs(A - np.array((247, 226, 205))).sum(axis=2) <= 36)
cols = np.where(peach[150:500].sum(axis=0) > 200)[0]
rows = np.where(peach[:, 100:900].sum(axis=1) > 400)[0]
print(f"PEACH panel solid: x {cols.min()}..{cols.max()}  rows-with-full-peach {rows.min()}..{rows.max()}")
rows_any = np.where(peach.sum(axis=1) > 30)[0]
print(f"PEACH rows any>30: {rows_any.min()}..{rows_any.max()}")
# top edge: first row where the row is mostly peach between x150..850
for y in range(30, 140):
    if peach[y, 150:850].sum() > 600:
        print(f"peach top edge y={y}")
        break
for y in range(539, 400, -1):
    if peach[y, 150:850].sum() > 600:
        print(f"peach bottom edge y={y}")
        break
for x in range(20, 100):
    if peach[150:500, x].sum() > 300:
        print(f"peach left edge x={x}")
        break
for x in range(959, 880, -1):
    if peach[150:500, x].sum() > 300:
        print(f"peach right edge x={x}")
        break

# ---- big boxes via fill masks ---------------------------------------------------
def comps(mask, min_area, k=24):
    seen = np.zeros(mask.shape, bool)
    out = []
    idx = np.argwhere(mask)
    for (yy, xx) in idx:
        if seen[yy, xx]:
            continue
        q = deque([(yy, xx)]); seen[yy, xx] = True
        ys, xs, n = [yy], [xx], 0
        while q:
            y, x = q.popleft(); n += 1
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < mask.shape[0] and 0 <= nx < mask.shape[1] and not seen[ny, nx] and mask[ny, nx]:
                        seen[ny, nx] = True; q.append((ny, nx)); ys.append(ny); xs.append(nx)
                if n > 120000:
                    break
        if n >= min_area:
            out.append((n, min(xs), max(xs), min(ys), max(ys)))
    out.sort(key=lambda b: (-b[1], b[3]))
    return out[:k]

print("\n== W boxes (chartreuse fill F8FA69, loose) ==")
wm = (np.abs(A - np.array((248, 250, 105))).sum(axis=2) <= 90)
for n, x0, x1, y0, y1 in comps(wm, 250):
    print(f"  n={n:5d} x {x0}..{x1}  y {y0}..{y1}  (w={x1-x0+1}, h={y1-y0+1})")

print("\n== DP box (fill DCCBBB) ==")
dm = (np.abs(A - np.array((220, 203, 187))).sum(axis=2) <= 42)
for n, x0, x1, y0, y1 in comps(dm, 4000, 4):
    print(f"  n={n:6d} x {x0}..{x1}  y {y0}..{y1}")

print("\n== Softmax bar (fill F8DDFC/FFCDFF) ==")
sm = ((np.abs(A - np.array((248, 221, 252))).sum(axis=2) <= 55) | (np.abs(A - np.array((255, 205, 255))).sum(axis=2) <= 55))
for n, x0, x1, y0, y1 in comps(sm, 3000, 4):
    print(f"  n={n:6d} x {x0}..{x1}  y {y0}..{y1}")

print("\n== Sigma box (fill EAFEFC) ==")
zb = (np.abs(A - np.array((234, 254, 252))).sum(axis=2) <= 40)
for n, x0, x1, y0, y1 in comps(zb, 1500, 4):
    print(f"  n={n:6d} x {x0}..{x1}  y {y0}..{y1}")

print("\n== mint containers (E7FFE9 fill) ==")
mm = (np.abs(A - np.array((231, 255, 233))).sum(axis=2) <= 36)
for n, x0, x1, y0, y1 in comps(mm, 900, 30):
    print(f"  n={n:6d} x {x0}..{x1}  y {y0}..{y1}")

print("\n== pills (FFFFE0-ish fill) ==")
pm = (np.abs(A - np.array((255, 255, 224))).sum(axis=2) <= 34)
for n, x0, x1, y0, y1 in comps(pm, 400, 8):
    print(f"  n={n:5d} x {x0}..{x1}  y {y0}..{y1}")

# ---- badge check ----------------------------------------------------------------
print("\n== badge region (x860..925, y45..100) mode colors ==")
sub = A[45:100, 860:925].reshape(-1, 3)
print("  ", [(f"#{r:02X}{g:02X}{b:02X}", n) for (r, g, b), n in Counter(map(tuple, sub // 8 * 8)).most_common(6)])
