#!/usr/bin/env python3
"""measure8.py — frame diff: slide_025 vs slide_024 shifted up (delta inventory).
Block mean-abs-diff grid at 16px; then red-ink check for col0->col1 mesh question.
Banked as measure8_out.txt."""
from PIL import Image
import numpy as np

D = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
a = np.asarray(Image.open(f"{D}/unique_slides/slide_025.jpg").convert("RGB"), dtype=np.int16)
bimg = Image.open(f"{D}/unique_slides/slide_024.jpg").convert("RGB")
L = []
def pr(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s)

best = None
for sh in (29, 30, 31):
    b = np.asarray(bimg, dtype=np.int16)[sh:, :, :]
    h = min(a.shape[0], b.shape[0])
    d = np.abs(a[:h] - b[:h]).mean()
    pr(f"shift {sh}: mean abs diff {d:.2f}")
    if best is None or d < best[1]: best = (sh, d)
sh = best[0]
pr(f"best shift = {sh}")
b = np.asarray(bimg, dtype=np.int16)[sh:, :, :]
h = min(a.shape[0], b.shape[0])
diff = np.abs(a[:h] - b[:h]).mean(axis=2)
pr("== 16px block mean diff (rows y-blocks 0..32, cols x-blocks 0..59; '.' <6, '-' <12, '+' <25, '#' >=25) ==")
for by in range(0, h // 16):
    row = ""
    for bx in range(0, 960 // 16):
        blk = diff[by * 16:(by + 1) * 16, bx * 16:(bx + 1) * 16]
        m = blk.mean()
        row += "." if m < 6 else ("-" if m < 12 else ("+" if m < 25 else "#"))
    pr(f"y{by * 16:3d} {row}")

# red-ink check: col0->col1 mesh region on slide25 vs parent-shifted
pa = a[:h]; pb = b[:h]
def redcount(img, x0, y0, x1, y1):
    r = img[y0:y1, x0:x1]
    return int(((r[:, :, 0] > 130) & (r[:, :, 1] < 80) & (r[:, :, 2] < 80)).sum())
pr("== red px counts x180..245 (col0->col1 gap), y-bands ==")
for y0 in range(160, 360, 60):
    pr(f"  y{y0}..{y0+60}: slide25={redcount(pa, 180, y0, 246, min(y0+60, h))} parent-sh={redcount(pb, 180, y0, 246, min(y0+60, h))}")
pr("== red px counts x455..505 (green->outbox gap) ==")
for y0 in range(160, 360, 60):
    pr(f"  y{y0}..{y0+60}: slide25={redcount(pa, 455, y0, 506, min(y0+60, h))} parent-sh={redcount(pb, 455, y0, 506, min(y0+60, h))}")

with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide025/measure8_out.txt", "w") as f:
    f.write("\n".join(L) + "\n")
print("WROTE measure8_out.txt")
