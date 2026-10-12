#!/usr/bin/env python3
"""Forensics pass 1 — slide_025.jpg (960x540, 1px = 1pt). PIL/numpy only.

Global structure: chrome landmarks (top rule candidates, bottom black bar, any yellow
badge probe), title red bands, beige network-panel bbox, all major FILL regions located
by color masks (pink boxes, magenta dots/line, green circles/boxes, lavender box, cream
equation boxes, red Error bar), and a quantized ink census (palette hexes).
"""
import numpy as np
from PIL import Image

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_025.jpg"
im = Image.open(ORIG).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]

print(f"size {W}x{H}")

def mask_report(name, m, min_row=3, min_col=1):
    rows = m.sum(axis=1)
    ys = np.where(rows >= min_row)[0]
    print(f"\n-- {name}: total {int(m.sum())} px")
    if len(ys) == 0:
        print("   (none)")
        return []
    bands = []
    in_b = False
    for y in range(H):
        if rows[y] >= min_row and not in_b:
            y0, in_b = y, True
        elif rows[y] < min_row and in_b:
            bands.append((y0, y - 1)); in_b = False
    if in_b:
        bands.append((y0, H - 1))
    # merge bands separated by <=2 rows
    merged = []
    for b in bands:
        if merged and b[0] - merged[-1][1] <= 2:
            merged[-1] = (merged[-1][0], b[1])
        else:
            merged.append(list(b))
    out = []
    for (y0, y1) in merged:
        sub = m[y0:y1 + 1, :]
        cols = sub.sum(axis=0)
        xs = np.where(cols >= min_col)[0]
        peak = int(rows[y0:y1 + 1].max())
        out.append((y0, y1, int(xs.min()), int(xs.max()), peak))
        print(f"   band y {y0:3d}..{y1:3d} (h {y1-y0+1:3d})  x {xs.min():3d}..{xs.max():3d} (w {xs.max()-xs.min()+1:3d})  peak_rows {peak}")
    return out

# ---- chrome landmark 1: top rule candidates (rows 0..40, full width) ----
print("\n== top strip rows 0..40: dominant colors per row ==")
for y in range(0, 40, 2):
    row = a[y]
    q = row // 16 * 16
    vals, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
    order = np.argsort(-counts)[:2]
    tops = [f"rgb{tuple(int(v) for v in vals[i])}x{int(counts[i])}" for i in order]
    print(f"  y{y:3d}: " + "  ".join(tops))

# dark-red mask for the top rule
dr = (R > 90) & (R < 180) & (G < 60) & (B < 60)
mask_report("dark-red (90<R<180, G<60, B<60) — top rule / dark red text", dr)

# bright red (title, arrows, Error bar)
red = (R > 150) & (G < 90) & (B < 90)
red_bands = mask_report("bright red (R>150, G<90, B<90) — title/arrows/Error", red)

# ---- chrome landmark 2: bottom black bar ----
print("\n== bottom rows 500..539 dark fraction ==")
dark = (R < 60) & (G < 60) & (B < 60)
for y in range(500, H, 2):
    print(f"  y{y:3d}: dark {int(dark[y].sum()):3d}")
mask_report("near-black (<60) — bottom bar + text", dark, min_row=50)

# ---- chrome landmark 3: yellow badge probe (originals carry no badge — verify) ----
yel = (R > 200) & (G > 200) & (B < 140)
mask_report("yellow FDFD96-like (R>200,G>200,B<140) — badge probe", yel)

# ---- beige panel ----
tan = (abs(R - 214) < 25) & (abs(G - 195) < 25) & (abs(B - 163) < 28)
mask_report("beige panel (214,195,163 +/-25)", tan, min_row=10)

# ---- pink boxes ----
pink = (R > 220) & (abs(G - 140) < 45) & (abs(B - 190) < 45) & (B > 120)
pink_bands = mask_report("pink FF99CC-like (R>220, G~140, B~190)", pink, min_row=2)

# ---- magenta (dots + dotted line) ----
mag = (R > 150) & (G < 110) & (B > 150)
mag_bands = mask_report("magenta CC00CC-like (R>150, G<110, B>150)", mag, min_row=1)

# ---- greens: neuron green 99FF66 vs class green 99FF99 ----
g1 = (abs(R - 153) < 35) & (G > 190) & (B < 140)   # 99FF66 yellow-green
g1_b = mask_report("neuron/arrow green 99FF66-like (R~153, G>190, B<140)", g1, min_row=2)
g2 = (abs(R - 153) < 35) & (G > 190) & (B >= 140)  # 99FF99 light green
g2_b = mask_report("class green 99FF99-like (R~153, G>190, B>=140)", g2, min_row=2)

# ---- lavender box ----
lav = (abs(R - 204) < 30) & (abs(G - 204) < 30) & (B > 210)
lav_b = mask_report("lavender CCCCFF-like (R~204, B>210)", lav, min_row=2)

# ---- cream equation boxes ----
cream = (R > 240) & (G > 240) & (abs(B - 204) < 30)
cream_b = mask_report("cream FFFFCC-like (R>240, G>240, B~204)", cream, min_row=2)

# ---- white circles/boxes on the panel (inside panel x-range, excluding page bg) ----
white = (R > 235) & (G > 235) & (B > 235)

# ---- quantized ink census (whole frame) ----
print("\n== ink census: quantized-to-16 RGB, counts >= 800 px ==")
q = (a // 16 * 16)
vals, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
order = np.argsort(-counts)
for i in order:
    v, c = vals[i], int(counts[i])
    if c < 800:
        break
    print(f"  rgb({v[0]:3d},{v[1]:3d},{v[2]:3d})  #{v[0]:02X}{v[1]:02X}{v[2]:02X}  {c:7d}")

# ---- cursor probe: near top edge of middle equation box (spec ~x400-430, y440-460) ----
print("\n== cursor probe region x390..440, y435..465: darkest pixels ==")
sub = a[435:465, 390:440]
dk = (sub[..., 0] < 90) & (sub[..., 1] < 90) & (sub[..., 2] < 90)
ys, xs = np.where(dk)
if len(ys):
    print(f"  dark px count {len(ys)}, x {390+xs.min()}..{390+xs.max()}, y {435+ys.min()}..{435+ys.max()}")
else:
    print("  no dark pixels found in probe region")
