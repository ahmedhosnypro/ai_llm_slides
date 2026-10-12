#!/usr/bin/env python3
"""d1_occlusion_test_045.py — DECISIVE D1 measurement: render_5 vs the no-star variant.
Any dark ink present in render_5's neighbourhood test (no-star) but absent in render_5,
inside the line-1 band, is ink COVERED by the starburst. Banked as d1_test_out.txt."""
import numpy as np
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide045"
SC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide045"
ren5 = np.asarray(Image.open(f"{QA}/render_5.png").convert("RGB")).astype(int)
nost = np.asarray(Image.open(f"{SC}/nostar_render/nostar-1.png").convert("RGB")).astype(int)
org = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg").convert("RGB")).astype(int)
S = ren5.shape[0] / 540.0
out = []
def P(*a):
    line = " ".join(str(x) for x in a)
    out.append(line); print(line)

def dark(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    lum = (r + g + b) / 3
    red = (r - g > 25) & (r - b > 15) & (r > 90)
    return (lum < 205) & ~red

d5, dn, do_ = dark(ren5), dark(nost), dark(org)

def win(m, x0, x1, y0, y1, k=1.0):
    return m[int(y0*k):int(y1*k)+1, int(x0*k):int(x1*k)+1]

P("== line-1 band y118..146: dark-ink column coverage, render_5 vs no-star ==")
covered_cols, covered_px = [], 0
for fx in range(700, 890):
    c5 = win(d5, fx, fx, 118, 146, S).sum()
    cn = win(dn, fx, fx, 118, 146, S).sum()
    if cn > 0 and c5 == 0:
        covered_cols.append(fx); covered_px += int(cn)
P(f"  columns with no-star ink but render_5 EMPTY: {covered_cols if covered_cols else 'NONE'}")
P(f"  covered ink pixels (frame-px): {covered_px}")

P("== same test on the ORIGINAL (org vs org — sanity: N/A) — instead: org line-1 tail extent ==")
ys, xs = np.where(win(do_, 700, 895, 118, 146))
P(f"  org line-1 tail ink bbox: x{700+xs.min()}..{700+xs.max()} y{118+ys.min()}..{118+ys.max()} n={len(ys)}")
ys, xs = np.where(win(dn, 700, 895, 118, 146, S))
P(f"  no-star line-1 tail ink bbox: x{700+xs.min()/S:.0f}..{700+xs.max()/S:.0f} y{118+ys.min()/S:.0f}..{118+ys.max()/S:.0f} n={int(len(ys)/S/S)}")
ys, xs = np.where(win(d5, 700, 895, 118, 146, S))
P(f"  render_5 line-1 tail ink bbox: x{700+xs.min()/S:.0f}..{700+xs.max()/S:.0f} y{118+ys.min()/S:.0f}..{118+ys.max()/S:.0f} n={int(len(ys)/S/S)}")

P("")
P("== where does the no-star render have ink that render_5 lacks (ANY dark, full line-1 window) ==")
diff = win(dn, 700, 895, 116, 150, S) & ~win(d5, 700, 895, 116, 150, S)
ys, xs = np.where(diff)
if len(ys):
    P(f"  covered bbox: x{700+xs.min()/S:.1f}..{700+xs.max()/S:.1f} y{116+ys.min()/S:.1f}..{116+ys.max()/S:.1f} n={int(len(ys)/S/S)}")
else:
    P("  NONE — the starburst covers zero line-1 ink in render_5")

open(f"{QA}/d1_test_out.txt", "w").write("\n".join(out) + "\n")
print("\nwrote d1_test_out.txt")
