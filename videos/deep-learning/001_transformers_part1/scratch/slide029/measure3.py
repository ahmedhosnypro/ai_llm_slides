#!/usr/bin/env python3
"""Detailed scanline forensics for slide-029 delta elements."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
A = np.asarray(Image.open(f"{V}/unique_slides/slide_029.jpg").convert("RGB"), dtype=np.int16)
B = np.asarray(Image.open(f"{V}/unique_slides/slide_026.jpg").convert("RGB"), dtype=np.int16)

def hexc(t):
    return "%02X%02X%02X" % tuple(int(round(v)) for v in t)

def runs_h(y, x0, x1, pred, img=A):
    """contiguous x-runs where pred holds"""
    row = img[y, x0:x1]
    m = pred(row)
    out = []
    s = None
    for i, v in enumerate(m):
        if v and s is None:
            s = i
        elif not v and s is not None:
            if i - s >= 2:
                out.append((x0 + s, x0 + i - 1))
            s = None
    if s is not None:
        out.append((x0 + s, x0 + len(m) - 1))
    return out

def runs_v(x, y0, y1, pred, img=A):
    col = img[y0:y1, x]
    m = pred(col)
    out = []
    s = None
    for i, v in enumerate(m):
        if v and s is None:
            s = i
        elif not v and s is not None:
            if i - s >= 2:
                out.append((y0 + s, y0 + i - 1))
            s = None
    if s is not None:
        out.append((y0 + s, y0 + len(m) - 1))
    return out

# pale cyan callout fill: b>=g>r with b-r>6, bright
palecyan = lambda p: (p[:, 2] >= p[:, 1] - 2) & (p[:, 1] > p[:, 0] + 4) & (p[:, 2] > 235)
orange = lambda p: (p[:, 0] > 225) & (p[:, 0] - p[:, 2] > 45) & (p[:, 1] - p[:, 2] > 25) & (p[:, 1] < 225)
red = lambda p: (p[:, 0] > 130) & (p[:, 0] - p[:, 1] > 60) & (p[:, 0] - p[:, 2] > 60)
white = lambda p: (p[:, 0] > 235) & (p[:, 1] > 235) & (p[:, 2] > 235)
blueink = lambda p: (p[:, 2] > 130) & (p[:, 2] - p[:, 0] > 55) & (p[:, 2] - p[:, 1] > 45)

print("== CALLOUT 1 (pale-cyan runs at several y) ==")
for y in [145, 150, 160, 170, 180, 185]:
    print(f" y{y}: {runs_h(y, 100, 940, palecyan)}")
print(" vertical extent at x=350:", runs_v(350, 120, 230, palecyan))
print(" vertical extent at x=700:", runs_v(700, 120, 230, palecyan))

print("\n== CALLOUT text ink (darkest) ==")
reg = A[140:195, 315:520].reshape(-1, 3)
i = reg.sum(axis=1).argmin(); print(" callout1 darkest:", hexc(reg[i]))
reg = A[140:195, 600:860].reshape(-1, 3)
i = reg.sum(axis=1).argmin(); print(" callout2 darkest:", hexc(reg[i]))

print("\n== QUERY BOX (orange runs) ==")
for y in [418, 425, 435, 445, 452, 458]:
    print(f" y{y}: {runs_h(y, 90, 560, orange)}")
print(" vertical x=150:", runs_v(150, 400, 475, orange))
print(" vertical x=250:", runs_v(250, 400, 475, orange))
reg = A[415:465, 100:250].reshape(-1, 3)
i = reg.sum(axis=1).argmin(); print(" querybox darkest (text):", hexc(reg[i]))

print("\n== red things y405..540 x90..560 ==")
for y in [410, 420, 430, 440, 450, 460, 465, 470, 480, 490, 500, 510, 520, 530]:
    print(f" y{y}: {runs_h(y, 90, 560, red)}")

print("\n== Q badge hunt (red blobs y400..475 x240..560) ==")
reg = A[400:475, 240:560]
m = (reg[:, :, 0] > 130) & (reg[:, :, 0] - reg[:, :, 1] > 60) & (reg[:, :, 0] - reg[:, :, 2] > 60)
ys, xs = np.nonzero(m)
if len(xs):
    print(" red bbox in region:", 240 + xs.min(), 400 + ys.min(), 240 + xs.max(), 400 + ys.max())
    # cluster columns
    cols = np.unique(xs + 240)
    print(" red cols:", cols.min(), "..", cols.max())

print("\n== RESULT BOX ==")
print(" white runs y440..500 x540..900:")
for y in [435, 440, 450, 460, 470, 480, 490, 495]:
    print(f" y{y}: {runs_h(y, 540, 900, white)}")
print(" blue ink runs:")
for y in [435, 445, 455, 465, 475, 485, 492]:
    print(f" y{y}: {runs_h(y, 540, 900, blueink)}")
print(" vertical white x=650:", runs_v(650, 410, 530, white))
reg = A[430:505, 560:830].reshape(-1, 3)
i = reg.sum(axis=1).argmin(); print(" resultbox darkest (text):", hexc(reg[i]))

print("\n== K / V badges detail ==")
for name, (x0, y0, x1, y1) in {"K": (145, 325, 182, 362), "V": (730, 325, 766, 362)}.items():
    reg = A[y0:y1, x0:x1]
    m = (reg[:, :, 0] > 130) & (reg[:, :, 0] - reg[:, :, 1] > 60) & (reg[:, :, 0] - reg[:, :, 2] > 60)
    ys, xs = np.nonzero(m)
    print(f" {name}: bbox x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()}")
    # center row/col
    cx, cy = (x0 + xs.min() + x0 + xs.max()) // 2, (y0 + ys.min() + y0 + ys.max()) // 2
    print(f"   center ({cx},{cy}) horiz extent at cy: {runs_h(cy, x0, x1, lambda p: (p[:,0]>130)&(p[:,0]-p[:,1]>60)&(p[:,0]-p[:,2]>60))}")
    # letter pixel (interior non-red)
    inner = A[cy - 5:cy + 5, cx - 5:cx + 5].reshape(-1, 3)
    i = inner.sum(axis=1).argmin(); print(f"   darkest near center: {hexc(inner[i])}")

print("\n== title y45..105 ==")
yellow = lambda p: (p[:, 0] > 215) & (p[:, 1] > 205) & (p[:, 2] < 190) & (p[:, 0] - p[:, 2] > 40)
print(" highlight runs y=60:", runs_h(60, 100, 870, yellow), " y=70:", runs_h(70, 100, 870, yellow))
darkink = lambda p: p.sum(axis=1) < 240
print(" title ink runs y=58:", runs_h(58, 100, 870, darkink)[:6])
print(" vertical ink x=200 (title L1):", runs_v(200, 40, 105, darkink))
print(" subtitle ink runs y=90:", runs_h(90, 100, 870, darkink)[:8])
print(" subtitle vertical x=600:", runs_v(600, 75, 108, darkink))
redsub = lambda p: (p[:, 0] > 100) & (p[:, 0] - p[:, 1] > 60) & (p[:, 0] - p[:, 2] > 50)
print(" subtitle red runs y=90:", runs_h(90, 100, 870, redsub)[:8])
print(" subtitle red vertical x=205:", runs_v(205, 75, 108, redsub))
