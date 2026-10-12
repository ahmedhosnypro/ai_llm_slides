#!/usr/bin/env python3
"""Flood-fill bbox + median fill measurement for slide_026 blocks."""
from PIL import Image
import statistics

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg').convert('RGB')
W, H = im.size
px = im.load()

def lum(c):
    return 0.299*c[0] + 0.587*c[1] + 0.114*c[2]

def flood_bbox(seed, tol=14, max_px=400000):
    sc = px[seed[0], seed[1]]
    seen = set([seed])
    stack = [seed]
    minx = maxx = seed[0]; miny = maxy = seed[1]
    fills = []
    n = 0
    while stack and n < max_px:
        x, y = stack.pop()
        n += 1
        minx = min(minx, x); maxx = max(maxx, x)
        miny = min(miny, y); maxy = max(maxy, y)
        c = px[x, y]
        if lum(c) > 170:
            fills.append(c)
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            p = (x+dx, y+dy)
            if p in seen or not (0 <= p[0] < W and 0 <= p[1] < H):
                continue
            c2 = px[p[0], p[1]]
            if all(abs(c2[i]-sc[i]) <= tol for i in range(3)):
                seen.add(p)
                stack.append(p)
    med = None
    if fills:
        med = tuple(int(statistics.median([f[i] for f in fills])) for i in range(3))
    return (n, minx, miny, maxx, maxy, med, sc)

seeds = {
    'blue_box': (300, 245),
    'subblock1': (250, 262),
    'subblock2': (250, 312),
    'subblock3': (250, 362),
    'host_box': (403, 265),
    'tida_container': (500, 210),
    'encoder_conn': (655, 290),
    'right_panel_inside': (710, 225),
    'diff_box': (745, 255),
    'dual_adc': (487, 252),
    'power_supplies': (490, 425),
    'v24_box': (418, 430),
    'sincos_box': (745, 452),
    'box16bit': (465, 222),
    'analog_path_box': (460, 325),
}
for name, seed in seeds.items():
    n, x0, y0, x1, y1, med, sc = flood_bbox(seed)
    print(f"{name:20s} seed{seed} bbox=({x0},{y0})..({x1},{y1}) n={n} fill={med} seedc={sc}")
