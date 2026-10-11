#!/usr/bin/env python3
"""PIL measurement of the original slide_001.jpg frame (ground truth).
Prints ink bboxes per color class, in px, %, and inches (13.33x7.5in slide).
"""
import json, sys
from PIL import Image

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_001.jpg"
im = Image.open(IMG).convert("RGB")
W, H = im.size
px = im.load()
print(f"image size: {W}x{H}  (1px = {13.33/W:.4f}in horiz, {7.5/H:.4f}in vert)")

def classify(r, g, b):
    # red text/frame: red dominant
    if r > 120 and g < 90 and b < 90 and (r - max(g, b)) > 60:
        return "red"
    # blue text: blue dominant
    if b > 100 and b - r > 60 and b - g > 40:
        return "blue"
    # teal (logo): g and b similar, both > r
    if g > 90 and b > 90 and abs(g - b) < 45 and (g - r) > 30 and (b - r) > 20:
        return "teal"
    # yellow (badge fill): r,g high, b low
    if r > 200 and g > 200 and b < 160 and (r - b) > 70:
        return "yellow"
    # purple/violet outline: r and b mid-high, g low
    if r > 80 and b > 120 and b - g > 40 and r - g > 20 and r < 180:
        return "purple"
    return None

# collect per-class pixels
boxes = {}
counts = {}
for y in range(H):
    for x in range(W):
        c = classify(*px[x, y])
        if c:
            counts[c] = counts.get(c, 0) + 1
            b = boxes.setdefault(c, [x, y, x, y])
            if x < b[0]: b[0] = x
            if y < b[1]: b[1] = y
            if x > b[2]: b[2] = x
            if y > b[3]: b[3] = y

def in_box(b):
    return [round(b[0]*13.33/W, 3), round(b[1]*7.5/H, 3),
            round((b[2]-b[0]+1)*13.33/W, 3), round((b[3]-b[1]+1)*7.5/H, 3)]

def pct_box(b):
    return [round(100*b[0]/W, 1), round(100*b[1]/H, 1),
            round(100*(b[2]-b[0]+1)/W, 1), round(100*(b[3]-b[1]+1)/H, 1)]

print("\n== coarse class bboxes (px / inches / %) ==")
for c, b in sorted(boxes.items()):
    print(f"{c:7s} n={counts[c]:6d} px={b} in={in_box(b)} pct={pct_box(b)}")

# --- row-band clustering per class (split blocks by empty rows) ---
def bands(cls, gap=3):
    b = boxes.get(cls)
    if not b: return []
    rows = []
    for y in range(b[1], b[3]+1):
        n = sum(1 for x in range(b[0], b[2]+1) if classify(*px[x, y]) == cls)
        rows.append((y, n))
    out = []
    cur = None
    for y, n in rows:
        if n > 0:
            if cur is None: cur = [y, y]
            else: cur[1] = y
        else:
            if cur and (y - cur[1]) > gap:
                out.append(tuple(cur)); cur = None
    if cur: out.append(tuple(cur))
    return out

def xband(cls, y0, y1, gap=8):
    """column bands within a row band"""
    b = boxes.get(cls)
    if not b: return []
    cols = []
    for x in range(b[0], b[2]+1):
        n = sum(1 for y in range(y0, y1+1) if classify(*px[x, y]) == cls)
        cols.append((x, n))
    out = []
    cur = None
    for x, n in cols:
        if n > 0:
            if cur is None: cur = [x, x]
            else: cur[1] = x
        else:
            if cur and (x - cur[1]) > gap:
                out.append(tuple(cur)); cur = None
    if cur: out.append(tuple(cur))
    return out

print("\n== red row-bands (title, labels, frame excluded later) ==")
for y0, y1 in bands("red"):
    xs = xband("red", y0, y1)
    print(f"red band y={y0}-{y1} (in {y0*7.5/H:.2f}-{(y1+1)*7.5/H:.2f}) xsegs={xs}")

print("\n== blue row-bands ==")
for y0, y1 in bands("blue"):
    xs = xband("blue", y0, y1)
    print(f"blue band y={y0}-{y1} (in {y0*7.5/H:.2f}-{(y1+1)*7.5/H:.2f}) xsegs={xs}")

print("\n== teal row-bands (logo) ==")
for y0, y1 in bands("teal"):
    xs = xband("teal", y0, y1)
    print(f"teal band y={y0}-{y1} (in {y0*7.5/H:.2f}-{(y1+1)*7.5/H:.2f}) xsegs={xs}")

print("\n== yellow bands (badge fill) ==")
for y0, y1 in bands("yellow"):
    xs = xband("yellow", y0, y1)
    print(f"yellow band y={y0}-{y1} (in {y0*7.5/H:.2f}-{(y1+1)*7.5/H:.2f}) xsegs={xs}")

print("\n== purple bands (badge outline) ==")
for y0, y1 in bands("purple"):
    xs = xband("purple", y0, y1)
    print(f"purple band y={y0}-{y1} (in {y0*7.5/H:.2f}-{(y1+1)*7.5/H:.2f}) xsegs={xs}")

# --- color samples ---
def sample(name, x, y):
    print(f"sample {name} @({x},{y}) = {px[x,y]} #{px[x,y][0]:02X}{px[x,y][1]:02X}{px[x,y][2]:02X}")

print("\n== color samples ==")
sample("outside frame (white margin)", 5, 5)
sample("inside frame (canvas)", W//2, 10)
# canvas: pick a point clearly inside frame but away from content
sample("canvas mid-left", int(0.08*W), int(0.5*H))
sample("red frame stroke top", W//2, int(0.035*H))
