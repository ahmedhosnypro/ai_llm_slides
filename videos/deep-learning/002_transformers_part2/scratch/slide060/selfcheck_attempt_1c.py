#!/usr/bin/env python3
"""Closed-loop attempt 1c: per-line bands from the ORIGINAL's ink rows (same threshold rule
both sides). Compares ink band edges (top/bottom/left/right) render vs original-mapped. Tol 4px."""
from PIL import Image

RN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide060/render_1.png"
img = Image.open(RN).convert("RGB")
W, H = img.size
px = img.load()
K = 150 / 72.0
SY = 2.1803  # frame row/col -> render px (1/0.95556*2.0833 for y; for x: 1/0.96123*2.0833=2.1679)

def reddish(p):
    r, g, b = p
    return r > 140 and r - g > 60 and r - b > 60

def blueish(p):
    r, g, b = p
    return b > 90 and b - r > 40 and b - g > 30

# name: (band_frame_rows, x_search_render_px, kind, orig_ink_frame_cols)
L = {
    # rows from measure4/5 (threshold >=2); cols -> targets
    "title": (64, 92, (400, 1500), "red", (272, 629)),
    "e1": (146, 163, (140, 1858), "mix", (89, 593)),
    "c1": (169, 184, (140, 1858), "blue", (128, 532)),
    "e2": (210, 227, (140, 1858), "mix", (90, 686)),
    "c2": (233, 249, (140, 1858), "blue", (128, 464)),
    "e3": (275, 292, (140, 1858), "mix", (89, 524)),
    "c3": (295, 310, (140, 1858), "blue", (128, 386)),
    "e4": (334, 351, (140, 1858), "mix", (92, 781)),
    "c4": (355, 370, (140, 1858), "blue", (128, 594)),
    "e5": (396, 413, (140, 1858), "mix", (89, 432)),
    "e6": (439, 455, (140, 1858), "mix", (89, 592)),
}
FX0, SX = 18.63, 0.96123
def tx(fx): return (fx - FX0) / SX * K  # frame col -> render px

print(f"render {W}x{H}  (tol 4px on ink edges; y targets = frame_row*{SY:.4f})")
print(f"{'line':6s} {'x0 t/dx':>14s} {'x1 t/dx':>14s} {'top t/dy':>14s} {'bot t/dy':>14s}")
bad = []
for name, (r0, r1, (xs0, xs1), kind, (fc0, fc1)) in L.items():
    y0, y1 = int(r0 * SY) - 2, int(r1 * SY) + 3
    def ok(p):
        return reddish(p) if kind == "red" else (blueish(p) or reddish(p))
    xs, rowc = [], {}
    for y in range(y0, y1):
        n = 0
        for x in range(xs0, xs1):
            if ok(px[x, y]):
                xs.append(x); n += 1
        rowc[y] = n
    if not xs:
        print(f"{name:6s} NO INK <-- BLOCKER"); bad.append(name); continue
    top = min(y for y, n in rowc.items() if n >= 3)
    bot = max(y for y, n in rowc.items() if n >= 3)
    x0, x1 = min(xs), max(xs)
    tx0, tx1 = tx(fc0), tx(fc1 + 1)
    ty0, ty1 = r0 * SY, (r1 + 1) * SY
    dxs = (x0 - tx0, x1 - tx1, top - ty0, bot - ty1)
    flag = "" if all(abs(d) <= 4 for d in dxs) else "  <-- FIX"
    if flag: bad.append(name)
    print(f"{name:6s} {x0:5.0f}/{dxs[0]:+5.1f} {x1:5.0f}/{dxs[1]:+5.1f} "
          f"{top:5.0f}/{dxs[2]:+5.1f} {bot:5.0f}/{dxs[3]:+5.1f}{flag}")
print("BAD:", bad if bad else "none")
# width ratios for size correction
print("\nsize correction (target/rendered ink width):")
for name, (r0, r1, (xs0, xs1), kind, (fc0, fc1)) in L.items():
    y0, y1 = int(r0 * SY) - 2, int(r1 * SY) + 3
    def ok(p):
        return reddish(p) if kind == "red" else (blueish(p) or reddish(p))
    xs = [x for y in range(y0, y1) for x in range(xs0, xs1) if ok(px[x, y])]
    if not xs: continue
    tw = tx(fc1 + 1) - tx(fc0)
    rw = (max(xs) + 1 - min(xs))
    # current build sizes
    cur = {"title": 31.0, "e1": 19.86, "e2": 19.85, "e3": 19.91, "e4": 19.88, "e5": 19.86,
           "e6": 20.07, "c1": 17.42, "c2": 17.41, "c3": 17.48, "c4": 17.77}[name]
    print(f"  {name:6s} target {tw:7.1f}px rendered {rw:7.1f}px ratio {tw/rw:.4f} -> size {cur*tw/rw:.2f}")
