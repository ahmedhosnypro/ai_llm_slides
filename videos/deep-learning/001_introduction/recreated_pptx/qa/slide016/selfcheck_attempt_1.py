#!/usr/bin/env python3
"""Closed-loop pre-judge self-check for slide 016 (attempt 1).
Render: qa/slide016/render_1.png (150dpi, 2001x1125; 1 frame px = 2001/960 = 2.0844 render px).
Delta regions checked against PIL-measured geometry of unique_slides/slide_016.jpg
(qa/slide016/measure_*.py); inherited regions checked pixel-equal to the parent's
certified render qa/slide009/render_1.png (same component draw; badge excluded —
numeral differs by law).
Tolerance: ~4 px @150dpi (worker instructions closed-loop standard)."""
from PIL import Image
import numpy as np
import sys

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa"
V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
S = 2001 / 960.0  # render px per frame px

r = np.asarray(Image.open(f"{QA}/slide016/render_1.png").convert("RGB")).astype(int)
o = np.asarray(Image.open(f"{V}/unique_slides/slide_016.jpg").convert("RGB")).astype(int)
p = np.asarray(Image.open(f"{QA}/slide009/render_1.png").convert("RGB")).astype(int)
assert r.shape[0] == 1125 and r.shape[1] == 2001, r.shape

fails = []
def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + ("  " + detail if detail else ""))
    if not cond:
        fails.append(name)

def fx(v):  # frame px -> render px (center of the frame pixel)
    return v * S

def region(img, y0, y1, x0, x1):  # frame-px inclusive coords -> render crop
    return img[int(round(y0*S)):int(round((y1+1)*S)), int(round(x0*S)):int(round((x1+1)*S))]

def ink_bbox(img, y0, y1, x0, x1, th=120):
    reg = img[int(y0*S):int((y1+1)*S), int(x0*S):int((x1+1)*S)]
    m = reg.max(axis=2) < th
    ys, xs = np.where(m)
    if len(ys) == 0:
        return None
    return (x0 + xs.min()/S, y0 + ys.min()/S, x0 + xs.max()/S, y0 + ys.max()/S)

def near(a, b, tol=4.0):
    return a is not None and abs(a-b) <= tol

# ---- 1. Training ellipse (shifted up 9px) ---------------------------------------
# fill core modal check: center of ellipse in render (frame 143.5,157)
c = r[int(157*S), int(143*S)]
peach = abs(int(c[0])-246) < 25 and abs(int(c[1])-222) < 25 and abs(int(c[2])-194) < 25
check("training_ellipse fill F6DEC2 at center", peach, f"render rgb={tuple(c)}")
# outline top edge: gray 999999-ish row at y~128 (frame)
top = region(r, 126, 132, 100, 190)
gray = ((np.abs(top[:,:,0]-top[:,:,1]) < 25) & (np.abs(top[:,:,1]-top[:,:,2]) < 25)
        & (top[:,:,0] > 110) & (top[:,:,0] < 200))
check("training_ellipse outline top ~y128", gray.sum() > 20, f"gray px={int(gray.sum())}")
# text ink bands y141..157 / y162..174 (frame)
b1 = ink_bbox(r, 138, 160, 90, 200, th=110)
b2 = ink_bbox(r, 160, 178, 90, 200, th=110)
check("ellipse text line1 cap-top ~141", b1 is not None and near(b1[1], 141, 4), f"got {b1}")
check("ellipse text line2 bottom ~174", b2 is not None and near(b2[3], 174, 5), f"got {b2}")

# ---- 2. box_pre shifted left (navy borders at frame x129-130 / x235-236) --------
# navy column check at y236
colL = r[int(230*S):int((243+1)*S), int(128*S):int((132+1)*S)]
navyL = ((colL[:,:,2].astype(int) - colL[:,:,0]) > 40) & (colL[:,:,0] < 150)
check("box_pre left navy border ~x129-130", navyL.sum() > 15, f"navy px={int(navyL.sum())}")
colR = r[int(230*S):int((243+1)*S), int(234*S):int((238+1)*S)]
navyR = ((colR[:,:,2].astype(int) - colR[:,:,0]) > 40) & (colR[:,:,0] < 150)
check("box_pre right navy border ~x235-236", navyR.sum() > 15, f"navy px={int(navyR.sum())}")
fill = r[int(236*S), int(182*S)]
check("box_pre fill FAFED8", abs(int(fill[0])-250) < 22 and abs(int(fill[1])-254) < 22
      and abs(int(fill[2])-216) < 25, f"rgb={tuple(fill)}")
