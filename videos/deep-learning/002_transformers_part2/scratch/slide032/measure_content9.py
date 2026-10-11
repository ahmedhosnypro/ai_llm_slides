#!/usr/bin/env python3
"""v9: italic-slant detection (top-half vs bottom-half centroid shift) + callout/title checks."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_032.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
dark = (R < 160) & (G < 160)

def slant(y0, y1, x0, x1, label):
    m = dark[y0:y1, x0:x1]
    h = y1 - y0
    top = m[: h // 2]; bot = m[h // 2:]
    def cx(mm):
        ys, xs = np.where(mm)
        return xs.mean() if len(xs) else float('nan')
    ct, cb = cx(top), cx(bot)
    # for italic (~12 deg), upper strokes shift RIGHT vs lower by ~ tan(12)*h/2
    print(f"{label:34s} h={h} cxTop={ct:.1f} cxBot={cb:.1f} shift(top-bot)={ct-cb:+.1f}px  {'ITALIC-ish' if ct-cb > 1.2 else 'upright' if ct-cb < -0.2 else 'ambiguous'}")

# pure-blue segments (exclude highlight/green/red zones)
slant(227, 245, 87, 300, "L1 'This vector can be used'")     # known italic (spec+read)
slant(292, 310, 103, 200, "L2 'Values are' (upright per read)")
slant(324, 342, 185, 550, "L3 mid 'between vectors...pos'")  # read says italic?
slant(324, 342, 685, 700, "L3 'is'")
slant(356, 374, 102, 270, "L4 'irrespective of \"t\"'")       # spec: italic
slant(388, 406, 103, 380, "L5 highlight '\"t\" may take...'") # read: bold italic
slant(452, 471, 102, 358, "L6 'Position Vector Length = 2'")
slant(452, 471, 362, 850, "L6 red warning")
slant(292, 310, 362, 518, "L2 green '(bounded values)'")     # read: green italic
slant(356, 374, 274, 728, "L4 green '[Distance...]'")
slant(60, 75, 337, 612, "TITLE")
slant(83, 100, 269, 690, "SUBTITLE")
slant(128, 145, 230, 560, "callout line A")
slant(149, 163, 230, 700, "callout line B")

# callout border core color at rows 119 & 171
from collections import Counter
ob = (R - B > 60) & (R > 130) & (G > 60) & (G < 190) & (B < 90)
print("\nborder row119 core:", Counter(map(tuple, a[119, 300:800][ob[119, 300:800]])).most_common(3))
print("border row171 core:", Counter(map(tuple, a[171, 300:800][ob[171, 300:800]])).most_common(3))
print("border col~219:", Counter(map(tuple, a[130:165, 219][ob[130:165, 219]])).most_common(3))
print("border col~853:", Counter(map(tuple, a[130:165, 853][ob[130:165, 853]])).most_common(3))

# subtitle: exclude vector-box-top noise -> ink rows with count>2
blueish = (R < 130) & (G < 130) & (B > 120)
m = blueish[78:106, 250:720]
rp = m.sum(axis=1)
print("\nsubtitle rows:", [(78 + i, int(rp[i])) for i in range(rp.shape[0]) if rp[i] > 2])
xs = np.where(m.any(axis=0))[0]
print("subtitle x extent:", 250 + xs.min(), "..", 250 + xs.max())
