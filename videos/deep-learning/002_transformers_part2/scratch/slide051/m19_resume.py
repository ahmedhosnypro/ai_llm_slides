#!/usr/bin/env python3
# m19_resume.py — adjudicate judge-2's MAJOR/MINOR claims against the original frame
# and the render. Every claim gets a direct pixel measurement.
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
orig = Image.open(f"{ROOT}/unique_slides/slide_051.jpg").convert("RGB")
r5 = Image.open(f"{ROOT}/recreated_pptx/qa/slide051/render_5.png").convert("RGB")
K = 150.0 / 72.0
RX, RY = lambda fx: (fx - 18.128) / 0.961235 * K, lambda fy: (fy + 0.045) / 0.956566 * K

def rp(fx, fy):
    return r5.getpixel((min(int(RX(fx)), 2000), min(int(RY(fy)), 1124)))

def isg(p): return p[1] > 130 and p[1] > p[0] + 30 and p[1] > p[2] + 20
def isy(p): return p[0] > 180 and p[1] > 180 and p[2] < 120
def isr(p): return p[0] > 140 and p[1] < 90 and p[2] < 90
def isk(p): return p[0] < 90 and p[1] < 90 and p[2] < 90

def gmask(img, x0, y0, x1, y1, step, pred, label, to_rend=False):
    print(f"--- {label} ({x0}..{x1}, {y0}..{y1}) step {step}")
    print("      " + "".join(f"{x % 10}" for x in range(x0, x1 + 1, step)))
    for y in range(y0, y1 + 1, step):
        row = f"y{y:<4d}"
        for x in range(x0, x1 + 1, step):
            if to_rend:
                p = img.getpixel((min(int(RX(x)), img.size[0] - 1), min(int(RY(y)), img.size[1] - 1)))
            else:
                p = img.getpixel((x, y))
            row += "#" if pred(p) else "."
        print(row)

# A) encoder: green rounded-rect outline around the stack?
gmask(orig, 203, 258, 292, 380, 3, isg, "A ORIG encoder green mask (outline hunt)")
# B) decoder: green topology around the stack
gmask(orig, 728, 195, 830, 400, 4, isg, "B ORIG decoder green mask (outline hunt)")
# C) yellow masks: orig vs render
gmask(orig, 200, 235, 300, 320, 3, isy, "C ORIG encoder yellow mask")
gmask(r5, 200, 235, 300, 320, 3, isy, "C RENDER encoder yellow mask", to_rend=True)
# D) encoder QKV row + olive bar band
gmask(orig, 193, 368, 292, 400, 3, lambda p: isg(p) or (150 < p[0] < 215 and 140 < p[1] < 215 and 90 < p[2] < 175), "D ORIG encoder QKV band (green+olive)")
# E) (shifted right) clearance in render
def ink_rows(img, x0, y0, x1, y1, pred, label, to_rend=False):
    rows = []
    for y in range(y0, y1 + 1):
        n = 0
        for x in range(x0, x1 + 1):
            if to_rend:
                p = img.getpixel((min(int(RX(x)), img.size[0] - 1), min(int(RY(y)), img.size[1] - 1)))
            else:
                p = img.getpixel((x, y))
            if pred(p):
                n += 1
        if n:
            rows.append((y, n))
    print(f"--- {label}: ink rows {rows[:3]} ... {rows[-3:] if len(rows) > 3 else ''}")
ink_rows(r5, 742, 484, 816, 504, isk, "E RENDER (shifted right) dark ink", to_rend=True)
print("    decoder panel bottom border ~y501-503 (build 568.5..877 x 102..503)")
ink_rows(orig, 742, 484, 816, 504, isk, "E ORIG (shifted right) dark ink")
# F) circle icons atop Output Embedding?
gmask(orig, 205, 376, 290, 401, 2, lambda p: isr(p) or isg(p) or (p[0] < 120 and p[1] < 120 and p[2] < 120), "F ORIG encoder atop-embedding (red/green/dark)")
gmask(orig, 733, 380, 812, 401, 2, lambda p: isr(p) or isg(p) or (p[0] < 120 and p[1] < 120 and p[2] < 120), "F ORIG decoder atop-embedding (red/green/dark)")
# G) red check beside decoder MHA?
gmask(orig, 798, 262, 836, 314, 2, isr, "G ORIG decoder right-of-MHA red mask")
# H) decoder top arrow clearance (orig)
gmask(orig, 718, 100, 756, 150, 2, isr, "H ORIG decoder top red arrow")
gmask(r5, 718, 100, 756, 150, 2, isr, "H RENDER decoder top red arrow", to_rend=True)
