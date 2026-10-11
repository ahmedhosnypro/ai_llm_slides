#!/usr/bin/env python3
"""Slide 043 pre-judge self-checks (17 §MANDATORY) on the 150dpi render.
Scale: render 2001x1125 for 13.333x7.5in slide; frame px (960x540, 1px=1pt) * 2.0833.
Checks: containment (house frame + inner panels), equation ink presence, wrap bands."""
import numpy as np
from PIL import Image
import sys

REND = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide043/render_2.png'
a = np.asarray(Image.open(REND).convert('RGB')).astype(int)
H, W = a.shape[:2]
S = H / 540.0  # render px per frame px
def F(v): return int(round(v * S))
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]
lum = (r+g+b)/3.0
fails = []

# 1. HOUSE CONTAINMENT: content ink inside x 42..918+2, y 45..540 (frame px)
inner = lum < 200
ys, xs = np.where(inner)
x0, x1 = xs.min()/S, xs.max()/S
y0, y1 = ys.min()/S, ys.max()/S
print(f"content ink bbox (frame px): x {x0:.1f}..{x1:.1f}  y {y0:.1f}..{y1:.1f}")
if x0 < 40: fails.append(f"ink crosses left chrome edge: {x0:.1f} < 42")
if x1 > 922: fails.append(f"ink crosses right chrome edge: {x1:.1f} > 918")
if y0 < 43: fails.append(f"ink crosses top chrome edge: {y0:.1f} < 45")

# badge region excluded (chrome itself)
# 2. EQUATIONS EXIST: fraction region (frame 305..330, y 292..322) must contain dark-red ink
def ink_in(x0f,y0f,x1f,y1f, pred):
    reg = pred[F(y0f):F(y1f), F(x0f):F(x1f)]
    return int(reg.sum())
brickish = (r>120)&(g<115)&(r-g>50)&(r-b>50)
n = ink_in(302, 291, 325, 323, brickish)
print(f"fraction region brick ink px: {n}")
if n < 30: fails.append("K,q/sqrt(d) fraction region has no ink (empty equation)")
# rotated pill labels: violet ink in softmax pill zone, dark red in scaling pill zone
vio = (b>140)&(b-g>40)&(r<200)&(g<190)
n2 = ink_in(333, 335, 356, 415, vio)
print(f"softmax pill violet ink px: {n2}")
if n2 < 20: fails.append("Soft max rotated label missing in pill")
n3 = ink_in(280, 315, 299, 440, (r>100)&(g<115)&(r-g>40)&(r-b>40))
print(f"scaling pill dark-red ink px: {n3}")
if n3 < 20: fails.append("Scaling by sqrt(d) rotated label missing in pill")

# 3. WRAP/CONTAINMENT of key boxes: LT box text inside box (frame 314..554, 90..114)
dk = lum < 120
n4 = int(dk[F(91):F(113), F(316):F(552)].sum())
print(f"LT box interior dark px: {n4}")
if n4 < 100: fails.append("LT box text missing")
# title lines present
n5 = int(dk[F(50):F(78), F(520):F(880)].sum())
n6 = int(dk[F(78):F(102), F(600):F(810)].sum())
print(f"title line1 ink {n5}, line2 ink {n6}")
if n5 < 200: fails.append("title line 1 missing")
if n6 < 100: fails.append("title line 2 missing")

# 4. highlight behind Wide present (yellow run in line2 zone)
ylw = (r>230)&(g>230)&(b<130)
n7 = ink_in(600, 76, 680, 104, ylw)
print(f"Wide highlight yellow px: {n7}")
if n7 < 60: fails.append("Wide yellow highlight missing")

# 5. card stack present: salmon fill at (300,400) frame
def at(xf, yf): return a[F(yf), F(xf)]
c = at(300, 400)
print(f"h1 card sample (300,400): #{c[0]:02X}{c[1]:02X}{c[2]:02X}")
if abs(int(c[0])-239) > 25 or abs(int(c[1])-140) > 30: fails.append("h1 card fill wrong at (300,400)")
c = at(770, 225)
print(f"h5 card sample (760,210): #{c[0]:02X}{c[1]:02X}{c[2]:02X}")
if abs(int(c[0])-247) > 25 or abs(int(c[1])-226) > 30: fails.append("h5 card fill wrong at (760,210)")

# 6. concat bar segments present
for nm, (xf, yf, er, eg, eb) in {
    'seg1': (322, 139, 0xBB, 0x4F, 0x07), 'seg3': (473, 139, 0xF2, 0xF2, 0x08),
    'seg5': (622, 139, 0xF3, 0xDE, 0xBC)}.items():
    c = at(xf, yf)
    d = abs(int(c[0])-er)+abs(int(c[1])-eg)+abs(int(c[2])-eb)
    print(f"{nm} sample: #{c[0]:02X}{c[1]:02X}{c[2]:02X} (diff {d})")
    if d > 150: fails.append(f"concat bar {nm} color off")

# 7. legend + swoosh presence
grn = (g>200)&(g-r>8)&(g-b>8)
n8 = ink_in(740, 470, 900, 530, grn)
print(f"legend pale-green px: {n8}")
if n8 < 2000: fails.append("legend box missing/fill wrong")
drk = (r>100)&(r<190)&(g<70)&(b<70)
n9 = ink_in(600, 340, 750, 460, (abs(r-139)<60)&(abs(g-26)<60)&(abs(b-16)<60))
print(f"swoosh dark-red px: {n9}")
if n9 < 400: fails.append("swoosh missing")

# 8. equation PNG ink exact-size sanity: fraction image w/h on slide = 0.225x0.31667in
#    -> render px 46.9x65.97; measure ink bbox in region
reg = brickish[F(291):F(323), F(302):F(325)]
ys2, xs2 = np.where(reg)
if len(ys2):
    print(f"fraction ink bbox in region: w {xs2.max()-xs2.min()+1} h {ys2.max()-ys2.min()+1} (expect ~47x66)")

print()
if fails:
    print("SELF-CHECK: FAIL")
    for f_ in fails: print("  -", f_)
    sys.exit(1)
print("SELF-CHECK: PASS")
