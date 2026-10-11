#!/usr/bin/env python3
# measure2_census.py — slide 042 definitive PIL census (worker attempt 3, 2026-10-12)
# Reuses the verified chrome mapping (left 59, right 902, top 43, bottom 516 — identical
# to certified 002/039): slide_x=(fx-18.63)/0.96123, slide_y=fy/0.95556.
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
img = np.asarray(Image.open(FR).convert("RGB")).astype(int)
H, W, _ = img.shape
print(f"frame {W}x{H}")

R, G, B = img[..., 0], img[..., 1], img[..., 2]

def dark(px):  # non-background (not near-white)
    return px.sum(axis=-1) < 690

def is_red(px):
    r, g, b = px[..., 0], px[..., 1], px[..., 2]
    return (r > 120) & (r - g > 60) & (r - b > 60)

def is_green(px):
    r, g, b = px[..., 0], px[..., 1], px[..., 2]
    return (g - r > 40) & (g - b > 40)

def is_blue(px):
    r, g, b = px[..., 0], px[..., 1], px[..., 2]
    return (b - r > 50) & (b - g > 20)

def is_magenta(px):
    r, g, b = px[..., 0], px[..., 1], px[..., 2]
    return (r - g > 60) & (b - g > 40) & (r > 80)

def is_yellow(px):
    r, g, b = px[..., 0], px[..., 1], px[..., 2]
    return (r - b > 80) & (g - b > 60) & (r > 150) & (g > 130)

def is_orange(px):
    r, g, b = px[..., 0], px[..., 1], px[..., 2]
    return (r - b > 90) & (r - g > 40) & (g - b > 10) & (g > 60) & (g < 190)

def is_bluegray(px):
    r, g, b = px[..., 0], px[..., 1], px[..., 2]
    return (b - r > 15) & (b - g > 5) & (b > 90) & (r < 160) & (g < 170)

def bbox(mask, x0=0, y0=0, x1=None, y1=None):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0:
        return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max(), len(xs))

# ---------- A. TITLE ----------
tm = is_red(img) & (np.arange(W)[None, :] > 150) & (np.arange(W)[None, :] < 850)
print("TITLE red bbox y50..135:", bbox(tm, 150, 45, 860, 135))
# per-column ink for x-extent and per-row for cap height
sub = tm[45:135, 150:860]
cols = np.nonzero(sub.any(axis=0))[0]
rows = np.nonzero(sub.any(axis=1))[0]
print("title col extent:", 150 + cols.min(), 150 + cols.max(), "row extent:", 45 + rows.min(), 45 + rows.max())
# core (dark red) pixels only for advance fit
core = (R > 130) & (R < 230) & (G < 80) & (B < 80)

# ---------- B. BLUE CONTENT FRAME ----------
bm = is_blue(img) & ~((np.arange(W)[None, :] > 880) & (np.arange(H)[:, None] < 100))
print("blue cols y300..450 (frac>0.3):", [int(x) for x in np.arange(W) if (bm[300:450, x]).mean() > 0.3])
print("blue rows x150..800 (frac>0.3):", [int(y) for y in np.arange(H) if (bm[y, 150:800]).mean() > 0.3])

# ---------- C. LABEL BOXES (red borders — thin/faded, use looser reddish test) ----------
def reddish(seg2d):
    r, g, b = seg2d[..., 0], seg2d[..., 1], seg2d[..., 2]
    return (r - g > 25) & (r - b > 25) & (r > 110)

for name, x0, x1, ys in [("leftbox", 80, 325, range(180, 250)), ("midbox", 345, 595, range(180, 250)), ("rightbox", 632, 868, range(155, 245))]:
    hits = [y for y in ys if reddish(img[y, x0:x1]).sum() > (x1 - x0) * 0.5]
    print(name, "border rows:", hits)
for name, y0, y1, xs in [("leftbox", 200, 230, range(60, 350)), ("midbox", 200, 230, range(335, 610)), ("rightbox", 175, 220, range(615, 885))]:
    hits = [x for x in xs if reddish(img[y0:y1, x]).sum() > (y1 - y0) * 0.5]
    print(name, "border cols:", hits)

