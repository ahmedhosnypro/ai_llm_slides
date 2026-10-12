#!/usr/bin/env python3
"""selfcheck_attempt_2.py — mandatory pre-judge self-checks for slide 008 attempt 2.

1. Inheritance diff: render_2 vs the parent's certified render_3 (001 slide033) —
   differences must be confined to the delta zones + badge numeral.
2. Frame-truth checks: title rows, W-box fills/edges, K.q ink, dots, nodes (d/stroke,
   no stems), Y strip, circle tint, highlight magenta, sentence container, block arrow.
"""
import numpy as np
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide008"
REN = np.asarray(Image.open(f"{QA}/render_2.png").convert("RGB")).astype(int)
PAR = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide033/render_3.png"
).convert("RGB")).astype(int)
FRM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_008.jpg"
).convert("RGB")).astype(int)
print("render:", REN.shape, "parent render:", PAR.shape, "frame:", FRM.shape)
SC = 150 / 72.0  # slide pt -> render px

ok = 0
fail = []
def check(name, cond, detail=""):
    global ok
    if cond:
        ok += 1
        print(f"[OK ] {name} {detail}")
    else:
        fail.append(name)
        print(f"[FAIL] {name} {detail}")

# ---- 1. inheritance diff (downsample both to 480x270 for speed) --------------------
a = np.asarray(Image.fromarray(REN.astype(np.uint8)).resize((480, 270))).astype(int)
b = np.asarray(Image.fromarray(PAR.astype(np.uint8)).resize((480, 270))).astype(int)
d = np.abs(a - b).sum(axis=2)
mask = d > 120  # significant diffs
ys, xs = np.where(mask)
print(f"inheritance diff: {len(xs)} cells >120 (of {480*270})")
# delta zones in render px (slide pt * SC), badge zone excluded
ZONES = [
    (135, 215, 225, 400),    # W_k boxes + connector heads
    (695, 755, 225, 400),    # W_v boxes
    (170, 505, 445, 535),    # sentence + highlight + block arrow
    (180, 840, 46, 82),      # title L1 (box to x833)
    (538, 628, 108, 172),    # Y strip + arrow
    (233, 368, 378, 512),    # circle + query zone
    (250, 380, 185, 400),    # DP box (dots +2/+3) + K.q + converging lines
    (503, 648, 212, 395),    # nodes
    (788, 838, 462, 512),    # legend W box
    (208, 256, 295, 342),    # parent's K2 red circle REMOVED (overlay moved to blue circle)
]
def in_zones(rx, ry):
    # downsampled(480x270) -> full-res render px -> slide pt
    sx, sy = rx * (2001 / 480) / SC, ry * (1125 / 270) / SC
    for (x0, x1, y0, y1) in ZONES:
        if x0 <= sx <= x1 and y0 <= sy <= y1:
            return True
    return False
stray = [(x, y) for x, y in zip(xs, ys) if not in_zones(x, y)]
# badge zone: render x ~1840..1890, y ~120..175
badge = [(x, y) for x, y in stray if 1830 <= x * (2001 / 480) <= 1900 and 110 <= y * (1125 / 270) <= 185]
stray2 = [(x, y) for x, y in stray if (x, y) not in badge]
check("inheritance diff confined to delta zones + badge", len(stray2) <= 12,
      f"stray={len(stray2)} badge={len(badge)} sample_stray={stray2[:8]}")

# ---- 2. frame-truth checks (render px vs frame px via composite map) ----------------
def f2r(fx, fy):
    sx = (fx - 17.628) / 0.961232
    sy = fy / 0.955556
    return sx * SC, sy * SC

# 2a. title L1 ink rows: frame 61..74 -> render
y0, y1 = f2r(0, 61)[1], f2r(0, 74)[1]
band = REN[int(y0) - 6:int(y1) + 6, 400:1500]
dk = (band.sum(axis=2) < 340)
rows = np.where(dk.sum(axis=1) > 10)[0]
check("title L1 ink rows ~ frame(61,74)", len(rows) > 0 and abs((int(y0) - 6 + rows.min()) - y0) <= 9 and abs((int(y0) - 6 + rows.max()) - y1) <= 9,
      f"render rows {int(y0)-6+rows.min()}..{int(y0)-6+rows.max()} vs want {y0:.0f}..{y1:.0f}")

# 2b. W_k box fill + edges: sample interior + border cols
fx, fy = 185, 247
rx, ry = f2r(fx, fy)
px_ = REN[int(ry), int(rx)]
check("W_k fill pale green", abs(px_[0] - 212) < 30 and px_[1] > 235 and abs(px_[2] - 220) < 30, f"{tuple(px_)}")
# left/right border cols of W_k box1: frame x 172..206, y ~240
row = REN[int(f2r(0, 240)[1]), :]
greenish = [x for x in range(int(f2r(160, 0)[0]), int(f2r(220, 0)[0])) if row[x][1] - row[x][0] > 15 and row[x][1] > 150]
if greenish:
    fx0 = (greenish[0] / SC) * 0.961232 + 17.628
    fx1 = (greenish[-1] / SC) * 0.961232 + 17.628
    check("W_k box1 cols ~ frame(172,206)", abs(fx0 - 172) <= 4 and abs(fx1 - 206) <= 4, f"frame-equiv {fx0:.1f}..{fx1:.1f}")
