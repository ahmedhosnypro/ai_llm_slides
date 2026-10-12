#!/usr/bin/env python3
"""measure_original6.py — pass 6: ink-based font fits with CORRECT font paths,
panel fill/border, underline core, caption L1 word check, crop-box sanity."""
import numpy as np
from PIL import Image, ImageFont, ImageDraw

FR = "videos/deep-learning/001_introduction/unique_slides/slide_035.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)

CAND = {
    "Arial": "/usr/share/fonts/truetype/msttcorefonts/Arial.TTF",
    "Arialbd": "/usr/share/fonts/truetype/msttcorefonts/Arialbd.TTF",
    "Ariali": "/usr/share/fonts/truetype/msttcorefonts/Ariali.TTF",
    "Arialbi": "/usr/share/fonts/truetype/msttcorefonts/Arialbi.TTF",
    "Verdana": "/usr/share/fonts/TTF/Verdana.TTF",
    "Verdanab": "/usr/share/fonts/TTF/Verdanab.TTF",
    "Verdanai": "/usr/share/fonts/TTF/Verdanai.TTF",
    "Verdanaz": "/usr/share/fonts/TTF/Verdanaz.TTF",
    "Tahoma": "/usr/share/fonts/TTF/Tahoma.TTF",
    "Tahomabd": "/usr/share/fonts/TTF/Tahomabd.TTF",
    "Calibri": "/usr/share/fonts/truetype/msttcorefonts/calibri.ttf",
    "Calibrib": "/usr/share/fonts/truetype/msttcorefonts/calibrib.ttf",
    "Calibrii": "/usr/share/fonts/truetype/msttcorefonts/calibrii.ttf",
    "Calibriz": "/usr/share/fonts/truetype/msttcorefonts/calibriz.ttf",
    "Timesbd": "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman_Bold.TTF",
    "Trebuchetbd": "/usr/share/fonts/truetype/msttcorefonts/trebucbd.ttf",
}
import os
for k in list(CAND):
    if not os.path.exists(CAND[k]):
        print(f"MISSING {k}: {CAND[k]}")
        del CAND[k]

def ink_render(font, text):
    """Render text, return ink mask + bbox."""
    W = int(font.getlength(text)) + 40
    H = int(font.size * 3) + 40
    img = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(img)
    d.text((20, 20), text, font=font, fill=0)
    arr = np.asarray(img)
    ink = arr < 128
    ys, xs = np.where(ink)
    if len(xs) == 0:
        return None, None, None
    return ink, xs.min(), (xs.max() - xs.min() + 1, ys.max() - ys.min() + 1, ys.min())

def fit_ink(fname, text, target_w, target_h, lo=8.0, hi=60.0):
    """Find size where INK width matches target_w; report ink h too."""
    p = CAND[fname]
    best = None
    s = lo
    while s <= hi:
        f = ImageFont.truetype(p, int(round(s)))
        _, _, wh = ink_render(f, text)
        if wh:
            err = abs(wh[0] - target_w)
            if best is None or err < best[0]:
                best = (err, s, wh[0], wh[1])
        s += 0.5
    return best

print("=== Q1. TITLE ink-based fit (target ink w=448, h=30 caps+desc; caps 23) ===")
T = "How to Apply Filter on image"
for fn in ["Arialbd", "Verdanab", "Tahomabd", "Timesbd", "Calibrib"]:
    if fn not in CAND: continue
    r = fit_ink(fn, T, 448, 30)
    print(f"  {fn}: best size={r[1]:.1f} ink={r[2]}x{r[3]} (err {r[0]:.1f})")
