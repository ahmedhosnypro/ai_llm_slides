#!/usr/bin/env python3
"""Probe round 3: verr border, container dashes, annot edges, panel, blackbar, text bands, box borders."""
import numpy as np
from PIL import Image
from collections import Counter

IM = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_019.jpg").convert("RGB")).astype(int)
r, g, b = IM[..., 0], IM[..., 1], IM[..., 2]
lum = (r * 299 + g * 587 + b * 114) // 1000

def modal(px, n=3):
    if len(px) == 0: return "[]"
    c = Counter((int(p[0]) // 16 * 16, int(p[1]) // 16 * 16, int(p[2]) // 16 * 16) for p in np.atleast_2d(px))
    return [(f"#{v[0]:02X}{v[1]:02X}{v[2]:02X}", k) for v, k in c.most_common(n)]

def runs(mask1d, base):
    out, s = [], None
    for i, v in enumerate(mask1d):
        if v and s is None: s = i
        elif not v and s is not None: out.append((base + s, base + i - 1)); s = None
    if s is not None: out.append((base + s, base + len(mask1d) - 1))
    return out

print("== VERR border: red-ish strokes cols/rows ==")
rred = (r > 150) & (g < 95) & (b < 95)
for x in (744, 746, 748, 750, 793, 795, 797, 799):
    rr = runs(rred[165:315, x], 165)
    if rr: print(f" col {x}: {rr} modal", modal(IM[[y for y0, y1 in rr for y in range(y0, y1+1)], x], 3))
    else: print(f" col {x}: none")
for y in (170, 172, 174, 302, 305, 308):
    rr = runs(rred[y, 740:805], 740)
    if rr: print(f" row {y}: {rr} modal", modal(IM[y, [x for x0, x1 in rr for x in range(x0, x1+1)]], 3))
    else: print(f" row {y}: none")
print(" verr fill extent: pink row200 runs:", runs(((r>230)&(g>140)&(g<215)&(b>140)&(b<220)&(r>g+30))[200, 730:820], 730),
      " col760:", runs(((r>230)&(g>140)&(g<215)&(b>140)&(b<220)&(r>g+30))[165:315, 760], 165))

print("== CONTAINER dashes ==")
cred = (r > 130) & (g < 80) & (b < 80)
for y in (194, 195, 196, 197, 198, 271, 272, 273, 274, 275):
    n = int(cred[y, 210:620].sum())
    print(f" row {y}: red n={n}", runs(cred[y, 210:620], 210)[:5] if n else "")
for x in (194, 196, 198, 200, 202, 624, 626, 628, 630, 634, 640, 650, 656, 660):
    n = int(cred[200:270, x].sum())
    print(f" col {x}: red n={n}", runs(cred[200:270, x], 200)[:4] if n else "")
print(" fill samples: (300,212)", IM[212,300], "(310,250)", IM[250,310], "(618,268)", IM[268,618], "(205,235)", IM[235,205])
print(" dash modal:", modal(IM[196, [x for x0,x1 in runs(cred[196,210:620],210)[:10] for x in range(x0,x1+1)]], 3))

print("== ANNOT edges ==")
grn = (g > r - 5) & (g > b - 5) & (lum < 225)
for y in (320, 322, 324, 326, 376, 378, 380, 382):
    rr = runs(grn[y, 250:760], 250)
    if rr: print(f" row {y}: nruns={len(rr)} first {rr[:3]} last {rr[-3:]} modal", modal(IM[y, [x for x0,x1 in rr[:6] for x in range(x0,x1+1)]], 3))
    else: print(f" row {y}: none")
for x in (258, 260, 262, 264, 266, 738, 740, 742, 744):
    rr = runs(grn[315:395, x], 315)
    if rr: print(f" col {x}: {rr[:4]} modal", modal(IM[[y for y0,y1 in rr[:4] for y in range(y0,y1+1)], x], 3))
    else: print(f" col {x}: none")

print("== PANEL border ==")
print(" row235 x60..100 runs(lum<190):", runs(lum[235, 60:100] < 190, 60), " modal:", modal(IM[235, 69:72].reshape(-1,3), 3))
print(" row235 x885..910:", runs(lum[235, 885:910] < 190, 885), " modal:", modal(IM[235, 893:896].reshape(-1,3), 3))
print(" col480 y92..108:", runs(lum[92:108, 480] < 190, 92), " modal:", modal(IM[100, 480:482].reshape(-1,3), 3))
print(" col480 y455..475:", runs(lum[455:475, 480] < 190, 455), " modal:", modal(IM[464, 480:482].reshape(-1,3), 3))
print(" panel bottom row464 extent:", runs(lum[464, 60:920] < 190, 60)[:2], runs(lum[464, 60:920] < 190, 60)[-2:])

print("== BLACKBAR ==")
blk = lum < 60
print(" row528:", runs(blk[528, 0:960], 0)[:3], " col100:", runs(blk[500:540, 100], 500))
print(" row520 n:", int(blk[520, 0:960].sum()), " row535 n:", int(blk[535, 0:960].sum()))

print("== TEXT BANDS ==")
def bands(x0, y0, x1, y1, label, thr=140):
    m = lum[y0:y1, x0:x1] < thr
    rows = np.nonzero(m.any(axis=1))[0] + y0
    if not len(rows): print(f" {label}: none"); return
    br, s = [], rows[0]
    for a, bb in zip(rows, rows[1:]):
        if bb - a > 2: br.append((int(s), int(a))); s = bb
    br.append((int(s), int(rows[-1])))
    cols = np.nonzero(m.any(axis=0))[0] + x0
    print(f" {label}: bands {br} cols {int(cols.min())}..{int(cols.max())}")
bands(84, 205, 158, 268, "input")
bands(808, 205, 886, 268, "samples")
bands(200, 236, 292, 268, "pre-line2")
bands(198, 236, 292, 232, "pre-zone-top")  # pencil zone handled separately
bands(318, 210, 412, 268, "extr")
bands(430, 210, 515, 268, "sel")
bands(658, 210, 740, 268, "pred")
bands(388, 113, 452, 152, "ellipse-text")
print(" classif white text: rows y226..246 whiteish x536..628:")
wt = (r>200)&(g>150)&(b>150)
rr = runs(wt[226:246, 536:628].any(axis=1), 226)
print("  white-text row runs:", rr, " cols:", runs(wt[226:246, 536:628].any(axis=0), 536))

print("== BOX BORDER STROKE modals (edge pixels) ==")
print(" input L border x79-81 y210..260:", modal(IM[210:260, 79:82].reshape(-1,3), 4))
print(" input R border x160..164:", runs(lum[235, 155:170] < 215, 155))
print(" samples L/R:", runs(lum[235, 805:825] < 215, 805), runs(lum[235, 875:895] < 215, 875))
print(" samples R modal:", modal(IM[210:260, 882:886].reshape(-1,3), 4))
print(" pre R border x278..284:", runs(lum[235, 276:290] < 215, 276), " modal:", modal(IM[220:250, 280:282].reshape(-1,3), 3))
print(" pre L border modal:", modal(IM[220:250, 194:196].reshape(-1,3), 3))
print(" extr borders L/R:", runs(lum[235, 316:326] < 215, 316), runs(lum[235, 400:410] < 215, 400),
      " L modal:", modal(IM[220:250, 321:323].reshape(-1,3), 3))
print(" sel borders L/R:", runs(lum[235, 426:434] < 215, 426), runs(lum[235, 508:516] < 215, 508),
      " L modal:", modal(IM[220:250, 428:430].reshape(-1,3), 3))
print(" pred borders L/R:", runs(lum[235, 656:664] < 215, 656), runs(lum[235, 733:741] < 215, 733),
      " L modal:", modal(IM[220:250, 660:662].reshape(-1,3), 3))
print(" classif L border modal x533-535:", modal(IM[215:255, 533:536].reshape(-1,3), 3))
print(" box top/bottom border rows (input col120):", runs(lum[195:285, 120] < 215, 195))
print(" pre col250 full:", runs(lum[190:285, 250] < 215, 190))
print(" classif col580 thr215:", runs(lum[190:285, 580] < 215, 190))
