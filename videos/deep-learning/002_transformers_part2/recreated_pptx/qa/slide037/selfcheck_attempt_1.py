#!/usr/bin/env python3
"""Pre-judge self-checks for slide 037 attempt 1 (150dpi render = 2001x1125; 1px = 0.48pt;
slide_pt = px*72/150). Checks: (1) full-render diff vs the imported parent composition
render (base-1.png) confined to the measured delta zones; (2) element presence (title,
pin, disc, dashbox, clocks, funnel, interior boxes) via ink counts in measured zones;
(3) frame containment for the new overlays."""
from PIL import Image
import json

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide037/render_1.png"
BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide037/base-1.png"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide037/selfcheck_attempt_1.txt"

S = 150 / 72.0  # slide pt -> render px
def R(v): return int(round(v * S))

render = Image.open(RENDER).convert("RGB")
base = Image.open(BASE).convert("RGB")
W, H = render.size
pr, pb = render.load(), base.load()
lines = []
lines.append(f"render {W}x{H}, base {base.size}")

# ---- 1. diff regions vs parent composition render --------------------------------
TH = 60
diff = [[0] * W for _ in range(H)]
for y in range(0, H, 2):
    for x in range(0, W, 2):
        a, b = pr[x, y], pb[x, y]
        d = (abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])) / 3
        if d > TH:
            diff[y][x] = 1
seen = [[False] * W for _ in range(H)]
comps = []
for y in range(0, H, 2):
    for x in range(0, W, 2):
        if diff[y][x] and not seen[y][x]:
            stack = [(x, y)]; seen[y][x] = True
            x0 = x1 = x; y0 = y1 = y; n = 0
            while stack:
                cx, cy = stack.pop(); n += 1
                x0 = min(x0, cx); x1 = max(x1, cx); y0 = min(y0, cy); y1 = max(y1, cy)
                for nx, ny in ((cx+2,cy),(cx-2,cy),(cx,cy+2),(cx,cy-2),(cx+2,cy+2),(cx-2,cy-2),(cx+2,cy-2),(cx-2,cy+2)):
                    if 0 <= nx < W and 0 <= ny < H and diff[ny][nx] and not seen[ny][nx]:
                        seen[ny][nx] = True; stack.append((nx, ny))
            if n >= 12:
                comps.append({"bbox_pt": [round(x0/S,1), round(y0/S,1), round(x1/S,1), round(y1/S,1)], "n": n})
comps.sort(key=lambda c: -c["n"])
lines.append(f"diff components (>=12 samples): {len(comps)}")

# measured delta zones (slide pt) — diffs must fall inside these
DELTA_ZONES = [
    ("title",        (80, 45, 905, 100)),
    ("legend_zone",  (130, 95, 525, 215)),
    ("pin",          (585, 165, 690, 280)),
    ("dashbox",      (610, 240, 755, 395)),
    ("disc",         (660, 322, 706, 366)),
    ("enc_interior", (628, 265, 730, 410)),
    ("enc_pe",       (585, 408, 732, 452)),
    ("dec_pe",       (785, 408, 890, 452)),
    ("funnel_d3ext", (185, 375, 290, 495)),
    ("funnel_new",   (500, 360, 655, 500)),
    ("badge",        (855, 45, 915, 100)),
    ("dec_chevrons", (760, 300, 845, 330)),
    ("gap_shafts",   (778, 188, 792, 270)),
]
def in_delta(c):
    x0, y0, x1, y1 = c["bbox_pt"]
    for name, (zx0, zy0, zx1, zy1) in DELTA_ZONES:
        if x0 >= zx0 - 6 and y0 >= zy0 - 6 and x1 <= zx1 + 6 and y1 <= zy1 + 6:
            return name
    return None
outside = []
for c in comps:
    z = in_delta(c)
    if z is None:
        outside.append(c)
lines.append("diff components OUTSIDE delta zones (must be empty or drift-only):")
for c in outside[:15]:
    lines.append(f"  {c}")

# ---- 2. element presence (ink in measured zones, in MY render) --------------------
def ink(x0, y0, x1, y1, pred):
    n = 0
    for y in range(R(y0), R(y1)):
        for x in range(R(x0), R(x1)):
            if pred(pr[x, y]):
                n += 1
    return n
is_red = lambda p: p[0] > 140 and (p[0]-p[1]) > 80 and (p[0]-p[2]) > 80
is_dark = lambda p: min(p) < 90
is_white = lambda p: p[0] > 235 and p[1] > 235 and p[2] > 230
checks = {
    "title_red_ink": ink(90, 50, 880, 100, is_red),
    "pin_red_ink": ink(590, 170, 690, 280, is_red),
    "pin_white_text": ink(600, 180, 670, 250, is_white),
    "disc_red_ink": ink(668, 328, 700, 360, is_red),
    "dashbox_red_ink": ink(612, 242, 752, 392, is_red),
    "graybox1_ink": ink(650, 274, 725, 294, is_dark),
    "brownbox_ink": ink(651, 289, 716, 321, is_dark),
    "graybox2_ink": ink(650, 339, 725, 356, is_dark),
    "bus_ink": ink(624, 352, 694, 410, lambda p: p[1] > 120 and (p[1]-p[0]) > 25 and (p[1]-p[2]) > 40),
    "enc_clock_ink": ink(650, 416, 678, 444, is_dark),
    "dec_clock_ink": ink(793, 415, 827, 448, is_dark),
    "enc_sine_ink": ink(679, 424, 704, 443, is_dark),
    "funnel_d3_ink": ink(185, 375, 290, 495, is_red),
    "funnel_new_ink": ink(500, 360, 655, 500, is_red),
}
lines.append("element ink counts (my render):")
for k, v in checks.items():
    lines.append(f"  {k}: {v}")
BLOCKERS = [k for k, v in checks.items() if v < 20]
lines.append(f"BLOCKERS (ink<20): {BLOCKERS}")

# ---- 3. frame containment (house frame x0.15..13.18in y0.15..7.35in -> pt 10.8..948.9 / 10.8..529.2) ----
containment = {}
for name, (x0, y0, x1, y1) in [("dashbox", (621, 250, 741, 384)), ("pin", (595, 173, 667, 268)),
                                ("disc", (672, 331, 696, 355)), ("title", (88, 52, 888, 100))]:
    ok = x0 >= 10 and y0 >= 10 and x1 <= 949 and y1 <= 530
    containment[name] = ok
lines.append(f"containment: {containment}")

result = "\n".join(lines)
print(result)
open(OUT, "w").write(result + "\n")