print("  word-position check at candidate sizes (target: How@0 w68, to@78 w29, Apply@118 w88, Filter@217 w79, on@306 w38, image@357 w91; ink span 448):")
targets = [("How", 0, 68), ("to", 78, 29), ("Apply", 118, 88), ("Filter", 217, 79), ("on", 306, 38), ("image", 357, 91)]
for fn, size in [("Verdanab", 31.5), ("Verdanab", 31.0), ("Arialbd", 33.0), ("Tahomabd", 32.0)]:
    f = ImageFont.truetype(CAND[fn], int(round(size)))
    # measure cumulative word ink offsets by rendering prefix+word
    out = []
    xcur = 0
    for i, (w, tpos, tw) in enumerate(targets):
        pre = " ".join(x[0] for x in targets[:i])
        adv_pre = f.getlength(pre + (" " if i else ""))
        ink_w = f.getlength(w)
        out.append(f"{w}: advstart={adv_pre:.0f} ink={ink_w:.0f}(t{tw})")
    print(f"  {fn}@{size}: " + " | ".join(out))

print("=== Q2. LABELS ink fit: 'Image' t79x24(cap18,g desc), 'Filter' t66x20(cap19) ===")
for fn in ["Verdanab", "Arialbd", "Tahomabd", "Calibrib"]:
    r1 = fit_ink(fn, "Image", 79, 24)
    r2 = fit_ink(fn, "Filter", 66, 20)
    print(f"  {fn}: Image size={r1[1]:.1f} ink={r1[2]}x{r1[3]} | Filter size={r2[1]:.1f} ink={r2[2]}x{r2[3]}")

print("=== Q3. CAPTION L1 ink fit (target ink w=804, h=28 asc+desc; cap17) ===")
L1 = "Apply Filter on Image is a Dot product between image values and filter values"
for fn in ["Ariali", "Verdanai", "Calibrii", "Arial", "Verdana"]:
    r = fit_ink(fn, L1, 804, 28)
    print(f"  {fn}: size={r[1]:.1f} ink={r[2]}x{r[3]}")
print("  L1 word check (target word starts rel x78: Apply0 w59, Filter66 w51, on124 w25, Image157 w64, is228 w17, a252 w12, Dot272 w37, product314 w80, between400 w88, image495 w64, values566 w67, and640 w40, filter686 w44, values738 w66):")
L1w = [("Apply", 0, 59), ("Filter", 66, 51), ("on", 124, 25), ("Image", 157, 64), ("is", 228, 17), ("a", 252, 12), ("Dot", 272, 37), ("product", 314, 80), ("between", 400, 88), ("image", 495, 64), ("values", 566, 67), ("and", 640, 40), ("filter", 686, 44), ("values", 738, 66)]
for fn, size in [("Ariali", 25.0), ("Ariali", 25.5), ("Verdanai", 22.0)]:
    f = ImageFont.truetype(CAND[fn], int(round(size)))
    pos = []
    for i, (w, tpos, tw) in enumerate(L1w):
        pre = " ".join(x[0] for x in L1w[:i])
        adv = f.getlength(pre + (" " if i else ""))
        pos.append(f"{w}@{adv:.0f}({tpos})")
    print(f"  {fn}@{size}: " + " ".join(pos))

print("=== Q4. CAPTION L2 pieces: '(can' t40, 'modeled' t97, 'by' t28, 'PERCEPTRON' t163 cap17, bold-italic ===")
for fn in ["Arialbi", "Verdanaz", "Calibriz"]:
    for txt, tw in [("(can", 40), ("modeled", 97), ("by", 28), ("PERCEPTRON", 163)]:
        r = fit_ink(fn, txt, tw, 20)
        print(f"  {fn} '{txt}': size={r[1]:.1f} ink={r[2]}x{r[3]}")
    # regular italic too
for fn in ["Ariali", "Verdanai"]:
    r = fit_ink(fn, "PERCEPTRON", 163, 20)
    print(f"  {fn} 'PERCEPTRON' (regular italic): size={r[1]:.1f} ink={r[2]}x{r[3]}")

print("=== Q5. FILTER DIGITS: '0' ink 10x11, '1' ink 7x11 (cap 11) ===")
for fn in ["Calibrib", "Arialbd", "Verdanab", "Tahomabd", "Trebuchetbd"]:
    if fn not in CAND: continue
    for sz in [15, 16, 17, 18]:
        f = ImageFont.truetype(CAND[fn], sz)
        _, _, w0 = ink_render(f, "0")
        _, _, w1 = ink_render(f, "1")
        print(f"  {fn} {sz}: '0' {w0[0]}x{w0[1]} | '1' {w1[0]}x{w1[1]}")

