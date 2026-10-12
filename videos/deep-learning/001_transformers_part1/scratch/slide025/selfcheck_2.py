#!/usr/bin/env python3
"""Pre-judge self-check for slide 025 attempt 1 (17 §mandatory): containment + bands.
Renders are 2000x1125 (150dpi). Frame px (960x540) -> render px: * 2.0833."""
import sys
import numpy as np
from PIL import Image

ren = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(int)
H, W = ren.shape[:2]
print(f"render {W}x{H}")
S = H / 540.0
fails = []

def ink_mask(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    # non-background: not white/panel-gray/containers/left-panel tans/highlight yellow
    bg = ((r > 235) & (g > 235) & (b > 235)) | \
         ((abs(r - 233) < 14) & (abs(g - 233) < 14) & (abs(b - 231) < 14)) | \
         ((abs(r - 253) < 10) & (abs(g - 237) < 12) & (abs(b - 220) < 14)) | \
         ((abs(r - 205) < 14) & (abs(g - 252) < 12) & (abs(b - 222) < 14)) | \
         ((abs(r - 222) < 14) & (abs(g - 170) < 14) & (abs(b - 117) < 16)) | \
         ((abs(r - 233) < 12) & (abs(g - 181) < 14) & (abs(b - 127) < 16)) | \
         ((r > 215) & (g > 215) & (b < 120))
    return ~bg

ink = ink_mask(ren)

def box(x0, x1, y0, y1):
    """frame-px box -> render px; return ink bbox inside"""
    X0, X1, Y0, Y1 = int(x0 * S), int(x1 * S), int(y0 * S), int(y1 * S)
    sub = ink[Y0:Y1, X0:X1]
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    return (xs.min() + X0, xs.max() + X0, ys.min() + Y0, ys.max() + Y0)

# 1. house-frame containment: content ink above the chrome's bottom stroke only
#    (the chrome's own red bottom stroke sits at the last ~5 render rows and is
#    expected; flag content ink in y 1104..1116 render px)
zone = ink[int(7.36 * 150):int(7.44 * 150), :]
# the chrome's red bottom stroke antialiases into this band across the full panel
# width — only flag ink that is NOT that chrome stroke red
zr = ren[int(7.36 * 150):int(7.44 * 150), :, 0]
zg = ren[int(7.36 * 150):int(7.44 * 150), :, 1]
content = zone & ~((zr > 120) & (zg < 110))
n = int(content.sum())
if n > 40:
    ys, xs = np.where(content)
    fails.append(f"house frame: content ink in bottom zone n={n} x{xs.min()}-{xs.max()}")

# 2. left panel containment (panel 44-207 x, 210-523 y frame px): content ink inside
lb = box(46, 206, 268, 492)  # inner chart region
if lb:
    # ink must not cross the inner chart border by more than 2 frame-px
    if lb[0] < int(56 * S) or lb[1] > int(193 * S) or lb[2] < int(266 * S) or lb[3] > int(494 * S):
        fails.append(f"left inner chart ink outside: {lb}")
else:
    fails.append("left inner chart: NO ink (boxes/circles missing)")

# 3. center panel containment (300-508 x, 246-516 y)
cb = box(302, 506, 248, 514)
if cb:
    if cb[0] < int(300 * S) - 2 or cb[1] > int(508 * S) + 2 or cb[2] < int(246 * S) - 2 or cb[3] > int(516 * S) + 2:
        fails.append(f"center panel ink outside border: {cb}")
else:
    fails.append("center panel: NO ink")

# 4. arch frame containment (572-895 x, 104-525 y)
ab = box(574, 893, 106, 523)
if ab:
    if ab[0] < int(572 * S) - 2 or ab[1] > int(895 * S) + 2 or ab[2] < int(104 * S) - 2 or ab[3] > int(525 * S) + 2:
        fails.append(f"arch ink outside frame: {ab}")
else:
    fails.append("arch: NO ink")

# 5. key regions contain ink (existence checks)
for nm, (x0, x1, y0, y1) in {
    "title": (200, 760, 50, 92), "bubble": (184, 250, 130, 200),
    "left MatMul top": (105, 173, 296, 312), "left circles": (78, 178, 456, 490),
    "center SDPA": (301, 478, 352, 397), "center circles": (318, 458, 486, 510),
    "enc MHA": (648, 723, 354, 390), "dec MHA": (747, 827, 276, 320),
    "enc embedding": (636, 723, 446, 485), "dec embedding": (750, 827, 446, 485),
    "OP band": (752, 819, 111, 130), "Outputs band": (762, 811, 493, 510),
}.items():
    bb = box(x0, x1, y0, y1)
    if bb is None:
        fails.append(f"region {nm}: EMPTY")
    else:
        print(f"  {nm}: ink x{bb[0]/S:.0f}-{bb[1]/S:.0f} y{bb[2]/S:.0f}-{bb[3]/S:.0f} (frame px)")

# 6. line-spacing pin check: bubble 3 lines pitch (drawn 14pt -> 14px@72dpi = 29px@150)
# sample the white text rows inside the bubble
sub = ren[int(130 * S):int(196 * S), int(190 * S):int(245 * S)]
wr = ((sub[:, :, 0] > 200) & (sub[:, :, 1] > 200) & (sub[:, :, 2] > 200)).sum(axis=1)
rows = [i for i, v in enumerate(wr) if v > 3]
if rows:
    groups = []
    s0 = rows[0]
    prev = rows[0]
    for y in rows[1:]:
        if y - prev > 3:
            groups.append((s0, prev))
            s0 = y
        prev = y
    groups.append((s0, prev))
    print(f"  bubble text line groups (render px): {groups}")
    if len(groups) != 3:
        fails.append(f"bubble: expected 3 text lines, got {len(groups)}")

if fails:
    print("SELF-CHECK: FAIL")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("SELF-CHECK: PASS (containment + existence + bubble lines)")
