#!/usr/bin/env python3
import numpy as np
from PIL import Image
IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
PEACH = np.array([247, 227, 206])

print("== node verticals: sensitive scan x centers +-3, y219..365 ==")
for cx in (532, 563, 591, 622):
    hits = []
    for y in range(219, 366):
        seg = A[y, cx-3:cx+4]
        d = np.abs(seg - PEACH).sum(axis=1)
        if (d > 25).any():
            hits.append(y)
    # summarize runs
    runs, s, p = [], None, None
    for y in hits:
        if s is None: s = y; p = y; continue
        if y > p + 4: runs.append((s, p)); s = y
        p = y
    if s is not None: runs.append((s, p))
    print(f"  x~{cx}: runs={runs}")

print("\n== arrowheads at Sigma bottom (y213..222, x526..630) ==")
for y in range(211, 224):
    row = "".join("R" if (A[y,x][0]-A[y,x][1] > 40 and A[y,x][0] > 150) else ("k" if A[y,x].sum() < 420 else ".") for x in range(522, 632))
    print(f"  y{y}: {row}")

print("\n== X2 glyph yellow cells? sample ==")
for (x, y) in [(270,490),(280,487),(300,483),(320,487),(325,495),(268,478),(280,502)]:
    c = A[y, x]
    print(f"  ({x},{y}) #{c[0]:02X}{c[1]:02X}{c[2]:02X}", end="")
print()

print("\n== highlight box border rows x258..340 y470..478 / y503..509 ==")
for y in list(range(470, 479)) + list(range(502, 510)):
    row = "".join("k" if A[y,x].sum() < 480 else ("R" if A[y,x][0]-A[y,x][1] > 45 else ".") for x in range(256, 342))
    print(f"  y{y}: {row}")
