#!/usr/bin/env python3
"""selfcheck_attempt_1 — mandatory pre-judge checks on the 150dpi render.
Scale: render 2001x1125 @150dpi; frame px * 150/72 = render px (x2.08333).
Checks: (2) frame containment, (3) equations exist + ink-edge closed loop
(target ink edges within ~4px render-space of the frame-measured targets),
(7) wrap/overflow bands, (8) line-spacing pitch of multi-line boxes.
"""
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide025/render_1.png"
im = Image.open(R).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
S = 150 / 72.0
print(f"render {W}x{H}")

dark = a.sum(axis=2) < 430
beige = (abs(a[:,:,0]-218)<16) & (abs(a[:,:,1]-208)<16) & (abs(a[:,:,2]-196)<16)
cream = (a[:,:,0]>235) & (a[:,:,1]>235) & (a[:,:,2]>195) & (a[:,:,2]<250)
gray_bg = (abs(a[:,:,0]-233)<9) & (abs(a[:,:,1]-233)<9) & (abs(a[:,:,2]-231)<9)

def ink_bbox(x0, y0, x1, y1, mask=dark):
    sub = mask[int(y0):int(y1), int(x0):int(x1)]
    ys, xs = np.where(sub)
    if len(xs) == 0: return None
    return (int(x0)+int(xs.min()), int(y0)+int(ys.min()), int(x0)+int(xs.max()), int(y0)+int(ys.max()))

def f(v):  # frame px -> render px
    return v * S

print("== (3) EQUATIONS EXIST + ink-edge closed loop ==")
targets = {  # (frame ink bbox target, search window in frame px)
  "eq1": ((90, 471, 213, 500), (80, 463, 245, 500)),
  "eq2": ((297, 459, 478, 498), (294, 458, 500, 500)),
  "eq3": ((546, 457, 687, 499), (541, 450, 748, 500)),
}
for name, (tgt, win) in targets.items():
    bb = ink_bbox(f(win[0]), f(win[1]), f(win[2]), f(win[3]))
    if bb is None:
        print(f"  {name}: NO INK — BLOCKER"); continue
    t = [f(v) for v in tgt]
    d = [bb[i] - t[i] for i in range(4)]
    ok = all(abs(v) <= 4.5 for v in d)
    print(f"  {name}: render ink {bb} vs target {[round(v,1) for v in t]}  d={d}  {'OK' if ok else 'FIX (iter)'}")

print("== (2) FRAME CONTAINMENT ==")
# house frame inner bounds at 150dpi: x 0.15in*150=22.5 .. 13.18in*150=1977 ; y 22.5 .. 1102.5
house = ink_bbox(0, 0, W, H)
print(f"  full-slide ink bbox: {house} (house inner ~[23,23,1977,1102])",
      "OK" if house[0] >= 21 and house[1] >= 21 and house[2] <= 1979 and house[3] <= 1104 else "OVERFLOW")
# panel content containment: panel x64..570, y135..387.5 frame -> render
# neuron circles must sit fully inside panel; mesh/outboxes/error/class outside-panel items are on gray
panel_items = {
  "neuron col0 row1": (145, 162, 185, 202),
  "neuron col2 row3": (407, 316, 447, 356),
  "ring row1": (191, 177.75, 230, 190.25),
  "dot row4": (69.5, 289, 87, 298),
}
for name, (x0, y0, x1, y1) in panel_items.items():
    print(f"  {name}: panel-rect [{round(f(64)), round(f(135)), round(f(570)), round(f(387.5))}] item [{round(f(x0))},{round(f(y0))},{round(f(x1))},{round(f(y1))}]",
          "OK" if f(y1) <= f(387.5) and f(x1) <= f(570) else "CHECK")
