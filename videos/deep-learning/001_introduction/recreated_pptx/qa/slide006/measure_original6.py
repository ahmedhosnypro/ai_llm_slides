#!/usr/bin/env python3
# measure_original6.py — final forensics: panel borders/extent, per-word title font test,
# blue pooled calibration vs 002 (0000AA) and 005 (000080), bullet density calibration.
from PIL import Image, ImageFont, ImageDraw
import numpy as np

ORG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_006.jpg"
a = np.asarray(Image.open(ORG).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

print("== panel gray extent: row y=270, gray mask (within 12 of (231,233,230)) ==")
row = a[270]
gray = (np.abs(row[:, 0] - 231) < 12) & (np.abs(row[:, 1] - 233) < 12) & (np.abs(row[:, 2] - 230) < 12)
xs = np.where(gray)[0]
print(f"  gray x extent: {xs.min()}..{xs.max()} (n={len(xs)})")
print("== column x=470 gray extent (y 46..540) ==")
col = a[:, 470]
grayc = (np.abs(col[:, 0] - 231) < 12) & (np.abs(col[:, 1] - 233) < 12) & (np.abs(col[:, 2] - 230) < 12)
ys = np.where(grayc)[0]
print(f"  gray y extent: {ys.min()}..{ys.max()}")
print("== left/right border columns: red_loose count per col x 50..70 and 890..910, y 50..500 ==")
red_loose = (r - g > 20) & (r - b > 20) & (r > 100)
for x in list(range(50, 70)) + list(range(890, 911)):
    c = int(red_loose[50:500, x].sum())
    if c > 60:
        print(f"  col {x}: {c}")
print("== border col sample colors ==")
print("  (57,270):", tuple(a[270, 57]), " (58,270):", tuple(a[270, 58]), " (901,270):", tuple(a[270, 901]), " (902,270):", tuple(a[270, 902]))

print("== per-word title advance test ==")
words = [("Machine", 167), ("Learning", 174), ("in", 35), ("the", 63), ("real-world", 198)]
cands = [("Arial45", "/usr/share/fonts/TTF/Arial.TTF", 45), ("Arial45.4", "/usr/share/fonts/TTF/Arial.TTF", 45.4),
         ("ArialB42", "/usr/share/fonts/TTF/Arialbd.TTF", 42), ("ArialB43", "/usr/share/fonts/TTF/Arialbd.TTF", 43),
         ("TimesB45", "/usr/share/fonts/TTF/Timesbd.TTF", 45), ("Times48.5", "/usr/share/fonts/TTF/Times.TTF", 48.5)]
print("  word       " + "  ".join(f"{n:>9}" for n, _, _ in cands) + "   target")
for w, tgt in words:
    row_s = f"  {w:<10}"
    for n, p, s in cands:
        f = ImageFont.truetype(p, int(round(s)))
        row_s += f"  {f.getlength(w):9.1f}"
    row_s += f"   {tgt}"
    print(row_s)

print("== stroke-width test: 'M' left stem width at mid-cap height ==")
# original title mid-row runs: first run (142,148) = 7px
red = (r > 110) & (r - g > 45) & (r - b > 35)
for y in [100, 104, 108]:
    xs = np.where(red[y, 140:320])[0]
    if len(xs):
        runs = []
        st = xs[0]; prev = xs[0]
        for x in xs[1:]:
            if x > prev + 1:
                runs.append((st + 140, prev + 140, prev - st + 1)); st = x
            prev = x
        runs.append((st + 140, prev + 140, prev - st + 1))
        print(f"  orig y={y}: {runs[:6]}")

def render_runs(font_path, size, y_frac):
    f = ImageFont.truetype(font_path, size)
    im = Image.new("L", (400, size * 2), 255)
    d = ImageDraw.Draw(im)
    d.text((20, 20), "Machine", font=f, fill=0)
    arr = np.asarray(im) < 128
    # find cap top and baseline of 'M'
    cols = np.where(arr.any(axis=0))[0]
    midy = int(20 + 0.716 * size * y_frac)
    xs = np.where(arr[midy])[0]
    runs = []
    if len(xs):
        st = xs[0]; prev = xs[0]
        for x in xs[1:]:
            if x > prev + 1:
                runs.append((prev - st + 1)); st = x
            prev = x
        runs.append(prev - st + 1)
    return runs

print("  PIL Arial45 M-runs @~0.75 cap:", render_runs("/usr/share/fonts/TTF/Arial.TTF", 45, 0.75))
print("  PIL ArialB42 M-runs @~0.75 cap:", render_runs("/usr/share/fonts/TTF/Arialbd.TTF", 42, 0.75))

print("== blue pooled 2x2-max calibration ==")
def pooled(img, y0, y1, x0, x1, lab):
    reg = img[y0:y1, x0:x1]
    rr, gg, bb = reg[:, :, 0], reg[:, :, 1], reg[:, :, 2]
    sat = bb - (rr + gg) / 2
    H, W = sat.shape
    H2, W2 = H // 2 * 2, W // 2 * 2
    s2 = sat[:H2, :W2].reshape(H2 // 2, 2, W2 // 2, 2)
    idx = np.argmax(s2.reshape(H2 // 2, W2 // 2, 4), axis=2)
    picks = reg[:H2:2, :W2:2].reshape(-1, 3)
    flat = idx.reshape(-1)
    picked = []
    for i in range(H2 // 2):
        for j in range(W2 // 2):
            dy, dx = divmod(int(flat[i * (W2 // 2) + j]), 2)
            picked.append(reg[i * 2 + dy, j * 2 + dx])
    picked = np.array(picked)
    s2v = picked[:, 2] - (picked[:, 0] + picked[:, 1]) / 2
    top = picked[np.argsort(-s2v)[:150]]
    print(f"  {lab}: pooled median {np.median(picked, axis=0)} top150 {np.median(top, axis=0)}")
o5 = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_005.jpg").convert("RGB")).astype(int)
o2 = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_002.jpg").convert("RGB")).astype(int)
pooled(o5, 194, 390, 125, 900, "005 truth 000080")
pooled(o2, 180, 420, 130, 860, "002 truth 0000AA")
pooled(a, 197, 476, 204, 565, "006 ?")

print("== bullet density calibration (fixed int) ==")
def render_density(font_path, size, text):
    f = ImageFont.truetype(font_path, int(round(size)))
    im = Image.new("L", (int(f.getlength(text)) + 40, int(size) * 2), 255)
    d = ImageDraw.Draw(im)
    d.text((20, int(size) // 2), text, font=f, fill=0)
    arr = np.asarray(im)
    return (arr < 128).sum() / f.getlength(text)

db1 = render_density("/usr/share/fonts/TTF/Arial.TTF", 17.5, "Spam filtering")
db2 = render_density("/usr/share/fonts/TTF/Arial.TTF", 17.5, " Machine Translation (e.g.,  Google Translate)")
print(f"  PIL b1 {db1:.2f} (orig 4.88 -> k {4.88/db1:.2f}); PIL b2 {db2:.2f} (orig 4.07 -> k {4.07/db2:.2f})")
k = (4.88 / db1 + 4.07 / db2) / 2
print(f"  k={k:.2f}; title orig 15.51/k = {15.51/k:.2f} vs PIL reg45 9.69 / bold42 11.61 / bold43 12.34")
