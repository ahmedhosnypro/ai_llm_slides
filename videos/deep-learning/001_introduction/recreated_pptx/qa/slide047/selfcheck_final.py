#!/usr/bin/env python3
"""Final self-check — render_5.png (pre-judge gate). All elements vs original targets."""
from PIL import Image
import numpy as np

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide047/render_5.png"
S = 2001 / 960.0
a = np.asarray(Image.open(REN).convert("RGB")).astype(int)
print(f"scale S={S:.4f}")
def t(v): return v * S
notred = lambda s: ~((s[:,:,0] > 120) & (s[:,:,0] - s[:,:,1] > 60) & (s[:,:,0] - s[:,:,2] > 60))
red = lambda s: (s[:,:,0] > 120) & (s[:,:,0] - s[:,:,1] > 60) & (s[:,:,0] - s[:,:,2] > 60)
blue = lambda s: (s[:,:,2] > 110) & (s[:,:,2] - s[:,:,0] > 50) & (s[:,:,2] - s[:,:,1] > 40)
dkn = lambda s: (s.sum(axis=2) < 330) & notred(s)
green = lambda s: (s[:,:,1] > 120) & (s[:,:,1] - s[:,:,0] > 40) & (s[:,:,1] - s[:,:,2] > 40)
yellow= lambda s: (s[:,:,0] > 180) & (s[:,:,1] > 170) & (s[:,:,2] < 130)
redf  = lambda s: (s[:,:,0] > 180) & (s[:,:,1] < 90) & (s[:,:,2] < 90)
cyan  = lambda s: (s[:,:,2] > 150) & (s[:,:,1] > 120) & (s[:,:,0] < 140) & (s[:,:,2] - s[:,:,0] > 60)
ok = lambda name, r, tgt, tol: print(f"  {'PASS' if all(abs(r[i]-tgt[i])<=tol for i in range(4)) else 'CHECK'} {name}: {[round(x,1) for x in r]} tgt {tgt}")

def bb(x0, y0, x1, y1, pred, label, tgt, tol=6):
    sub = a[int(t(y0)):int(t(y1)), int(t(x0)):int(t(x1))]
    m = pred(sub)
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        print(f"  FAIL {label} EMPTY"); return None
    r = (x0 + xs.min()/S, y0 + ys.min()/S, x0 + xs.max()/S, y0 + ys.max()/S)
    ok(label, r, tgt, tol)
    return r

print("== FINAL PRE-JUDGE SELF-CHECK (render_5) ==")
bb(60, 60, 870, 105, red, "title red", (140, 71, 825, 98), 8)
bb(60, 60, 860, 105, blue, "title Layer", (448, 67, 542, 100), 8)
for i, (y0, y1, tx0, tx1) in enumerate([(128, 151, 81, 502), (155, 178, 81, 525), (182, 205, 81, 723)]):
    sub = a[int(t(y0)):int(t(y1)), int(t(60)):int(t(900))]
    m = (sub.sum(axis=2) < 520)
    ys, xs = np.nonzero(m)
    print(f"  {'PASS' if abs(tx1-(60+xs.max()/S))<15 else 'CHECK'} intro{i+1}: x {60+xs.min()/S:.1f}..{60+xs.max()/S:.1f} (target {tx0}..{tx1})")
bb(95, 224, 560, 247, dkn, "bullet1", (116, 226, 475, 242), 8)
bb(95, 254, 560, 277, dkn, "bullet2", (116, 258, 529, 268), 10)
bb(112, 289, 308, 308, dkn, "box1 text", (114, 291, 307, 303), 6)
bb(112, 327, 308, 346, dkn, "box2 text", (114, 330, 307, 342), 6)
bb(316, 277, 560, 319, dkn, "eq3 ink", (317, 284, 536, 312), 12)
bb(316, 317, 470, 362, dkn, "eq4 ink", (320, 321, 428, 359), 12)
bb(730, 410, 770, 440, dkn, "arrow", (738, 422, 757, 431), 5)
# fraction
sub = a[int(t(395)):int(t(460)), int(t(768)):int(t(793))]
m = red(sub)
ys, xs = np.nonzero(m)
print(f"  {'PASS' if abs(775-(768+xs.min()/S))<4 else 'CHECK'} fraction: x {768+xs.min()/S:.1f}..{768+xs.max()/S:.1f} y {395+ys.min()/S:.1f}..{395+ys.max()/S:.1f} (target 775..790 / 405..449)")
# grids
sub = a[int(t(360)):int(t(481)), int(t(565)):int(t(735))]
colored = green(sub) | yellow(sub) | redf(sub) | cyan(sub)
ys, xs = np.nonzero(colored)
print(f"  {'PASS' if abs(571-(565+xs.min()/S))<3 and abs(483.5-(360+ys.max()/S))<3 else 'CHECK'} input grid: x {565+xs.min()/S:.1f}..{565+xs.max()/S:.1f} y {360+ys.min()/S:.1f}..{360+ys.max()/S:.1f} (target 571..726 / 365..483.5)")
sub = a[int(t(390)):int(t(458)), int(t(790)):int(t(875))]
colored = green(sub) | yellow(sub) | redf(sub) | cyan(sub)
ys, xs = np.nonzero(colored)
print(f"  {'PASS' if abs(796-(790+xs.min()/S))<3 else 'CHECK'} output grid: x {790+xs.min()/S:.1f}..{790+xs.max()/S:.1f} y {390+ys.min()/S:.1f}..{390+ys.max()/S:.1f} (target 796..871 / 396..453.5)")
# legend rows
lightblue = lambda s: (s[:,:,2] > 200) & (s[:,:,0] > 150) & (s[:,:,0] < 240) & (s[:,:,2] - s[:,:,0] > 15)
bb(445, 340, 580, 485, lightblue, "legend fill", (455, 348, 566, 475), 5)
# equation bar rows (the alignment-law anchor)
for lbl, (y0, y1, x0, x1, tgt) in [('eq3 bar', (280, 315, 320, 540, 298)), ('eq4 bar', (318, 362, 318, 460, 337))]:
    best = None
    for y in range(int(t(y0)), int(t(y1))):
        row = a[y, int(t(x0)):int(t(x1))]
        m = dkn(row)
        run = mx = 0
        for v in m:
            run = run + 1 if v else 0
            mx = max(mx, run)
        if best is None or mx > best[1]: best = (y, mx)
    print(f"  {'PASS' if abs(best[0]/S - tgt) <= 4 else 'CHECK'} {lbl}: orig y {best[0]/S:.1f} (target {tgt}, tol 4), run {best[1]/S:.1f}")
