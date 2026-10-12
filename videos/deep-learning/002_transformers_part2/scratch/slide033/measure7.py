#!/usr/bin/env python3
"""slide033 measure-7: precise fill/border colors (patch modes) + targeted dumps."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(FR).convert("RGB")).astype(int)

def patch(x0, x1, y0, y1, label):
    p = a[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3)
    q = (p // 8 * 8)
    colors, counts = np.unique(q, axis=0, return_counts=True)
    top = colors[np.argsort(-counts)[:3]]
    med = tuple(int(v) for v in np.median(p, axis=0))
    tops = ", ".join(f"#{c[0]:02x}{c[1]:02x}{c[2]:02x}({int(n)})" for c, n in zip(top, np.sort(counts)[::-1][:3]))
    print(f"  {label:38s} med=#{med[0]:02x}{med[1]:02x}{med[2]:02x}  modes: {tops}")

print("== FILLS ==")
patch(232, 244, 238, 248, "vector box B (tan) interior")
patch(232, 244, 398, 408, "vector box D (tan) interior")
patch(230, 246, 138, 146, "vector box A (green) interior")
patch(350, 390, 130, 138, "pair box 1 (green) interior top")
patch(350, 390, 222, 230, "pair box 2 interior mid (no text)")
patch(350, 390, 268, 276, "pair box 3 (green) interior top")
patch(350, 390, 382, 390, "pair box 4 interior mid")
patch(350, 390, 458, 466, "pair box 5 (green) interior top")
patch(280, 300, 160, 190, "index strip interior")
patch(500, 560, 130, 150, "defs box interior")
patch(800, 860, 130, 150, "example box interior")
patch(520, 560, 430, 450, "omega box interior")
patch(760, 840, 370, 385, "white eq sub-box interior")
patch(120, 160, 165, 175, "general pair box interior")
patch(120, 180, 250, 260, "green info box interior")

print("== TEXT INK (dark px in region) ==")
def ink(x0, x1, y0, y1, label, maxlum=140):
    p = a[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3)
    lum = p.mean(axis=1)
    d = p[lum < maxlum]
    if len(d) == 0:
        print(f"  {label:38s} NO DARK PX")
        return
    med = tuple(int(v) for v in np.median(d, axis=0))
    print(f"  {label:38s} n={len(d):5d} med=#{med[0]:02x}{med[1]:02x}{med[2]:02x}")

ink(330, 400, 140, 165, "pair box 1 text (green box)")
ink(330, 400, 235, 250, "pair box 2 text (tan box)")
ink(325, 405, 196, 214, "pair box 2 text line1")
ink(230, 245, 148, 162, "vector '0' text")
ink(232, 244, 214, 228, "vector '1' text")
ink(226, 262, 474, 490, "vector '[d/2]-1' text")
ink(278, 292, 126, 142, "index 'i' text")
ink(280, 296, 455, 470, "index 'd-1-1' text")
ink(336, 612, 46, 64, "title ink")
ink(143, 800, 71, 91, "subtitle ink")
ink(75, 200, 234, 278, "info box text")

print("== BORDERS ==")
def border(x0, x1, y0, y1, label, exclude_bg=True):
    p = a[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3)
    lum = p.mean(axis=1)
    d = p[lum < 200] if exclude_bg else p
    if len(d) == 0:
        print(f"  {label:38s} nothing")
        return
    med = tuple(int(v) for v in np.median(d, axis=0))
    print(f"  {label:38s} n={len(d):5d} med=#{med[0]:02x}{med[1]:02x}{med[2]:02x}")

border(310, 313, 200, 400, "index strip right border stroke")
border(412, 417, 200, 400, "dx1 bracket stroke")
border(424, 432, 120, 130, "dx1 label 'dx1'")
border(429, 432, 100, 288, "defs box left border col")
border(429, 761, 101, 104, "defs box top border row")
border(475, 880, 298, 301, "omega box top border row")
border(709, 866, 346, 349, "eq subbox top border row")
border(91, 94, 130, 200, "general pair box left border")
border(180, 190, 130, 200, "general pair box right border?")
border(96, 190, 117, 121, "general pair box top border?")
border(96, 190, 208, 214, "general pair box bottom border?")
border(66, 70, 240, 310, "info box left border")
border(206, 213, 240, 310, "info box right border")
border(66, 213, 224, 228, "info box top border")
border(66, 213, 318, 323, "info box bottom border")

print("== dumps ==")
print("-- row y=123, x 262..320 (index strip top edge?) --")
print("  " + " ".join(f"{x}:{a[123,x,0]:3d},{a[123,x,1]:3d},{a[123,x,2]:3d}" for x in range(262, 320, 4)))
print("-- row y=140, x 260..275 (strip left edge) --")
print("  " + " ".join(f"{x}:{a[140,x,0]:3d},{a[140,x,1]:3d},{a[140,x,2]:3d}" for x in range(260, 276)))
print("-- col x=311, y 116..132 (border top start) --")
print("  " + " ".join(f"{y}:{a[y,311,0]:3d},{a[y,311,1]:3d},{a[y,311,2]:3d}" for y in range(116, 133)))
print("-- col x=414, y 116..130 (dx1 bracket top) --")
print("  " + " ".join(f"{y}:{a[y,414,0]:3d},{a[y,414,1]:3d},{a[y,414,2]:3d}" for y in range(116, 131)))
print("-- col x=414, y 500..516 (dx1 bracket bottom) --")
print("  " + " ".join(f"{y}:{a[y,414,0]:3d},{a[y,414,1]:3d},{a[y,414,2]:3d}" for y in range(500, 517)))
