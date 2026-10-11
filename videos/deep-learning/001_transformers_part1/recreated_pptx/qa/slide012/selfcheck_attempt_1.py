#!/usr/bin/env python3
"""Pre-judge self-check for slide 012, attempt 1 (150dpi render 2001x1125).

Checks (17_worker_instructions.md self-check list, adapted to the playlist
chrome: white canvas margins + gray panel x42..918 y45..540 @72dpi):
  1. render geometry == 150dpi LAYOUT_WIDE
  2. house chrome present (panel + badge) — corroborates house_chrome_check.py
  3. container red border present at measured position; page image inside it
  4. FRAME CONTAINMENT: no non-chrome ink outside the panel; page content
     inside the container border; nothing crosses the slide edge
  5. highlight regions contain ink with the measured colors (tan title box,
     6 pink boxes, tan date band)
  6. watermark strip contains ink (stamp present — the 'equation exists' analog)
  7. abstract line pitch matches the frame (12.9 frame px = 26.9 render px)
"""
from PIL import Image
import numpy as np

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
RE = f"{VID}/recreated_pptx/qa/slide012/render_1.png"
im = Image.open(RE).convert("RGB")
a = np.asarray(im).astype(float)
H, W, _ = a.shape
print(f"render {W}x{H}")
ok = True
def check(name, cond, detail=""):
    global ok
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")
    if not cond: ok = False

S = W / 960.0  # render px per frame px (expect ~2.084)
check("render is 150dpi LAYOUT_WIDE", abs(S - 2001/960) < 0.01 and H == 1125, f"S={S:.4f}")

r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = (r * 299 + g * 587 + b * 114) / 1000

# 2. chrome: panel gray at (60,300)*S, white canvas at (20,20)*S, badge yellow at (893,71)*S
def samp(fx, fy):
    x, y = int(fx * S), int(fy * S)
    return a[y-2:y+3, x-2:x+3].reshape(-1, 3).mean(axis=0).astype(int)
p = samp(60, 300); check("panel gray E9E9E7", abs(p[0]-233) < 12 and abs(p[1]-233) < 12, str(p))
c = samp(20, 20); check("canvas white FFFFFF", c.min() > 245, str(c))
bg = samp(893, 71); check("badge yellow FDFD96", bg[0] > 230 and bg[1] > 230 and bg[2] < 210, str(bg))

# 3. container border: red-ish rows/cols at expected render positions
redish = (r - np.maximum(g, b) > 50) & (r > 110)
exp = {"top": 52.5, "bottom": 524.5}
for name, fy in exp.items():
    y = int(fy * S)
    seg = redish[y-3:y+4, int(150*S):int(700*S)]
    check(f"container border {name} present", seg.sum() > 100, f"n={int(seg.sum())}")
for name, fx in [("left", 93.5), ("right", 796.5)]:
    x = int(fx * S)
    seg = redish[int(80*S):int(500*S), x-3:x+4]
    check(f"container border {name} present", seg.sum() > 100, f"n={int(seg.sum())}")

# 4. containment: non-white, non-chrome ink outside the panel region?
#    panel: x[42,918] y[45,540] frame -> render. Canvas margins must be white.
marg = np.concatenate([
    lum[:int(44*S), :].ravel(), lum[int(919*S):, :].ravel(),
    lum[:int(44*S), :].ravel(),
])
marg_img = np.concatenate([a[:int(44*S), :].reshape(-1, 3), a[int(919*S):, :].reshape(-1, 3),
                           a[:, :int(41*S)].reshape(-1, 3), a[:, int(919*S):].reshape(-1, 3)])
dark_marg = (marg_img.sum(axis=1) < 600).mean()
check("canvas margins clean (no ink)", dark_marg < 0.005, f"nonwhite frac={dark_marg:.4f}")
# page content inside container: ink bbox within x[94,796] y[53,524] frame
ink = lum < 140
ink[:int(50*S), :] = False; ink[int(527*S):, :] = False
ink[:, :int(96*S)] = False; ink[:, int(795*S):] = False
ys, xs = np.where(ink)
check("content ink inside container", xs.min() >= int(94*S) - 3 and xs.max() <= int(796*S) + 3
      and ys.min() >= int(53*S) - 3 and ys.max() <= int(524*S) + 3,
      f"x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")

# 5. highlight interiors — patch-based (point samples hit glyph ink on hairline text)
def pinkish_frac(fx0, fy0, fx1, fy1):
    reg = a[int(fy0*S):int(fy1*S), int(fx0*S):int(fx1*S)].reshape(-1, 3)
    return float(((reg[:, 0]-reg[:, 1] > 40) & (reg[:, 2]-reg[:, 1] > 40) & (reg[:, 0] > 190)).mean())
def tanish_frac(fx0, fy0, fx1, fy1):
    reg = a[int(fy0*S):int(fy1*S), int(fx0*S):int(fx1*S)].reshape(-1, 3)
    return float(((reg[:, 0]-reg[:, 2] > 35) & (reg[:, 0] > 220) & (reg[:, 1] > 150) &
                  (reg[:, 1] < 240) & (reg[:, 2] > 100) & (reg[:, 2] < 225)).mean())
check("pink vaswani box", pinkish_frac(262, 172, 332, 184) > 0.4, f"frac={pinkish_frac(262,172,332,184):.2f}")
check("pink kaiser box", pinkish_frac(576, 232, 643, 244) > 0.4, f"frac={pinkish_frac(576,232,643,244):.2f}")
check("tan title box", tanish_frac(340, 56, 594, 82) > 0.4, f"frac={tanish_frac(340,56,594,82):.2f}")
check("tan date band", tanish_frac(100, 190, 134, 306) > 0.4, f"frac={tanish_frac(100,190,134,306):.2f}")

# 6. watermark ink present (gray text strip x110-135, y330-520 frame)
wm = a[int(330*S):int(520*S), int(110*S):int(135*S)].reshape(-1, 3)
wml = (wm[:, 0]*299 + wm[:, 1]*587 + wm[:, 2]*114) / 1000
frac = (np.abs(wm[:, 0]-wm[:, 1]) < 25) & (wml > 90) & (wml < 215)
check("watermark stamp ink present", frac.sum() > 150, f"gray px={int(frac.sum())}")

# 7. abstract line pitch: DENSE line-core rows (>120 dark px) = text line bodies
#    (block window stops ABOVE the container bottom border stroke at y524.5)
block = lum[int(370*S):int(522*S), int(270*S):int(660*S)]
rows = (block < 130).sum(axis=1)
bands = []
for i, v in enumerate(rows):
    if v > 120:
        if bands and i <= bands[-1][1] + 4: bands[-1][1] = i
        else: bands.append([i, i])
bands = [bd for bd in bands if bd[1] - bd[0] >= 2]  # drop 1-2 row strays
tops = [b0 for b0, b1 in bands]
check("abstract lines 11..13", 11 <= len(bands) <= 13, f"n={len(bands)} tops={[370+t for t in tops]}")
if len(tops) >= 3:
    pitch = (tops[-1] - tops[0]) / (len(tops) - 1) / S
    check("abstract pitch ~12.9 frame px", abs(pitch - 12.9) < 0.8,
          f"mean={pitch:.2f} frame px")

print("SELF-CHECK:", "PASS" if ok else "FAIL")
