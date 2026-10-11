#!/usr/bin/env python3
"""Forensics 2: connected components of color masks on original slide_041.jpg."""
from PIL import Image
import sys
sys.setrecursionlimit(10000)

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_041.jpg"
im = Image.open(ORIG).convert("RGB")
W, H = im.size
px = im.load()

def near(c, t, tol=40):
    return all(abs(c[i] - t[i]) <= tol for i in range(3))

MASKS = {
    "red_borders":  ((190, 40, 40), 60),      # CC0000-ish
    "blue_ankn":    ((110, 150, 178), 45),    # blue-gray Add&Norm (6E95B2 / 6990AF)
    "olive":        ((125, 121, 21), 45),     # olive/dark-yellow (7D7915, 767F22)
    "tan_mha":      ((197, 123, 84), 38),     # encoder MHA fill (C57B58/C07B54)
    "yellow":       ((250, 255, 60), 60),     # FFFF00-ish
    "purple":       ((179, 157, 219), 40),    # B39DDB masked MHA
    "gray_block":   ((168, 168, 168), 28),    # A8A8A8
    "brown_emb":    ((200, 154, 106), 35),    # C89A6A input embedding
    "maroon_emb":   ((139, 74, 74), 35),      # 8B4A4A output embedding
    "ltgreen":      ((168, 232, 168), 35),    # A8E8A8 linear/softmax
}

def components(mask, min_px=30):
    """simple BFS connected components; returns list of (n, bbox, sample_center_color)"""
    seen = set()
    comps = []
    pts = list(mask.keys())
    for p in pts:
        if p in seen:
            continue
        stack = [p]; seen.add(p)
        comp = []
        while stack:
            x, y = stack.pop()
            comp.append((x, y))
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    q = (x + dx, y + dy)
                    if q in mask and q not in seen:
                        seen.add(q); stack.append(q)
        if len(comp) >= min_px:
            xs = [c[0] for c in comp]; ys = [c[1] for c in comp]
            cx, cy = sum(xs) // len(comp), sum(ys) // len(comp)
            comps.append((len(comp), (min(xs), min(ys), max(xs), max(ys)), px[cx, cy]))
    comps.sort(reverse=True)
    return comps

# region windows
PANEL = (575, 104, 897, 527)     # right panel incl border
ZOOM  = (286, 196, 524, 527)     # center zoom
SCHM  = (55, 265, 196, 496)      # left schematic

for name, (target, tol) in MASKS.items():
    for rname, (x0, y0, x1, y1) in (("PANEL", PANEL), ("ZOOM", ZOOM), ("SCHM", SCHM)):
        mask = {}
        for y in range(y0, y1):
            for x in range(x0, x1):
                c = px[x, y]
                if near(c, target, tol):
                    mask[(x, y)] = True
        if not mask:
            continue
        comps = components(mask, min_px=25)
        if not comps:
            continue
        print(f"== {name} @ {rname}: total {len(mask)} px, {len(comps)} comps")
        for n, bb, cc in comps[:14]:
            print(f"   n={n:6d} bbox x{bb[0]}..{bb[2]} y{bb[1]}..{bb[3]}  ctr=#{cc[0]:02X}{cc[1]:02X}{cc[2]:02X}")
