#!/usr/bin/env python3
# selfcheck_attempt_1.py — pre-judge self-checks for slide 004 attempt 1.
# 1) house chrome (playlist law)  2) inheritance diff vs imported base render
#    (must be confined to: two highlight rects + badge numeral zone)
# 3) highlight geometry vs measured rects (<=4px @150dpi tolerance)
# 4) containment: highlights fully inside the green card interior
import numpy as np
from PIL import Image

Q = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide004"
S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
rend = np.asarray(Image.open(f"{Q}/render_1.png").convert("RGB"), dtype=np.int16)
base = np.asarray(Image.open(f"{S}/base-1.png").convert("RGB"), dtype=np.int16)
ok = True

print(f"render {rend.shape} base {base.shape}")
# --- 2. inheritance diff ---
d = np.abs(rend - base).sum(axis=2)
hot = d > 30
ys, xs = np.where(hot)
# expected zones (render px @150dpi, slide_pt*150/72): enc (582.3,356.5,153.0,48.7), dec (737.3,278.0,147.8,47.1)
pt = lambda v: v * 150.0 / 72.0
zones = {
    "enc_hl": (pt(582.3) - 6, pt(356.5) - 6, pt(735.3) + 6, pt(405.2) + 6),
    "dec_hl": (pt(737.3) - 6, pt(278.0) - 6, pt(885.1) + 6, pt(325.1) + 6),
    "badge":  (pt(875 - 18), pt(71 - 18) - 10, pt(893 + 18), pt(71 + 18) + 10),
}
def inzone(x, y):
    for x0, y0, x1, y1 in zones.values():
        if x0 <= x <= x1 and y0 <= y <= y1:
            return True
    return False
outside = [(x, y) for x, y in zip(xs, ys) if not inzone(x, y)]
print(f"hot px total {len(xs)}, outside delta zones {len(outside)}")
if outside:
    ok = False
    ox = np.array([p[0] for p in outside]); oy = np.array([p[1] for p in outside])
    print(f"  outside bbox x {ox.min()}..{ox.max()} y {oy.min()}..{oy.max()}")
    # coarse cluster print
    from collections import Counter
    c = Counter((x // 64, y // 64) for x, y in outside)
    for (cx, cy), n in c.most_common(8):
        print(f"  cluster cell ({cx*64},{cy*64}) n={n}")
else:
    print("  PASS: inheritance diff confined to delta zones (highlights + badge)")
# per-zone hot counts (sanity: highlights actually differ)
for name, (x0, y0, x1, y1) in zones.items():
    if name == "badge":
        continue
    z = d[int(y0):int(y1), int(x0):int(x1)]
    print(f"  zone {name}: hot {int((z>30).sum())} px, mean diff {z.mean():.1f}")

# --- 3. highlight geometry in MY render (orange census per rect) ---
r, g, b = rend[..., 0], rend[..., 1], rend[..., 2]
om = (r > 200) & (b < 175) & (g > 130) & (g < 225) & ((r - b) > 60) & ((g - b) > 25)
def rect_check(x0, y0, x1, y1, tag):
    global ok
    X0, Y0, X1, Y1 = int(pt(x0)), int(pt(y0)), int(pt(x1)), int(pt(y1))
    sub = om[Y0 - 8:Y1 + 8, X0 - 8:X1 + 8]
    ysi, xsi = np.where(sub)
    if len(xsi) == 0:
        print(f"  {tag}: NO orange ink — FAIL"); ok = False; return
    fx0, fx1 = xsi.min() + X0 - 8, xsi.max() + X0 - 8
    fy0, fy1 = ysi.min() + Y0 - 8, ysi.max() + Y0 - 8
    dx0, dy0, dx1, dy1 = fx0 - X0, fy0 - Y0, fx1 - X1, fy1 - Y1
    good = max(abs(dx0), abs(dy0), abs(dx1), abs(dy1)) <= 4
    print(f"  {tag}: orange bbox render ({fx0},{fy0})..({fx1},{fy1}) vs expected ({X0},{Y0})..({X1},{Y1})  edges d=({dx0},{dy0},{dx1},{dy1}) px  {'PASS' if good else 'FAIL'}")
    if not good:
        ok = False
    # tint sample at rect center
    cx, cy = (X0 + X1) // 2, (Y0 + Y1) // 2
    print(f"    center RGB {rend[cy-2:cy+3, cx-2:cx+3].reshape(-1,3).mean(axis=0).round(0)}")
print("highlight geometry (my render):")
rect_check(582.3, 356.5, 735.3, 405.2, "enc_hl")
rect_check(737.3, 278.0, 885.1, 325.1, "dec_hl")

# --- 4. containment: highlights inside green card interior (card 573..894 pt, stroke ~573-575 / 892-894) ---
for tag, (x0, y0, x1, y1) in (("enc_hl", (582.3, 356.5, 735.3, 405.2)), ("dec_hl", (737.3, 278.0, 885.1, 325.1))):
    inside = x0 > 576 and x1 < 891 and y0 > 107 and y1 < 522
    print(f"  containment {tag}: {'PASS' if inside else 'FAIL'} (card interior ~576..891 x 107..522)")
    if not inside:
        ok = False

print(f"\nSELF-CHECK RESULT: {'PASS' if ok else 'FAIL'}")
