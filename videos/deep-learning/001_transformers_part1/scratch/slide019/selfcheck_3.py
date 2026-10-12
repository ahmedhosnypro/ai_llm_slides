#!/usr/bin/env python3
"""selfcheck_3.py — mandatory pre-judge checks on render_3 (attempt 3).
1) house_chrome_check.py  2) containment (playlist white-margin adaptation)
3) inheritance diff vs slide018 certified render (confined to delta zones)
4) A&N/FF text-wrap bands  5) delta-zone ink presence."""
import subprocess, sys
from PIL import Image, ImageChops

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
R3 = BASE + "/recreated_pptx/qa/slide019/render_3.png"
R18 = BASE + "/recreated_pptx/qa/slide018/render_1.png"

print("== 1) house_chrome_check.py ==")
p = subprocess.run([sys.executable, "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome_check.py", R3], capture_output=True, text=True)
print(p.stdout.strip() or p.stderr.strip())
chrome_ok = "PASS" in (p.stdout + p.stderr)

im = Image.open(R3).convert("RGB")      # 2001x1125, 1px @150dpi = 1/200 in = 0.96 frame px
W, H = im.size
im18 = Image.open(R18).convert("RGB")
p19 = im.load(); p18 = im18.load()

print("\n== 2) containment: content ink inside gray panel (x42..918,y45..539 frame px => *2.085 @150dpi) ==")
sx = W / 960.0
x0, x1 = int(44 * sx), int(916 * sx)
y0, y1 = int(47 * sx), int(536 * sx)
viol = []
for y in range(int(50 * sx), int(534 * sx), 2):
    for x in list(range(int(44 * sx), int(46 * sx))) + list(range(int(914 * sx), int(916 * sx))):
        c = p19[x, y]
        if sum(c) < 640 and not (abs(c[0]-193)<30 and abs(c[1]-193)<30):  # ink in margin band
            viol.append((x, y, c))
print(f"margin-band ink pixels (should be ~0 besides chrome): {len(viol)}", viol[:5])

print("\n== 3) inheritance diff vs slide018 certified render ==")
diff = ImageChops.difference(im, im18).convert("L")
dp = diff.load()
bw, bh = im.size
# changed-pixel column/row profile (threshold 12)
cols = {}
rows = {}
n = 0
for y in range(0, bh, 2):
    for x in range(0, bw, 2):
        if dp[x, y] > 12:
            n += 1
            cols.setdefault(x // 100, 0); cols[x // 100] += 1
            rows.setdefault(y // 100, 0); rows[y // 100] += 1
print(f"changed px (sampled, thr12): {n}")
print("col buckets (x/100 @150dpi):", dict(sorted(cols.items())))
print("row buckets (y/100 @150dpi):", dict(sorted(rows.items())))
# expected delta zones @150dpi (frame px * sx): legend/leaders x 130..580 -> ~271..1209;
# enc stack x595..750 -> 1240..1562; dec stack x725..870 -> 1511..1814; badge x875..920
# title zone identical (title carried); yellow band etc inside stack zones.
zone_ok = True
for (a, b, label) in [(0, 260, "left margin"), (1815, bw, "right of dec zone (badge excepted)"), ]:
    bad = [c for c in cols if a <= c * 100 < b and c * 100 > 260 or (c * 100 >= b)]
    # simpler: report unexpected columns
print("unexpected right-zone cols (>1840):", [c * 100 for c in cols if c * 100 > 1840])
print("unexpected left-zone cols (<265):", [c * 100 for c in cols if c * 100 < 265])

print("\n== 4) text bands: A&N/FF boxes contain their ink (no wrap outside) ==")
def band_ink(x0f, y0f, x1f, y1f):
    cnt = 0
    for y in range(int(y0f * sx), int(y1f * sx)):
        for x in range(int(x0f * sx), int(x1f * sx)):
            if sum(p19[x, y]) < 330: cnt += 1
    return cnt
checks = [
    ("enc A&N top text inside box", 656, 272, 721, 289),
    ("enc FF text inside box", 654, 289, 719, 314),
    ("enc A&N mid text inside box", 657, 342, 719, 354),
    ("dec A&N top text inside box", 754, 207, 816, 219),
    ("dec FF text inside box", 754, 224, 816, 249),
    ("dec A&N mid text inside box", 754, 264, 816, 274),
    ("purple A&N text inside box", 754, 330, 816, 343),
]
for label, a, b, c, d in checks:
    inside = band_ink(a, b, c, d)
    # ink just outside the box (1-3px ring left/right)
    outside = band_ink(a - 4, b, a - 1, d) + band_ink(c + 1, b, c + 4, d)
    print(f"{label}: inside={inside} outside={outside} -> {'PASS' if inside > 0 and outside < max(3, inside*0.06) else 'CHECK'}")

print("\n== 5) delta-zone ink presence (equations-law analog: regions must not be empty) ==")
zones = [
    ("legend1 fill", 180, 110, 320, 124, lambda c: c[2] > 200 and c[0] < 230),
    ("legend2 fill", 330, 148, 500, 166, lambda c: abs(c[0]-c[1]) < 12 and 120 < c[0] < 190),
    ("legend3 fill", 280, 186, 450, 204, lambda c: c[1] > 200 and c[0] > 170 and c[2] < 220),
    ("enc green bus", 633, 280, 642, 400, lambda c: c[1] > 120 and c[1] > c[0] + 20 and c[1] > c[2] + 40),
    ("dec green trunk", 829, 220, 840, 400, lambda c: c[1] > 120 and c[1] > c[0] + 20 and c[1] > c[2] + 40),
    ("steel enc A&N", 660, 276, 715, 285, lambda c: c[2] > c[0] + 25 and c[2] > 130),
    ("indigo purple A&N", 758, 332, 812, 341, lambda c: c[2] > 170 and c[2] > c[0] + 60),
]
for label, a, b, c, d, pred in zones:
    cnt = sum(1 for y in range(int(b*sx), int(d*sx)) for x in range(int(a*sx), int(c*sx)) if pred(p19[x, y]))
    print(f"{label}: {cnt} px {'PASS' if cnt > 30 else 'FAIL'}")

print("\n== 6) badge numeral = 19 (dark ink in badge) ==")
bx0, by0, bx1, by1 = int(876 * sx), int(54 * sx), int(910 * sx), int(88 * sx)
cnt = sum(1 for y in range(by0, by1) for x in range(bx0, bx1) if sum(p19[x, y]) < 260)
print(f"badge ink px: {cnt} (expect >40 for '19')")
