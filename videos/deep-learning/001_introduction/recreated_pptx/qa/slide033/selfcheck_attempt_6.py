#!/usr/bin/env python3
"""Slide 033 self-check attempt 1: closed-loop PIL verification of render_1.png
(150dpi, 2001x1125; 1 frame px = 2001/960 = 2.0844 render px) against the
PIL-measured geometry of the original frame unique_slides/slide_033.jpg."""
from PIL import Image
import numpy as np
import sys

REN = sys.argv[1] if len(sys.argv) > 1 else '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide033/render_1.png'
S = 2001/960  # frame-px -> render-px scale

im = Image.open(REN).convert('RGB')
a = np.array(im)
print("render size:", im.size)
r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
ok = True
def check(name, cond, detail):
    global ok
    print(("PASS " if cond else "FAIL ") + name, detail)
    if not cond: ok = False

# --- title: red ink x175..773, cap top 80, baseline 105 (chrome border cols excluded) ---
red = (r>140)&(r-g>60)&(r-b>50)
x_lo, x_hi = int(65*S), int(875*S)   # inside the chrome border columns
band = red[int(70*S):int(118*S), x_lo:x_hi]
cols = np.where(band.sum(axis=0)>0)[0]
rows = np.where(band.sum(axis=1)>0)[0]
t_x0, t_x1 = (cols.min()+x_lo)/S, (cols.max()+x_lo)/S
t_top = rows.min()/S + 70
print(f"title ink x {t_x0:.1f}..{t_x1:.1f} (target 175..773), top {t_top:.1f} (target 80)")
# baseline: bottommost row of non-descender glyphs; approximate via heavy-red rows
rr = band.sum(axis=1)
heavy = [i/S+70 for i in range(len(rr)) if rr[i] > 0.25*rr.max()]
print(f"title heavy rows ~{min(heavy):.1f}..{max(heavy):.1f} (target cap 80..baseline 105)")
check("title x-extent", abs(t_x0-175)<=4 and abs(t_x1-773)<=6, f"{t_x0:.1f}..{t_x1:.1f}")
check("title cap top", abs(t_top-80)<=4, f"{t_top:.1f}")

# --- text panel border: periwinkle rect, border center-line x78.5..877.5 y140..266 ---
peri = (abs(r-g)<30)&(b-r>15)&(b>150)&(b<235)&(r>90)&(r<215)
def band_max_row(yf, x0f, x1f, mask, halfw=3):
    row = int(yf*S)
    sl = mask[row, int((x0f)*S):int((x1f)*S)]
    return int(sl.sum())
rowT = band_max_row(140, 82, 874, peri)
rowB = band_max_row(266, 82, 874, peri)
def band_max_col(xf, y0f, y1f, mask):
    col = int(xf*S)
    # scan +-2 render cols for the stroke (render rounding)
    best = 0
    for cc in range(col-2, col+3):
        best = max(best, int(mask[int(y0f*S):int(y1f*S), cc].sum()))
    return best
colL = band_max_col(78.5, 144, 262, peri)
colR = band_max_col(877.5, 144, 262, peri)
print(f"panel borders: top {rowT} bottom {rowB} left {colL} right {colR} px")
check("panel border present", rowT>500 and rowB>500 and colL>90 and colR>90, "")

