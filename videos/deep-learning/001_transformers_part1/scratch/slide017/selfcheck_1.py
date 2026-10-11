#!/usr/bin/env python3
"""Closed-loop self-check: render (2001x1125) vs original frame (960x540).
Downscales the render to 960x540 and re-runs the key measurements:
callout boxes, title extent, panel fills, node bands, circle positions."""
import numpy as np
from PIL import Image

REN = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide017/render_1.png'
ORIG = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg'

r = Image.open(REN).convert('RGB').resize((960, 540), Image.LANCZOS)
R = np.asarray(r).astype(int)
O = np.asarray(Image.open(ORIG).convert('RGB')).astype(int)

def mask_comp(A, test, x0, x1, y0, y1, min_px=40):
    from collections import deque
    H, W = A.shape[:2]
    seen = np.zeros((H, W), dtype=bool)
    best = None
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            if seen[y, x] or not test(*A[y, x]):
                continue
            q = deque([(y, x)]); seen[y, x] = True; n = 0
            bx0, by0, bx1, by1 = x, y, x, y
            while q:
                cy, cx = q.popleft(); n += 1
                bx0 = min(bx0, cx); bx1 = max(bx1, cx); by0 = min(by0, cy); by1 = max(by1, cy)
                for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    ny, nx = cy+dy, cx+dx
                    if y0 <= ny <= y1 and x0 <= nx <= x1 and not seen[ny, nx] and test(*A[ny, nx]):
                        seen[ny, nx] = True; q.append((ny, nx))
            if n >= min_px:
                if best is None or n > best[0]:
                    best = (n, bx0, by0, bx1, by1)
    return best

def yellowish(r, g, b): return r > 200 and g > 200 and b < 200
def pinkish(r, g, b): return r > 200 and 130 < g < 210 and b > 200
def tanish(r, g, b): return 190 < r < 240 and 170 < g < 220 and 150 < b < 205 and r > g > b

print("== callout boxes (render vs orig) ==")
for name, test, region in [
    ("callout1", yellowish, (60, 60, 580, 300)),
    ("callout2", pinkish, (60, 60, 580, 320)),
    ("callout3", tanish, (60, 300, 580, 430)),
    ("callout4", tanish, (60, 430, 580, 540)),
]:
    cr = mask_comp(R, test, *region)
    co = mask_comp(O, test, *region)
    print(f"  {name}: render {cr}  orig {co}")

def red_extent(A, x0, x1, y0, y1):
    xs, ys = [], []
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            rr, gg, bb = A[y, x]
            if rr > 130 and gg < 120 and bb < 120 and rr-gg > 50:
                xs.append(x); ys.append(y)
    return (min(xs), max(xs), min(ys), max(ys)) if xs else None

print("title: render", red_extent(R, 150, 820, 40, 100), " orig", red_extent(O, 150, 820, 40, 100))

# panel fill samples
def avg(A, x0, y0, x1, y1):
    rr = A[y0:y1+1, x0:x1+1].reshape(-1, 3)
    return tuple(int(v) for v in rr.mean(axis=0))
print("enc panel: render", avg(R, 590, 200, 600, 210), " orig", avg(O, 590, 200, 600, 210))
print("dec panel: render", avg(R, 880, 200, 890, 210), " orig", avg(O, 880, 200, 890, 210))
print("margin:    render", avg(R, 20, 300, 30, 310), " orig", avg(O, 20, 300, 30, 310))

# containment: any ink outside the house content zone (x>42/72*... in 960-space: panel x42..918, content inside)
H, W = R.shape[:2]
viol = 0
for y in range(0, H):
    for x in range(0, W):
        rr, gg, bb = R[y, x]
        ink = not (rr > 240 and gg > 240 and bb > 240)
        if ink and (x < 40 or x > 920):
            viol += 1
print("ink pixels outside white margin x[40,920]:", viol)
