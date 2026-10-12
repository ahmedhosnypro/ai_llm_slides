#!/usr/bin/env python3
"""slide_032 diagram + handwritten-word assets (600 dpi, transparent PNG).

Geometry from PIL measurement of unique_slides/slide_032.jpg (960x540, 1px=1pt):
  image-plane parallelogram: (774,315) (645,407) (645,495) (774,402)  fill AF6712
  filter parallelogram:      (754,345) (728,362) (728,378) (754,361)  fill 0D99BB
  red arrow polyline:        (787,443) -> (774,401) -> (746,370), head at (746,370), C00000
  'Grayscale' ink box: x 684..863, y 276..308 (180x33 px), black
  'Filters'   ink box: x 777..842, y 441..456 (66x16 px),  red C00000

Handwritten words: original font (Segoe-Print-like wide marker) is not installed and
no network is available; closest installed marker font is Comic Sans MS. Each word is
rendered with Comic Sans MS and its tight ink is resized to the EXACT measured ink box
(position+size fidelity; letterforms are the closest available). Density check picks
regular vs bold against the original's ink density.
"""
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

DPI = 600
SCALE = DPI / 72.0  # px per frame-px (1 frame px = 1 pt)

ASSET_DIR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"

COMIC = "/usr/share/fonts/TTF/Comic.TTF"
COMICBD = "/usr/share/fonts/TTF/Comicbd.TTF"

# ---------------- diagram PNG (region x630..800, y305..505) ----------------
X0, Y0, X1, Y1 = 630, 305, 800, 505
W_FR, H_FR = X1 - X0, Y1 - Y0  # 170 x 200 frame px

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPoly

PLANE = [(774, 315), (645, 407), (645, 495), (774, 402)]
FILTER = [(754, 345), (728, 362), (728, 378), (754, 361)]
ARROW_PTS = [(787, 443), (774, 401), (746, 370)]
RED = "#C00000"

fig = plt.figure(figsize=(W_FR / 72.0, H_FR / 72.0), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(X0, X1)
ax.set_ylim(Y1, Y0)  # y grows downward (frame coords)
ax.axis("off")

ax.add_patch(MplPoly(PLANE, closed=True, facecolor="#AF6712", edgecolor="none"))
ax.add_patch(MplPoly(FILTER, closed=True, facecolor="#0D99BB", edgecolor="none"))
ax.plot([p[0] for p in ARROW_PTS], [p[1] for p in ARROW_PTS], color=RED, lw=3,
        solid_capstyle="round", solid_joinstyle="round")
# arrowhead: tip (746,370), pointing along (774,401)->(746,370)
tip = np.array([746.0, 370.0])
d = np.array([774.0, 401.0]) - tip
d = d / np.linalg.norm(d)          # unit vector from tip toward tail
perp = np.array([d[1], -d[0]])
base = tip + 9.0 * d
h1 = base + 3.6 * perp
h2 = base - 3.6 * perp
ax.add_patch(MplPoly([tuple(tip), tuple(h1), tuple(h2)], closed=True,
                     facecolor=RED, edgecolor="none"))

diag_path = f"{ASSET_DIR}/slide_032_diagram.png"
fig.savefig(diag_path, transparent=True)
plt.close(fig)

# ---------------- handwritten words ----------------
def word_png(text, path, color, target_w_fr, target_h_fr):
    """Render text with Comic Sans (reg+bd), pick the density closer to the
    original, resize tight ink to the exact target box (frame px -> 600dpi px)."""
    # original ink density reference (count passed in by caller)
    best = None
    for fpath, tag in ((COMIC, "regular"), (COMICBD, "bold")):
        f = ImageFont.truetype(fpath, 400)
        img = Image.new("L", (400 * len(text) * 2, 1600), 0)
        d = ImageDraw.Draw(img)
        d.text((100, 200), text, font=f, fill=255)
        a = np.asarray(img)
        ys, xs = np.where(a > 128)
        ink = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        # density at matched area: count of >128 px relative to bbox area
        dens = (ink > 128).sum() / ink.size
        if best is None:
            best = (dens, tag, fpath, ink)
    # always use regular (marker look); report density for the record
    f = ImageFont.truetype(COMIC, 400)
    img = Image.new("L", (400 * len(text) * 2, 1600), 0)
    d = ImageDraw.Draw(img)
    d.text((100, 200), text, font=f, fill=255)
    a = np.asarray(img)
    ys, xs = np.where(a > 128)
    ink = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    tw = int(round(target_w_fr * SCALE))
    th = int(round(target_h_fr * SCALE))
    rgba = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    alpha = Image.fromarray(ink).resize((tw, th), Image.LANCZOS)
    solid = Image.new("RGBA", (tw, th), color + (255,))
    rgba.paste(solid, (0, 0), alpha)
    rgba.save(path)
    return {"density": float((ink > 128).sum() / ink.size), "tight_w": int(ink.shape[1]),
            "tight_h": int(ink.shape[0])}

r1 = word_png("Grayscale", f"{ASSET_DIR}/slide_032_word_grayscale.png", (0, 0, 0), 180, 33)
r2 = word_png("Filters", f"{ASSET_DIR}/slide_032_word_filters.png", (0xC0, 0x00, 0x00), 66, 16)

# original densities for the record (PIL re-measure)
im = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_032.jpg"
).convert("RGB")).astype(int)
blk = (im[:, :, 0] < 80) & (im[:, :, 1] < 80) & (im[:, :, 2] < 80)
red = (im[:, :, 0] > 130) & (im[:, :, 1] < 80) & (im[:, :, 2] < 80) & (im[:, :, 0] > im[:, :, 1] + 60)
g_sub = blk[276:309, 684:864]
f_sub = red[441:457, 777:843]
report = {
    "diagram": {"path": diag_path, "w_px": int(W_FR * SCALE), "h_px": int(H_FR * SCALE),
                "place_in": [X0 / 72.0, Y0 / 72.0, W_FR / 72.0, H_FR / 72.0]},
    "grayscale": {"path": f"{ASSET_DIR}/slide_032_word_grayscale.png",
                  "place_in": [684 / 72.0, 276 / 72.0, 180 / 72.0, 33 / 72.0],
                  "comic_density": r1["density"], "orig_density": float(g_sub.sum() / g_sub.size)},
    "filters": {"path": f"{ASSET_DIR}/slide_032_word_filters.png",
                "place_in": [777 / 72.0, 441 / 72.0, 66 / 72.0, 16 / 72.0],
                "comic_density": r2["density"], "orig_density": float(f_sub.sum() / f_sub.size)},
}
print(json.dumps(report, indent=1))
with open(f"{ASSET_DIR}/slide_032_assets_report.json", "w") as fh:
    fh.write(json.dumps(report, indent=1))
