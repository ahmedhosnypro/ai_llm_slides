#!/usr/bin/env python3
# m20_resume.py — raw-RGB adjudication of the remaining judge-2 claims.
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
orig = Image.open(f"{ROOT}/unique_slides/slide_051.jpg").convert("RGB")
r5 = Image.open(f"{ROOT}/recreated_pptx/qa/slide051/render_5.png").convert("RGB")
K = 150.0 / 72.0
RX, RY = lambda fx: (fx - 18.128) / 0.961235 * K, lambda fy: (fy + 0.045) / 0.956566 * K
def rp(fx, fy): return r5.getpixel((min(int(RX(fx)), 2000), min(int(RY(fy)), 1124)))

print("=== 1) encoder connector/atop-embedding x238..252 y372..402 (orig) step 2")
for y in range(372, 403, 2):
    row = f"y{y}: "
    for x in range(238, 253, 2):
        r, g, b = orig.getpixel((x, y))
        row += f"({r:3},{g:3},{b:3})"
    print(row)

print("=== 2) the y394 dark line: x196..286 y390..399 (orig) step 4")
for y in range(390, 400, 2):
    row = f"y{y}: "
    for x in range(196, 287, 4):
        r, g, b = orig.getpixel((x, y))
        row += f"({r:3},{g:3},{b:3})"
    print(row)

print("=== 3) decoder red right of MHA: x795..822 y286..306 (orig) step 2")
for y in range(286, 307, 2):
    row = f"y{y}: "
    for x in range(795, 823, 2):
        r, g, b = orig.getpixel((x, y))
        row += f"({r:3},{g:3},{b:3})"
    print(row)

print("=== 4) decoder top arrow redo (r>120): x716..758 y102..148 (orig | render) step 3")
def isr2(p): return p[0] > 120 and p[1] < 100 and p[2] < 100
for y in range(102, 149, 3):
    ro = "o:"
    rr = "r:"
    for x in range(716, 759, 3):
        ro += "#" if isr2(orig.getpixel((x, y))) else "."
        rr += "#" if isr2(rp(x, y)) else "."
    print(f"y{y:<4d} {ro}  {rr}")

print("=== 5) (shifted right) green ink rows, orig vs render, x742..816 y482..504")
def isg2(p): return p[1] > 100 and p[1] > p[0] + 15 and p[1] > p[2] + 15
for img, tag, to_rend in ((orig, "ORIG", False), (r5, "REND", True)):
    rows = []
    for y in range(482, 505):
        n = 0
        for x in range(742, 817):
            p = rp(x, y) if to_rend else img.getpixel((x, y))
            if isg2(p):
                n += 1
        if n:
            rows.append((y, n))
    print(f"  {tag}: {rows}")

print("=== 6) spot samples ===")
for tag, xy in [("orig yellow-left-v", [(201, 280), (201, 300), (202, 290)]),
                ("orig QKV bar", [(210, 388), (235, 388), (222, 388), (240, 389)]),
                ("orig dec trunk band", [(818, 240), (820, 300), (822, 350), (825, 320), (818, 200)]),
                ("orig y395 band", [(750, 396), (760, 397), (790, 396), (810, 397)]),
                ("orig dec y383-391 band", [(790, 386), (800, 388), (815, 388)])]:
    print(f"  {tag}: {[orig.getpixel(p) for p in xy]}")
print("  render QKV bar:", [rp(x, 388) for x in (210, 222, 235)])
print("  render dec trunk:", [rp(x, y) for x, y in ((816, 240), (818, 300), (816, 350))])
