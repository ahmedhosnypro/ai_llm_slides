#!/usr/bin/env python3
"""Probe round 2: feed curves fate, right edge, remaining colors."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
A = np.asarray(Image.open(f"{V}/unique_slides/slide_029.jpg").convert("RGB"), dtype=np.int16)
B = np.asarray(Image.open(f"{V}/unique_slides/slide_026.jpg").convert("RGB"), dtype=np.int16)

def px(img, x, y):
    return "%02X%02X%02X" % tuple(int(v) for v in img[y, x])

print("== right-edge canvas check ==")
for pt in [(880, 300), (880, 460), (875, 120), (890, 250), (930, 300), (940, 100)]:
    print(f" ({pt[0]},{pt[1]}) child {px(A,*pt)} parent {px(B,*pt)}")

print("\n== right feed-curve fate (child vs parent, x480..940 y380..540) ==")
# find pixels that are 'curvy' (non-canvas, non-white, non-peach-family) in each
def curve_mask(img):
    r = img[:, :, 0].astype(int); g = img[:, :, 1].astype(int); b = img[:, :, 2].astype(int)
    canvas = (r > 230) & (g > 205) & (b > 180) & (b < 230) & (r - b > 20)
    white = (r > 235) & (g > 235) & (b > 235)
    dark_txt = (r + g + b < 300)
    red = (r > 130) & (r - g > 60) & (r - b > 60)
    green = (g > 100) & (g - r > 30) & (g - b > 20)
    blue = (b > 120) & (b - r > 50) & (b - g > 40)
    return (red | green) & ~canvas

for tag, img in [("child", A), ("parent", B)]:
    m = curve_mask(img[380:540, 480:945])
    ys, xs = np.nonzero(m)
    pts = sorted(zip(xs + 480, ys + 380))
    # cluster into blobs
    print(f" {tag}: {len(pts)} red/green px in region")
    if pts:
        segs = {}
        for x, y in pts:
            segs.setdefault(y // 10, []).append((x, y))
        for k in sorted(segs):
            xs_ = [p[0] for p in segs[k]]
            print(f"   y{ k*10 }..{k*10+9}: x {min(xs_)}..{max(xs_)} n={len(xs_)}")

print("\n== left curve path child (red?) ==")
for pt in [(170, 471), (150, 470), (130, 468), (120, 464), (104, 448), (102, 430), (102, 415)]:
    print(f" ({pt[0]},{pt[1]}) child {px(A,*pt)} parent {px(B,*pt)}")

print("\n== strip-end diffs ==")
for pt in [(497, 494), (500, 493), (510, 493), (530, 492), (175, 471), (172, 470)]:
    print(f" ({pt[0]},{pt[1]}) child {px(A,*pt)} parent {px(B,*pt)}")

print("\n== thin red query arrow (parent x298 y406..473) in child ==")
for y in [410, 420, 430, 440, 450, 460, 468, 472]:
    print(f" (298,{y}) child {px(A,298,y)} parent {px(B,298,y)}")

print("\n== chunky diagonal arrow (parent 266,526 -> 284,512) in child ==")
for pt in [(268, 522), (274, 518), (280, 514), (284, 512)]:
    print(f" ({pt[0]},{pt[1]}) child {px(A,*pt)} parent {px(B,*pt)}")

print("\n== tan label box fills (clean corners) ==")
print(" KEYs (66..74,207..212):", "%02X%02X%02X" % tuple(A[207:212, 66:74].reshape(-1, 3).mean(axis=0).astype(int)))
print(" KEYs (120..130,192..196):", "%02X%02X%02X" % tuple(A[192:196, 120:130].reshape(-1, 3).mean(axis=0).astype(int)))
print(" Values (746..756,210..215):", "%02X%02X%02X" % tuple(A[210:215, 746:756].reshape(-1, 3).mean(axis=0).astype(int)))
print(" Values (815..825,190..196):", "%02X%02X%02X" % tuple(A[190:196, 815:825].reshape(-1, 3).mean(axis=0).astype(int)))

print("\n== result box border profile (top edge x=650, y429..438) ==")
for y in range(429, 439):
    print(f" y{y}: {px(A,650,y)}")
print(" left edge y=465, x553..562:")
for x in range(553, 563):
    print(f" x{x}: {px(A,x,465)}")

print("\n== callout border profile (c1 left edge y=165, x312..320; c1 top x=400 y138..145) ==")
for x in range(312, 321):
    print(f" x{x}: {px(A,x,165)}")
for y in range(138, 146):
    print(f" y{y}: {px(A,400,y)}")

print("\n== query box border profile (top x=170 y417..424; left y=440 x107..114) ==")
for y in range(417, 425):
    print(f" y{y}: {px(A,170,y)}")
for x in range(107, 115):
    print(f" x{x}: {px(A,x,440)}")

print("\n== K badge ring check: row y=342 x148..178 ==")
print(" ".join(px(A, x, 342) for x in range(148, 179, 2)))
print("== Q badge: row y=439 x244..274 ==")
print(" ".join(px(A, x, 439) for x in range(244, 275, 2)))

print("\n== title/subtitle vertical ink profile ==")
col = A[50:105, 200]
print(" x=200 y50..104:", " ".join("%02X%02X%02X" % tuple(int(v) for v in col[i]) for i in range(0, 55, 3)))
print("\n== subtitle: black vs red token map (y84..96) ==")
redsub = lambda reg: (reg[:, :, 0] > 110) & (reg[:, :, 0] - reg[:, :, 1] > 55) & (reg[:, :, 0] - reg[:, :, 2] > 45)
darkp = lambda reg: reg.sum(axis=2) < 300
reg = A[82:100, 100:840]
dcols = np.nonzero(darkp(reg).sum(axis=0) > 0)[0] + 100
def runs(cols, gap=8):
    out = []
    if len(cols) == 0: return out
    s = p = cols[0]
    for c in cols[1:]:
        if c - p > gap:
            out.append((s, p)); s = c
        p = c
    out.append((s, p)); return out
print(" all-ink word runs:", runs(dcols, 6))
