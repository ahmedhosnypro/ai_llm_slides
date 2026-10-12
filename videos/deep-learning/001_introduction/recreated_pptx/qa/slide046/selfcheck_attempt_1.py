#!/usr/bin/env python3
"""Closed-loop self-check attempt 1 — render_1.png (2001x1125, 150dpi) vs the
original frame's measured geometry (frame px * 2001/960). Tolerance ~4px @150dpi
(= ~2 frame px) per dispatch; report per-element deltas in frame px."""
from PIL import Image
import numpy as np

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
REN = f"{BASE}/recreated_pptx/qa/slide046/render_1.png"
im = Image.open(REN).convert("RGB")
W, H = im.size
S = W / 960.0
a = np.asarray(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

redm   = (R > 110) & (R - G > 25) & (R - B > 25)
bluem  = (B - R > 30) & (B - G > 25) & (B > 100)
greenm = (G - R > 40) & (G - B > 40) & (G > 120)
textm  = (R + G + B < 620) & ~redm & ~bluem & ~greenm

def bb(x0, y0, x1, y1, mask):
    sub = mask[int(y0*S):int(y1*S)+1, int(x0*S):int(x1*S)+1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0: return None
    return ((x0*S+xs.min())/S, (y0*S+ys.min())/S, (x0*S+xs.max())/S, (y0*S+ys.max())/S)

def check(label, got, want, tol=2.0):
    if got is None:
        print(f"  {label:32s} EMPTY  << FAIL"); return False
    d = [g-w for g, w in zip(got, want)]
    ok = all(abs(v) <= tol for v in d)
    print(f"  {label:32s} got ({got[0]:6.1f},{got[1]:6.1f})..({got[2]:6.1f},{got[3]:6.1f})  "
          f"d=[{d[0]:+.1f},{d[1]:+.1f},{d[2]:+.1f},{d[3]:+.1f}]  {'ok' if ok else '<< FAIL'}")
    return ok

print(f"render {W}x{H}, scale {S:.5f}, tol 2.0 frame-px (~4px @150dpi)")
fails = 0

print("== title ==")
fails += not check("POOLING ink", bb(300, 60, 700, 130, redm), (403, 80, 563, 106))

print("== bullets ==")
fails += not check("main line", bb(100, 145, 800, 175, textm), (116, 151, 540, 169), 2.5)
fails += not check("sub1", bb(100, 174, 800, 194, textm), (128, 176, 414, 188), 2.5)
fails += not check("sub2", bb(100, 196, 800, 218, textm), (128, 198, 758, 214), 2.5)
fails += not check("sub3", bb(100, 221, 800, 242, textm), (128, 223, 547, 238), 2.5)

print("== option boxes ==")
fails += not check("box1 blue", bb(95, 244, 330, 280, bluem), (106, 249, 294, 277), 2.5)
fails += not check("box2 blue", bb(95, 280, 330, 316, bluem), (106, 283, 294, 310), 2.5)
fails += not check("box1 text", bb(110, 250, 300, 280, textm), (116, 254, 248, 272), 2.5)
fails += not check("box2 text", bb(110, 284, 300, 314, textm), (116, 288, 283, 307), 2.5)

print("== diagram ==")
fails += not check("matrix green", bb(150, 320, 290, 430, greenm), (172, 336, 242, 399), 2.5)
fails += not check("arrow ink", bb(245, 340, 325, 400, textm), (256, 351, 321, 383), 3.0)
fails += not check("z green", bb(300, 340, 370, 400, greenm), (314, 352, 348, 383), 2.5)
fails += not check("Pool (", bb(358, 335, 423, 415, textm), (370, 361, 420, 377), 2.5)
fails += not check(") ==", bb(605, 335, 660, 415, textm), (611, 361, 650, 377), 3.0)
fails += not check("caption", bb(640, 390, 810, 425, bluem), (676, 398, 773, 410), 2.5)

# photos: embedded at exact size — verify corners render non-white
print("== photos ==")
notw = (R + G + B < 690)
for lbl, (x0, y0, x1, y1) in [("large tiger", (424, 325, 610, 413)), ("small tiger", (670, 342, 767, 389))]:
    g = bb(x0-6, y0-6, x1+6, y1+6, notw)
    fails += not check(lbl, g, (x0, y0, x1, y1), 2.0)

# markers: ink presence near expected centers
print("== markers (ink presence) ==")
for lbl, (cx, cy, d) in [("main", (121, 161, 10.5)), ("box1", (121, 264.5, 10.5)),
                          ("box2", (121, 297.5, 10.5)), ("sub1", (132.5, 182.5, 8)),
                          ("sub2", (132.5, 205.5, 8)), ("sub3", (132.5, 229.5, 8))]:
    g = bb(cx-8, cy-8, cx+8, cy+8, textm)
    ok = g is not None
    print(f"  {lbl:32s} {'ink ok' if ok else 'EMPTY << FAIL'}")
    fails += not ok

# frame containment: no content ink outside content panel (57.5..877.5, 133..456.5)
print("== frame containment (content inside panel) ==")
panel = (57.5, 133, 877.5, 456.5)
for lbl, m in [("red", redm), ("text", textm), ("blue", bluem), ("green", greenm)]:
    sub = m[0:int(panel[1]*S)-2, :]   # above panel top: only title+chrome allowed
    # title zone x 300..700, y 60..130 expected; anything else above panel = leak
    leak = m[:int(132*S)-2, :].copy()
    ys, xs = np.nonzero(leak)
    if len(xs):
        # exclude title ink zone and chrome border/badge zone
        keep = ~(((xs/S > 390) & (xs/S < 575) & (ys/S > 75) & (ys/S < 110)) |
                 (xs/S < 44) | (xs/S > 916) | (ys/S < 47))
        if keep.any():
            print(f"  leak above panel ({lbl}): {int(keep.sum())} px at "
                  f"x {xs[keep].min()/S:.0f}..{xs[keep].max()/S:.0f} y {ys[keep].min()/S:.0f}..{ys[keep].max()/S:.0f} << FAIL")
            fails += 1
        else:
            print(f"  above panel ({lbl}): only chrome/title ink — ok")
    else:
        print(f"  above panel ({lbl}): clean")
# below panel bottom (y > 457) should have no content ink (chrome gray only)
for lbl, m in [("text", textm), ("blue", bluem), ("green", greenm)]:
    ys, xs = np.nonzero(m[int(459*S):, :])
    if len(xs):
        print(f"  below panel ({lbl}): {len(xs)} px at x {xs.min()/S:.0f}..{xs.max()/S:.0f} << FAIL")
        fails += 1
    else:
        print(f"  below panel ({lbl}): clean")

print(f"\nSELF-CHECK RESULT: {'PASS' if fails == 0 else f'FAIL ({fails})'}")
