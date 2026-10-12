#!/usr/bin/env python3
"""Pass 3: ASCII structure maps + clean scanlines for slide 030."""
import numpy as np
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_030.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = 0.299 * R + 0.587 * G + 0.114 * B
red = (R > 130) & (G < 90) & (B < 90)
black = (R < 90) & (G < 90) & (B < 90)
dark = lum < 130
white = (R > 228) & (G > 228) & (B > 228)

def amap(mask, x0, y0, x1, y1, step, label):
    print(f"--- {label} (x{x0}..{x1}, y{y0}..{y1}, step {step}; #=mask .=other) ---")
    hdr = "     " + "".join(str(((x0 + i * step) // 10) % 10) for i in range(0, (x1 - x0) // step))
    print(hdr)
    for y in range(y0, y1, step):
        row = "".join("#" if mask[y:y+step, x:x+step].any() else "." for x in range(x0, x1, step))
        print(f"{y:4d} {row}")

# full-slide red map
amap(red, 0, 0, 960, 540, 10, "RED mask full slide")
# full-slide black map
amap(black, 0, 0, 960, 540, 10, "BLACK mask full slide")
# gray-panel map (E7E9E6-ish)
grayish = (np.abs(R - 0xE7) < 14) & (np.abs(G - 0xE9) < 14) & (np.abs(B - 0xE6) < 14)
amap(grayish, 0, 0, 960, 540, 10, "GRAY-PANEL mask full slide")

# scanline dumps
def scan_y(y, x0, x1, lbl, every=4):
    print(f"--- scan y={y} ({lbl}) ---")
    out = []
    for x in range(x0, x1, every):
        out.append(f"x{x}:#{R[y,x]:02X}{G[y,x]:02X}{B[y,x]:02X}")
    print(" ".join(out))

def scan_x(x, y0, y1, lbl, every=4):
    print(f"--- scan x={x} ({lbl}) ---")
    out = []
    for y in range(y0, y1, every):
        out.append(f"y{y}:#{R[y,x]:02X}{G[y,x]:02X}{B[y,x]:02X}")
    print(" ".join(out))

scan_y(350, 70, 500, "through left panel mid + arrow")
scan_y(350, 460, 900, "through arrow + right image")
scan_x(300, 225, 300, "left panel top edge region")
scan_x(300, 460, 490, "left panel bottom edge region")
scan_x(700, 255, 290, "right panel top edge region")
scan_x(700, 435, 460, "right panel bottom edge region")
scan_y(250, 80, 500, "left panel top border + caption row")
scan_x(90, 230, 260, "left panel top-left corner")
scan_x(890, 260, 285, "right panel top-right corner")
scan_x(480, 230, 250, "right panel top-left corner region")

# caption: black-only ink above panel? in y200..285, x80..480
cap = black.copy(); cap[:200, :] = False; cap[290:, :] = False; cap[:, :80] = False; cap[:, 480:] = False
ys, xs = np.where(cap)
print(f"caption BLACK ink: px={len(xs)}", f"bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]" if len(xs) else "NONE")
if len(xs):
    for y in range(ys.min(), ys.max() + 1, 4):
        rr = np.where(cap[y])[0]
        if len(rr): print(f"  y={y}: x{rr.min()}..{rr.max()} n={len(rr)}")

# arrow isolate: red in x485..540, y300..430 minus border col
ar = red.copy(); ar[:, :486] = False; ar[:, 545:] = False; ar[:300, :] = False; ar[432:, :] = False
ys, xs = np.where(ar)
print(f"arrow red (x486-544, y300-431): px={len(xs)}", f"bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]" if len(xs) else "NONE")
if len(xs):
    for y in range(ys.min(), ys.max() + 1, 3):
        rr = np.where(ar[y])[0]
        if len(rr): print(f"  y={y}: x{rr.min()}..{rr.max()} n={len(rr)}")
