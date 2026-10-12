#!/usr/bin/env python3
"""PIL forensics pass 5 — slide_046.jpg: markers, stroke-center modals, fits, crops."""
from PIL import Image, ImageFont
import numpy as np
from collections import Counter
import os

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
IMG = f"{BASE}/unique_slides/slide_046.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
redm   = (R > 110) & (R - G > 25) & (R - B > 25)
bluem  = (B - R > 30) & (B - G > 25) & (B > 100)
greenm = (G - R > 40) & (G - B > 40) & (G > 120)
textm  = (R + G + B < 620) & ~redm & ~bluem & ~greenm

def bb(x0, y0, x1, y1, mask, label):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0: print(f"{label:30s} EMPTY"); return None
    r = (x0+int(xs.min()), y0+int(ys.min()), x0+int(xs.max()), y0+int(ys.max()))
    print(f"{label:30s} x {r[0]}..{r[2]}  y {r[1]}..{r[3]}  (w {r[2]-r[0]+1} h {r[3]-r[1]+1})")
    return r

print("== markers ==")
bb(110, 146, 131, 174, textm, "main marker")
for i, (y0, y1) in enumerate([(174, 194), (196, 218), (221, 240)], 1):
    bb(124, y0, 139, y1, textm, f"sub{i} marker")
bb(110, 250, 131, 280, textm, "box1 marker")
bb(110, 284, 131, 312, textm, "box2 marker")
core_color = a[146:174, 110:131][textm[146:174, 110:131]]
print("main marker core:", Counter(map(tuple, core_color[np.argsort(core_color.sum(axis=1))[:8]])).most_common(2))

print("== stroke-center modals ==")
border_px = np.concatenate([a[131:136, 200:700].reshape(-1,3), a[455:460, 200:700].reshape(-1,3)])
red_px = border_px[(border_px[:,0] > 110) & (border_px[:,0] - border_px[:,1] > 25)]
print("panel border red modal:", Counter(map(tuple, red_px)).most_common(3))
vpx = np.concatenate([a[250:310, 106:109].reshape(-1,3), a[250:310, 292:295].reshape(-1,3)])
bl = vpx[(vpx[:,2] - vpx[:,0] > 30) & (vpx[:,2] > 100)]
print("box border blue stroke modal:", Counter(map(tuple, bl)).most_common(3))
cppx = a[396:413, 676:774][bluem[396:413, 676:774]]
print("caption blue modal:", Counter(map(tuple, cppx)).most_common(3))
print("gray chrome modal:", Counter(map(tuple, a[100:120, 480:600].reshape(-1,3))).most_common(2))
print("panel white modal:", Counter(map(tuple, a[420:450, 340:600].reshape(-1,3))).most_common(2))
print("== core colors (text) ==")
tb = a[150:170, 137:540][textm[150:170, 137:540]]
print("main text:", Counter(map(tuple, tb[np.argsort(tb.sum(axis=1))[:100]])).most_common(2))
sb = a[176:238, 140:758][textm[176:238, 140:758]]
print("sub text:", Counter(map(tuple, sb[np.argsort(sb.sum(axis=1))[:150]])).most_common(2))
mb = a[254:272, 138:248][textm[254:272, 138:248]]
print("box text:", Counter(map(tuple, mb[np.argsort(mb.sum(axis=1))[:60]])).most_common(2))

print("== font fits (final targets) ==")
FP = "/usr/share/fonts/liberation"
def fit(fontfile, text, target_w, lo=8, hi=60):
    best = None
    for s10 in range(lo*10, hi*10):
        s = s10/10
        f = ImageFont.truetype(f"{FP}/{fontfile}", int(round(s*4)))
        b = f.getbbox(text)
        wpx = (b[2]-b[0])/4
        err = abs(wpx - target_w)
        if best is None or err < best[0]: best = (err, s, wpx)
    print(f"  {fontfile:26s} '{text[:34]}' tgt={target_w} -> {best[1]:.1f}pt (w {best[2]:.1f})")
    return best[1]

fit("LiberationSans-Bold.ttf", "POOLING", 161)
fit("LiberationSans-Regular.ttf", "Aggregate multiple values into a single value", 404)
fit("LiberationSans-Regular.ttf", "Invariance to small transformations", 275)
fit("LiberationSans-Regular.ttf", "Reduces the size of the layer output/input to next layer \u2192 Faster computations", 619)
fit("LiberationSans-Regular.ttf", "Keeps most important information for the next layer", 408)
fit("LiberationSans-Regular.ttf", "Max pooling", 111)
fit("LiberationSans-Regular.ttf", "Average pooling", 147)
fit("LiberationSerif-Italic.ttf", "Pool", 38)
fit("LiberationSerif-Italic.ttf", "(", 7)
fit("LiberationSans-Regular.ttf", "==", 25)
fit("LiberationSans-Bold.ttf", "Size is reduced", 98)
fit("LiberationSans-Bold.ttf", "a", 10)

print("== crops ==")
os.makedirs(f"{BASE}/recreated_pptx/build/assets", exist_ok=True)
im.crop((424, 325, 611, 414)).save(f"{BASE}/recreated_pptx/build/assets/tiger_large.png")
im.crop((670, 342, 768, 390)).save(f"{BASE}/recreated_pptx/build/assets/tiger_small.png")
print("tiger_large 187x89 ->", os.path.getsize(f"{BASE}/recreated_pptx/build/assets/tiger_large.png"))
print("tiger_small  98x48 ->", os.path.getsize(f"{BASE}/recreated_pptx/build/assets/tiger_small.png"))