# ---------- D. TEXT LINE BANDS + WORD COLORS (dense, tight rows) ----------
def word_census(y0, y1, x0, x1, tag):
    seg = img[y0:y1, x0:x1]
    dk = seg.sum(axis=-1) < 640
    if dk.sum() == 0:
        print(tag, "NO INK"); return
    cols = np.nonzero(dk.any(axis=0))[0]
    # column runs (gap > 3px splits words)
    runs, start, prev = [], cols[0], cols[0]
    for c in cols[1:]:
        if c - prev > 3:
            runs.append((start, prev)); start = c
        prev = c
    runs.append((start, prev))
    out = []
    for a, b in runs:
        m = dk[:, a:b + 1]
        px = seg[:, a:b + 1][m]
        r, g, bl = px[:, 0].mean(), px[:, 1].mean(), px[:, 2].mean()
        # darkest-quartile core color
        s = px.sum(axis=1); idx = np.argsort(s)[:max(1, len(s) // 4)]
        cr, cg, cb = px[idx, 0].mean(), px[idx, 1].mean(), px[idx, 2].mean()
        out.append(f"x{x0+a}..{x0+b} w{b-a+1} n={m.sum()} core=({cr:.0f},{cg:.0f},{cb:.0f})")
    print(tag, "|", " ; ".join(out))

print("--- LEFT BOX text")
word_census(196, 214, 78, 330, "L-L1")
word_census(214, 232, 78, 330, "L-L2")
print("--- MID BOX text")
word_census(196, 214, 338, 600, "M-L1")
word_census(214, 232, 338, 600, "M-L2")
print("--- RIGHT BOX text")
word_census(170, 185, 630, 880, "R-L1")
word_census(186, 204, 630, 880, "R-L2")
word_census(203, 221, 630, 880, "R-L3")

# ---------- E. LEFT STACK geometry (green) ----------
gm = is_green(img)
print("left stack bbox:", bbox(gm, 150, 240, 250, 445))
# per-row green count x160..240
rows = [(y, int(gm[y, 160:240].sum())) for y in range(245, 445)]
nz = [y for y, n in rows if n > 8]
print("left stack green rows:", nz[0], "..", nz[-1])
# column profile
colsn = [(x, int(gm[250:440, x].sum())) for x in range(155, 245)]
print("left stack col extents:", [x for x, n in colsn if n > 5][0], "..", [x for x, n in colsn if n > 5][-1])
# row bands (front faces vs top slivers): rows with green count > 40 = front, 8..40 = top sliver
fb = [y for y, n in rows if n > 45]
tb = [y for y, n in rows if 8 < n <= 45]
def bands(lst):
    if not lst: return []
    out, s, p = [], lst[0], lst[0]
    for v in lst[1:]:
        if v - p > 1: out.append((s, p)); s = v
        p = v
    out.append((s, p)); return out
print("left FRONT bands:", bands(fb))
print("left TOP slivers:", bands(tb))

# ---------- F. MIDDLE GRID geometry ----------
print("mid grid bbox:", bbox(gm, 360, 240, 540, 435))
rows = [(y, int(gm[y, 370:525].sum())) for y in range(245, 435)]
fb = [y for y, n in rows if n > 60]
tb = [y for y, n in rows if 8 < n <= 60]
print("mid FRONT bands:", bands(fb))
print("mid TOP slivers:", bands(tb))
colsn = [(x, int(gm[250:430, x].sum())) for x in range(365, 535)]
nz = [x for x, n in colsn if n > 5]
print("mid grid col extent:", nz[0], "..", nz[-1])
# column runs inside (gaps between the 4 columns): count per column of front-band rows
fr = bands(fb)
mid_rows = range(fr[0][0], fr[-1][1] + 1) if fr else []
colprof = [(x, int(gm[list(mid_rows), x].sum())) for x in range(365, 535)]
gaps = [x for x, n in colprof if n < 10]
print("mid grid col gaps:", bands(gaps))

# ---------- G. RIGHT BLOCK: layer order/colors (THE open [?]) ----------
print("--- RIGHT BLOCK dense census")
# vertical scan at several x through the top staircase (y270..330)
for x in [660, 700, 740, 770, 800, 820, 840, 855]:
    col = []
    for y in range(260, 335):
        px = img[y, x]
        cls = ("M" if is_magenta(px[None, None])[0, 0] else
               "Y" if is_yellow(px[None, None])[0, 0] else
               "O" if is_orange(px[None, None])[0, 0] else
               "G" if is_green(px[None, None])[0, 0] else
               "b" if is_bluegray(px[None, None])[0, 0] else
               "K" if px.sum() < 300 else ".")
        col.append(cls)
    s = "".join(col)
    import re
    s2 = re.sub(r"(.)\1+", lambda m: m.group(1) + str(len(m.group(0))), s)
    print(f"  x={x} y260..335: {s2}")
# horizontal scan at several y through the right staircase (x770..890)
for y in [330, 360, 390, 420, 450]:
    row = []
    for x in range(620, 890):
        px = img[y, x]
        cls = ("M" if is_magenta(px[None, None])[0, 0] else
               "Y" if is_yellow(px[None, None])[0, 0] else
               "O" if is_orange(px[None, None])[0, 0] else
               "G" if is_green(px[None, None])[0, 0] else
               "b" if is_bluegray(px[None, None])[0, 0] else
               "K" if px.sum() < 300 else ".")
        row.append(cls)
    s = "".join(row)
    s2 = re.sub(r"(.)\1+", lambda m: m.group(1) + str(len(m.group(0))), s)
    print(f"  y={y} x620..890: {s2}")

# core colors of each class region (darkest quartile) in the right block
seg = img[240:480, 600:900]
def corecol(mask, tag):
    px = seg[mask]
    if len(px) == 0: print(tag, "none"); return
    s = px.sum(axis=1); idx = np.argsort(s)[:max(1, len(s) // 5)]
    print(tag, f"n={len(px)} core=({px[idx,0].mean():.0f},{px[idx,1].mean():.0f},{px[idx,2].mean():.0f})")
rr, gg, bb = seg[..., 0], seg[..., 1], seg[..., 2]
corecol((rr - gg > 60) & (bb - gg > 40), "magenta")
corecol((rr - bb > 80) & (gg - bb > 60) & (rr > 150) & (gg > 130), "yellow")
corecol((rr - bb > 90) & (rr - gg > 40) & (gg - bb > 10) & (gg > 60) & (gg < 190), "orange")
corecol((gg - rr > 40) & (gg - bb > 40), "green")
corecol((bb - rr > 15) & (bb > 90) & (rr < 160), "bluegray")

# ---------- H. ARROWS ----------
# vertical arrow: red pixels x630..660, y315..475 (excluding text strip x626..640?)
va = rm[300:480, 634:652]
ys2, xs2 = np.nonzero(va)
if len(xs2): print("v-arrow red bbox:", 634 + xs2.min(), 300 + ys2.min(), 634 + xs2.max(), 300 + ys2.max(), "n", len(xs2))
# horizontal arrow: red px y455..470, x640..810 excluding labels below
ha = rm[452:472, 640:812]
ys2, xs2 = np.nonzero(ha)
if len(xs2): print("h-arrow red bbox:", 640 + xs2.min(), 452 + ys2.min(), 640 + xs2.max(), 452 + ys2.max(), "n", len(xs2))
# diagonal arrow: red px x790..895, y380..480 excluding rotated text
da = rm[380:480, 786:896]
ys2, xs2 = np.nonzero(da)
if len(xs2): print("d-arrow red bbox:", 786 + xs2.min(), 380 + ys2.min(), 786 + xs2.max(), 380 + ys2.max(), "n", len(xs2))
# rotated labels bboxes
for tag, x0, x1, y0, y1 in [("rot 'Feature Vector'", 615, 640, 330, 460), ("rot 'Batch size'", 800, 860, 390, 470),
                            ("'Channels'", 645, 740, 468, 485), ("'(4 Filters)'", 645, 740, 483, 500),
                            ("'(5 samples)'", 800, 880, 415, 470)]:
    print(tag, "ink bbox:", bbox(dark(img), x0, y0, x1, y1))
# stacking arrow (white arrow between magenta & yellow near top): light pixels y285..320 x680..780 on colored bg
print("stack-arrow region white px bbox:", bbox((seg.sum(axis=-1) > 700), 60, 30, 190, 100))

# ---------- I. badge numeral ink (red 42?) ----------
badge = rm[52:92, 855:900]
ys2, xs2 = np.nonzero(badge)
if len(xs2): print("badge red-ink bbox:", 855 + xs2.min(), 52 + ys2.min(), 855 + xs2.max(), 52 + ys2.max(), "n", len(xs2))
