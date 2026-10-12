#!/usr/bin/env python3
# selfcheck5.py — closed-loop numeric pass on render_5.png (attempt 5: PNG braces).
# Element checks compare RENDER vs ORIGINAL directly. Original ink is mapped to
# render space: render_x = (fx-17.628)/0.961232 * S, render_y = fy/0.955556 * S.
# Windows exclude the right1 panel's rounded-corner top border (slide y<=108.7+halo).
from PIL import Image
REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide010/render_5.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_010.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide010/selfcheck_attempt_5_output.txt"
r = Image.open(REN).convert("RGB"); o = Image.open(ORIG).convert("RGB")
rp, op = r.load(), o.load()
RW, RH = r.size; S = RW / 960.0  # render px per slide pt
FX = lambda sx: 17.628 + 0.961232 * sx          # slide -> frame x
FY = lambda sy: 0.955556 * sy                   # slide -> frame y
f2r_x = lambda fx: (fx - 17.628) / 0.961232 * S # frame -> render x
f2r_y = lambda fy: fy / 0.955556 * S            # frame -> render y
out = []
def p(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s)
def isred(c):  x,g,b = c; return x > 140 and g < 100 and b < 100
def isblue(c): x,g,b = c; return b > 140 and b - x > 50 and g < 150
def isdark(c): x,g,b = c; return x < 75 and g < 75 and b < 75
def isgreen(c): x,g,b = c; return g > 110 and g - x > 40 and g - b > 40
def bbox(px_, x0, y0, x1, y1, fn):
    xs = []; ys = []
    for y in range(max(0, int(y0)), min(RH, int(y1))):
        for x in range(max(0, int(x0)), min(RW, int(x1))):
            if fn(px_[x, y]): xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None
fails = 0
def pair(tag, sx0, sy0, sx1, sy1, fn, tol=6):
    """Ink bbox in render (slide-px window) vs original (mapped), tolerance in render px."""
    g = bbox(rp, sx0 * S, sy0 * S, sx1 * S, sy1 * S, fn)
    e = bbox(op, FX(sx0), FY(sy0), FX(sx1), FY(sy1), fn)
    if g is None: p("FAIL", tag, "render no ink"); return 1
    if e is None: p("FAIL", tag, "original no ink"); return 1
    er = (f2r_x(e[0]), f2r_y(e[1]), f2r_x(e[2]), f2r_y(e[3]))
    dx = max(abs(g[0] - er[0]), abs(g[2] - er[2])); dy = max(abs(g[1] - er[1]), abs(g[3] - er[3]))
    ok = "OK " if (dx <= tol and dy <= tol) else "FAIL"
    p(ok, tag, "render", tuple(round(v, 1) for v in g),
      "orig(mapped)", tuple(round(v, 1) for v in er), "d", (round(dx, 1), round(dy, 1)))
    return 0 if ok == "OK " else 1

# ---- braces (attempt-5 PNG braces; y window 110.5..305.5 avoids panel corner arc) -----
fails += pair("braceL1", 522, 110.5, 545, 305.5, isblue)
fails += pair("braceR1", 833, 110.5, 853, 305.5, isblue)
fails += pair("braceL2", 522, 334.5, 545, 510, isblue)
fails += pair("braceR2", 833, 334.5, 853, 510, isblue)
# brace CURL: ink x-extent profile at top/mid/bottom thirds; render vs original.
def prof(px_, xs_range, ys_samples, to_slide):
    rows = []
    for yy in ys_samples:
        xs = [x for x in xs_range if isblue(px_[x, int(yy)])]
        rows.append((round(to_slide(min(xs)), 1), round(to_slide(max(xs)), 1)) if xs else None)
    return rows
for tag, sx0, sx1, sy0, sy1 in [("curlL1", 522, 545, 110.5, 305.5), ("curlR1", 833, 853, 110.5, 305.5)]:
    yr = [(sy0 + (sy1 - sy0) * f) * S for f in (0.12, 0.5, 0.88)]
    yo = [FY(sy0 + (sy1 - sy0) * f) for f in (0.12, 0.5, 0.88)]
    pr = prof(rp, range(int(sx0 * S), int(sx1 * S)), yr, lambda x: x / S)
    po = prof(op, range(int(FX(sx0)), int(FX(sx1))), yo, lambda x: (x - 17.628) / 0.961232)
    p(tag, "render(slide-px)", pr, "orig(slide-px)", po)
    if any(v is None for v in pr) or any(v is None for v in po):
        p("FAIL", tag, "missing profile row (JPEG-thin stroke? widen band)"); fails += 1
    else:
        wmr = pr[1][1] - pr[1][0]; wmo = po[1][1] - po[1][0]
        wtr = pr[0][1] - pr[0][0]; wto = po[0][1] - po[0][0]
        ok = abs(wmr - wmo) <= 3 and abs(wtr - wto) <= 3
        p("OK " if ok else "FAIL", tag, "widths render(top,mid)", (round(wtr,1), round(wmr,1)),
          "orig(top,mid)", (round(wto,1), round(wmo,1)))
        fails += 0 if ok else 1

# ---- mid-panel row elements (direct vs original) ---------------------------------------
fails += pair("bracketL1", 289, 172, 302, 240, isred)
fails += pair("bracketR1", 438, 172, 450, 240, isred)
fails += pair("yt.Y", 350, 148, 378, 178, isred)
fails += pair("sigmoid", 444, 190, 520, 222, isblue)
fails += pair("callout2", 791, 288, 905, 330, isdark)
fails += pair("y1.green", 240, 148, 292, 184, isgreen, tol=6)
fails += pair("parens1", 848, 112, 872, 300, isred, tol=6)
fails += pair("pill.row1", 537, 102, 665, 145, isred, tol=6)
# ---- callout1 line bands (window = box interior only, slide 416..522 x 296..331) -------
def iswhite(c): x, g, b = c; return x > 200 and g > 200 and b > 200
x0, x1, y0, y1 = int(416 * S), int(522 * S), int(296 * S), int(331 * S)
rows = [y for y in range(y0, y1) if sum(1 for x in range(x0, x1) if iswhite(rp[x, y])) > 4]
bands = []
if rows:
    st = rows[0]; prev = rows[0]
    for y in rows[1:]:
        if y - prev > 3: bands.append((st, prev)); st = y
        prev = y
    bands.append((st, prev))
p("callout1 white bands (box interior):", bands, "count:", len(bands),
  "pitch:", bands[1][0] - bands[0][0] if len(bands) > 1 else None, "(want 2 bands, pitch ~27)")
if len(bands) != 2:
    p("FAIL callout1 bands"); fails += 1
p("TOTAL FAILS:", fails)
open(OUT, "w").write("\n".join(out))
