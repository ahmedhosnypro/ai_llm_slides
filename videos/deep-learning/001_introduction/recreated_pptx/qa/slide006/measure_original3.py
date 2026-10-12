#!/usr/bin/env python3
# measure_original3.py — font metric solve (real Arial/Times TTFs), underline detection,
# bullet-12 color, bullet-dot color, box right edge with loose red.
from PIL import Image, ImageFont
import numpy as np

ORG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_006.jpg"
a = np.asarray(Image.open(ORG).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

FONTS = {
    "Arial": "/usr/share/fonts/TTF/Arial.TTF",
    "ArialB": "/usr/share/fonts/TTF/Arialbd.TTF",
    "Times": "/usr/share/fonts/TTF/Times.TTF",
    "TimesB": "/usr/share/fonts/TTF/Timesbd.TTF",
}
_cache = {}
def fnt(name, size):
    k = (name, round(size, 2))
    if k not in _cache:
        _cache[k] = ImageFont.truetype(FONTS[name], int(round(size)))
    return _cache[k]

def adv(name, size, text):
    return fnt(name, size).getlength(text)

def ink_span(name, size, text):
    # cap-top..desc-bottom span at this size (approx via 'M' top and 'g' bottom bearings)
    fo = fnt(name, size)
    bbox = fo.getbbox("Mg")  # (l,t,r,b) relative to origin at ascender line
    return bbox[3] - bbox[1]

def solve(text, target_adv, target_span, fonts, lo=8, hi=80):
    out = []
    for name in fonts:
        # size from advance
        s1 = target_adv / adv(name, 40, text) * 40
        # size from span
        fo = fnt(name, 40)
        bb = fo.getbbox("Mg")
        span40 = bb[3] - bb[1]
        s2 = target_span / span40 * 40
        out.append((name, round(s1, 2), round(s2, 2)))
    return out

print("== title solve: 'Machine Learning in the real-world' target adv 692, span(cap M..g) 42 ==")
for name, s1, s2 in solve("Machine Learning in the real-world", 692, 42, ["Arial", "ArialB", "Times", "TimesB"]):
    print(f"  {name}: size_by_adv={s1} size_by_span={s2}")

print("== header L1 solve (bold phrase + regular rest treated full regular then full bold) ==")
L1 = "Broadly applicable in many domains (e.g., finance, robotics,"
L2 = "bioinformatics, vision, natural language, etc.). Some applications:"
for name, s1, s2 in solve(L1, 600, 22, ["Arial", "Times"]):
    print(f"  L1 {name}: size_by_adv={s1} size_by_span={s2}")
for name, s1, s2 in solve(L2, 626, 21, ["Arial", "Times"]):
    print(f"  L2 {name}: size_by_adv={s1} size_by_span={s2}")

print("== bullets solve ==")
B1 = "Spam filtering"
B2 = " Machine Translation (e.g.,  Google Translate)"
B11 = "Webpage clustering (e.g., Google News)"
B12 = ".. and many more"
for nm, txt, tgt in [("b1", B1, 107), ("b2", B2, 353), ("b11", B11, 319), ("b12", B12, 136)]:
    for name in ["Arial", "Times"]:
        s1 = tgt / adv(name, 40, txt) * 40
        print(f"  {nm} {name}: size_by_adv={s1:.2f}  (adv@17={adv(name,17,txt):.1f} adv@18={adv(name,18,txt):.1f})")

print("== mixed-weight header check: line1 = TimesB phrase + Times rest, at candidate sizes ==")
PHRASE = "Broadly applicable in many domains"
REST1 = " (e.g., finance, robotics,"
for s in [18, 19, 20, 21, 22, 23, 24]:
    tot = adv("TimesB", s, PHRASE) + adv("Times", s, REST1)
    print(f"  size {s}: phrase {adv('TimesB',s,PHRASE):.1f} + rest {adv('Times',s,REST1):.1f} = {tot:.1f} (target 600)")
    tot2 = adv("Times", s, L2)
    print(f"           L2 regular {tot2:.1f} (target 626)")

print("== underline: contiguous dark runs y 154..168 ==")
strict = a.max(axis=2) < 100
for y in range(154, 169):
    row = strict[y, 91:880]
    runs = []
    inr = False
    for i, v in enumerate(row):
        if v and not inr:
            st = i; inr = True
        elif not v and inr:
            if i - st > 100:
                runs.append((st + 91, i - 1 + 91, i - st))
            inr = False
    if inr and len(row) - st > 100:
        runs.append((st + 91, len(row) - 1 + 91, len(row) - st))
    if runs:
        print(f"  y={y}: {runs}")

print("== bullet12 color: pixels y 485..497 x 190..345, loose blue or dark ==")
reg = a[485:498, 190:345]
rr, gg, bb2 = reg[:, :, 0], reg[:, :, 1], reg[:, :, 2]
bluish = (bb2 - rr > 30) & (bb2 - gg > 30)
darkish = reg.max(axis=2) < 110
print("  n bluish:", int(bluish.sum()), "n darkish:", int(darkish.sum()))
if bluish.sum():
    print("  bluish median:", np.median(reg[bluish], axis=0))
if darkish.sum():
    vals, counts = np.unique(reg[darkish].reshape(-1, 3), axis=0, return_counts=True)
    order = np.argsort(-counts)[:3]
    print("  darkish modes:", [(tuple(int(v) for v in vals[i]), int(counts[i])) for i in order])
# dot color
dot = a[488:495, 179:186]
print("  dot12 pixels min:", dot.reshape(-1,3).min(axis=0), "median dark:", np.median(dot[dot.max(axis=2)<120], axis=0) if (dot.max(axis=2)<120).sum() else None)

print("== bullet dot color (dots 1-11) ==")
d1 = a[201:206, 180:185]
dm = d1[d1.max(axis=2) < 120]
print("  dot1 dark px median:", np.median(dm, axis=0) if len(dm) else None, "n:", len(dm))

print("== box right edge: loose red columns x 855..905, y 140..500 ==")
red_loose = (r - g > 25) & (r - b > 25) & (r > 110)
for x in range(855, 906):
    c = red_loose[140:500, x].sum()
    if c > 50:
        print(f"  col {x}: {c}")
print("== border row 133 exact extent (loose red) ==")
xs = np.where(red_loose[133, 0:960])[0]
print("  row133 red x:", xs.min(), "..", xs.max())
xs = np.where(red_loose[503, 0:960])[0]
print("  row503 red x:", xs.min(), "..", xs.max())
print("== left border col 88 extent (loose red) ==")
ys = np.where(red_loose[0:540, 88])[0]
print("  col88 red y:", ys.min(), "..", ys.max())

print("== title per-word segmentation (red col profile y 84..125) ==")
red = (r > 110) & (r - g > 45) & (r - b > 35)
cols = red[84:126, 100:900].sum(axis=0)
words = []
inw = False
gap = 0
for i, v in enumerate(cols):
    if v > 0:
        if not inw:
            st = i; inw = True
        gap = 0
    else:
        if inw:
            gap += 1
            if gap > 8:  # word gap ~ space width
                words.append((st + 100, i - gap + 100)); inw = False
if inw:
    words.append((st + 100, len(cols) - 1 + 100))
print("  word runs:", words)
print("  word advances:", [w1 - w0 + 1 for w0, w1 in words])
