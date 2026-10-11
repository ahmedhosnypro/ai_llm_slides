#!/usr/bin/env python3
"""Precision probes for slide-029 delta geometry + colors."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
A = np.asarray(Image.open(f"{V}/unique_slides/slide_029.jpg").convert("RGB"), dtype=np.int16)
B = np.asarray(Image.open(f"{V}/unique_slides/slide_026.jpg").convert("RGB"), dtype=np.int16)

def px(img, x, y):
    return "%02X%02X%02X" % tuple(int(v) for v in img[y, x])

def bbox(img, x0, y0, x1, y1, pred):
    reg = img[y0:y1, x0:x1]
    m = pred(reg)
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    return (int(x0 + xs.min()), int(y0 + ys.min()), int(x0 + xs.max()), int(y0 + ys.max()))

def avg(img, x0, y0, x1, y1):
    return "%02X%02X%02X" % tuple(int(round(v)) for v in img[y0:y1, x0:x1].reshape(-1, 3).mean(axis=0))

redp = lambda reg: (reg[:, :, 0] > 130) & (reg[:, :, 0] - reg[:, :, 1] > 60) & (reg[:, :, 0] - reg[:, :, 2] > 60)
magp = lambda reg: (reg[:, :, 0] > 120) & (reg[:, :, 0] < 215) & (reg[:, :, 1] < 140) & (reg[:, :, 2] > 130) & (reg[:, :, 2] - reg[:, :, 1] > 35)
bluep = lambda reg: (reg[:, :, 2] > 120) & (reg[:, :, 2] - reg[:, :, 0] > 50) & (reg[:, :, 2] - reg[:, :, 1] > 40)
darkp = lambda reg: reg.sum(axis=2) < 260

print("== A/B. CALLOUTS ==")
palecyan = lambda reg: (reg[:, :, 2] > 238) & (reg[:, :, 1] > 238) & (reg[:, :, 2] - reg[:, :, 0] > 4) & (reg[:, :, 1] - reg[:, :, 0] > 4)
noncanvas = lambda reg: ~((reg[:, :, 0] > 235) & (reg[:, :, 1] > 210) & (reg[:, :, 1] < 245) & (reg[:, :, 2] < 225))
print(" c1 fill interior samples:", avg(A, 340, 162, 355, 170), avg(A, 460, 160, 475, 168), avg(A, 330, 143, 470, 146))
print(" c1 fill bbox-ish (noncanvas in y142..186 x300..500):", bbox(A, 300, 142, 500, 187, noncanvas))
print(" c1 text dark bbox:", bbox(A, 310, 144, 500, 186, darkp))
print(" c1 magenta-only bbox:", bbox(A, 310, 144, 500, 186, magp))
print(" c1 red-only bbox:", bbox(A, 310, 144, 500, 186, redp))
print(" c1 line1 dark bbox y144..163:", bbox(A, 310, 144, 500, 164, darkp))
print(" c1 line2 dark bbox y164..186:", bbox(A, 310, 164, 500, 186, darkp))
# text core colors: darkest 20 pixels in magenta class and red class
reg = A[144:186, 315:495]
mm = magp(reg); rr = redp(reg)
if mm.sum():
    vals = reg[mm]; s = vals.sum(axis=1); idx = np.argsort(s)[:20]
    print(" c1 magenta darkest20 avg:", "%02X%02X%02X" % tuple(vals[idx].mean(axis=0).astype(int)))
if rr.sum():
    vals = reg[rr]; s = vals.sum(axis=1); idx = np.argsort(s)[:20]
    print(" c1 red darkest20 avg:", "%02X%02X%02X" % tuple(vals[idx].mean(axis=0).astype(int)))
# red vs magenta word x-ranges on line1 and line2
for (y0, y1, tag) in [(147, 163, "c1L1"), (165, 182, "c1L2")]:
    reg = A[y0:y1, 310:500]
    rcols = np.nonzero(redp(reg).sum(axis=0) > 0)[0] + 310
    mcols = np.nonzero(magp(reg).sum(axis=0) > 0)[0] + 310
    def runs(cols):
        out = []
        if len(cols) == 0: return out
        s = p = cols[0]
        for c in cols[1:]:
            if c - p > 6:
                out.append((s, p)); s = c
            p = c
        out.append((s, p)); return out
    print(f" {tag} red x-runs:", runs(rcols))
    print(f" {tag} mag x-runs:", runs(mcols))

print(" c2 fill interior samples:", avg(A, 650, 160, 665, 168), avg(A, 800, 160, 815, 168))
print(" c2 fill bbox-ish:", bbox(A, 620, 142, 860, 187, noncanvas))
print(" c2 text dark bbox:", bbox(A, 630, 144, 855, 186, darkp))
print(" c2 line1 y144..163 dark:", bbox(A, 630, 144, 855, 164, darkp))
print(" c2 line2 y164..186 dark:", bbox(A, 630, 164, 855, 186, darkp))
reg = A[144:186, 635:850]
mm = magp(reg); rr = redp(reg)
if mm.sum():
    vals = reg[mm]; idx = np.argsort(vals.sum(axis=1))[:20]
    print(" c2 mag darkest20 avg:", "%02X%02X%02X" % tuple(vals[idx].mean(axis=0).astype(int)))
if rr.sum():
    vals = reg[rr]; idx = np.argsort(vals.sum(axis=1))[:20]
    print(" c2 red darkest20 avg:", "%02X%02X%02X" % tuple(vals[idx].mean(axis=0).astype(int)))
for (y0, y1, tag) in [(147, 163, "c2L1"), (165, 182, "c2L2")]:
    reg = A[y0:y1, 630:855]
    rcols = np.nonzero(redp(reg).sum(axis=0) > 0)[0] + 630
    mcols = np.nonzero(magp(reg).sum(axis=0) > 0)[0] + 630
    def runs2(cols):
        out = []
        if len(cols) == 0: return out
        s = p = cols[0]
        for c in cols[1:]:
            if c - p > 6:
                out.append((s, p)); s = c
            p = c
        out.append((s, p)); return out
    print(f" {tag} red x-runs:", runs2(rcols))
    print(f" {tag} mag x-runs:", runs2(mcols))
# callout borders: sample edge rows/cols
print(" c1 border probes top/bot/left/right:", px(A, 400, 141), px(A, 400, 142), px(A, 400, 184), px(A, 400, 185), px(A, 316, 165), px(A, 317, 165), px(A, 483, 165), px(A, 484, 165))
print(" c2 border probes:", px(A, 700, 141), px(A, 700, 142), px(A, 700, 184), px(A, 700, 185), px(A, 634, 165), px(A, 635, 165), px(A, 845, 165), px(A, 846, 165))

print("\n== C. QUERY BOX + Q BADGE ==")
orange_fill = lambda reg: (reg[:, :, 0] > 230) & (reg[:, :, 0] - reg[:, :, 2] > 40) & (reg[:, :, 1] - reg[:, :, 2] > 20) & (reg[:, :, 1] < 230)
print(" box fill samples:", avg(A, 120, 428, 135, 436), avg(A, 200, 452, 220, 457), avg(A, 120, 452, 130, 457))
print(" box fill bbox:", bbox(A, 90, 410, 300, 470, orange_fill))
print(" box text red bbox:", bbox(A, 115, 422, 245, 460, redp))
print(" Q badge red bbox:", bbox(A, 242, 420, 285, 460, redp))
print(" Q badge interior probes:", px(A, 258, 439), px(A, 252, 439), px(A, 265, 439), px(A, 258, 432), px(A, 258, 447))
reg = A[422:460, 115:245]
rr = redp(reg)
if rr.sum():
    vals = reg[rr]; idx = np.argsort(vals.sum(axis=1))[:20]
    print(" query text darkest20:", "%02X%02X%02X" % tuple(vals[idx].mean(axis=0).astype(int)))
print(" query text line1 bbox y424..442:", bbox(A, 115, 424, 245, 442, redp))
print(" query text line2 bbox y442..458:", bbox(A, 115, 442, 245, 458, redp))
print(" box border probes:", px(A, 170, 420), px(A, 170, 421), px(A, 170, 459), px(A, 170, 460), px(A, 111, 440), px(A, 240, 440), px(A, 241, 440))
# Q badge ring: scan row through badge center
row = A[439, 244:274]
print(" Q badge row y439:", " ".join("%02X%02X%02X" % tuple(int(v) for v in row[i]) for i in range(0, 30, 3)))

print("\n== D. RESULT BOX ==")
print(" fill:", avg(A, 600, 455, 640, 462), avg(A, 700, 492, 740, 497))
print(" border probes top:", px(A, 650, 432), px(A, 650, 433), px(A, 650, 434), " bottom:", px(A, 650, 498), px(A, 650, 499), px(A, 650, 500))
print(" border probes left:", px(A, 557, 465), px(A, 558, 465), px(A, 559, 465), " right:", px(A, 825, 465), px(A, 826, 465), px(A, 827, 465))
print(" box white bbox:", bbox(A, 540, 420, 900, 520, lambda reg: (reg[:, :, 0] > 235) & (reg[:, :, 1] > 235) & (reg[:, :, 2] > 235)))
print(" line bboxes: L1", bbox(A, 560, 440, 825, 458, darkp), " L2", bbox(A, 560, 460, 825, 477, darkp), " L3", bbox(A, 560, 478, 825, 496, darkp))
for (y0, y1, tag) in [(440, 458, "rL1"), (460, 477, "rL2"), (478, 496, "rL3")]:
    reg = A[y0:y1, 560:825]
    bcols = np.nonzero(bluep(reg).sum(axis=0) > 0)[0] + 560
    rcols = np.nonzero(redp(reg).sum(axis=0) > 0)[0] + 560
    def runs3(cols):
        out = []
        if len(cols) == 0: return out
        s = p = cols[0]
        for c in cols[1:]:
            if c - p > 7:
                out.append((s, p)); s = c
            p = c
        out.append((s, p)); return out
    print(f" {tag} blue x-runs:", runs3(bcols))
    print(f" {tag} red  x-runs:", runs3(rcols))
reg = A[440:496, 560:825]
bb = bluep(reg); rr = redp(reg)
if bb.sum():
    vals = reg[bb]; idx = np.argsort(vals.sum(axis=1))[:20]
    print(" result blue darkest20:", "%02X%02X%02X" % tuple(vals[idx].mean(axis=0).astype(int)))
if rr.sum():
    vals = reg[rr]; idx = np.argsort(vals.sum(axis=1))[:20]
    print(" result red darkest20:", "%02X%02X%02X" % tuple(vals[idx].mean(axis=0).astype(int)))

print("\n== E. K/V/Q badge colors ==")
print(" K circle fill:", avg(A, 154, 336, 158, 348), " K letter probe:", px(A, 160, 342), px(A, 161, 342), px(A, 162, 342))
print(" V circle fill:", avg(A, 739, 336, 743, 348), " V letter probe:", px(A, 747, 342), px(A, 748, 342))
print(" K bbox tight:", bbox(A, 145, 325, 185, 362, redp), " V bbox tight:", bbox(A, 730, 325, 768, 362, redp))

print("\n== F. KEYs / Values tan label boxes ==")
tanfill = lambda reg: (reg[:, :, 0] > 200) & (reg[:, :, 0] < 250) & (reg[:, :, 1] > 170) & (reg[:, :, 1] < 225) & (reg[:, :, 2] > 130) & (reg[:, :, 2] < 190)
print(" KEYs box bbox (tan):", bbox(A, 40, 180, 160, 225, tanfill))
print(" Values box bbox (tan):", bbox(A, 740, 180, 860, 225, tanfill))
print(" KEYs fill sample:", avg(A, 75, 200, 95, 208), " Values fill:", avg(A, 775, 200, 795, 208))
print(" KEYs text dark bbox:", bbox(A, 50, 185, 150, 222, darkp))
print(" Values text dark bbox:", bbox(A, 750, 185, 850, 222, darkp))
reg = A[185:222, 60:140]
dd = darkp(reg)
if dd.sum():
    vals = reg[dd]; idx = np.argsort(vals.sum(axis=1))[:15]
    print(" KEYs text darkest15:", "%02X%02X%02X" % tuple(vals[idx].mean(axis=0).astype(int)))
print(" KEYs border probes:", px(A, 98, 191), px(A, 98, 192), px(A, 98, 216), px(A, 98, 217), px(A, 64, 204), px(A, 133, 204))

print("\n== G. FEED CURVES ==")
print(" LEFT curve child:", px(A, 130, 468), px(A, 112, 460), px(A, 104, 448), px(A, 102, 430), px(A, 102, 415))
print(" LEFT curve parent:", px(B, 130, 468), px(B, 112, 460), px(B, 104, 448), px(B, 102, 430), px(B, 102, 415))
print(" LEFT head child region probes:", px(A, 98, 408), px(A, 100, 410), px(A, 99, 414), px(A, 97, 404))
print(" LEFT head parent:", px(B, 98, 408), px(B, 100, 410), px(B, 99, 414), px(B, 97, 404))
print(" RIGHT curve child:", px(A, 790, 425), px(A, 795, 416), px(A, 801, 404), px(A, 780, 440))
print(" RIGHT curve parent:", px(B, 790, 425), px(B, 795, 416), px(B, 801, 404), px(B, 780, 440))
print(" RIGHT head child:", px(A, 802, 400), px(A, 804, 402), px(A, 800, 398), px(A, 806, 404))
print(" RIGHT head parent:", px(B, 802, 400), px(B, 804, 402), px(B, 800, 398), px(B, 806, 404))
print(" right-curve-behind-box probes child:", px(A, 560, 492), px(A, 615, 487), px(A, 660, 483), px(A, 700, 476))
print(" mystery probes:", px(A, 670, 503), px(A, 675, 505), px(A, 745, 507), px(A, 848, 519), px(A, 475, 417), px(A, 505, 450))

print("\n== H. STRIP delta (child vs parent) ==")
D = (np.abs(A - B).sum(axis=2) > 60)
reg = D[468:522, 170:500]
ys, xs = np.nonzero(reg)
if len(xs):
    print(" strip diff bbox:", 170 + xs.min(), 468 + ys.min(), 170 + xs.max(), 468 + ys.max(), "count", len(xs))
    colsum = reg.sum(axis=0)
    nz = np.nonzero(colsum)[0] + 170
    segs = []
    if len(nz):
        s = p = nz[0]
        for c in nz[1:]:
            if c - p > 8:
                segs.append((s, p)); s = c
            p = c
        segs.append((s, p))
    print(" strip diff col segs:", segs)
print(" X2 highlight region child probes:", px(A, 300, 478), px(A, 300, 494), px(A, 270, 488), px(A, 330, 488), px(A, 285, 497), px(A, 263, 476))
print(" X2 highlight region parent probes:", px(B, 300, 478), px(B, 300, 494), px(B, 270, 488), px(B, 330, 488), px(B, 285, 497), px(B, 263, 476))
print(" child glyph label 3 probe:", px(A, 370, 492), px(A, 371, 494), " parent:", px(B, 370, 492), px(B, 371, 494))
print(" child glyph label 4 probe:", px(A, 445, 492), px(A, 446, 494), " parent:", px(B, 445, 492), px(B, 446, 494))
print(" child glyph label 1 probe:", px(A, 208, 492), " parent:", px(B, 208, 492))

print("\n== I. TITLE / SUBTITLE ==")
print(" title L1 black ink bbox:", bbox(A, 100, 45, 870, 79, darkp))
print(" highlight bbox:", bbox(A, 100, 45, 870, 82, lambda reg: (reg[:, :, 0] > 235) & (reg[:, :, 1] > 225) & (reg[:, :, 2] < 190) & (reg[:, :, 0] - reg[:, :, 2] > 50)))
print(" highlight color:", avg(A, 430, 56, 445, 62), avg(A, 750, 66, 765, 72))
print(" title ink sample (dark core):", px(A, 300, 65), px(A, 320, 65))
print(" subtitle ink bbox:", bbox(A, 90, 79, 880, 106, darkp))
redsub = lambda reg: (reg[:, :, 0] > 110) & (reg[:, :, 0] - reg[:, :, 1] > 55) & (reg[:, :, 0] - reg[:, :, 2] > 45)
reg = A[80:104, 90:880]
rcols = np.nonzero(redsub(reg).sum(axis=0) > 0)[0] + 90
def runs4(cols):
    out = []
    if len(cols) == 0: return out
    s = p = cols[0]
    for c in cols[1:]:
        if c - p > 8:
            out.append((s, p)); s = c
        p = c
    out.append((s, p)); return out
print(" subtitle red x-runs:", runs4(rcols))
rr = redsub(reg)
if rr.sum():
    vals = reg[rr]; idx = np.argsort(vals.sum(axis=1))[:20]
    print(" subtitle red darkest20:", "%02X%02X%02X" % tuple(vals[idx].mean(axis=0).astype(int)))
print(" subtitle black core:", px(A, 200, 90), px(A, 480, 90))
print(" subtitle line y extents: ink rows", bbox(A, 90, 75, 880, 108, darkp))
