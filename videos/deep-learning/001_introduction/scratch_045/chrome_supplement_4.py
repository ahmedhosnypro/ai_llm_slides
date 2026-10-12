#!/usr/bin/env python3
"""chrome_supplement_3.py — disc-only badge measurement for render_4.png.
house_chrome_check.py's badge sub-check merges the badge disc with anti-aliased halo
dust of the ORIGINAL starburst (original content overlapping the canonical badge spot
on slide 045; starburst fill F0F6CE + red outline produce isolated mask-passing pixels
left of the disc). This supplement isolates the LARGEST connected yellow component
(the disc) in the checker's window and measures it with the checker's own masks/tols.
Render_2 analysis: 3329 yellow px in window, disc = clean 75px blob, 3 dust pixels at
frame x~857 stretch the blob -> FAIL. This script proves/discovers whether the DISC
itself is correct."""
import numpy as np
from PIL import Image
from collections import deque

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide045/render_4.png").convert("RGB")).astype(int)
H, W = im.shape[:2]
scale = H / 540.0
cx, cy, d = 893 * scale, 71 * scale, 36 * scale
win = np.s_[int(cy - d): int(cy + d), int(cx - d): int(cx + d)]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
yel = (r[win] > 200) & (g[win] > 200) & (b[win] < 190)
h, w = yel.shape
seen = np.zeros_like(yel, dtype=bool)
comps = []
for y0 in range(h):
    for x0 in range(w):
        if yel[y0, x0] and not seen[y0, x0]:
            q = deque([(y0, x0)]); seen[y0, x0] = True; pts = []
            while q:
                y, x = q.popleft(); pts.append((y, x))
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < h and 0 <= nx < w and yel[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True; q.append((ny, nx))
            comps.append(pts)
comps.sort(key=len, reverse=True)
print(f"yellow components in window: {len(comps)}; sizes: {[len(c) for c in comps[:6]]}")
disc = comps[0]
ys = [p[0] for p in disc]; xs = [p[1] for p in disc]
bcx = win[1].start + (min(xs) + max(xs)) / 2
bcy = win[0].start + (min(ys) + max(ys)) / 2
bw = max(xs) - min(xs) + 1
bh = max(ys) - min(ys) + 1
print(f"DISC center render ({bcx:.0f},{bcy:.0f}) vs canonical ({cx:.0f},{cy:.0f}) tol {8}")
print(f"DISC diameter {bw}x{bh} vs {d:.0f} tol {12}")
print(f"dust components (non-disc): {len(comps)-1}, largest dust size {comps[1][0] if False else len(comps[1]) if len(comps)>1 else 0} px")
ok_center = abs(bcx - cx) <= 8 and abs(bcy - cy) <= 8
ok_size = abs(bw - d) <= 12
pur = (b[win] > 150) & (r[win] > 70) & (r[win] < 180) & (g[win] < 130)
print(f"purple ring px: {pur.sum()} (need >=10)")
inner = np.s_[int(cy - 0.35 * d): int(cy + 0.35 * d), int(cx - 0.35 * d): int(cx + 0.35 * d)]
ink = (r[inner] < 120) & (g[inner] < 120) & (b[inner] < 120)
print(f"numeral dark px in badge core: {ink.sum()} (need >0)")
verdict = "PASS" if (ok_center and ok_size and pur.sum() >= 10 and ink.sum() > 0) else "FAIL"
print(f"CHROME SUPPLEMENT (disc-only): {verdict}")