t1 = ink_bbox(r, 216, 236, 132, 234, th=110)
t2 = ink_bbox(r, 238, 260, 132, 234, th=110)
check("box_pre text line1 band ~221..232", t1 is not None and near(t1[1], 221, 4) and near(t1[3], 232, 5), f"got {t1}")
check("box_pre text line2 bottom ~255", t2 is not None and near(t2[3], 255, 6), f"got {t2}")
# text centered on box center 182.5
if t1:
    ctr = (t1[0] + t1[2]) / 2
    check("box_pre 'Pre' centered ~x182.5", near(ctr, 182.5, 5), f"center={ctr:.1f}")

# ---- 3. arrow1 re-spanned x236..293 at y236.5 -----------------------------------
ar = region(r, 232, 241, 238, 288)
redm = (ar[:,:,0] > 140) & (ar[:,:,1] < 95) & (ar[:,:,2] < 95)
check("arrow1 red line present x238..288", int(redm.sum()) > 40, f"red px={int(redm.sum())}")
rows_red = redm.sum(axis=1)
yc = 232 + (rows_red.argmax() if rows_red.max() > 0 else 0)
check("arrow1 line y ~236.5", abs(yc - 236.5) < 4, f"peak row={yc}")
# head tip near box2 left border (frame x292): red ink just left of it
tipz = region(r, 231, 243, 284, 291)
redt = (tipz[:,:,0] > 140) & (tipz[:,:,1] < 95) & (tipz[:,:,2] < 95)
check("arrow1 head near x292", int(redt.sum()) > 8, f"red px={int(redt.sum())}")

# ---- 4. curve1 PNG (bbox x91..133, y175..245) -----------------------------------
cv = region(r, 176, 244, 92, 132)
redc = ((cv[:,:,0].astype(int) - cv[:,:,1]) > 40) & ((cv[:,:,0].astype(int) - cv[:,:,2]) > 40)
check("curve1 red ink present", int(redc.sum()) > 60, f"red px={int(redc.sum())}")
ys, xs = np.where(redc)
if len(ys):
    bb = (92 + xs.min()/S, 176 + ys.min()/S, 92 + xs.max()/S, 176 + ys.max()/S)
    check("curve1 ink bbox within measured region",
          bb[0] >= 90 and bb[1] >= 174 and bb[2] <= 134 and bb[3] <= 246, f"bbox={tuple(round(v,1) for v in bb)}")
# stem at x96 vertical
stem = region(r, 182, 200, 94, 100)
reds = ((stem[:,:,0].astype(int) - stem[:,:,1]) > 40) & ((stem[:,:,0].astype(int) - stem[:,:,2]) > 40)
check("curve1 stem at x~96", int(reds.sum()) > 20, f"red px={int(reds.sum())}")

# ---- 5. Classifier Output box (x748..863, y208..265) ----------------------------
f5 = r[int(236*S), int(805*S)]
check("box5 fill DCBFA1", abs(int(f5[0])-220) < 22 and abs(int(f5[1])-191) < 22
      and abs(int(f5[2])-161) < 22, f"rgb={tuple(f5)}")
bd = r[int(207.5*S), int(805*S)]
check("box5 top border dark brown", int(bd.max()) < 150, f"rgb={tuple(bd)}")
k1 = ink_bbox(r, 216, 236, 752, 860, th=110)
k2 = ink_bbox(r, 238, 262, 752, 860, th=110)
check("box5 'Classifier' band ~221..233", k1 is not None and near(k1[1], 221, 4) and near(k1[3], 233, 5), f"got {k1}")
check("box5 'Output' bottom ~255", k2 is not None and near(k2[3], 255, 6), f"got {k2}")
if k1:
    ctr = (k1[0] + k1[2]) / 2
    check("box5 'Classifier' centered ~x805.5", near(ctr, 805.5, 6), f"center={ctr:.1f}")

# ---- 6. callouts A-D: fill bbox + text bands ------------------------------------
def gray_bbox(img, y0, y1, x0, x1):
    reg = img[int(y0*S):int((y1+1)*S), int(x0*S):int((x1+1)*S)]
    m = ((np.abs(reg[:,:,0]-reg[:,:,1]) < 14) & (np.abs(reg[:,:,1]-reg[:,:,2]) < 14)
         & (reg[:,:,0] > 195) & (reg[:,:,0] < 246))
    ys, xs = np.where(m)
    return (x0 + xs.min()/S, y0 + ys.min()/S, x0 + xs.max()/S, y0 + ys.max()/S) if len(ys) else None