print("=== Q6. PANEL fill + border color ===")
print("  panel fill samples (empty areas):")
for (x, y) in [(390, 300), (392, 400), (878, 300), (880, 200), (500, 180), (600, 175), (450, 425), (700, 430), (860, 420), (385, 250)]:
    r, g, b = a[y, x]
    print(f"    ({x},{y}) #{r:02X}{g:02X}{b:02X}")
print("  panel border samples:")
for (x, y) in [(380, 300), (886, 300), (500, 168), (500, 169), (500, 431), (500, 432), (600, 168)]:
    r, g, b = a[y, x]
    print(f"    ({x},{y}) #{r:02X}{g:02X}{b:02X}")
print("  underline core (y499..501, x330..460):")
reg = a[499:502, 330:460].reshape(-1, 3)
lum = reg.sum(axis=1)
idx = np.argsort(lum)[: max(1, int(len(lum) * 0.3))]
core = np.median(reg[idx], axis=0).astype(int)
print(f"    core: {tuple(core)} #{core[0]:02X}{core[1]:02X}{core[2]:02X}")
print("  line2 'modeled' core (y483..497, x173..269):")
reg = a[483:497, 173:269].reshape(-1, 3)
rr = reg[:, 0]
mask = rr < 190
if mask.any():
    core = np.median(reg[mask], axis=0).astype(int)
    print(f"    core: {tuple(core)} #{core[0]:02X}{core[1]:02X}{core[2]:02X}")

print("=== Q7. CROP-BOX SANITY: edges of proposed crops ===")
print("  left-grid crop x77..243 y207..337 — edge strips (should be border/AA/panel-gray only):")
for (x0, x1, y0, y1, lab) in [(77, 243, 205, 208, "top edge"), (77, 243, 336, 339, "bottom edge"),
                               (75, 78, 207, 337, "left edge"), (242, 245, 207, 337, "right edge")]:
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    med = np.median(reg, axis=0).astype(int)
    mx = reg.sum(axis=1).max()
    print(f"    {lab}: median #{med[0]:02X}{med[1]:02X}{med[2]:02X} maxlum {mx}")
print("  panel-content crop x398..875 y185..420 — edge strips:")
for (x0, x1, y0, y1, lab) in [(398, 875, 182, 186, "top"), (398, 875, 419, 423, "bottom"),
                               (395, 399, 185, 420, "left"), (874, 878, 185, 420, "right")]:
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    med = np.median(reg, axis=0).astype(int)
    dark = (reg.sum(axis=1) < 400).sum()
    print(f"    {lab}: median #{med[0]:02X}{med[1]:02X}{med[2]:02X} dark-px {dark}")
print("  cursor zone content check x715..760 y360..395 (ink classes):")
sub = a[360:395, 715:760]
rr, gg, bb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
nonwhite = (rr < 240) | (gg < 240) | (bb < 235)
ys, xs = np.where(nonwhite)
if len(xs):
    print(f"    nonwhite n={len(xs)} bbox x{xs.min()+715}..{xs.max()+715} y{ys.min()+360}..{ys.max()+360}")
    dk = (rr < 180)
    if dk.any():
        ys2, xs2 = np.where(dk)
        print(f"    dark n={dk.sum()} bbox x{xs2.min()+715}..{xs2.max()+715} y{ys2.min()+360}..{ys2.max()+360}")

print("=== Q8. CHROME check: original panel top border faint red at y44? full-width? ===")
red2 = (a[:, :, 0] - a[:, :, 1] > 25) & (a[:, :, 0] - a[:, :, 2] > 25)
for y in [43, 44, 45, 46]:
    xs = np.where(red2[y, :])[0]
    if len(xs):
        print(f"  y={y}: n={len(xs)} x{xs.min()}..{xs.max()}")
    else:
        print(f"  y={y}: none")
