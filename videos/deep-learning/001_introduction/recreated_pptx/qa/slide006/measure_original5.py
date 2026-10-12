#!/usr/bin/env python3
# measure_original5.py — original frame chrome structure, blue calibration vs certified 005.
from PIL import Image, ImageFont
import numpy as np

ORG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_006.jpg"
a = np.asarray(Image.open(ORG).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

print("== raw pixel samples ==")
for (x, y, lab) in [(20, 270, "far left mid"), (480, 20, "top center above red line"),
                    (480, 60, "between line and title"), (30, 30, "top-left corner"),
                    (940, 270, "far right mid"), (480, 530, "bottom center"), (930, 30, "top-right"),
                    (470, 43, "ON the red line"), (100, 43, "red line left"), (900, 43, "red line right")]:
    print(f"  ({x},{y}) {lab}: {tuple(a[y, x])}")

print("== red line at y42..45: exact extent per row (r-g>20) ==")
red_loose = (r - g > 20) & (r - b > 20) & (r > 100)
for y in range(40, 48):
    xs = np.where(red_loose[y, :])[0]
    if len(xs):
        print(f"  row {y}: x {xs.min()}..{xs.max()} n={len(xs)}")

print("== vertical structure: column x=470, y 0..140 colors every 4px ==")
col = a[0:140, 470]
for y in range(0, 140, 4):
    print(f"  y={y}: {tuple(col[y])}")

print("== is there a gray panel? sample corners/edges ==")
for (x, y) in [(5, 5), (955, 5), (5, 270), (955, 270), (5, 470), (955, 470), (480, 535), (100, 270), (860, 270)]:
    print(f"  ({x},{y}): {tuple(a[y, x])}")

print("== blue calibration: slide_005 (certified truth 000080) same analysis ==")
o5 = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_005.jpg").convert("RGB")).astype(int)
def blue_report(img, y0, y1, x0, x1, lab):
    rr, gg, bb = img[y0:y1, x0:x1, 0], img[y0:y1, x0:x1, 1], img[y0:y1, x0:x1, 2]
    core = (bb - rr > 50) & (bb - gg > 50)
    px = img[y0:y1, x0:x1][core]
    if not len(px):
        print(f"  {lab}: no core px")
        return
    sats = px[:, 2] - (px[:, 0] + px[:, 1]) / 2
    idx = np.argsort(-sats)[:200]
    print(f"  {lab}: n={len(px)} median {np.median(px, axis=0)} top200 {np.median(px[idx], axis=0)} maxB px {px[np.argmax(px[:, 2])]}")
blue_report(o5, 194, 390, 125, 900, "slide005 blue (truth 000080)")
blue_report(a, 197, 476, 204, 565, "slide006 blue")

print("== bullet-12 grays: top-20 darkest px ==")
reg = a[485:498, 200:345]
dk = reg.reshape(-1, 3)
mx = dk.max(axis=1)
idx = np.argsort(mx)[:20]
print("  darkest:", [tuple(int(v) for v in dk[i]) for i in idx[:10]])

print("== title: PIL-render calibration of density ==")
def render_density(font_path, size, text):
    f = ImageFont.truetype(font_path, size)
    im = Image.new("L", (int(f.getlength(text)) + 40, size * 2), 255)
    from PIL import ImageDraw
    d = ImageDraw.Draw(im)
    d.text((20, size // 2), text, font=f, fill=0)
    arr = np.asarray(im)
    ink = arr < 128
    return ink.sum() / f.getlength(text)

t = "Machine Learning in the real-world"
d45r = render_density("/usr/share/fonts/TTF/Arial.TTF", 45, t)
d42b = render_density("/usr/share/fonts/TTF/Arialbd.TTF", 42, t)
d43b = render_density("/usr/share/fonts/TTF/Arialbd.TTF", 43, t)
print(f"  PIL Arial45 regular density: {d45r:.2f}")
print(f"  PIL ArialB42 bold density: {d42b:.2f}  ArialB43: {d43b:.2f}")
# bullet calibration: b1 'Spam filtering' orig density 4.88
db1 = render_density("/usr/share/fonts/TTF/Arial.TTF", 17.5, "Spam filtering")
print(f"  PIL Arial17.5 'Spam filtering' density: {db1:.2f}  (orig 4.88 -> JPEG factor {4.88/db1:.2f})")
db2 = render_density("/usr/share/fonts/TTF/Arial.TTF", 17.5, " Machine Translation (e.g.,  Google Translate)")
print(f"  PIL Arial17.5 b2 density: {db2:.2f}  (orig 4.07 -> factor {4.07/db2:.2f})")
k = ((4.88 / db1) + (4.07 / db2)) / 2
print(f"  mean JPEG inflation k = {k:.2f}")
print(f"  orig title density 15.51 / k = {15.51/k:.2f} -> compare PIL: reg45 {d45r:.2f} vs bold42-43 {d42b:.2f}-{d43b:.2f}")
