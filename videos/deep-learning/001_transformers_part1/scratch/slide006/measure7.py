#!/usr/bin/env python3
"""measure7: exact ink runs per row for decoder and encoder structures."""
from PIL import Image
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_006.jpg"
a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)

def runs_for_rows(rows, x0, x1, ref, tol, minw=2):
    for y in rows:
        d = np.abs(a[y, x0:x1] - np.array(ref)).sum(axis=1)
        m = d > tol
        out = []
        s = None
        for i, v in enumerate(m):
            if v and s is None: s = i
            elif not v and s is not None:
                if i - s >= minw: out.append((x0 + s, x0 + i - 1))
                s = None
        if s is not None and (len(m) - s) >= minw: out.append((x0 + s, x0 + len(m) - 1))
        print(f"  y={y}: " + " ".join(f"{r0}-{r1}" for r0, r1 in out))

DEC = (253, 255, 133); ENCT = (248, 213, 173)
print("== DECODER: o-label rows ==");   runs_for_rows(range(129, 141, 2), 480, 900, DEC, 80)
print("== DECODER: shaft/arrow rows =="); runs_for_rows([146, 150, 155, 160, 165, 170, 175, 180, 185, 188, 190, 192, 194, 196], 480, 900, DEC, 80)
print("== DECODER: dome rows ==");      runs_for_rows(range(186, 200), 480, 900, DEC, 80)
print("== DECODER: inter-bar rows =="); runs_for_rows(range(219, 256, 3), 480, 900, DEC, 80)
print("== DECODER: s-arrow rows ==");   runs_for_rows([262, 263, 264, 265, 266], 480, 900, DEC, 80)
print("== DECODER: below-barB rows =="); runs_for_rows(range(274, 283, 2), 480, 900, DEC, 80)
print("== DECODER: below container =="); runs_for_rows([284, 288, 292, 296], 480, 900, (255, 255, 255), 90)

print("== ENCODER: h-label rows ==");   runs_for_rows(range(311, 319, 2), 48, 485, ENCT, 80)
print("== ENCODER: h-arrow rows ==");   runs_for_rows([327, 329, 331], 48, 485, ENCT, 80)
print("== ENCODER: emb-arrow rows =="); runs_for_rows([345, 360, 380, 395, 402], 48, 485, ENCT, 80)
print("== ENCODER: x-arrow rows ==");   runs_for_rows([428, 440, 455, 468], 48, 485, ENCT, 80)
print("== ENCODER: below container =="); runs_for_rows([498, 502], 48, 485, (255, 255, 255), 90)
print("== ENCODER: container top/bot edges =="); runs_for_rows([306, 307, 495, 496], 40, 495, (255, 255, 255), 90)

# container bounds precise: scan columns/rows where fill changes from white bg
print("\n== decoder container edge scan ==")
for y in (114, 115, 116, 117, 118, 281, 282, 283, 284, 285):
    d = np.abs(a[y, 480:900] - np.array((253, 255, 133))).sum(axis=1)
    print(f"  y={y}: container-fill px={int((d < 60).sum())}")
for x in (476, 477, 478, 479, 900, 901, 902, 903, 904):
    d = np.abs(a[120:280, x] - np.array((253, 255, 133))).sum(axis=1)
    print(f"  x={x}: container-fill px={int((d < 60).sum())}")
print("== encoder container edge scan ==")
for y in (304, 305, 306, 307, 308, 494, 495, 496, 497, 498):
    d = np.abs(a[y, 50:480] - np.array((248, 213, 173))).sum(axis=1)
    print(f"  y={y}: container-fill px={int((d < 60).sum())}")
for x in (44, 45, 46, 47, 48, 485, 486, 487, 488, 489):
    d = np.abs(a[310:490, x] - np.array((248, 213, 173))).sum(axis=1)
    print(f"  x={x}: container-fill px={int((d < 60).sum())}")

# callout box borders precise
print("\n== callout box edges ==")
for y in (400, 401, 402, 403, 440, 441, 442, 443, 444):
    d = np.abs(a[y, 550:850] - np.array((246, 220, 221))).sum(axis=1)
    print(f"  y={y}: fill px={int((d < 60).sum())}")
for x in (556, 557, 558, 559, 836, 837, 838, 839, 840):
    d = np.abs(a[405:440, x] - np.array((246, 220, 221))).sum(axis=1)
    print(f"  x={x}: fill px={int((d < 60).sum())}")

# leader line: scan the diagonal band between encoder dot and callout TL
print("\n== leader line scan ( reddish pixels x470-560 y330-405) ==")
red = (a[:, :, 0] > 140) & (a[:, :, 1] < 110) & (a[:, :, 2] < 110)
for y in range(330, 406, 5):
    xs = np.where(red[y, 460:600])[0]
    if len(xs): print(f"  y={y}: red x at {460+xs.min()}-{460+xs.max()} n={len(xs)}")
