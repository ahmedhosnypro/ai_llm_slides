#!/usr/bin/env python3
"""m7_scan.py - dec mid A&N 1px dump + A&N text colors + enc FF border check."""
from PIL import Image
import collections
IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg").convert("RGB")
px = IM.load()

print("== dec mid compartment rows 249-265, x746-842 (every 2nd px) ==")
for y in range(249, 266):
    row = []
    for x in range(746, 843, 2):
        r, g, b = px[x, y]
        if b > r + 30 and b > 140: k = "B"   # steel blue
        elif g > 150 and g > r + 25 and g > b + 60 and r > 60: k = "V"
        elif abs(r-176) < 25 and abs(g-184) < 25 and abs(b-144) < 30: k = "o"
        elif r + g + b < 240: k = "D"
        elif r > 200 and g > 200 and b < 120: k = "Y"
        else: k = "."
        row.append(k)
    print(f"{y:3d} {''.join(row)}")

print("\n== A&N text dark modes ==")
def dark_modes(x0, y0, x1, y1, thresh=300):
    cnt = collections.Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = px[x, y]
            if sum(c) < thresh: cnt[c] += 1
    return cnt.most_common(6)
print("enc top A&N text (658,273)-(720,287):", dark_modes(658, 273, 720, 287))
print("enc mid A&N text (658,344)-(716,354):", dark_modes(658, 344, 716, 354))
print("dec top A&N text (756,208)-(816,219):", dark_modes(756, 208, 816, 219))
print("dec purple A&N text (753,331)-(815,342):", dark_modes(753, 331, 815, 342))
print("gray callout text row (330,150)-(500,164) 200:", dark_modes(330, 150, 500, 164, 200))

print("\n== enc FF box border scan row y300 x645-728 ==")
print([px[x, 300] for x in range(645, 729, 4)])
print("== enc FF top/bottom edges x685 ==")
print("y287-292:", [px[685, y] for y in range(287, 293)])
print("y313-317:", [px[685, y] for y in range(313, 318)])
print("\n== dec FF box edges x780 ==")
print("y219-223:", [px[780, y] for y in range(219, 224)])
print("y248-251:", [px[780, y] for y in range(248, 252)])
print("left edge y235 x744-758:", [px[x, 235] for x in range(744, 759, 2)])
print("right edge y235 x814-826:", [px[x, 235] for x in range(814, 827, 2)])
