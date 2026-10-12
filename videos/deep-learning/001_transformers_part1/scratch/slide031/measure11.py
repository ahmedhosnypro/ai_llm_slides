#!/usr/bin/env python3
"""Mean-color scans for text strokes + emphasis box structure + callout fills."""
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
W, H = im.size
px = im.load()

def mean_text(x0, y0, x1, y1, keep, label):
    tot = [0, 0, 0]; n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = px[x, y]
            if keep(c):
                for i in range(3): tot[i] += c[i]
                n += 1
    if n == 0:
        print(f"  {label}: NONE")
        return
    m = tuple(t // n for t in tot)
    print(f"  {label}: mean {m} #{m[0]:02X}{m[1]:02X}{m[2]:02X} n={n}")

# dark text pixels: clearly darker than any plausible bg
dark = lambda c: sum(c) < 330
print("== matrix text row means (Q) ==")
mean_text(222, 128, 372, 150, dark, "Q row1")
mean_text(222, 168, 372, 190, dark, "Q row2")
mean_text(222, 210, 372, 233, dark, "Q row3")
mean_text(222, 252, 372, 273, dark, "Q row4")
print("== matrix text row means (V) ==")
mean_text(622, 128, 772, 150, dark, "V row1")
mean_text(622, 168, 772, 190, dark, "V row2")
mean_text(622, 210, 772, 233, dark, "V row3")
mean_text(622, 252, 772, 273, dark, "V row4")
print("== matrix text row means (K) ==")
mean_text(222, 345, 372, 367, dark, "K row1")
mean_text(222, 386, 372, 408, dark, "K row2")
mean_text(222, 429, 372, 451, dark, "K row3")
mean_text(222, 470, 372, 491, dark, "K row4")

print("== label means ==")
red = lambda c: c[0] > 90 and c[0] - c[1] > 45 and c[0] - c[2] > 45
blue = lambda c: c[2] > 60 and c[2] - c[0] > 40 and c[2] - c[1] > 40
mean_text(183, 170, 210, 187, dark, "Q '1xd'")
mean_text(108, 183, 142, 214, dark, "Q 'X2'")
mean_text(172, 234, 212, 260, red, "Q 'W_Q' red px")
mean_text(336, 250, 372, 294, dark, "Q 'dxd'")
mean_text(385, 195, 408, 212, dark, "Q '='")
mean_text(415, 96, 448, 116, red, "Q role letter")
mean_text(495, 452, 890, 515, blue, "notebox blue px")
mean_text(495, 452, 890, 515, red, "notebox red px")
mean_text(645, 386, 885, 436, red, "emphasis red px")
mean_text(455, 278, 675, 306, blue, "callout1 blue px")
mean_text(455, 278, 675, 306, dark, "callout1 dark px")
mean_text(115, 71, 175, 92, red, "subtitle 'Query'")
mean_text(108, 71, 890, 92, dark, "subtitle dark px")

print("== title ink extent (rows 48..70, dark px per col-span) ==")
cols = [x for x in range(40, 930) if any(sum(px[x, y]) < 250 for y in range(46, 70))]
def spans(cols, gap=8):
    if not cols: return []
    out = []; s = cols[0]; p = cols[0]
    for x in cols[1:]:
        if x - p > gap: out.append((s, p)); s = x
        p = x
    out.append((s, p)); return out
sp = spans(cols, 25)
print("  dark col spans (gap 25):", sp[:6], "...", sp[-3:] if len(sp) > 9 else "")
print("  first/last:", (min(cols), max(cols)) if cols else None)

print("== emphasis box structure ==")
for (x, y) in [(875, 400), (875, 430), (660, 400), (660, 433), (700, 388), (700, 410), (700, 432), (850, 415), (770, 392), (640, 410), (890, 410)]:
    print(f"  ({x},{y}): {px[x, y]}")
# yellow col extent per row band
def yext(y):
    ys = [x for x in range(630, 900) if px[x, y][0] > 235 and px[x, y][1] > 215 and px[x, y][2] < 160]
    return (min(ys), max(ys), len(ys)) if ys else None
for y in range(384, 438, 2):
    print(f"  y={y}: yellow {yext(y)}")

print("== callout fills (clean samples) ==")
for lbl, pts in [
    ("callout1", [(470, 285), (470, 300), (610, 285), (610, 302), (540, 282)]),
    ("callout2", [(730, 316), (730, 336), (860, 316), (860, 338), (800, 315)]),
    ("callout3", [(470, 342), (470, 372), (610, 342), (610, 374), (540, 340)]),
]:
    print(f"  {lbl}: " + " ".join(f"{px[x, y]}" for x, y in pts))

print("== callout border color (darkest on border rows) ==")
def darkest(x0, y0, x1, y1):
    best = None; bl = 10**9
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = px[x, y]; l = sum(c)
            if l < bl: bl = l; best = (c, x, y)
    return best
print("  c1 top border:", darkest(470, 275, 610, 282))
print("  c2 top border:", darkest(740, 306, 870, 315))
print("  c3 top border:", darkest(470, 330, 610, 340))

print("== Q matrix tile border + fill ==")
mean_text(227, 130, 251, 148, lambda c: sum(c) < 480 and c[0] > c[2], "Q tile r1c1 borderish")
print("  tile interior samples:", [px[x, y] for x, y in [(240, 145), (280, 145), (320, 185), (240, 225), (350, 260)]])
print("  matrix bg samples:", [px[x, y] for x, y in [(220, 150), (258, 170), (296, 250), (334, 155), (372, 200)]])