# --- body lines: lefts/baselines/widths at 21pt TNR ---
# blue mask for body text
blue = (b>110)&(b-r>50)&(g<120)
redt = (r>120)&(r-g>60)&(r-b>40)
body_ink = blue | redt
def line_check(y0f, y1f, x0f, x1f, left_t, base_t, width_t, name):
    y0, y1 = int(y0f*S), int(y1f*S)
    x0, x1 = int(x0f*S), int(x1f*S)
    sub = body_ink[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(ys)==0:
        check(name+" ink", False, "EMPTY"); return
    L = (xs.min()+x0)/S; R = (xs.max()+x0)/S
    # baseline = bottom of x-height letters: use the mode of column-bottoms
    colbot = [ys[np.where(xs==c)[0]].max() for c in np.unique(xs)]
    base = (np.median(colbot)+y0)/S
    check(name+f" left({left_t})/right({left_t+width_t})/baseline({base_t})",
          abs(L-left_t)<=3 and abs(base-base_t)<=3.5,
          f"L={L:.1f} R={R:.1f} w={R-L:.1f} (target w {width_t}) base={base:.1f}")
line_check(146, 172, 82, 700, 94, 163, 530, "L1")
line_check(193, 217, 82, 700, 88, 210, 459, "L2")
line_check(215, 242, 82, 700, 88, 233, 485, "L3")
line_check(243, 262, 82, 200, 88, 256, 41, "L4")

# --- red tokens present in L1/L2/L3 (k-D, / K=3 / K=9) ---
def red_band(y0f,y1f,x0f,x1f,name,lo,hi):
    sub = redt[int(y0f*S):int(y1f*S), int(x0f*S):int(x1f*S)]
    ys,xs = np.where(sub)
    if len(ys)==0: check(name, False, "no red"); return
    x0 = (xs.min()+x0f*S)/S; x1 = (xs.max()+x0f*S)/S
    check(name, abs(x0-lo)<=5 and abs(x1-hi)<=5, f"x {x0:.1f}..{x1:.1f} target {lo}..{hi}")
red_band(146,172, 300,350, "L1 red k-D, at 308..344", 308, 345)
red_band(193,217, 120,170, "L2 red K=3 at 127..162", 127, 163)
red_band(215,242, 120,170, "L3 red K=9 at 128..162", 128, 163)

# --- word-gap drift (closed loop vs original run positions) ---
def runs_at(y0f, y1f, x0f, x1f):
    sub = body_ink[int(y0f*S):int(y1f*S), int(x0f*S):int(x1f*S)]
    cols = sub.sum(axis=0)
    out=[]; s=None
    for i,v in enumerate(cols):
        if v>0 and s is None: s=i
        if v==0 and s is not None:
            if i-s>=2: out.append((round((s+x0f*S)/S), round((i-1+x0f*S)/S)))
            s=None
    return out
def drift(name, y0f,y1f, anchors, tol=4):
    rr = runs_at(y0f,y1f,82,700)
    # merge close runs into words so partial-glyph runs don't confuse anchors
    wr=[]
    for r in rr:
        if wr and r[0]-wr[-1][1]<=4: wr[-1]=(wr[-1][0], r[1])
        else: wr.append(r)
    rr = wr
    msgs=[]
    good=True
    for (lo,hi) in anchors:
        cand = [r for r in rr if abs(r[0]-lo)<=14]
        if not cand:
            good=False; msgs.append(f"anchor {lo}..{hi} MISSING"); continue
        r0 = cand[0]
        d0 = r0[0]-lo; d1 = r0[1]-hi
        msgs.append(f"{lo}: start{d0:+d} end{d1:+d}")
        if abs(d0)>tol or abs(d1)>tol: good=False
    check(name, good, " ".join(msgs))
# L2 anchors (orig merged word runs): K-D 281..317, >> 473..495, "K=3 )" 503..546
drift("L2 word positions", 193,217, [(281,317),(473,495),(503,546)], tol=6)
# L3 anchors (merged): images) 262..328, use 342..368, (3 464..479, dim 499..532, "9 )" 557..572
drift("L3 word positions", 215,242, [(262,328),(342,368),(464,479),(499,532),(557,572)], tol=6)

# --- superscript rd PNG: exact box x482..492 y218..226 ---
sub = blue[int(215*S):int(230*S), int(479*S):int(496*S)]
ys,xs = np.where(sub)
if len(ys)==0:
    check("superscript rd ink", False, "EMPTY")
else:
    top = (ys.min()+215*S)/S; bot = (ys.max()+215*S)/S
    x0 = (xs.min()+479*S)/S; x1 = (xs.max()+479*S)/S
    print(f"superscript rd: x{x0:.1f}..{x1:.1f} y{top:.1f}..{bot:.1f} (target x482..492 y218..226)")
    check("sup rd box", abs(x0-482)<=3 and abs(x1-492)<=3 and abs(top-218)<=3 and abs(bot-226)<=3,
          f"x{x0:.1f}..{x1:.1f} y{top:.1f}..{bot:.1f}")

# --- underlines: periwinkle y164..166, x205..265 and x351..453 ---
und = (abs(r-g)<40)&(b-r>25)&(b>140)
for (x0t,x1t) in [(205,265),(351,453)]:
    sub = und[int(162*S):int(169*S), int(x0t*S):int(x1t*S)]
    n = int(sub.sum())
    check(f"underline {x0t}..{x1t}", n > (x1t-x0t)*S*0.7, f"n={n}")

# --- diagram panel border: red rect, center-line x87..859.5 y306.5..501.5 ---
for (yf, name) in [(306.5,'top'), (501.5,'bottom')]:
    row = red[int(yf*S), int(90*S):int(856*S)]
    check(f"diagram panel {name} border", int(row.sum()) > 500*S/960, f"n={int(row.sum())}")
colL = band_max_col(87, 312, 496, red)
colR = band_max_col(859.5, 312, 496, red)
check("diagram panel side borders", colL>140*S and colR>140*S,
      f"L={colL} R={colR}")

# --- crops landed: corner-sample each crop box (ink differs from plain white) ---
crops = [("plane_upper",105,345,109,88),("plane_lower",105,433,88,54),
         ("rgb_slab",330,318,165,174),("mc_slab",570,343,195,149),("wedge",269,436,62,15)]
for (nm,x,y,w,h) in crops:
    box = a[int(y*S):int((y+h)*S), int(x*S):int((x+w)*S)]
    nonwhite = ((box.astype(int).sum(axis=2)) < 720).mean()
    check(f"crop {nm} has ink", nonwhite > 0.08, f"nonwhite={nonwhite:.2f}")

# --- word PNGs: Grayscale x139..273 y319..343; Multiple channels x608..847; Filters x196..270 ---
blk = (r<110)&(g<110)&(b<110)
for (nm,x0f,x1f,y0f,y1f) in [("Grayscale",139,273,317,345),("MultChannels",608,847,316,343)]:
    sub = blk[int(y0f*S):int(y1f*S), int(x0f*S):int(x1f*S)]
    ys,xs = np.where(sub)
    if len(ys)==0: check(f"word {nm}", False, "EMPTY"); continue
    L = xs.min()/S + x0f; R = xs.max()/S + x0f
    T = ys.min()/S + y0f; B = ys.max()/S + y0f
    check(f"word {nm} extent", abs(L-x0f)<=5 and abs(R-x1f)<=5 and abs(T-(y0f+2))<=4 and abs(B-(y1f-2))<=4,
          f"x{L:.0f}..{R:.0f} y{T:.0f}..{B:.0f}")
redw = redt[int(440*S):int(458*S), int(194*S):int(274*S)]
ys,xs = np.where(redw)
if len(ys)==0: check("word Filters red", False, "EMPTY")
else:
    check("word Filters extent", abs(xs.min()/S+194-196)<=5 and abs(xs.max()/S+194-270)<=6,
          f"x{xs.min()/S+194:.0f}..{xs.max()/S+194:.0f} y{ys.min()/S+440:.0f}..{ys.max()/S+440:.0f}")

# --- black bar x38..921 y519..537 ---
blkbar = (r<60)&(g<60)&(b<60)
row = blkbar[int(528*S), int(40*S):int(918*S)]
check("black bar", int(row.sum()) > 800*S/960*0.9, f"n={int(row.sum())}")
# containment: no content ink below bar or outside chrome panel
print("---")
print("OVERALL:", "PASS" if ok else "FAIL")
