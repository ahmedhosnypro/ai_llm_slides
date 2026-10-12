#!/usr/bin/env python3
"""Probe: disambiguate selfcheck_attempt_3 flags (h-arrow tips, h-label metrics,
diag-label extents, label-box borders with looser mask, magenta-mask tightening)."""
from PIL import Image
import numpy as np

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
K = 150 / 72.0
SX = lambda fx: (fx - 18.63) / 0.96123 * K
SY = lambda fy: fy / 0.95556 * K

def load(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    return a

O = load(f"{VID}/unique_slides/slide_042.jpg")
R = load(f"{VID}/recreated_pptx/qa/slide042/render_3.png")

def red(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 130) & (r - g > 60) & (r - b > 60)

def redloose(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 150) & (r - g > 30) & (r - b > 30)

def mag_tight(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 150) & (b > 150) & (g < 80)

ro, rr = red(O), red(R)
mo, mr = mag_tight(O), mag_tight(R)

def bb(mask, x0, y0, x1, y1):
    m = mask[int(y0):int(y1), int(x0):int(x1)]
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    return (xs.min() + int(x0), ys.min() + int(y0), xs.max() + int(x0), ys.max() + int(y0))

print("== h-arrow tips, clean band y483.5..491 (excludes Channels above, (4F) below, diag head y<479):")
print("  orig  :", bb(ro, 640, 483.5, 800, 491))
print("  render:", bb(rr, SX(640), SY(483.5), SX(800), SY(491)), "-> frame",
      tuple(round(v * (0.46139 if i % 2 == 0 else 0.45867), 1) for i, v in enumerate(bb(rr, SX(640), SY(483.5), SX(800), SY(491)))))

print("== h-arrow shaft row extent y486..488:")
print("  orig  :", bb(ro, 640, 486, 800, 488.5))
print("  render:", bb(rr, SX(640), SY(486), SX(800), SY(488.5)))

print("== 'Channels' band (above shaft, y470..484):")
print("  orig  :", bb(ro, 645, 470, 795, 484))
print("  render:", bb(rr, SX(645), SY(470), SX(795), SY(484)), "-> frame",
      tuple(round(v * (0.46139 if i % 2 == 0 else 0.45867), 1) for i, v in enumerate(bb(rr, SX(645), SY(470), SX(795), SY(484)))))

print("== '(4 Filters)' band (below shaft, y492..504):")
print("  orig  :", bb(ro, 645, 492, 795, 504))
print("  render:", bb(rr, SX(645), SY(492), SX(795), SY(504)), "-> frame",
      tuple(round(v * (0.46139 if i % 2 == 0 else 0.45867), 1) for i, v in enumerate(bb(rr, SX(645), SY(492), SX(795), SY(504)))))

print("== red ink rows 1010..1095 render px in h-window (what is at bbox top/bottom?):")
for y0 in range(1012, 1094, 6):
    n = int(rr[y0:y0+6, 1370:1690].sum())
    print(f"   rows {y0}..{y0+6}: {n}")

print("== diag labels: bottom-right extremity window x840..880 y440..480:")
print("  orig  :", bb(ro, 840, 440, 880, 480))
print("  render:", bb(rr, SX(840), SY(440), SX(880), SY(480)), "-> frame",
      tuple(round(v * (0.46139 if i % 2 == 0 else 0.45867), 1) for i, v in enumerate(bb(rr, SX(840), SY(440), SX(880), SY(480)))))
print("== diag labels: top-left extremity window x788..835 y366..404:")
print("  orig  :", bb(ro, 788, 366, 835, 404))
print("  render:", bb(rr, SX(788), SY(366), SX(835), SY(404)), "-> frame",
      tuple(round(v * (0.46139 if i % 2 == 0 else 0.45867), 1) for i, v in enumerate(bb(rr, SX(788), SY(366), SX(835), SY(404)))))

print("== label-box borders with LOOSE red mask (orig video-blurred strokes):")
lo = redloose(O)
lr = redloose(R)
for name, (x0, y0, x1, y1) in dict(Lbox=(70, 188, 312, 244), Mbox=(335, 186, 604, 242),
                                   Rbox=(620, 158, 880, 234)).items():
    print(f"  {name} orig  : {bb(lo, x0, y0, x1, y1)}")
    b = bb(lr, SX(x0), SY(y0), SX(x1), SY(y1))
    print(f"  {name} render: {b} -> frame",
          tuple(round(v * (0.46139 if i % 2 == 0 else 0.45867), 1) for i, v in enumerate(b)))

print("== right-magenta with TIGHT mask (g<80):")
print("  orig  :", bb(mo, 600, 250, 880, 500))
b = bb(mr, SX(600), SY(250), SX(880), SY(500))
print("  render:", b, "-> frame",
      tuple(round(v * (0.46139 if i % 2 == 0 else 0.45867), 1) for i, v in enumerate(b)))

print("== sample orig border pixel colors (Lbox top row y195-196, x150):")
print("  ", O[195, 150], O[196, 150], O[194, 150])
print("== sample orig h-arrow shaft pixel (y486-487, x700):")
print("  ", O[486, 700], O[487, 700], O[488, 700])
