#!/usr/bin/env python3
"""Self-check 2: structural masks on the downscaled render vs original."""
import numpy as np
from PIL import Image
from collections import deque

REN = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide017/render_1.png'
ORIG = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg'
R = np.asarray(Image.open(REN).convert('RGB').resize((960, 540), Image.LANCZOS)).astype(int)
O = np.asarray(Image.open(ORIG).convert('RGB')).astype(int)

def biggest(A, test, x0, x1, y0, y1, min_px=40):
    H, W = A.shape[:2]
    seen = np.zeros((H, W), dtype=bool)
    best = None
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if seen[y, x] or not test(*A[y, x]):
                continue
            q = deque([(y, x)]); seen[y, x] = True; n = 0
            bx0 = by0 = 10**9; bx1 = by1 = -1
            while q:
                cy, cx = q.popleft(); n += 1
                bx0 = min(bx0, cx); bx1 = max(bx1, cx); by0 = min(by0, cy); by1 = max(by1, cy)
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = cy + dy, cx + dx
                    if y0 <= ny <= y1 and x0 <= nx <= x1 and not seen[ny, nx] and test(*A[ny, nx]):
                        seen[ny, nx] = True; q.append((ny, nx))
            if n >= min_px and (best is None or n > best[0]):
                best = (n, bx0, by0, bx1, by1)
    return best

yellowish = lambda r, g, b: r > 200 and g > 200 and b < 200
pinkish = lambda r, g, b: r > 200 and 130 < g < 215 and b > 200
tanish = lambda r, g, b: 185 < r < 245 and 165 < g < 225 and 145 < b < 210 and r > g > b
olive = lambda r, g, b: 140 < r < 215 and 140 < g < 215 and 60 < b < 150 and abs(r - g) < 30
purpleish = lambda r, g, b: 150 < r < 230 and 100 < g < 175 and 175 < b < 245
maroonish = lambda r, g, b: 150 < r < 215 and 75 < g < 140 and 75 < b < 135 and r - g > 45
blueish = lambda r, g, b: b > 110 and b - r > 40 and b - g > 25

print(f"{'element':22s} {'render bbox':30s} {'orig bbox':30s}")
for name, test, box in [
    ("callout1_yellow", yellowish, (60, 580, 60, 300)),
    ("callout2_pink", pinkish, (60, 580, 60, 320)),
    ("callout3_tan", tanish, (60, 580, 300, 430)),
    ("callout4_tan", tanish, (60, 580, 430, 539)),
    ("enc_container_tan", tanish, (575, 745, 240, 420)),
    ("dec_stack_olive", olive, (740, 845, 190, 310)),
    ("dec_purple", purpleish, (740, 845, 320, 412)),
    ("dec_maroon", maroonish, (740, 845, 412, 485)),
]:
    cr = biggest(R, test, *box)
    co = biggest(O, test, *box)
    f = lambda c: "None" if c is None else f"x{c[1]}..{c[3]} y{c[2]}..{c[4]}"
    print(f"{name:22s} {f(cr):30s} {f(co):30s}")

# circle positions (render vs orig)
def circles(A, x0, x1, y0, y1):
    out = []
    for t, nm in ((blueish, 'B'), ):
        c = biggest(A, t, x0, x1, y0, y1, 8)
        if c: out.append((nm, (c[1]+c[3])//2, (c[2]+c[4])//2))
    return out
print("enc VK blue circles render:", circles(R, 630, 730, 388, 412), " orig:", circles(O, 630, 730, 388, 412))
print("dec cross blue render:", circles(R, 740, 840, 382, 400), " orig:", circles(O, 740, 840, 382, 400))
print("dec masked blue render:", circles(R, 740, 840, 305, 326), " orig:", circles(O, 740, 840, 305, 326))
