#!/usr/bin/env python3
# selfcheck6.py — closed-loop numeric pass on render_6.png (attempt 6: red y-labels).
# Render vs ORIGINAL direct comparisons (mapped); thin-JPEG-stroke elements use a
# looser red/green predicate on the original and tol 8 (stroke-end fade).
from PIL import Image
REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide010/render_6.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_010.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide010/selfcheck_attempt_6_output.txt"
r = Image.open(REN).convert("RGB"); o = Image.open(ORIG).convert("RGB")
rp, op = r.load(), o.load()
RW, RH = r.size; S = RW / 960.0
FX = lambda sx: 17.628 + 0.961232 * sx
FY = lambda sy: 0.955556 * sy
f2r_x = lambda fx: (fx - 17.628) / 0.961232 * S
f2r_y = lambda fy: fy / 0.955556 * S
out = []
def p(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s)
def isred(c):  x,g,b = c; return x > 140 and g < 100 and b < 100
def isredish(c): x,g,b = c; return x-g > 60 and x-b > 50 and x > 90
def isblue(c): x,g,b = c; return b > 140 and b - x > 50 and g < 150
def isblueish(c): x,g,b = c; return b-x > 30 and b > 120 and g < 170
def isdark(c): x,g,b = c; return x < 75 and g < 75 and b < 75
def isgreen(c): x,g,b = c; return g > 110 and g - x > 40 and g - b > 40
def bbox(px_, x0, y0, x1, y1, fn):
    xs = []; ys = []
    for y in range(max(0, int(y0)), min(RH, int(y1))):
        for x in range(max(0, int(x0)), min(RW, int(x1))):
            if fn(px_[x, y]): xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None
fails = 0
def pair(tag, sx0, sy0, sx1, sy1, fnr, fno=None, tol=6):
    fno = fno or fnr
    g = bbox(rp, sx0 * S, sy0 * S, sx1 * S, sy1 * S, fnr)
    e = bbox(op, FX(sx0), FY(sy0), FX(sx1), FY(sy1), fno)
    if g is None: p("FAIL", tag, "render no ink"); return 1
    if e is None: p("FAIL", tag, "original no ink"); return 1
    er = (f2r_x(e[0]), f2r_y(e[1]), f2r_x(e[2]), f2r_y(e[3]))
    dx = max(abs(g[0] - er[0]), abs(g[2] - er[2])); dy = max(abs(g[1] - er[1]), abs(g[3] - er[3]))
    ok = "OK " if (dx <= tol and dy <= tol) else "FAIL"
    p(ok, tag, "render", tuple(round(v, 1) for v in g),
      "orig(mapped)", tuple(round(v, 1) for v in er), "d", (round(dx, 1), round(dy, 1)))
    return 0 if ok == "OK " else 1

# ---- braces (attempt-5 PNG braces; unchanged in 6) -------------------------------------
fails += pair("braceL1", 522, 110.5, 545, 305.5, isblue)
fails += pair("braceR1", 833, 110.5, 853, 305.5, isblue)
fails += pair("braceL2", 522, 334.5, 545, 510, isblue)
fails += pair("braceR2", 833, 334.5, 853, 510, isblue)
# ---- y labels: RED glyphs (attempt-6 fix) vs original ----------------------------------
fails += pair("y1.label.red", 240, 146, 268, 178, isred, isredish, tol=8)
fails += pair("y2.label.red", 240, 250, 268, 282, isred, isredish, tol=8)
fails += pair("y4.label.red", 240, 462, 268, 494, isred, isredish, tol=8)
# ---- green arrow band (unchanged; stroke-end fade -> tol 8) ----------------------------
fails += pair("y1.arrow.green", 238, 163, 270, 174, isgreen, isgreen, tol=8)
# ---- mid-panel row elements (unchanged since attempt 5) --------------------------------
fails += pair("sigmoid", 444, 190, 516, 222, isblue, isblueish)  # window ends 516: excludes panel border
fails += pair("callout2", 791, 288, 905, 330, isdark)
fails += pair("pill.row1", 537, 102, 665, 145, isred, tol=8)
# ---- brackets + delimiter coverage ------------------------------------------------------
gBL = bbox(rp, 289 * S, 172 * S, 302 * S, 240 * S, isred)
gBR = bbox(rp, 438 * S, 172 * S, 450 * S, 240 * S, isred)
p("bracketL1 ink:", gBL, "bracketR1 ink:", gBR)
if gBL and gBR:
    top = min(gBL[1], gBR[1]); bot = max(gBL[3], gBR[3])
    box_top, box_bot = 190 / 0.955556 * S, 211 / 0.955556 * S
    ok = top <= box_top + 2 and bot >= box_bot - 2
    p("DELIM brackets cover y-boxes:", "OK" if ok else "FAIL")
    fails += 0 if ok else 1
else:
    p("FAIL brackets missing"); fails += 1
p("TOTAL FAILS:", fails)
open(OUT, "w").write("\n".join(out))
