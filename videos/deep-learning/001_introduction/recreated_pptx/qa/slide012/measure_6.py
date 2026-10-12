from PIL import Image, ImageFont
import numpy as np
from collections import Counter

# font metrics: Liberation Sans is metric-compatible with Arial
FONT = "/usr/share/fonts/TTF/LiberationSans-Regular.ttf"
FONTB = "/usr/share/fonts/TTF/LiberationSans-Bold.ttf"
import os
if not os.path.exists(FONT):
    for p in ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]:
        if os.path.exists(p): FONT = p; FONTB = p.replace("-Regular","-Bold"); break
print("fonts:", os.path.exists(FONT), os.path.exists(FONTB))

def adv(text, pt, bold=False):
    f = ImageFont.truetype(FONTB if bold else FONT, pt*4)  # 4x for precision (1pt=1px at 72dpi scale)
    w = f.getlength(text)/4.0
    return w

tests = [
    ("Feature Invariants", 208, True),      # measured x 125..333
    ("Features Invariants are", 227, True), # red run 128..355
    ("is", 10, False),
    ("Problem dependent", 189, True),       # underline 378..567 -> text ~376..567
    ("Rotation Invariant", 176, None),
    ("Scaling Invariant", 166, None),       # 127..293
    ("Translation invariant", 203, None),   # 127..330
    ("Mirroring Invariant", 183, None),     # 127..310
]
print("\n== advance solve: size s.t. predicted ~ measured (regular vs bold) ==")
for text, meas, maybe_bold in tests:
    cands = []
    for pt in range(14, 30):
        r = adv(text, pt); b = adv(text, pt, True)
        cands.append((pt, r, b))
    best = sorted(cands, key=lambda c: min(abs(c[1]-meas), abs(c[2]-meas)))[:3]
    print(f" '{text}' meas {meas}px -> best: " + ", ".join(f"pt{p}(reg{r:.0f}/bold{b:.0f})" for p,r,b in best))

# baseline/cap analysis
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)
# badge zone check (no badge in original): sample (860..930, 40..105)
print("\n== badge zone (875..915, 50..95) modal ==", Counter(tuple(a[y,x]) for y in range(50,96,2) for x in range(875,916,2)).most_common(2))

# bullet dots precise: threshold sum<520 in x 100..130
print("\n== dots precise ==")
for (y0,y1) in [(232,252),(276,296),(320,340),(364,384)]:
    pts=[(y,x) for y in range(y0,y1) for x in range(100,130) if a[y,x].sum()<520]
    if pts:
        ys=[p[0] for p in pts]; xs=[p[1] for p in pts]
        yc=(min(ys)+max(ys))/2; xc=(min(xs)+max(xs))/2
        print(f" band{y0}: y {min(ys)}..{max(ys)} x {min(xs)}..{max(xs)} center ({xc:.1f},{yc:.1f}) n={len(pts)}")

# cursor artifact check near bullet3 (x 190..260, y 322..345) — brightness map
print("\n== bullet3 zone row-profile x 185..265 (sum<560) ==")
for y in range(320, 346):
    dk=[x for x in range(185,266) if a[y,x].sum()<560]
    if dk: print(" row",y, dk[:20], "..." if len(dk)>20 else "")
