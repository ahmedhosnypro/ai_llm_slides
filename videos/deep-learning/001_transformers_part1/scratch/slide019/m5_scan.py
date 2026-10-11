#!/usr/bin/env python3
"""m5_scan.py - circle blobs via connected components + FF fill exact + leader isolation."""
from PIL import Image
import collections

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg").convert("RGB")
px = IM.load()

def sat_class(c):
    r, g, b = c
    if g > 100 and g > r + 30 and g > b + 30: return "green"
    if b > 90 and b > r + 40 and g < b: return "blue"
    if r > 110 and r > g + 55 and r > b + 55: return "red"
    return None

def blobs(x0, y0, x1, y1, label):
    seen = set()
    out = []
    for yy in range(y0, y1):
        for xx in range(x0, x1):
            if (xx, yy) in seen: continue
            k = sat_class(px[xx, yy])
            if not k: continue
            stack = [(xx, yy)]; comp = []
            seen.add((xx, yy))
            while stack:
                cx, cy = stack.pop()
                comp.append((cx, cy))
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = cx + dx, cy + dy
                        if (nx, ny) in seen or not (x0 <= nx < x1 and y0 <= ny < y1): continue
                        if sat_class(px[nx, ny]) == k:
                            seen.add((nx, ny)); stack.append((nx, ny))
            if len(comp) >= 25:
                xs = [p[0] for p in comp]; ys = [p[1] for p in comp]
                cnt = collections.Counter(px[p] for p in comp)
                out.append((k, len(comp), (min(xs), min(ys), max(xs), max(ys)),
                            (sum(xs)//len(comp), sum(ys)//len(comp)), cnt.most_common(3)))
    print(f"\n== {label} ==")
    for k, n, bb, ctr, modes in sorted(out, key=lambda t: t[3]):
        print(f"{k:5s} n={n:4d} bbox={bb} ctr={ctr} modes={modes}")

blobs(630, 382, 745, 418, "ENC circles band y382-418")
blobs(735, 372, 845, 408, "DEC-MASKED circles band y372-408")
blobs(730, 300, 845, 330, "DEC-CROSS circles band y300-330")

def mode_all(x0, y0, x1, y1, topn=6):
    cnt = collections.Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            cnt[px[x, y]] += 1
    return cnt.most_common(topn)

print("\n== FF fills (all modes) ==")
print("enc FF (660,295)-(714,312):", mode_all(660, 295, 714, 312, 6))
print("dec FF (758,224)-(816,247):", mode_all(758, 224, 816, 247, 6))
print("\n== enc A&N boxes: border check ==")
print("enc top A&N row y272 x650-730:", [px[x, 272] for x in range(650, 731, 8)])
print("enc top A&N row y288 x650-730:", [px[x, 288] for x in range(650, 731, 8)])
print("dec top A&N row y204 x750-842:", [px[x, 204] for x in range(750, 843, 8)])
print("\n== L2 leader isolation x517-570 y150-180 ==")
for y in range(150, 181):
    xs = [x for x in range(517, 570) if sum(px[x, y]) < 690]
    if xs: print(f"y={y}: {min(xs)}..{max(xs)} n={len(xs)} {px[xs[0], y]}")
print("\n== L3 tail x517-570 y235-262 ==")
for y in range(235, 263):
    xs = [x for x in range(517, 570) if sum(px[x, y]) < 690]
    if xs: print(f"y={y}: {min(xs)}..{max(xs)} n={len(xs)} {px[xs[0], y]}")
print("\n== L1 start check x345-460 y112-125 ==")
for y in range(112, 126):
    xs = [x for x in range(345, 460) if sum(px[x, y]) < 700]
    if xs: print(f"y={y}: {min(xs)}..{max(xs)} n={len(xs)} {px[xs[0], y]}")
