#!/usr/bin/env python3
"""measure_original6.py — slide 019 final geometry/color probes (pre-build).

Settles: exact box outer rects (8 boxes), verr rounded-rect + 2 text columns,
red families (title/arrow/container-dash/panel-border cores vs slide_009/018),
x70 stroke extent, ellipse outline/text, annotation border, samples/pred edges.
960x540 frame, 1px = 1pt.
"""
import numpy as np
from PIL import Image
from collections import Counter

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_019.jpg"
F9 = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_009.jpg"
F18 = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_018.jpg"

im = np.asarray(Image.open(F).convert("RGB")).astype(int)
im9 = np.asarray(Image.open(F9).convert("RGB")).astype(int)
im18 = np.asarray(Image.open(F18).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def core(sub, n=5):
    """top-n modal colors of a pixel sub-array (flattened)."""
    px = sub.reshape(-1, 3)
    c = Counter(map(tuple, px))
    return [(f"#{rr:02X}{gg:02X}{bb:02X}", n_) for (rr, gg, bb), n_ in c.most_common(n)]

def ink_mask(sub):
    rr, gg, bb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    return (rr < 140) & (gg < 120) & (bb < 120)

# ---- 1. panel border reds (slide 19) -------------------------------------------
print("== panel borders (19) ==")
for name, sl in [("left x56..60 y300", (slice(300, 301), slice(56, 61))),
                 ("x70 y300", (slice(300, 301), slice(69, 72))),
                 ("right x893..896 y300", (slice(300, 301), slice(893, 897))),
                 ("top y99..102 x500", (slice(99, 103), slice(500, 501))),
                 ("bottom y462..466 x500", (slice(462, 467), slice(500, 501)))]:
    print(f"  {name}:", [tuple(v) for v in im[sl][0]])

# x70 stroke y-extent: red pixels in cols 69..71
redcol = (r > 110) & (g < 110) & (b < 110)
col70 = np.where(redcol[:, 69:72].any(axis=1))[0]
print("  x70 red rows:", col70.min() if len(col70) else None, "..", col70.max() if len(col70) else None, "n=", len(col70))
col57 = np.where(redcol[:, 56:59].any(axis=1))[0]
print("  x57-58 red rows:", col57.min() if len(col57) else None, "..", col57.max() if len(col57) else None, "n=", len(col57))
col894 = np.where(redcol[:, 893:896].any(axis=1))[0]
print("  x894 red rows:", col894.min() if len(col894) else None, "..", col894.max() if len(col894) else None, "n=", len(col894))
row100 = np.where(redcol[99:102, :].any(axis=0))[0]
print("  y100 red cols:", row100.min() if len(row100) else None, "..", row100.max() if len(row100) else None, "n=", len(row100))
row464 = np.where(redcol[462:467, :].any(axis=0))[0]
print("  y464 red cols:", row464.min() if len(row464) else None, "..", row464.max() if len(row464) else None, "n=", len(row464))
print("  x70 stroke core:", core(im[150:450, 69:72], 3))
print("  x57 stroke core:", core(im[150:450, 56:59], 3))
print("  panel border 19 vs 9 vs 18 @ (x57..72,y300):", [tuple(v) for v in im[300, 56:73]],
      "| 9:", [tuple(v) for v in im9[300, 56:73]], "| 18:", [tuple(v) for v in im18[300, 56:73]])

# ---- 2. title core (19 vs 9 vs 18, same window method) --------------------------
def title_core(img, x0, x1, y0=68, y1=93):
    sub = img[y0:y1, x0:x1]
    m = (sub[:, :, 0] > 100) & (sub[:, :, 1] < 90) & (sub[:, :, 2] < 90)
    return core(sub[m], 4)
print("== title cores ==")
print("  19 (x222..654):", title_core(im, 222, 654))
print("  18 (x223..654):", title_core(im18, 223, 654))
print("   9 (x219..715):", title_core(im9, 219, 715))

# ---- 3. chain arrows core --------------------------------------------------------
print("== chain arrow cores (19) ==")
for name, (x0, x1) in [("a1 input->pre", (160, 194)), ("a2 pre->extr", (284, 318)),
                       ("a3 extr->sel", (408, 428)), ("a4 sel->class", (517, 532)),
                       ("a5 class->pred", (636, 659)), ("a6 pred->verr", (739, 751)),
                       ("a7 verr<-samples", (794, 807))]:
    sub = im[231:240, x0:x1]
    m = (sub[:, :, 0] > 110) & (sub[:, :, 1] < 100) & (sub[:, :, 2] < 100)
    print(f"  {name} n={int(m.sum())} core:", core(sub[m], 3))
# arrow 7 direction: ink profile along x at y233..237
sub = im[231:240, 788:815]
m = (sub[:, :, 0] > 110) & (sub[:, :, 1] < 100) & (sub[:, :, 2] < 100)
for x in range(m.shape[1]):
    print("   a7 x", 788 + x, "rows", np.where(m[:, x])[0] + 231)

# ---- 4. container dashes + fill cores --------------------------------------------
print("== container ==")
top = im[195:199, 210:620]
mred = (top[:, :, 0] > 110) & (top[:, :, 1] < 110) & (top[:, :, 2] < 110)
print("  dash core:", core(top[mred], 3))
fill = im[200:206, 300:340]
print("  fill core (y200..206 x300..340):", core(fill, 4))
fill2 = im[265:270, 610:650]
print("  fill core (y265..270 x610..650):", core(fill2, 4))

# ---- 5. verr box: outer rect, border color, rounded corners, text columns --------
print("== verr ==")
# border: scan row y=210 (above text? text y183..286 — use y=175 near top and x-scan)
rowy = 178
print("  row y=178 x742..800:", [f"{x}:{tuple(im[rowy, x])}" for x in range(742, 800)])
colx = 768
print("  col x=768 y165..175:", [f"{y}:{tuple(im[y, colx])}" for y in range(165, 176)])
print("  col x=768 y292..302:", [f"{y}:{tuple(im[y, colx])}" for y in range(292, 303)])
# text columns: dark-red ink inside fill zone x750..790, y175..295
sub = im[175:296, 748:792]
rr, gg, bb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
mtxt = (rr > 90) & (rr < 200) & (gg < 90) & (bb < 90)
cols = mtxt.sum(axis=0)
print("  text col profile x748+i:", {748 + i: int(c) for i, c in enumerate(cols) if c})
colink = mtxt.sum(axis=1)
print("  text row extent:", np.where(mtxt.any(axis=1))[0] + 175)
# per column band
runs_ = []
s = p = None
for i, c in enumerate(cols):
    if c > 0:
        if s is None:
            s = p = i
        else:
            p = i
    else:
        if s is not None:
            runs_.append((748 + s, 748 + p))
            s = None
if s is not None:
    runs_.append((748 + s, 748 + p))
print("  text column x-runs:", runs_)
for (cx0, cx1) in runs_:
    m2 = mtxt[:, cx0 - 748:cx1 - 748 + 1]
    ys = np.where(m2.any(axis=1))[0] + 175
    print(f"   run x{cx0}..{cx1}: y {ys.min()}..{ys.max()} len={ys.max()-ys.min()+1}")
print("  verr text core:", core(sub[mtxt], 4))
print("  verr border core (x746..749 y200..260):", core(im[200:260, 746:750][(im[200:260, 746:750, 0] > 110) & (im[200:260, 746:750, 1] < 110)], 3))
print("  verr fill core (y220..260 x756..786):", core(im[220:260, 756:787], 4))

# ---- 6. exact box outer rects via border scans ------------------------------------
print("== box outer rects ==")
def box_rect(name, xwin, ywin, edge_fn):
    x0, x1 = xwin
    y0, y1 = ywin
    sub = im[y0:y1, x0:x1]
    m = edge_fn(sub)
    ys, xs = np.where(m)
    if not len(xs):
        print(f"  {name}: NO INK")
        return
    print(f"  {name}: x {x0+xs.min()}..{x0+xs.max()} y {y0+ys.min()}..{y0+ys.max()} (w{xs.max()-xs.min()+1} h{ys.max()-ys.min()+1})")

dark = lambda s: (s[:, :, 0] < 150) & (s[:, :, 1] < 130) & (s[:, :, 2] < 130)
# input (brown border): window tight around box, exclude blue head (x100..135 y<215) and arrow (y>228? no arrow y231.. inside) — use border scan on rows/cols
box_rect("input", (74, 164), (206, 262), dark)
box_rect("pre", (198, 292), (202, 268), dark)          # incl pencil (x245..280 y206..231) -> top may read 206
box_rect("extr", (318, 412), (202, 268), dark)
box_rect("sel", (426, 528), (202, 268), dark)
box_rect("classif", (530, 634), (200, 270), dark)
box_rect("pred", (655, 740), (206, 262), dark)
box_rect("samples", (808, 890), (206, 262), dark)
# cleaner: per-box border pixel walk on the center row/col
def edge_walk(name, ycen, x0, x1):
    row = im[ycen, x0:x1]
    m = dark(row.reshape(1, -1, 3))[0]
    xs = np.where(m)[0] + x0
    print(f"  {name} row y={ycen} dark cols {x0}..{x1}: {xs[:6]}...{xs[-6:] if len(xs)>6 else ''}")
edge_walk("input", 234, 74, 100)
edge_walk("input", 234, 145, 170)
edge_walk("pre", 234, 196, 216)
edge_walk("pre", 234, 270, 292)
edge_walk("extr", 234, 314, 330)
edge_walk("extr", 234, 396, 414)
edge_walk("sel", 234, 424, 438)
edge_walk("sel", 234, 500, 520)
edge_walk("classif", 234, 528, 542)
edge_walk("classif", 234, 618, 636)
edge_walk("pred", 234, 652, 672)
edge_walk("pred", 234, 724, 742)
edge_walk("samples", 234, 806, 822)
edge_walk("samples", 234, 872, 890)
def edge_walkv(name, xcen, y0, y1):
    col = im[y0:y1, xcen]
    m = dark(col.reshape(-1, 1, 3))[:, 0]
    ys = np.where(m)[0] + y0
    print(f"  {name} col x={xcen} dark rows {y0}..{y1}: {ys[:6]}...{ys[-6:] if len(ys)>6 else ''}")
edge_walkv("input", 118, 200, 220)
edge_walkv("input", 118, 250, 268)
edge_walkv("pre", 242, 198, 214)
edge_walkv("pre", 242, 252, 268)   # note pencil zone x245..280 — use x242
edge_walkv("extr", 362, 198, 214)
edge_walkv("extr", 362, 252, 268)
edge_walkv("sel", 470, 198, 214)
edge_walkv("sel", 470, 252, 268)
edge_walkv("classif", 580, 198, 216)
edge_walkv("classif", 580, 252, 270)
edge_walkv("pred", 698, 204, 218)
edge_walkv("pred", 698, 248, 262)
edge_walkv("samples", 846, 200, 220)
edge_walkv("samples", 846, 250, 268)

# ---- 7. box borders colors (fresh cores) -------------------------------------------
print("== box border cores ==")
print("  input border (x80..82 y220..250):", core(im[220:250, 79:83], 3))
print("  pre border (x203..207 y220..250):", core(im[220:250, 203:208], 4))
print("  extr border (x321..325 y220..250):", core(im[220:250, 320:325], 4))
print("  sel border (x429..433 y220..250):", core(im[220:250, 428:433], 4))
print("  classif border (x533..537 y220..250):", core(im[220:250, 532:538], 4))
print("  pred border (x660..664 y220..250):", core(im[220:250, 659:664], 4))
print("  samples border (x810..814 y220..250):", core(im[220:250, 809:814], 3))
print("  extr border top (y207..211 x340..390):", core(im[206:212, 340:390], 4))
print("  pre border top (y207..211 x215..245):", core(im[206:212, 215:245], 4))

# ---- 8. fills (fresh cores) ---------------------------------------------------------
print("== fill cores ==")
print("  input fill:", core(im[225:245, 90:150], 3))
print("  pre fill:", core(im[235:250, 215:270], 3))
print("  extr fill:", core(im[225:245, 330:400], 3))
print("  sel fill:", core(im[225:245, 440:500], 3))
print("  classif fill:", core(im[220:250, 545:625], 3))
print("  pred fill:", core(im[225:245, 670:730], 3))
print("  samples fill:", core(im[225:245, 820:875], 3))
print("  ellipse fill:", core(im[125:145, 385:455], 3))
print("  ellipse outline (top y110..113 x410..430):", core(im[109:114, 410:430], 4))
print("  annot fill:", core(im[342:352, 280:300], 3))
print("  annot border left (x260..263 y350..370):", core(im[350:370, 259:264], 4))
print("  annot text core (dark):", core(im[343:375, 303:700][ink_mask(im[343:375, 303:700])], 4))
print("  ellipse text ink (x388..446 y120..150):", core(im[120:150, 388:446][ink_mask(im[120:150, 388:446])], 3))
print("  input text ink:", core(im[220:252, 86:152][ink_mask(im[220:252, 86:152])], 3))
print("  classif white text core:", core(im[229:241, 540:622], 3))

# text ink extents per box (clean, for font sizing)
def text_extent(name, x0, x1, y0, y1):
    sub = im[y0:y1, x0:x1]
    m = ink_mask(sub)
    ys, xs = np.where(m)
    if not len(xs):
        print(f"  {name}: none")
        return
    print(f"  {name} ink x {x0+xs.min()}..{x0+xs.max()} y {y0+ys.min()}..{y0+ys.max()}")
text_extent("input line1", 86, 152, 218, 236)
text_extent("input line2", 86, 152, 236, 254)
text_extent("pre line1 'Pre'", 210, 244, 214, 236)
text_extent("pre line2 'processing'", 210, 282, 236, 254)
text_extent("extr line1", 322, 404, 214, 236)
text_extent("extr line2", 322, 404, 236, 252)
text_extent("sel line1", 436, 506, 214, 236)
text_extent("sel line2", 436, 506, 236, 252)
text_extent("pred line1", 662, 734, 216, 236)
text_extent("pred line2", 662, 734, 236, 252)
text_extent("samples line1", 812, 884, 218, 236)
text_extent("samples line2", 812, 884, 236, 254)
text_extent("ellipse 'Training'", 380, 460, 118, 136)
text_extent("ellipse 'Data'", 380, 460, 136, 152)
text_extent("annot line1", 300, 702, 340, 358)
text_extent("annot line2", 300, 702, 358, 378)
text_extent("classif", 536, 630, 226, 244)
