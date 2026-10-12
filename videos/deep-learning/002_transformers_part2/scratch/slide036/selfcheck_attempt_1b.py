#!/usr/bin/env python3
"""Self-check attempt 1b: tightened regions for the 4 ambiguous checks."""
import numpy as np
from PIL import Image

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide036/render_2.png"
im = np.asarray(Image.open(R).convert("RGB")).astype(int)
S = 150 / 72.0
FX = lambda fx: (fx - 18.628) / 0.961231
FY = lambda fy: fy / 0.955556
PX = lambda fx: FX(fx) * S
PY = lambda fy: FY(fy) * S
fails = []
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red = (r > 130) & (g < 110) & (b < 110)
blue = (b > 120) & (r < 110) & (g < 110)

# gutter-up: region strictly inside diagram panel, left of strips, above banner
x0, x1 = int(PX(68)), int(PX(163))
y0, y1 = int(PY(356)), int(PY(392))
sub = blue[y0:y1, x0:x1]
ys, xs = np.where(sub)
print(f"gutter-up blue ink: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+y0}..{ys.max()+y0}")
print(f"  expect line1 'Output of Self' x {PX(74):.0f}..{PX(157):.0f}, line2 'Attention' centered ~{PX(115):.0f}, band y {PY(361):.0f}..{PY(391):.0f}")
if xs.min() + x0 < PX(70) - 6: fails.append("gutter-up: ink left of expected")
if ys.min() + y0 < PY(359) - 6: fails.append("gutter-up: ink above expected")
# two line bands?
rows = sub.sum(axis=1)
bands = []
inb = False
for i, v in enumerate(rows):
    if v > 1 and not inb: st = i; inb = True
    elif v <= 1 and inb: bands.append((st + y0, i - 1 + y0)); inb = False
if inb: bands.append((st + y0, len(rows) - 1 + y0))
print(f"  gutter-up line bands: {bands} (expect 2)")
if len(bands) != 2: fails.append(f"gutter-up: {len(bands)} line bands vs 2")

# gutter-dn: region inside panel, away from left border col
x0, x1 = int(PX(68)), int(PX(160))
y0, y1 = int(PY(442)), int(PY(480))
sub = red[y0:y1, x0:x1]
ys, xs = np.where(sub)
print(f"gutter-dn red ink: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+y0}..{ys.max()+y0}")
print(f"  expect line1 'Input  to Self' x {PX(72):.0f}..{PX(153):.0f} band y {PY(446):.0f}..{PY(462):.0f}; line2 'Attention' y {PY(462):.0f}..{PY(478):.0f}")
if xs.min() + x0 < PX(70) - 6: fails.append("gutter-dn: ink left of expected")
rows = sub.sum(axis=1)
bands = []
inb = False
for i, v in enumerate(rows):
    if v > 1 and not inb: st = i; inb = True
    elif v <= 1 and inb: bands.append((st + y0, i - 1 + y0)); inb = False
if inb: bands.append((st + y0, len(rows) - 1 + y0))
print(f"  gutter-dn line bands: {bands} (expect 2)")
if len(bands) != 2: fails.append(f"gutter-dn: {len(bands)} line bands vs 2")

# caption text: dark-red ink (990000) inside the yellow band
cap = (r > 90) & (r < 190) & (g < 110) & (b < 110)
x0, x1 = int(PX(290)), int(PX(576))
y0, y1 = int(PY(487)), int(PY(503))
sub = cap[y0:y1, x0:x1]
ys, xs = np.where(sub)
if len(ys) < 100:
    fails.append(f"caption text: only {len(ys)} dark-red px")
else:
    print(f"caption text ink: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+y0}..{ys.max()+y0} n={len(ys)}")
    print(f"  expect x ~{PX(294):.0f}..{PX(570):.0f} y {PY(489):.0f}..{PY(503):.0f}")

# panel gaps re-check (descender-safe mid-gap bands)
for (g0, g1, tag) in ((178, 192, "gap1"), (238, 252, "gap2")):
    sub = blue[int(PY(g0)):int(PY(g1)), int(PX(100)):int(PX(855))]
    print(f"panel {tag} mid-gap blue px: {int(sub.sum())} (expect <10)")
    if sub.sum() > 10: fails.append(f"panel {tag}: ink in mid-gap")

print()
if fails:
    print("1b FAILURES:")
    for f in fails: print("  -", f)
    raise SystemExit(1)
print("SELF-CHECK 1b: ALL PASS")
