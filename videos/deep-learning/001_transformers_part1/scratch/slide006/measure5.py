#!/usr/bin/env python3
"""measure5: ASCII ink maps of decoder + encoder containers, plus label color samples."""
from PIL import Image
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_006.jpg"
a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)

def ascii_map(x0, y0, x1, y1, ref, tol, step=3, label=""):
    print(f"\n== {label} ({x0},{y0})-({x1},{y1}) step={step} ref=#{ref[0]:02x}{ref[1]:02x}{ref[2]:02x} ==")
    hdr = "     " + "".join(str((x0 + i * step) // 100 % 10) for i in range((x1 - x0) // step))
    hdr2 = "     " + "".join(str((x0 + i * step) // 10 % 10) for i in range((x1 - x0) // step))
    print(hdr); print(hdr2)
    for y in range(y0, y1, step):
        row = ""
        for x in range(x0, x1, step):
            blk = a[y:y + step, x:x + step].reshape(-1, 3)
            d = np.abs(blk - np.array(ref)).sum(axis=1)
            frac = (d > tol).mean()
            row += "#" if frac > 0.55 else ("+" if frac > 0.25 else ("." if frac > 0.08 else " "))
        print(f"{y:4d} {row}")

# decoder container
ascii_map(478, 116, 903, 284, (253, 255, 133), 95, 3, "DECODER ink map")
# zoom col1 top: x480-625 y120-205, 1px
ascii_map(480, 120, 625, 205, (253, 255, 133), 95, 2, "DECODER col1 top zoom (step2)")
# zoom under barB1 / s1 area: x480-680 y250-295
ascii_map(480, 248, 680, 296, (253, 255, 133), 95, 2, "DECODER under-barB1 zoom (step2)")
# encoder container
ascii_map(46, 306, 488, 497, (248, 213, 173), 80, 3, "ENCODER ink map")
# callout + leader + context arrow zone
ascii_map(440, 250, 850, 510, (255, 255, 255), 60, 4, "CENTER zone (callout/leader/arc) vs white-ish")

print("\n== label color samples ==")
for k, (x, y) in {
    "o1 glyph": (549, 134), "o1 glyph2": (552, 136), "o2 glyph": (682, 135), "o3 glyph": (813, 135),
    "softmax s": (491, 178), "softmax o": (500, 178), "softmax ftmax": (521, 178), "softmax2": (536, 178),
    "h1 glyph": (213, 318), "h1 sub": (222, 323), "h2 glyph": (344, 318),
    "emb e": (65, 371), "emb mid": (90, 370), "emb x": (143, 371), "emb sub1": (151, 375),
    "s1 label": (616, 276), "s1 sub": (622, 278), "s2 label": (747, 276), "s3 label": (878, 276),
    "x1 label": (156, 478), "x1 sub": (164, 480),
    "caption Enc E": (226, 515), "caption Dec D": (690, 97),
    "title T": (268, 68), "title rad T2": (398, 68),
    "callout C": (582, 422), "callout mid": (700, 423),
    "s-arrow line": (610, 264), "h-arrow line": (220, 329),
}.items():
    r, g, b = a[y, x]
    print(f"  {k} ({x},{y}): #{r:02x}{g:02x}{b:02x}")