else:
    check("W_k box1 cols ~ frame(172,206)", False, "no greenish cols")

# 2c. K.q ink position: red text right of DP box
x0, y0 = f2r(345, 188); x1, y1 = f2r(385, 212)
sub = REN[int(y0):int(y1), int(x0):int(x1)]
m = (sub[:, :, 0] > 120) & (sub[:, :, 0] - sub[:, :, 1] > 50) & (sub[:, :, 0] - sub[:, :, 2] > 40)
ys, xs = np.where(m)
if len(xs):
    gx0 = (int(x0) + xs.min()) / SC * 0.961232 + 17.628
    gx1 = (int(x0) + xs.max()) / SC * 0.961232 + 17.628
    gy0 = (int(y0) + ys.min()) / SC * 0.955556
    gy1 = (int(y0) + ys.max()) / SC * 0.955556
    check("K.q ink ~ frame(352..373, 192..203)", abs(gx0 - 352) <= 4 and abs(gy0 - 192) <= 4 and abs(gy1 - 203) <= 5,
          f"frame-equiv x {gx0:.0f}..{gx1:.0f} y {gy0:.0f}..{gy1:.0f}")
else:
    check("K.q ink", False, "no red ink found")

# 2d. nodes: ring top arcs present at frame y ~211-216, NO red between sigma and rings
sub = REN[int(f2r(0, 188)[1]):int(f2r(0, 210)[1]), int(f2r(505, 0)[0]):int(f2r(645, 0)[0])]
redc = ((sub[:, :, 0] > 125) & (sub[:, :, 0] - sub[:, :, 1] > 40) & (sub[:, :, 0] - sub[:, :, 2] > 35)).sum()
check("no stems between Sigma and rings", redc < 30, f"red px={redc}")
# ring top arcs present
sub = REN[int(f2r(0, 209)[1]):int(f2r(0, 217)[1]), int(f2r(505, 0)[0]):int(f2r(645, 0)[0])]
redc = ((sub[:, :, 0] > 125) & (sub[:, :, 0] - sub[:, :, 1] > 40) & (sub[:, :, 0] - sub[:, :, 2] > 35)).sum()
check("ring top arcs present", redc >= 30, f"red px={redc}")

# 2e. Y strip: label ink green at frame (567..577, 124..132); cells pale green
rx, ry = f2r(572, 128)
px_ = REN[int(ry), int(rx)]
check("Y label green ink", px_[1] - px_[0] > 20 and px_[1] > 110, f"{tuple(px_)}")

# 2f. circle tint over peach: frame (262,415)
rx, ry = f2r(262, 415)
px_ = REN[int(ry), int(rx)]
check("circle tint over peach ~ (181,194,203)", abs(px_[0] - 181) < 25 and abs(px_[1] - 194) < 25 and abs(px_[2] - 203) < 25, f"{tuple(px_)}")

# 2g. highlight magenta-ish: frame (300,477) region has B>R? (dotted, tolerate)
hits = 0
for (fx, fy) in [(295, 476), (300, 477), (305, 478), (310, 476), (315, 477)]:
    rx, ry = f2r(fx, fy)
    px_ = REN[int(ry), int(rx)]
    if px_[2] > px_[1] + 25 and px_[0] > 120:
        hits += 1
check("X2 highlight magenta-family present", hits >= 1, f"hits={hits}/5")

# 2g2. sentence container fill just below its top border: frame (200, 459)
rx, ry = f2r(200, 459)
px_ = REN[int(ry), int(rx)]
check("sentence container fill near top", px_[1] > 200 and px_[1] - px_[0] > 8, f"{tuple(px_)}")

# 2h. block arrow: dark red at slide(278,520) = frame(285,497)
rx, ry = f2r(285, 497)
px_ = REN[int(ry), int(rx)]
check("block arrow dark red", px_[0] > 120 and px_[0] - px_[1] > 60, f"{tuple(px_)}")

# 2j. Y2 has NO subscript: right zone (frame 585..600, 130..140) no dark ink besides dividers
x0, y0 = f2r(584, 128); x1, y1 = f2r(600, 140)
sub = REN[int(y0):int(y1), int(x0):int(x1)]
dk = ((sub[:, :, 0] < 110) & (sub[:, :, 1] < 130)).sum()
check("no subscript ink right of Y", dk < 25, f"dark px={dk}")

# 2k. W_v fill
rx, ry = f2r(715, 240)
px_ = REN[int(ry), int(rx)]
check("W_v fill pale blue", px_[2] > 230 and abs(px_[0] - 210) < 30 and px_[1] > 235, f"{tuple(px_)}")

# 2l. ring stroke: red arc columns at node2 center row: red at ~±17 slide from center
rx, ry = f2r(559, 277.5)
row = REN[int(ry), int(rx) - 45:int(rx) + 45]
redx = [j - 45 for j in range(90) if row[j][0] > 125 and row[j][0] - row[j][1] > 40]
# ring radius 18.25 slide pt = ~38 render px
mindist = min([abs(v) for v in redx if abs(v) > 8], default=99)
check("node2 ring arcs at ~±18 slide px (38 render px)", len(redx) >= 4 and 30 <= mindist <= 46,
      f"red offsets: {redx}")

print(f"\nSELFCHECK RESULT: {ok} OK, {len(fail)} FAIL {fail if fail else ''}")
