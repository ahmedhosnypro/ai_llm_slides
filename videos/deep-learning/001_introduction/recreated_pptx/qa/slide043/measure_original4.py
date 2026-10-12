#!/usr/bin/env python3
"""Fourth forensics pass: correct font fingerprinting (Times/Georgia/Comic present),
slice profiles for the 3x3 grid / 18-cell / arrows, border stroke colors, blue-box
border color, title/navy/bullet/label font+size solving."""
import numpy as np
from PIL import Image, ImageFont
import os

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_043.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

def modal(x0, x1, y0, y1, label, n=4):
    reg = IM[y0:y1+1, x0:x1+1].reshape(-1, 3)
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    top = vals[np.argsort(-counts)[:n]]
    cnts = np.sort(counts)[::-1][:n]
    print(f"{label}: modal {['#%02X%02X%02X' % tuple(v) for v in top]} counts {list(cnts)}")

def darkest_modal(x0, x1, y0, y1, label):
    reg = IM[y0:y1+1, x0:x1+1].reshape(-1, 3)
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    order = np.argsort(-counts)
    lum = vals.sum(axis=1)
    cand = [(counts[i], lum[i], tuple(vals[i])) for i in order if counts[i] >= 3]
    cand.sort(key=lambda t: t[1])
    print(f"{label}: darkest modal {['#%02X%02X%02X (n=%d)' % (t[2][0], t[2][1], t[2][2], t[0]) for t in cand[:4]]}")

# ---------- slice profiles ----------
def slice_h(y, x0, x1, label, step=1):
    row = IM[y, x0:x1+1]
    # compact: mark transitions
    s = []
    prev = None
    for i, p in enumerate(row):
        c = '#%02X%02X%02X' % tuple(p)
        lum = int(p.sum())
        tag = 'K' if lum < 240 else ('D' if lum < 480 else ('M' if lum < 640 else ('Y' if p[2] < 120 and p[0] > 200 else 'W')))
        if tag != prev:
            s.append(f"{x0+i}:{tag}")
            prev = tag
    print(f"{label} y={y}: " + " ".join(s[:80]))

def slice_v(x, y0, y1, label):
    col = IM[y0:y1+1, x]
    s = []
    prev = None
    for i, p in enumerate(col):
        lum = int(p.sum())
        tag = 'K' if lum < 240 else ('D' if lum < 480 else ('M' if lum < 640 else ('Y' if p[2] < 120 and p[0] > 200 else 'W')))
        if tag != prev:
            s.append(f"{y0+i}:{tag}")
            prev = tag
    print(f"{label} x={x}: " + " ".join(s[:80]))

print("--- 3x3 grid slice profiles ---")
slice_h(305, 490, 700, "3x3 mid-row")   # through row 1 (2 4 3)
slice_v(530, 235, 380, "3x3 mid-col1")
slice_h(305, 720, 800, "18-cell row")
slice_v(760, 275, 335, "18-cell col")

print("\n--- arrow slices ---")
slice_h(306, 430, 520, "arrow1 mid")
slice_v(470, 285, 330, "arrow1 vcut")
slice_h(306, 660, 740, "arrow2 mid")

print("\n--- 5x5 border colors ---")
darkest_modal(250, 270, 257, 258, "5x5 horiz border y257-258 (x250-270)")
darkest_modal(280, 284, 240, 254, "5x5 vert border x281-283")
darkest_modal(244, 245, 240, 370, "5x5 left border x244")
darkest_modal(437, 438, 240, 370, "5x5 right border x437-438")

print("\n--- 3x3 border colors ---")
darkest_modal(510, 555, 245, 247, "3x3 cell0 top border zone")
darkest_modal(503, 506, 250, 280, "3x3 cell0 left border zone")
modal(505, 560, 250, 280, "3x3 cell0 interior")

print("\n--- 18-cell border colors ---")
darkest_modal(737, 740, 292, 318, "18-cell left border x738")
darkest_modal(740, 785, 286, 288, "18-cell top border zone")

print("\n--- blue box border colors ---")
darkest_modal(200, 700, 398, 401, "blue box top border rows 398-400")
darkest_modal(200, 700, 508, 511, "blue box bottom border rows 508-510")
darkest_modal(84, 88, 420, 490, "blue box left border x84-87")
darkest_modal(857, 860, 420, 490, "blue box right border x857-859")

print("\n--- title/text colors ---")
darkest_modal(100, 400, 62, 90, "title red ink")
darkest_modal(150, 490, 125, 140, "bullet text ink")
darkest_modal(88, 240, 406, 423, "navy L1 ink")
darkest_modal(270, 285, 248, 255, "x1 annotation red")
darkest_modal(530, 660, 200, 220, "label 'After conv 1' ink")

print("\n--- grid fill colors (clean interiors) ---")
modal(248, 260, 248, 255, "5x5 yellow cell (0,0) below number")
modal(405, 430, 240, 246, "5x5 green cell (0,4) above number")
modal(515, 550, 255, 275, "3x3 cell (0,0) interior")
modal(745, 780, 292, 298, "18-cell interior")
modal(455, 495, 300, 312, "arrow1 fill")

