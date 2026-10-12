#!/usr/bin/env python3
"""measure_original5.py — pass 5: caption forensics, label metrics, filter borders,
left r1c2 glyph, PIL font fits."""
import numpy as np
from PIL import Image, ImageFont

FR = "videos/deep-learning/001_introduction/unique_slides/slide_035.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

print("=== P1. CAPTION BOX borders: loose blue mask, exact extents ===")
looseblue = (B - R > 10) & (B - G > 5) & (B > 110)
for y in [445, 446, 447, 506, 507, 508]:
    xs = np.where(looseblue[y, 30:930])[0]
    if len(xs):
        print(f"  y={y}: x{xs.min()+30}..{xs.max()+30} n={len(xs)}")
for x in [62, 63, 64, 65, 66, 67, 68, 884, 885, 886, 887, 888, 889, 890]:
    ys = np.where(looseblue[440:512, x])[0]
    if len(ys) > 5:
        print(f"  col x={x}: n={len(ys)} y{ys.min()+440}..{ys.max()+440}")
print("border color samples:")
for (x, y) in [(200, 446), (400, 446), (600, 446), (200, 507), (500, 507), (800, 507)]:
    r, g, b = a[y, x]
    print(f"  ({x},{y}) #{r:02X}{g:02X}{b:02X} ({r},{g},{b})")
print("fill modal (x300..800, y474..478 + y448..456):")
reg = np.concatenate([a[448:457, 300:800].reshape(-1, 3), a[473:479, 300:800].reshape(-1, 3),
                      a[482:498, 520:860].reshape(-1, 3)])
med = np.median(reg, axis=0).astype(int)
print("  fill median:", tuple(med), f"#{med[0]:02X}{med[1]:02X}{med[2]:02X}")

print("=== P2. LINE 1 core color (darkest 15% of text ink) ===")
reg = a[450:478, 70:890]
rr, gg, bb = reg[:, :, 0], reg[:, :, 1], reg[:, :, 2]
ink = (bb - rr > 15) & (bb > 70)
ys, xs = np.where(ink)
vals = reg[ys, xs]
lum = vals.sum(axis=1)
idx = np.argsort(lum)[: max(1, int(len(lum) * 0.15))]
core = np.median(vals[idx], axis=0).astype(int)
print(f"  line1 ink n={len(ys)}, core(15% darkest): {tuple(core)} #{core[0]:02X}{core[1]:02X}{core[2]:02X}")

print("=== P3. LINE 2 core color + '(' color + ')' check ===")
reg = a[478:505, 85:500]
rr, gg, bb = reg[:, :, 0], reg[:, :, 1], reg[:, :, 2]
ink = (rr - gg > 40) & (rr > 90)
ys, xs = np.where(ink)
vals = reg[ys, xs]
lum = vals.sum(axis=1)
idx = np.argsort(lum)[: max(1, int(len(lum) * 0.15))]
core = np.median(vals[idx], axis=0).astype(int)
print(f"  line2 red n={len(ys)}, core: {tuple(core)} #{core[0]:02X}{core[1]:02X}{core[2]:02X}")
print("  '(' zone x84..93 samples:")
for y in range(482, 500, 3):
    r, g, b = a[y, 87]
    print(f"    (87,{y}) #{r:02X}{g:02X}{b:02X}")
print("  after PERCEPTRON x480..520, y480..505 — any ink?")
zz = (np.abs(a[:, :, 2] - a[:, :, 0]) > 12) | (a[:, :, 0] < 150)
sub = zz[478:506, 480:530]
ys, xs = np.where(sub)
if len(xs):
    print(f"    ink bbox x{xs.min()+480}..{xs.max()+480} y{ys.min()+478}..{ys.max()+478} n={len(xs)}")
    for (x, y) in [(x, y) for x in range(482, 525, 6) for y in (485, 490, 495, 500)]:
        r, g, b = a[y, x]
        if r < 200 or abs(r - b) > 15:
            print(f"      ({x},{y}) #{r:02X}{g:02X}{b:02X}")
else:
    print("    NO ink after x480 in line2 band")

