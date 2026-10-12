#!/usr/bin/env python3
"""PIL: count circle-x nodes, W_v column rows, ovals, pills, bottom strip cells, legend parts."""
from PIL import Image
import numpy as np
from scipy import ndimage

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)

def cc(mask, min_area=30):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < min_area: continue
        out.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), len(xs)))
    return sorted(out, key=lambda b: (b[1], b[0]))

# 1) red circle-x nodes in the h1 right zone (x400..545, y300..460): red rings
print("== red rings (tensor nodes) x400..545 y300..470 ==")
red = (a[:, :, 0] > 140) & (a[:, :, 1] < 120) & (a[:, :, 2] < 120)
sub = np.zeros_like(red); sub[300:470, 400:545] = red[300:470, 400:545]
for b in cc(sub, 40): print("  ", b)

# 2) gold column rows: scan x=515 vertically y300..430
print("\n== gold column x497..534: vertical profile at x=515 ==")
col = a[300:430, 515]
prev = None
for y in range(130):
    r, g, b = col[y]
    key = (r // 30, g // 30, b // 30)
    if key != prev:
        print(f"  y={y+300}: #{r:02X}{g:02X}{b:02X}")
        prev = key

# 3) K column rows: scan x=153 vertically y300..430
print("\n== K gold column x135..172: vertical profile at x=153 ==")
col = a[300:430, 153]
prev = None
for y in range(130):
    r, g, b = col[y]
    key = (r // 30, g // 30, b // 30)
    if key != prev:
        print(f"  y={y+300}: #{r:02X}{g:02X}{b:02X}")
        prev = key

# 4) white ovals in pills band y270..320 x250..545
print("\n== white ovals y268..320 x250..545 ==")
white = (a[:, :, 0] > 225) & (a[:, :, 1] > 215) & (a[:, :, 2] > 215)
sub = np.zeros_like(white); sub[268:320, 250:545] = white[268:320, 250:545]
for b in cc(sub, 60): print("  ", b)

# 5) ovals on rear cards y180..270 x430..780
print("\n== white ovals y178..270 x430..790 (rear heads) ==")
sub = np.zeros_like(white); sub[178:270, 430:790] = white[178:270, 430:790]
for b in cc(sub, 50): print("  ", b)

# 6) bottom strip: cells + magenta cell bbox
print("\n== magenta cell bbox (x150..400, y470..515) ==")
mag = (a[:, :, 0] > 180) & (a[:, :, 1] < 160) & (a[:, :, 2] > 140) & (a[:, :, 2] < 230)
sub = np.zeros_like(mag); sub[470:515, 150:400] = mag[470:515, 150:400]
for b in cc(sub, 30): print("  ", b)

# 7) legend structure: green dashes bbox + inner boxes
print("\n== legend green dashed border bbox (x700..920, y425..515) ==")
grn = (np.abs(a - np.array([0, 176, 80])).max(axis=2) <= 90) & (a[:, :, 1] > a[:, :, 0] + 30) & (a[:, :, 1] > a[:, :, 2] + 20)
sub = np.zeros_like(grn); sub[425:515, 700:920] = grn[425:515, 700:920]
for b in cc(sub, 20)[:12]: print("  ", b)

# 8) W_q red box: red-ish box x250..320 y440..480
print("\n== red box (W_q) candidates x230..340 y430..485 ==")
sub = np.zeros_like(red); sub[430:485, 230:340] = red[430:485, 230:340]
for b in cc(sub, 40)[:8]: print("  ", b)

# 9) swoosh thick red curve bbox (already have) + blue label bbox precise
print("\n== blue label bbox (x580..870, y360..470) ==")
blue = (a[:, :, 2] > 120) & (a[:, :, 2] > a[:, :, 0] + 40) & (a[:, :, 1] < a[:, :, 2])
sub = np.zeros_like(blue); sub[360:470, 580:870] = blue[360:470, 580:870]
for b in cc(sub, 25)[:10]: print("  ", b)

# 10) q strip: red bar near x205..260 y465..480?
print("\n== red bar (q vector) x180..280 y455..485 ==")
sub = np.zeros_like(red); sub[455:485, 180:280] = red[455:485, 180:280]
for b in cc(sub, 30)[:8]: print("  ", b)

# 11) Similarity/Probabilities/WeightedSUM pill positions via white cc in y270..320 done above.
# 12) Scaling + Softmax pill fills: sample columns x285, x300, x320, x340, x360 at y=380
print("\n== pill fills at y380: x=280..370 ==")
for x in range(280, 372, 6):
    print(f"  x={x}: #%02X%02X%02X" % tuple(a[380, x]))
