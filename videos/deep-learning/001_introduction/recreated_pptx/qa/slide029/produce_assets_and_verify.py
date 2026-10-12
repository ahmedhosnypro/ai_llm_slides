#!/usr/bin/env python3
"""slide 029 — re-verify banked measurements + produce crop assets (resume worker).

Re-verifies the predecessor's banked measurements (measure_original*_out.txt) against
unique_slides/slide_029.jpg, metric-solves the body font, and crops the three
photographic regions (meme / card stack / close-up+arrows) into build/assets/ at
exact 1px=1pt geometry, inpainting the captured mouse cursor (artifact law).
"""
import numpy as np
from PIL import Image, ImageFont

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_029.jpg"
ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"

im = Image.open(ORIG).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print(f"original {W}x{H}")
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = (r * 299 + g * 587 + b * 114) // 1000

def ink_bbox(x0, y0, x1, y1, thr=200):
    """bbox of pixels darker than thr in region (inclusive coords)."""
    sub = lum[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(sub < thr)
    if not len(ys):
        return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())

# ---------- 1. title ----------
tb = ink_bbox(100, 60, 880, 160, thr=180)
print(f"title ink bbox: {tb} (expect x179..755 y86..118)")
# cap of 'S' (first glyph): column band x179..212
scap = ink_bbox(179, 60, 212, 160, thr=180)
print(f"title S cap: {scap} (expect y86..117 h32)")

# ---------- 2. content frame strokes ----------
# horizontal strokes: rows where many red-ish px between x100..880
redish = (r > 110) & (g < 120) & (b < 120)
rowsum = redish[:, 100:880].sum(axis=1)
rows = [y for y in range(150, 520) if rowsum[y] > 500]
print(f"frame horizontal stroke rows (n>500): {rows} (expect ~202-204, 480-481)")
colsum_top = redish[210:470, :].sum(axis=0)
cols = [x for x in range(60, 900) if colsum_top[x] > 200]
print(f"frame vertical stroke cols (n>200): {cols} (expect ~72-73, 894)")

# ---------- 3. bullet lines ----------
LINES = {
    "L1a": (130, 225, 520, 249),
    "L2a": (130, 250, 520, 272),
    "L2b": (130, 273, 520, 295),
    "L1b": (130, 328, 520, 352),
    "L2c": (130, 353, 520, 373),
}
meas = {}
for k, (x0, y0, x1, y1) in LINES.items():
    bb = ink_bbox(x0, y0, x1, y1, thr=190)
    meas[k] = bb
    print(f"{k}: ink {bb}  advance={bb[2]-bb[0]+1 if bb else None}")

# ring markers (saturated tan px left of text): scan x120..150
ring_zones = {"L1a": (120, 228, 150, 250), "L2a": (120, 250, 150, 268),
              "L2b": (120, 273, 150, 291), "L2c": (120, 356, 150, 372)}
for k, (x0, y0, x1, y1) in ring_zones.items():
    sub = a[y0:y1 + 1, x0:x1 + 1]
    # non-white-ish ink
    m = (sub.sum(axis=2) < 700)
    ys, xs = np.where(m)
    if len(ys):
        bb = (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())
        cx = (bb[0] + bb[2]) / 2; cy = (bb[1] + bb[3]) / 2
        # darkest color
        flat = sub.reshape(-1, 3); dk = flat[flat.sum(axis=1).argmin()]
        print(f"ring {k}: bbox {bb} center ({cx:.1f},{cy:.1f}) d={bb[2]-bb[0]+1} darkest #{dk[0]:02X}{dk[1]:02X}{dk[2]:02X}")
    else:
        print(f"ring {k}: NO INK")

# ---------- 4. meme edges ----------
# left edge at y250: first non-white from x620
row = lum[250, 620:700]
xs = np.where(row < 240)[0]
print(f"meme left edge @y250: x{620 + xs.min()} (expect 638-639)")
# right edge: max non-white x over rows 211..330 in x850..892 (frame stroke at 893+)
sub = lum[211:331, 850:892]
ys, xs = np.where(sub < 240)
print(f"meme right edge (rows 211..330): x{850 + xs.max()} (expect 865-866)")
# top edge at col band x700..800
col = lum[195:230, 700:800].min(axis=1)
ys = np.where(col < 240)[0]
print(f"meme top edge: y{195 + ys.min()} (expect 211)")
# bottom edge: scan col band x638..650 (left of red card x690, below y333)
col = lum[320:375, 638:651].min(axis=1)
ys = np.where(col < 240)[0]
print(f"meme bottom edge (x638..650): y{320 + ys.max() if len(ys) else None} (expect ~345-351)")
# caption band check (bottom caption left of red card)
bb = ink_bbox(638, 320, 690, 352, thr=190)
print(f"bottom-caption sliver (x638..690, y320..352): {bb}")

# ---------- 5. cards ----------
sub = redish[330:478, 600:900]
ys, xs = np.where(sub)
print(f"red-card red-ink bbox: x{600+xs.min()}..{600+xs.max()} y{330+ys.min()}..{330+ys.max()}")
# blue card left/bottom: dark blue mask
bluem = (b > 90) & (r < 60) & (g < 80)
sub = bluem[370:478, 600:830]
ys, xs = np.where(sub)
print(f"blue-card ink bbox: x{600+xs.min()}..{600+xs.max()} y{370+ys.min()}..{370+ys.max()}")
# green mask
greenm = (g > 90) & (r < 80) & (b < 80)
sub = greenm[345:460, 640:860]
ys, xs = np.where(sub)
print(f"green-card ink bbox: x{640+xs.min()}..{640+xs.max()} y{345+ys.min()}..{345+ys.max()}")

