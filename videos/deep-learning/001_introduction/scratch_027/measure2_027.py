#!/usr/bin/env python3
"""Forensics pass 2 for slide_027: per-line cap heights, baselines, ascender/x-height,
bracket extents, and a font solve (sans vs serif) via width/cap-error + mask IoU."""
from PIL import Image, ImageFont, ImageDraw
import numpy as np, os

P = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_027.jpg"
a = np.asarray(Image.open(P).convert("RGB")).astype(int)
red = (a[:, :, 0] - a[:, :, 1] > 60) & (a[:, :, 0] - a[:, :, 2] > 50)

def rows_in(y0, y1, x0, x1):
    m = red[y0:y1 + 1, x0:x1 + 1]
    rs = np.where(m.sum(axis=1) > 0)[0]
    return (y0 + rs.min(), y0 + rs.max()) if len(rs) else None

# L1 band 133..179: "[4]" 264..319, "Introduction" 339..621, "to" 638..682
print("L1 '[' rows:", rows_in(125, 185, 264, 273))
print("L1 '4' rows:", rows_in(125, 185, 276, 300))
print("L1 'I' (Introduction) rows:", rows_in(125, 185, 339, 351))
print("L1 't' (to) rows:", rows_in(125, 185, 638, 650))
# L2 band 229..295: "Deep" 240..404, "Learning" 431..719
print("L2 'D' rows:", rows_in(220, 300, 240, 292))
print("L2 'p' rows:", rows_in(220, 300, 330, 360))
print("L2 'g' rows:", rows_in(220, 300, 431, 470))
print("L2 'L' rows:", rows_in(220, 300, 431, 462))
# L3 band 312..347: 'a' 439..~462, 'd' ~505..518
print("L3 'a' rows:", rows_in(305, 355, 439, 462))
print("L3 'd' rows:", rows_in(305, 355, 504, 518))
# L4 band 372..423: "CNN" 406..551
print("L4 'C' rows:", rows_in(365, 430, 406, 455))
print("L4 'N' rows:", rows_in(365, 430, 460, 500))

FONTS = {
    "LiberationSansBold": "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
    "LiberationSerifBold": "/usr/share/fonts/liberation/LiberationSerif-Bold.ttf",
    "DejaVuSansBold": "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
}
FONTS = {k: v for k, v in FONTS.items() if os.path.exists(v)}

def render_mask(text, fontpath, size):
    f = ImageFont.truetype(fontpath, size)
    img = Image.new("L", (2000, 400), 0)
    ImageDraw.Draw(img).text((30, 60), text, font=f, fill=255)
    m = np.asarray(img) > 100
    ys, xs = np.where(m)
    if not len(ys):
        return None
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def crop_mask(y0, y1, x0, x1):
    m = red[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(m)
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def iou(a, bmask):
    bi = np.asarray(Image.fromarray((bmask * 255).astype(np.uint8)).resize((a.shape[1], a.shape[0]), Image.LANCZOS)) > 100
    return (a & bi).sum() / (a | bi).sum()

L1m = crop_mask(125, 185, 264, 682)   # "[4] Introduction to"
L2m = crop_mask(220, 300, 240, 719)   # "Deep Learning"
L4m = crop_mask(365, 430, 406, 551)   # "CNN"
MEAS = [
    ("L1", "[4] Introduction to", L1m, 419, 34),   # cap 'I' ~ rows? fill after print
    ("L2", "Deep Learning", L2m, 480, 38),
    ("L4", "CNN", L4m, 146, 52),
]
print("\n--- font solve (width + cap-height err) ---")
results = []
for name, path in FONTS.items():
    best = None
    for size in range(30, 100):
        m1 = render_mask("[4] Introduction to", path, size)
        m2 = render_mask("Deep Learning", path, size)
        m4 = render_mask("CNN", path, size)
        if m1 is None or m2 is None or m4 is None:
            continue
        capH = render_mask("HMD", path, size).shape[0]
        err = (abs(m1.shape[1] - 419) + abs(m2.shape[1] - 480) + abs(m4.shape[1] - 146)
               + abs(capH - 52) + abs(capH - 38))
        if best is None or err < best[0]:
            best = (err, size, m1.shape[1], m2.shape[1], m4.shape[1], capH)
    print(f"{name}: size={best[1]} w1={best[2]}(err{abs(best[2]-419)}) w2={best[3]}(err{abs(best[3]-480)}) "
          f"w4={best[4]}(err{abs(best[4]-146)}) cap={best[5]}")
    results.append((name, best[1], path))

print("\n--- IoU ---")
for name, size, path in results:
    print(f"{name}@{size}: L1={iou(L1m, render_mask('[4] Introduction to', path, size)):.3f} "
          f"L2={iou(L2m, render_mask('Deep Learning', path, size)):.3f} "
          f"L4={iou(L4m, render_mask('CNN', path, size)):.3f}")

print("\n--- per-line best size per font (independent) ---")
for name, path in FONTS.items():
    for label, text, w, m in (("L1", "[4] Introduction to", 419, L1m), ("L2", "Deep Learning", 480, L2m),
                              ("L4", "CNN", 146, L4m)):
        best = None
        for size in range(30, 100):
            mm = render_mask(text, path, size)
            if mm is None:
                continue
            e = abs(mm.shape[1] - w)
            if best is None or e < best[0]:
                best = (e, size, mm.shape[1])
        print(f"{name} {label}: size={best[1]} w={best[2]} err={best[0]} IoU={iou(m, render_mask(text, path, best[1])):.3f}")