CALLOUTS = {
    "A inspection":  (85, 291, 278, 331, [(298, 310), (314, 325)]),
    "B handcrafted": (280, 336, 433, 395, [(353, 362), (369, 381)]),
    "C decision":    (435, 282, 574, 341, [(290, 300), (306, 318), (322, 334)]),
    "D apply":       (612, 282, 700, 322, [(289, 301), (305, 314)]),
}
for name, (x0, y0, x1, y1, bands) in CALLOUTS.items():
    gb = gray_bbox(r, y0-3, y1+3, x0-3, x1+3)
    ok = gb is not None and near(gb[0], x0, 5) and near(gb[1], y0, 5) and near(gb[2], x1, 5) and near(gb[3], y1, 5)
    check(f"callout {name} bbox ~({x0},{y0},{x1},{y1})", ok, f"got {tuple(round(v,1) for v in gb) if gb else None}")
    # band-profile check: detect the text ink bands INSIDE the box (inset from the
    # border so the box's own edge pixels don't count), then compare count + extents
    reg = r[int((y0+3)*S):int((y1-2)*S), int((x0+3)*S):int((x1-2)*S)]
    m = reg.max(axis=2) < 110
    rows = m.sum(axis=1)
    got = []
    inr = False
    for i, cnt in enumerate(rows):
        if cnt > 0 and not inr:
            s = i; inr = True
        if cnt == 0 and inr:
            got.append((y0+3 + s/S, y0+3 + (i-1)/S)); inr = False
    if inr:
        got.append((y0+3 + s/S, y0+3 + (len(rows)-1)/S))
    check(f"callout {name} text band count {len(bands)}", len(got) == len(bands),
          f"got {[(round(a,1),round(b,1)) for a,b in got]}")
    if len(got) == len(bands):
        for i, ((ty0, ty1), (gy0, gy1)) in enumerate(zip(bands, got)):
            ok = near(gy0, ty0, 5) and near(gy1, ty1, 5)
            check(f"callout {name} text line{i+1} band ~{ty0}..{ty1}", ok,
                  f"got ({gy0:.1f}..{gy1:.1f})")

# ---- 7. removed parent elements are absent (white in render) --------------------
def is_white(img, y0, y1, x0, x1):
    reg = region(img, y0, y1, x0, x1)
    return int((reg.min(axis=2) > 235).sum()) > 0.9 * reg.shape[0] * reg.shape[1]
check("final_ellipse region white (removed)", is_white(r, 312, 348, 790, 878))
check("parent label_vectors region white (removed)", is_white(r, 295, 330, 390, 432))
check("parent label_predicted region white (removed)", is_white(r, 295, 330, 710, 780))
check("curve2 region white (removed)", is_white(r, 270, 305, 870, 895))

# ---- 8. inherited regions pixel-equal to the certified parent render ------------
# (same component draw; badge zone x875..911 excluded — numeral 16 vs 9 by law)
mask = np.ones((1125, 2001), bool)
mask[int(43*S):int(110*S), :] = False          # title band holds no delta but keep it: actually title identical; keep
mask[int(43*S):int(540*S), int(870*S):int(915*S)] = False  # badge zone
dr = (np.abs(r.astype(int) - p.astype(int)).max(axis=2) > 48) & mask
# expected-delta zones (frame coords): ellipse+curve1 (x70..250 y125..250), box_pre band
# (x125..255 y205..270), arrow1 (x232..296 y230..244), box5 (x744..868 y204..270),
# callout band (x80..580 y278..400), removed-elements zones (x705..900 y265..355)
dz = np.zeros((1125, 2001), bool)
for (y0, y1, x0, x1) in [(125, 250, 70, 250), (205, 270, 125, 255), (230, 244, 232, 296),
                         (204, 270, 744, 868), (278, 400, 80, 580), (265, 355, 705, 900),
                         (264, 400, 575, 710)]:
    dz[int(y0*S):int((y1+1)*S), int(x0*S):int((x1+1)*S)] = True
stray = dr & ~dz
check("inherited regions pixel-equal to certified parent render", int(stray.sum()) < 400,
      f"stray diff px={int(stray.sum())} (tol 400 ~ 92 frame px)")

print()
if fails:
    print(f"SELF-CHECK RESULT: {len(fails)} FAIL(ures): {fails}")
    sys.exit(1)
print("SELF-CHECK RESULT: ALL PASS")