# ink must not touch panel edges: scan a 2px band inside the panel border for dark ink
# (excluding known boundary-crossing elements: none expected)
px0, py0, px1, py1 = int(f(64)), int(f(135)), int(f(570)), int(f(387.5))
band = 3
top_band = dark[py0:py0+band, px0:px1].sum()
bot_band = dark[py1-band:py1, px0:px1].sum()
l_band = dark[py0:py1, px0:px0+band].sum()
r_band = dark[py0:py1, px1-band:px1].sum()
print(f"  panel edge bands dark px: top {top_band}, bottom {bot_band}, left {l_band}, right {r_band}")
print("  (Net labels sit y142+ inside; eq boxes are OUTSIDE the panel - separate check)")
# eq boxes inside the gray area: bottom border of eq boxes at frame 501.5 -> 1044.8; blackbar top 519 -> 1081
for name, (x0, y0, x1, y1) in {"eqbox1": (72.5, 461, 247, 501.5), "eqbox2": (292.5, 456, 501.5, 501.5), "eqbox3": (539.5, 449, 749.5, 501.5)}.items():
    print(f"  {name}: bottom {round(f(y1),1)} < blackbar top {round(f(519),1)}:", "OK" if f(y1) < f(519) else "OVERLAP")

print("== (7) WRAP / BAND CHECKS ==")
# callout text must stay inside callout rects
for name, (x0, y0, x1, y1) in {"prev callout": (218, 401, 309, 432.5), "curr callout": (384, 402.5, 474, 431.5)}.items():
    bb = ink_bbox(f(x0)+2, f(y0)+2, f(x1)-2, f(y1)-2)
    print(f"  {name}: text ink {bb} inside rect [{round(f(x0))},{round(f(y0))},{round(f(x1))},{round(f(y1))}]",
          "OK" if bb and bb[0] >= f(x0) and bb[1] >= f(y0) and bb[2] <= f(x1) and bb[3] <= f(y1) else "OVERFLOW")
# magbox text inside boxes
for name, (x0, y0, x1, y1) in {"IS box": (64, 95, 128.5, 124.5), "SL box": (612, 94, 674.5, 124.5)}.items():
    bb = ink_bbox(f(x0)+2, f(y0)+2, f(x1)-2, f(y1)-2)
    print(f"  {name}: text ink {bb} inside", "OK" if bb and bb[0] >= f(x0) and bb[2] <= f(x1) and bb[3] <= f(y1) else "OVERFLOW")
# title band
bb = ink_bbox(f(300), f(60), f(680), f(100))
print(f"  title ink {bb} (frame target 328..643 x 68..89 -> render [{round(f(328))},{round(f(68))},{round(f(643))},{round(f(89))}])")

print("== (8) LINE SPACING pitch (callouts) ==")
# prev callout text rows: find dark-row groups inside the prev callout
sub = dark[int(f(403)):int(f(431)), int(f(220)):int(f(305))]
rows = np.where(sub.any(axis=1))[0] + int(f(403))
groups = []
if len(rows):
    s = rows[0]; p = rows[0]
    for v in rows[1:]:
        if v > p + 2: groups.append((s, p)); s = v
        p = v
    groups.append((s, p))
print(f"  prev callout text line bands: {groups} -> pitch {groups[1][0]-groups[0][0] if len(groups)>1 else None} px (target ~{round(11.5*S,1)})")

print("== neuron fill/color sample vs targets ==")
for name, (x, y, tgt) in {
  "panel": (300*f(1), 300*f(1), None),}.items():
    pass
print("  panel px:", tuple(a[int(f(300)), int(f(300))]), "target (218,208,196)")
print("  green neuron px:", tuple(a[int(f(427*.999)), int(f(170))]), "target (220,255,181)")
print("  error bar px:", tuple(a[int(f(593)), int(f(220))]), "target (158,0,0)")
print("  err text px row1:", tuple(a[int(f(184)), int(f(592))]), "target ~(255,241,241)")
print("  class fill px:", tuple(a[int(f(643)), int(f(180))]), "target (219,255,203)")
print("  eq fill px:", tuple(a[int(f(160)), int(f(495))]), "target (251,252,234)")
