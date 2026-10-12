#!/usr/bin/env python3
"""Slide 038 asset generation: quantized slab PNGs (redrawn from measured geometry)
+ font metric solving. Assets -> recreated_pptx/build/assets/.
Banked outputs: out_assets.txt."""
from PIL import Image, ImageFilter
import numpy as np
import os, json

ROOT = '/home/ahmed/Projects/ai_llm_slides'
VID = f'{ROOT}/videos/deep-learning/001_introduction'
ASSETS = f'{VID}/recreated_pptx/build/assets'
os.makedirs(ASSETS, exist_ok=True)
OUT = []

im = Image.open(f'{VID}/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(float)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
lum = 0.299 * r + 0.587 * g + 0.114 * b

# ---------------------------------------------------------------- palette utils
def quantize_region(crop, palette, alpha_mask):
    """crop HxWx3 float; palette list of RGB; alpha_mask HxW bool (True=keep).
    Returns RGBA uint8 image: nearest palette color where mask, alpha 0 elsewhere."""
    h, w, _ = crop.shape
    pal = np.asarray(palette, float)               # K x 3
    px = crop.reshape(-1, 3)                       # N x 3
    d = ((px[:, None, :] - pal[None, :, :]) ** 2).sum(axis=2)   # N x K
    idx = d.argmin(axis=1)
    out = pal[idx].reshape(h, w, 3)
    rgba = np.dstack([out, np.where(alpha_mask, 255, 0)]).astype(np.uint8)
    return rgba

def auto_palette(crop, mask, k=12):
    """median-cut-ish: k-means with numpy, few iters, on masked pixels."""
    px = crop[mask]
    rng = np.random.default_rng(38)
    centers = px[rng.choice(len(px), size=min(k, len(px)), replace=False)]
    for _ in range(12):
        d = ((px[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        lab = d.argmin(axis=1)
        for j in range(len(centers)):
            sel = px[lab == j]
            if len(sel):
                centers[j] = sel.mean(axis=0)
    return [tuple(np.round(c).astype(int)) for c in centers]

# force key palette colors to exist
def merge_palette(auto, forced):
    pal = list(auto)
    for f in forced:
        # replace nearest auto color if within 40, else append
        d = [sum((p[i] - f[i]) ** 2 for i in range(3)) ** 0.5 for p in auto]
        j = int(np.argmin(d))
        if d[j] < 45:
            pal[j] = f
        else:
            pal.append(f)
    return pal

WHITE = (255, 255, 255)

# ================================================================ image slab PNG
X0, X1, Y0, Y1 = 246, 353, 289, 447          # bbox (pad around ink x250..347 y294..441)
S = 8                                        # supersample
crop = a[Y0:Y1, X0:X1]
hh, ww, _ = crop.shape
big = np.asarray(Image.fromarray(crop.astype(np.uint8)).resize((ww * S, hh * S), Image.LANCZOS)).astype(float)

# silhouette mask (frame-px space): brownish OR dark-outline OR light-tan, NOT white/gray bg
rb = big[..., 0] - big[..., 2]
mask_bg = (big[..., 0] > 225) & (big[..., 1] > 225) & (big[..., 2] > 225)
mask_gray = (abs(big[..., 0] - 232) < 14) & (abs(big[..., 1] - 232) < 14) & (abs(big[..., 2] - 231) < 14)
sil = ~mask_bg & ~mask_gray
# keep only the largest connected region (the slab), then fill holes
from scipy import ndimage
lab, n = ndimage.label(sil)
if n > 1:
    sizes = ndimage.sum(sil, lab, range(1, n + 1))
    sil = lab == (1 + int(np.argmax(sizes)))
sil = ndimage.binary_fill_holes(sil)
# clean: open then close (3px at S=8 -> 5% px)
st = np.ones((3 * S // 2, 3 * S // 2), bool)
sil = ndimage.binary_opening(sil, st)
sil = ndimage.binary_closing(sil, st)

# inpaint the dashed lines inside the slab (rows y353..392 frame -> local) using vertical neighbors
yy0 = (353 - Y0) * S
yy1 = (393 - Y0) * S
darkmark = (0.299 * big[..., 0] + 0.587 * big[..., 1] + 0.114 * big[..., 2]) < 150
zone = np.zeros_like(sil)
zone[yy0:yy1] = True
fix = sil & zone & darkmark
OUT.append(f"slab dash-inpaint px: {int(fix.sum())}")
bigq = big.copy()
if fix.sum():
    med = Image.fromarray(big.astype(np.uint8)).filter(ImageFilter.MedianFilter(9))
    big[fix] = np.asarray(med, float)[fix]

pal = merge_palette(auto_palette(big, sil, 10), [
    (175, 104, 19),    # main brown (measured modal)
    (215, 129, 24),    # light tan strip
    (233, 178, 120),   # very light tan
    (45, 26, 8),       # dark outline
])
OUT.append(f"slab palette: {pal}")
rgba = quantize_region(big, pal, sil)
Image.fromarray(rgba).save(f'{ASSETS}/slab038_image.png')
OUT.append(f"slab038_image.png {ww}x{hh} @x{S}  bbox frame x{X0}..{X1} y{Y0}..{Y1}")

# ================================================================ filter stack PNG
X0, X1, Y0, Y1 = 388, 554, 330, 420
crop = a[Y0:Y1, X0:X1]
hh, ww, _ = crop.shape
big = np.asarray(Image.fromarray(crop.astype(np.uint8)).resize((ww * S, hh * S), Image.LANCZOS)).astype(float)
mask_bg = (big[..., 0] > 225) & (big[..., 1] > 225) & (big[..., 2] > 225)
mask_gray = (abs(big[..., 0] - 232) < 14) & (abs(big[..., 1] - 232) < 14) & (abs(big[..., 2] - 231) < 14)
sil = ~mask_bg & ~mask_gray
lab, n = ndimage.label(sil)
if n > 1:
    sizes = ndimage.sum(sil, lab, range(1, n + 1))
    keep = np.argsort(sizes)[::-1][:3] + 1     # the slabs form up to 3 touching groups
    sil = np.isin(lab, keep)
sil = ndimage.binary_fill_holes(sil)
sil = ndimage.binary_closing(sil, np.ones((2 * S, 2 * S), bool))

# inpaint arrow-tip marks near the bottom (frame y>=399): dark marks -> local median
yy0 = (399 - Y0) * S
darkmark = (0.299 * big[..., 0] + 0.587 * big[..., 1] + 0.114 * big[..., 2]) < 130
zone = np.zeros(big.shape[:2], bool)
zone[yy0:] = True
fix = sil & zone & darkmark
OUT.append(f"stack tip-inpaint px: {int(fix.sum())}")
if fix.sum():
    med = Image.fromarray(big.astype(np.uint8)).filter(ImageFilter.MedianFilter(9))
    big[fix] = np.asarray(med, float)[fix]

pal = merge_palette(auto_palette(big, sil, 14), [
    (16, 190, 232), (28, 167, 191),    # cyan bright/dark
    (29, 163, 69),                     # green
    (211, 0, 2),                       # red
    (238, 224, 14), (204, 218, 13),    # yellow bright/dark
    (104, 33, 127), (86, 28, 123),     # purple
    (40, 20, 15),                      # outline
])
OUT.append(f"stack palette: {pal}")
rgba = quantize_region(big, pal, sil)
Image.fromarray(rgba).save(f'{ASSETS}/stack038_filters.png')
OUT.append(f"stack038_filters.png {ww}x{hh} @x{S}  bbox frame x{X0}..{X1} y{Y0}..{Y1}")

# ================================================================ font metrics
from PIL import ImageFont
FONTS = {
    'Times New Roman': '/usr/share/fonts/TTF/Times.TTF',
    'Times New Roman Bold': '/usr/share/fonts/TTF/Timesbd.TTF',
    'Arial': '/usr/share/fonts/TTF/Arial.TTF',
    'Arial Bold': '/usr/share/fonts/TTF/Arialbd.TTF',
    'Comic Sans MS': '/usr/share/fonts/TTF/Comic.TTF',
    'Comic Sans MS Bold': '/usr/share/fonts/TTF/Comicbd.TTF',
}
for k, v in list(FONTS.items()):
    if not os.path.exists(v):
        del FONTS[k]

def probe(fontfile, text, pt):
    # pt -> px at 72dpi = 1px/pt; PIL truetype size is px per em
    try:
        f = ImageFont.truetype(fontfile, int(round(pt)))
    except Exception:
        return None
    x0, y0, x1, y1 = f.getbbox(text)
    asc, desc = f.getmetrics()
    return (x1 - x0, y1 - y0, asc, desc, y1)

targets = [
    ("L1", 'Times New Roman', "Number of parameters for different filters applied to same location in the image", 716, 139, 157),
    ("L2", 'Times New Roman', "= Filter size (2-D) * Number of channels (K)  * number of different filters", 699, 174, 191),
    ("L3", 'Times New Roman', "= 7*7  * 3  * 5  =735", 219, 210, 223),
]
OUT.append("--- serif width solve (target px @ 1px=1pt) ---")
for name, face, text, target, ytop, ybot in targets:
    for fn, fp in FONTS.items():
        if 'Times' not in fn:
            continue
        best = None
        for pt in range(14, 30):
            m = probe(fp, text, pt)
            if m and abs(m[0] - target) < 14:
                best = (pt, m[0], m[1], m[2], m[3])
        if best:
            OUT.append(f"{name} '{fn}': size={best[0]}pt width={best[1]} (target {target}) glyphH={best[2]} asc={best[3]} desc={best[4]}")

OUT.append("--- annotation metrics (Comic Sans MS) ---")
ann = [
    ("RGB", "RGB", 66, 14),          # width target 297..363, cap ~14
    ("3dims", "3 dims", 50, 7),
    ("7left", "7", 12, 12),
    ("3ann", "3", 14, 8),
    ("735w", "735 weights", 172, 13),
]
for name, text, tw, cap in ann:
    fp = FONTS['Comic Sans MS']
    for pt in range(8, 30):
        f = ImageFont.truetype(fp, pt)
        x0, y0, x1, y1 = f.getbbox(text)
        if abs((x1 - x0) - tw) <= 8:
            OUT.append(f"{name}: '{text}' ComicSans {pt}pt -> w={x1-x0} h={y1-y0} (target w={tw})")
OUT.append("--- title metric ---")
for fn in ['Times New Roman Bold', 'Arial Bold']:
    fp = FONTS[fn]
    for pt in range(28, 44):
        f = ImageFont.truetype(fp, pt)
        x0, y0, x1, y1 = f.getbbox("Filters parameters")
        w = x1 - x0
        if abs(w - 300) <= 12:
            OUT.append(f"title {fn} {pt}pt -> w={w} (target 300) bboxY {y0}..{y1} asc/desc={f.getmetrics()}")

print('\n'.join(OUT))
with open(f'{ROOT}/videos/deep-learning/001_introduction/scratch/slide038/out_assets.txt', 'w') as fh:
    fh.write('\n'.join(OUT))