# ---------- 6. cursor bbox (bright whites on card zone x765..795 y370..395) ----------
sub = a[370:396, 765:795]
m = (sub[:, :, 0] > 200) & (sub[:, :, 1] > 200) & (sub[:, :, 2] > 200)
ys, xs = np.where(m)
if len(ys):
    cur = (765 + xs.min(), 370 + ys.min(), 765 + xs.max(), 370 + ys.max())
    print(f"cursor bbox: {cur} (banked: 775..782, 378..385)")
else:
    cur = None
    print("cursor: none found")

# ---------- 7. black bottom bar ----------
row = lum[528, :]
dark = np.where(row < 80)[0]
print(f"black bar @y528: x{dark.min()}..{dark.max()}" if len(dark) else "no bar")
rows_bar = [y for y in range(505, 540) if (lum[y, 100:860] < 80).sum() > 500]
print(f"bar rows: {rows_bar[:3]}..{rows_bar[-3:] if rows_bar else None}")

# ---------- 8. font metric solve (body) ----------
FONTS = {
    "Carlito": "/usr/share/fonts/carlito/Carlito-Regular.ttf",
    "LiberationSans": "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
    "DejaVuSans": "/usr/share/fonts/TTF/DejaVuSans.ttf",
}
TEXTS = {
    "L1a": ("Images are 2-D", 11.5, 294 - 151 + 1),
    "L2a": ("k-D if you also count the extra channels", 10.0, 472 - 153 + 1),
    "L2b": ("RGB, hyperspectral, etc.", 10.0, 334 - 154 + 1),
    "L1b": ("What does a 2-D input really mean?", 12.0, 499 - 151 + 1),
    "L2c": ("Neighboring variables are locally correlated", 10.0, 512 - 154 + 1),
}
print("\n--- body font solve (size from cap height; charSpacing to hit advance) ---")
for fname, fpath in FONTS.items():
    f100 = ImageFont.truetype(fpath, 100)
    capr = f100.getbbox("H")[3] - f100.getbbox("H")[1]  # cap px @100
    out = []
    for k, (txt, capt, adv) in TEXTS.items():
        size = capt / (capr / 100.0)
        f = ImageFont.truetype(fpath, int(round(size * 4)))  # 4x for sub-px
        nat = f.getlength(txt) / 4.0
        cs = (adv - nat) / max(1, len(txt) - 1)
        out.append(f"{k}@{size:.1f} nat={nat:.0f} tgt={adv} cs={cs:+.2f}")
    print(f"{fname}: " + " | ".join(out))

# title check: LiberationSans-Bold
fb = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSans-Bold.ttf", 465)
adv = fb.getlength("Spatial Structure of Image") / 10.0
print(f"\ntitle LiberationSans-Bold @46.5pt advance={adv:.1f} (target 577)")

# ---------- 9. crops ----------
def crop_save(box, name):
    c = im.crop(box)
    c.save(f"{ASSETS}/{name}")
    print(f"{name}: box {box} -> {c.size[0]}x{c.size[1]} px ({c.size[0]/72:.4f}x{c.size[1]/72:.4f} in)")

# A: meme (above cards). rows 209..331 incl -> exclusive 332
crop_save((636, 209, 868, 332), "meme029.png")
# B: card stack (incl meme sliver + all 3 cards), cursor inpainted from below
B = im.crop((616, 332, 892, 474))
if cur:
    x0, y0, x1, y1 = cur
    # pad 1, coords relative to B's origin (616, 332)
    rx0, ry0, rx1, ry1 = x0 - 1 - 616, y0 - 1 - 332, x1 + 2 - 616, y1 + 2 - 332
    src = np.asarray(B).copy()
    hgt = ry1 - ry0
    # clone from hgt+2 rows below (still inside B: region y up to 474)
    for yy in range(ry0, ry1):
        sy = yy + hgt + 2
        if sy >= src.shape[0]:
            sy = src.shape[0] - 1
        src[yy, rx0:rx1] = src[sy, rx0:rx1]
    B = Image.fromarray(src)
    print(f"cursor inpainted in B: rel box ({rx0},{ry0},{rx1},{ry1}) cloned from +{hgt+2} rows")
B.save(f"{ASSETS}/cards029.png")
print(f"cards029.png: box (616,332,892,474) -> {B.size[0]}x{B.size[1]} px ({B.size[0]/72:.4f}x{B.size[1]/72:.4f} in)")
# C: close-up + 4 arrows. rows 389..478 incl -> exclusive 479 (frame stroke at 480)
crop_save((188, 389, 472, 479), "closeup029.png")

# zoomed evidence crops for the QA bank
im.crop((616, 332, 892, 474)).resize((552, 284)).save("/tmp/qa029_cards_orig.png")
Image.open(f"{ASSETS}/cards029.png").resize((552, 284)).save("/tmp/qa029_cards_inpaint.png")
print("evidence crops -> /tmp/qa029_cards_orig.png /tmp/qa029_cards_inpaint.png")
