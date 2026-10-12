#!/usr/bin/env python3
"""Self-check 2 — render_2.png focused re-verification of the fixed elements."""
from PIL import Image
import numpy as np

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide047/render_2.png"
S = 2001 / 960.0
a = np.asarray(Image.open(REN).convert("RGB")).astype(int)
print(f"scale S={S:.4f}")
def t(v): return v * S
notred = lambda s: ~((s[:,:,0] > 120) & (s[:,:,0] - s[:,:,1] > 60) & (s[:,:,0] - s[:,:,2] > 60))
dkn = lambda s: (s.sum(axis=2) < 330) & notred(s)
red = lambda s: (s[:,:,0] > 120) & (s[:,:,0] - s[:,:,1] > 60) & (s[:,:,0] - s[:,:,2] > 60)
blue = lambda s: (s[:,:,2] > 110) & (s[:,:,2] - s[:,:,0] > 50) & (s[:,:,2] - s[:,:,1] > 40)

def bb(x0, y0, x1, y1, pred, label, tgt):
    sub = a[int(t(y0)):int(t(y1)), int(t(x0)):int(t(x1))]
    m = pred(sub)
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        print(f"{label:24s} EMPTY"); return
    r = (x0 + xs.min() / S, y0 + ys.min() / S, x0 + xs.max() / S, y0 + ys.max() / S)
    d = [round(r[i] - tgt[i], 1) for i in range(4)]
    print(f"{label:24s} orig x {r[0]:.1f}..{r[2]:.1f} y {r[1]:.1f}..{r[3]:.1f}  delta {d} vs {tgt}")

# title
bb(60, 60, 870, 105, red, "title red", (140, 71, 825, 98))
bb(60, 60, 860, 105, blue, "title Layer", (448, 67, 542, 100))
# intro line widths
for i, (y0, y1, tgt) in enumerate([(128, 151, (81, 502)), (155, 178, (81, 525)), (182, 205, (81, 723))]):
    sub = a[int(t(y0)):int(t(y1)), int(t(60)):int(t(900))]
    m = (sub.sum(axis=2) < 520)
    ys, xs = np.nonzero(m)
    print(f"intro{i+1}: orig x {60+xs.min()/S:.1f}..{60+xs.max()/S:.1f} (target x {tgt[0]}..{tgt[1]}, w {tgt[1]-tgt[0]})")
# bullets
bb(95, 224, 560, 246, dkn, "bullet1", (116, 226, 475, 242))
bb(95, 254, 560, 276, dkn, "bullet2", (116, 258, 529, 268))
# label texts
bb(112, 289, 308, 308, dkn, "box1 text", (114, 291, 307, 303))
bb(112, 327, 308, 346, dkn, "box2 text", (114, 330, 307, 342))
# eq3 clean window (below bullet2 underline, above box2)
bb(316, 276, 560, 319, dkn, "eq3 ink", (317, 284, 536, 312))
# eq3 bar row
best = None
for y in range(int(t(280)), int(t(315))):
    row = a[y, int(t(320)):int(t(540))]
    m = dkn(row)
    run = mx = 0
    for v in m:
        run = run + 1 if v else 0
        mx = max(mx, run)
    if best is None or mx > best[1]: best = (y, mx)
print(f"eq3 bar row: orig y {best[0]/S:.1f} (target 298), run len {best[1]/S:.1f} (orig bar ~24)")
# eq4
bb(316, 317, 470, 362, dkn, "eq4 ink", (320, 321, 428, 359))
# legend word width (row2 'Column', x-limit inside border)
sub = a[int(t(396)):int(t(407)), int(t(460)):int(t(560))]
m = blue(sub)
ys, xs = np.nonzero(m)
print(f"legend 'c Column': orig x {460+xs.min()/S:.1f}..{460+xs.max()/S:.1f} (target 465..547)")
# grid cells clean windows
green = lambda s: (s[:,:,1] > 120) & (s[:,:,1] - s[:,:,0] > 40) & (s[:,:,1] - s[:,:,2] > 40)
yellow= lambda s: (s[:,:,0] > 180) & (s[:,:,1] > 170) & (s[:,:,2] < 130)
redf  = lambda s: (s[:,:,0] > 180) & (s[:,:,1] < 90) & (s[:,:,2] < 90)
cyan  = lambda s: (s[:,:,2] > 150) & (s[:,:,1] > 120) & (s[:,:,0] < 140) & (s[:,:,2] - s[:,:,0] > 60)
sub = a[int(t(360)):int(t(480)), int(t(565)):int(t(735))]
colored = green(sub) | yellow(sub) | redf(sub) | cyan(sub)
ys, xs = np.nonzero(colored)
print(f"input grid cells: orig x {565+xs.min()/S:.1f}..{565+xs.max()/S:.1f} y {360+ys.min()/S:.1f}..{360+ys.max()/S:.1f} (target 571..726 / 365..483)")
sub = a[int(t(390)):int(t(460)), int(t(790)):int(t(868))]
colored = green(sub) | yellow(sub) | redf(sub) | cyan(sub)
ys, xs = np.nonzero(colored)
print(f"output grid cells: orig x {790+xs.min()/S:.1f}..{790+xs.max()/S:.1f} y {390+ys.min()/S:.1f}..{390+ys.max()/S:.1f} (target 796..871 / 396..453)")