print("=== P4. LINE 1/2 vertical metrics ===")
reg = a[440:480, 70:890]
rr, gg, bb = reg[:, :, 0], reg[:, :, 1], reg[:, :, 2]
ink = (bb - rr > 15) & (bb > 70)
rowc = ink.sum(axis=1)
print("  line1 row counts y440+i:")
for i, c in enumerate(rowc):
    if c > 3:
        print(f"    y{440+i}: {c}")
reg = a[476:510, 85:500]
rr, gg, bb = reg[:, :, 0], reg[:, :, 1], reg[:, :, 2]
ink2 = (rr - gg > 40) & (rr > 90)
rowc = ink2.sum(axis=1)
print("  line2 row counts:")
for i, c in enumerate(rowc):
    if c > 3:
        print(f"    y{476+i}: {c}")

print("=== P5. LABELS per-glyph tops/bottoms ===")
darkl = (R < 110) & (G < 110) & (B < 110)
for (x0, x1, lab) in [(100, 190, "Image"), (270, 345, "Filter")]:
    print(f"  {lab}:")
    for x in range(x0, x1):
        col = np.where(darkl[170:215, x])[0]
        if len(col):
            print(f"    x={x}: y{col.min()+170}..{col.max()+170}")

print("=== P6. FILTER GRID: rows, outer border, border core ===")
print("  vertical strip x=285 (through c1), y210..300:")
prev = None
for y in range(210, 300):
    r, g, b = a[y, 285]
    key = (r // 30, g // 30, b // 30)
    if key != prev:
        print(f"    y{y}: #{r:02X}{g:02X}{b:02X} ({r},{g},{b})")
        prev = key
print("  horizontal strip y=255 (through r2), x260..380:")
prev = None
for x in range(260, 380):
    r, g, b = a[255, x]
    key = (r // 30, g // 30, b // 30)
    if key != prev:
        print(f"    x{x}: #{r:02X}{g:02X}{b:02X} ({r},{g},{b})")
        prev = key
print("  border core (darkest 15% of separator zone x296..306 y220..290):")
reg = a[222:288, 297:305].reshape(-1, 3)
lum = reg.sum(axis=1)
idx = np.argsort(lum)[: max(1, int(len(lum) * 0.15))]
core = np.median(reg[idx], axis=0).astype(int)
print(f"    core: {tuple(core)} #{core[0]:02X}{core[1]:02X}{core[2]:02X}")

print("=== P7. LEFT GRID r1c2 glyph ASCII (x108..145 y210..236, darkish) ===")
for y in range(210, 237):
    row = ""
    for x in range(108, 146):
        r, g, b = a[y, x]
        if r < 140 and g < 200 and g - r > 30:
            row += "#"
        elif g - r > 20:
            row += "+"
        else:
            row += "."
    print(f"  y{y}: {row}")

print("=== P8. FILTER r1 digits ASCII (x271..364 y222..240) ===")
for y in range(222, 241):
    row = ""
    for x in range(271, 364):
        r, g, b = a[y, x]
        row += "#" if (r < 120 and g < 120 and b < 120) else ("+" if r < 180 else ".")
    print(f"  y{y}: {row}")

print("=== P9. FONT FITS (PIL, 1pt=1px at 72dpi) ===")
FONTS = {
    "Arial": "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf",
    "Arialbd": "/usr/share/fonts/truetype/msttcorefonts/Arialbd.ttf",
    "Ariali": "/usr/share/fonts/truetype/msttcorefonts/Ariali.ttf",
    "Arialbi": "/usr/share/fonts/truetype/msttcorefonts/Arialbi.ttf",
    "Verdana": "/usr/share/fonts/TTF/Verdana.TTF",
    "Verdanab": "/usr/share/fonts/TTF/Verdanab.TTF",
    "Verdanai": "/usr/share/fonts/TTF/Verdanai.TTF",
    "Verdanaz": "/usr/share/fonts/TTF/Verdanaz.TTF",
    "Tahoma": "/usr/share/fonts/TTF/Tahoma.TTF",
    "Tahomabd": "/usr/share/fonts/TTF/Tahomabd.TTF",
    "Times": "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf",
    "Timesbd": "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman_Bold.ttf",
}
import os
for k, p in list(FONTS.items()):
    if not os.path.exists(p):
        alt = p.replace("/usr/share/fonts/truetype/msttcorefonts/", "/usr/share/fonts/TTF/").replace("Times_New_Roman_Bold", "timesbd").replace("Times_New_Roman", "times")
        alts = [p, alt, p.replace("_", "")]
        found = None
        for cand in alts:
            if os.path.exists(cand):
                found = cand; break
        if not found:
            import glob
            g = glob.glob("/usr/share/fonts/**/*imes*", recursive=True) + glob.glob("/usr/share/fonts/**/Times*", recursive=True)
            found = g[0] if g else None
        FONTS[k] = found
        print(f"  font {k}: {found}")

def fit(fname, text, target_adv, target_cap, lo=10, hi=60):
    p = FONTS.get(fname)
    if not p: return None
    best = None
    for size10 in range(lo * 10, hi * 10):
        size = size10 / 10.0
        f = ImageFont.truetype(p, int(round(size)))
        adv = f.getlength(text)
        bb2 = f.getbbox("H")
        cap = bb2[3] - bb2[1]
        err = abs(adv - target_adv) / max(target_adv, 1) + abs(cap - target_cap) / max(target_cap, 1)
        if best is None or err < best[0]:
            best = (err, size, adv, cap)
    return best

print("  TITLE 'How to Apply Filter on image' target adv=448 cap=23:")
for fn in ["Arialbd", "Verdanab", "Tahomabd", "Timesbd"]:
    r = fit(fn, "How to Apply Filter on image", 448, 23)
    if r: print(f"    {fn}: err={r[0]:.3f} size={r[1]:.1f} adv={r[2]:.1f} cap={r[3]}")
print("  TITLE word-level check at fitted sizes (Arialbd):")
for sz in [31, 31.5, 32, 32.5, 33]:
    f = ImageFont.truetype(FONTS["Arialbd"], int(round(sz)))
    for w in ["How", "to", "Apply", "Filter", "on", "image"]:
        pass
    print(f"    size {sz}: adv={f.getlength('How to Apply Filter on image'):.1f} (target 448), How={f.getlength('How'):.1f} (67), Apply={f.getlength('Apply'):.1f} (88), image={f.getlength('image'):.1f} (91)")
print("  LABEL 'Image' target adv=79 cap=15; 'Filter' adv=66 cap=16:")
for fn in ["Arialbd", "Verdanab", "Tahomabd"]:
    r1 = fit(fn, "Image", 79, 15)
    r2 = fit(fn, "Filter", 66, 16)
    if r1 and r2: print(f"    {fn}: Image err={r1[0]:.3f} size={r1[1]:.1f} | Filter err={r2[0]:.3f} size={r2[1]:.1f}")
print("  CAPTION L1 'Apply Filter on Image is a Dot product between image values and filter values' target adv=804 cap=20:")
L1 = "Apply Filter on Image is a Dot product between image values and filter values"
for fn in ["Ariali", "Verdanai", "Arial", "Verdana"]:
    r = fit(fn, L1, 804, 20)
    if r: print(f"    {fn}: err={r[0]:.3f} size={r[1]:.1f} adv={r[2]:.1f} cap={r[3]}")
print("  CAPTION L2 '(can be modeled  by PERCEPTRON )' pieces: '(can be modeled  by ' adv target=388-163=225? Let: '(can' w=40 '(92..131)', PERCEPTRON w=163 cap=17:")
for fn in ["Arialbi", "Verdanaz", "Arialbd", "Verdanab"]:
    f15 = None
    r = fit(fn, "PERCEPTRON", 163, 17)
    if r: print(f"    {fn}: PERCEPTRON err={r[0]:.3f} size={r[1]:.1f} adv={r[2]:.1f} cap={r[3]}")
print("  FILTER DIGITS '0' ink 10 cap 11 / '1' ink 6 cap 11:")
for fn in ["Arialbd", "Verdanab", "Tahomabd"]:
    for sz in [14, 15, 16, 17]:
        f = ImageFont.truetype(FONTS[fn], sz)
        b0 = f.getbbox("0"); b1 = f.getbbox("1")
        print(f"    {fn} {sz}pt: '0' ink w={b0[2]-b0[0]} h={b0[3]-b0[1]} | '1' ink w={b1[2]-b1[0]} h={b1[3]-b1[1]}")
