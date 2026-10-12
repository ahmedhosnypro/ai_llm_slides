#!/usr/bin/env python3
"""Pass 3: solve 'and' size; dump Liberation Sans hhea metrics for the baseline model."""
from PIL import Image, ImageFont, ImageDraw
import numpy as np

P = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_027.jpg"
a = np.asarray(Image.open(P).convert("RGB")).astype(int)
red = (a[:, :, 0] - a[:, :, 1] > 60) & (a[:, :, 0] - a[:, :, 2] > 50)

# "and" band cols 439..518, rows 312..347 — column profile to find glyph splits
seg = red[312:348, 435:525]
colprof = seg.sum(axis=0)
print("and colprof (cols 435..524):")
print("".join(str(min(9, int(v / 3))) for v in colprof))

m = red[305:355, 435:525]
ys, xs = np.where(m)
mm = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def render_mask(text, fontpath, size):
    f = ImageFont.truetype(fontpath, size)
    img = Image.new("L", (800, 300), 0)
    ImageDraw.Draw(img).text((30, 60), text, font=f, fill=255)
    t = np.asarray(img) > 100
    ys, xs = np.where(t)
    return t[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def iou(a, bmask):
    bi = np.asarray(Image.fromarray((bmask * 255).astype(np.uint8)).resize((a.shape[1], a.shape[0]), Image.LANCZOS)) > 100
    return (a & bi).sum() / (a | bi).sum()

FP = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"
best = None
for size in range(30, 90):
    t = render_mask("and", FP, size)
    e = abs(t.shape[1] - 80) + abs(t.shape[0] - 36)
    if best is None or e < best[0]:
        best = (e, size, t.shape[1], t.shape[0])
print(f"and best: size={best[1]} w={best[2]} h={best[3]} err={best[0]} IoU={iou(mm, render_mask('and', FP, best[1])):.3f}")
# independent width-only and x-height-only estimates
for size in range(35, 70):
    t = render_mask("and", FP, size)
    if abs(t.shape[1] - 80) <= 1:
        print(f"  width-fit size={size} h={t.shape[0]} (orig h 36)")

try:
    from fontTools.ttLib import TTFont
    f = TTFont(FP)
    hhea = f["hhea"]
    upm = f["head"].unitsPerEm
    print(f"LiberationSans-Bold hhea: ascent={hhea.ascent} descent={hhea.descent} lineGap={hhea.lineGap} upm={upm}")
    print(f"ascent_em={hhea.ascent / upm:.4f} descent_em={hhea.descent / upm:.4f}")
    os2 = f["OS/2"]
    print(f"OS/2 typo: Asc={os2.sTypoAscender} Desc={os2.sTypoDescender} Gap={os2.sTypoLineGap}; win: Asc={os2.usWinAscent} Desc={os2.usWinDescent}")
    print(f"capHeight={os2.sCapHeight} xHeight={os2.sxHeight}")
except Exception as e:
    print("fontTools:", e)