# ---------- font fingerprints (correct paths) ----------
FONTS = {
    "TimesB": "/usr/share/fonts/TTF/Timesbd.TTF",
    "Times": "/usr/share/fonts/TTF/Times.TTF",
    "ArialB": "/usr/share/fonts/TTF/Arialbd.TTF",
    "Arial": "/usr/share/fonts/TTF/Arial.TTF",
    "GeorgiaB": "/usr/share/fonts/TTF/Georgiab.TTF",
    "Comic": "/usr/share/fonts/TTF/Comic.TTF",
    "ComicB": "/usr/share/fonts/TTF/Comicbd.TTF",
}

def solve(text, target_w, fonts, lo=100, hi=420):
    results = []
    for name, path in fonts.items():
        best = None
        for s10 in range(lo, hi):
            f = ImageFont.truetype(path, s10)
            bb = f.getbbox(text)
            w = bb[2] - bb[0]
            if best is None or abs(w - target_w * 10) < best[0]:
                best = (abs(w - target_w * 10), s10 / 10.0, w / 10.0)
        results.append((best[0] / 10.0, name, best[1], best[2]))
    results.sort()
    for err, name, size, w in results:
        print(f"  {name}: {size:.1f}pt -> w {w:.1f} (target {target_w}, err {err:.1f}px)")

print("\nTITLE full 'Problem: Image will vanish  if applying more filters in cascade' target 768:")
solve("Problem: Image will vanish  if applying more filters in cascade", 768,
      {k: FONTS[k] for k in ("TimesB", "GeorgiaB", "ArialB")}, lo=200, hi=420)
print("TITLE 'Problem:' target 126:")
solve("Problem:", 126, {k: FONTS[k] for k in ("TimesB", "GeorgiaB", "ArialB")}, lo=200, hi=420)
print("TITLE 'Image' target 70:")
solve("Image", 70, {k: FONTS[k] for k in ("TimesB", "GeorgiaB", "ArialB")}, lo=200, hi=420)
print("TITLE 'vanish' target 76:")
solve("vanish", 76, {k: FONTS[k] for k in ("TimesB", "GeorgiaB", "ArialB")}, lo=200, hi=420)
print("TITLE 'applying' target 104:")
solve("applying", 104, {k: FONTS[k] for k in ("TimesB", "GeorgiaB", "ArialB")}, lo=200, hi=420)
print("TITLE 'cascade' target 90:")
solve("cascade", 90, {k: FONTS[k] for k in ("TimesB", "GeorgiaB", "ArialB")}, lo=200, hi=420)
print("TITLE 'filters' target 69:")
solve("filters", 69, {k: FONTS[k] for k in ("TimesB", "GeorgiaB", "ArialB")}, lo=200, hi=420)

print("\nLABEL 'Image' handwriting target ~75 (x302..377):")
solve("Image", 75, {k: FONTS[k] for k in ("Comic", "ComicB")}, lo=140, hi=400)
print("LABEL 'After conv 1' target 146 (x512..657):")
solve("After conv 1", 146, {k: FONTS[k] for k in ("Comic", "ComicB")}, lo=140, hi=400)
print("LABEL 'After conv 2' target 149 (x681..829):")
solve("After conv 2", 149, {k: FONTS[k] for k in ("Comic", "ComicB")}, lo=140, hi=400)

print("\nNAVY L2 'After apply one filter  of size 3x3, output will be3x3' target 445:")
solve("After apply one filter  of size 3x3, output will be3x3", 445,
      {k: FONTS[k] for k in ("Times", "Arial", "Georgia")}, lo=120, hi=320)
print("NAVY L3 'After applying second filter on the output (cascaded filters)' target 499:")
solve("After applying second filter on the output (cascaded filters)", 499,
      {k: FONTS[k] for k in ("Times", "Arial", "Georgia")}, lo=120, hi=320)
print("NAVY L4 'Output will be 1x1' target 154:")
solve("Output will be 1x1", 154,
      {k: FONTS[k] for k in ("Times", "Arial", "Georgia")}, lo=120, hi=320)
print("NAVY L1 'Original 5x5' bold target 111:")
solve("Original 5x5", 111,
      {k: FONTS[k] for k in ("TimesB", "ArialB", "GeorgiaB")}, lo=120, hi=320)

print("\nBULLETS Arial check:")
solve("Our images get smaller and smaller", 350, {"Arial": FONTS["Arial"], "Times": FONTS["Times"], "Comic": FONTS["Comic"]}, lo=120, hi=300)
solve("Not too deep architectures", 267, {"Arial": FONTS["Arial"], "Times": FONTS["Times"], "Comic": FONTS["Comic"]}, lo=120, hi=300)
solve("Details are lost", 141, {"Arial": FONTS["Arial"], "Times": FONTS["Times"], "Comic": FONTS["Comic"]}, lo=120, hi=300)

print("\nNUMBERS '1' target w9 h12, '18' target w23:")
for name in ("ArialB", "TimesB", "ComicB"):
    f = ImageFont.truetype(FONTS[name], 10)
    for size in (14, 15, 16, 17, 18):
        f = ImageFont.truetype(FONTS[name], size * 10)
        b1 = f.getbbox("1"); b18 = f.getbbox("18")
        print(f"  {name} {size}pt: '1' w{b1[2]-b1[0]} h{b1[3]-b1[1]} | '18' w{b18[2]-b18[0]} h{b18[3]-b18[1]}")

print("\nANNOT 'x1' target w~16 h7 red:")
solve("x1", 16, {k: FONTS[k] for k in ("Comic", "Arial", "Times")}, lo=60, hi=180)
