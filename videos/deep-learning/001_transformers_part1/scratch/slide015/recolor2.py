# slide 015 asset v2: frame-derived background class map + per-box tint remap.
# Canvas = right-panel interior; background fields (white/peach/green) traced from the
# frame (flat cores, inpainted under ink); paper Figure 1 alpha-composited on top with
# per-comp remaps measured from the frame.
import json
import numpy as np
from PIL import Image
from scipy import ndimage

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1'
OUT = f'{BASE}/recreated_pptx/build/assets'
f15 = np.asarray(Image.open(f'{BASE}/unique_slides/slide_015.jpg').convert('RGB')).astype(int)

# panel border strokes: cols 572-574 / 893-895, rows 104-106 / 523-525 -> interior:
IX0, IX1, IY0, IY1 = 575, 892, 107, 522
IW, IH = IX1 - IX0 + 1, IY1 - IY0 + 1
print('panel interior canvas:', IX0, IY0, IW, IH)

# ---- 1. background class map -----------------------------------------------------
WHITE = np.array([255, 255, 255], float)
PEACH = np.array([253, 237, 221], float)
GREEN = np.array([206, 255, 225], float)
zone = f15[IY0:IY1 + 1, IX0:IX1 + 1].astype(float)
zf = zone.reshape(-1, 3)
d_w = np.linalg.norm(zf - WHITE, axis=1)
d_p = np.linalg.norm(zf - PEACH, axis=1)
d_g = np.linalg.norm(zf - GREEN, axis=1)
dmin = np.minimum(np.minimum(d_w, d_p), d_g)
cls = np.full(len(zf), 3, int)  # 3 = other
cls[(dmin < 18) & (d_w == dmin)] = 0
cls[(dmin < 18) & (d_p == dmin)] = 1
cls[(dmin < 18) & (d_g == dmin)] = 2
cls = cls.reshape(zone.shape[:2])
print('class counts: white', (cls == 0).sum(), 'peach', (cls == 1).sum(), 'green', (cls == 2).sum(), 'other', (cls == 3).sum())
# 3x3 majority filter for non-other, then inpaint other
for it in range(40):
    if not (cls == 3).any():
        break
    pad = np.pad(cls, 1, mode='edge')
    H_, W_ = cls.shape
    nb = np.stack([pad[1 + dy:1 + dy + H_, 1 + dx:1 + dx + W_] for dy in (-1, 0, 1) for dx in (-1, 0, 1)])
    known = (nb != 3).sum(axis=0) > 0
    fill = (cls == 3) & known
    if not fill.any():
        break
    v = np.stack([(nb == c).sum(axis=0) for c in (0, 1, 2)])
    win = np.argmax(v, axis=0)
    cls[fill] = win[fill]
print('after inpaint: other left', (cls == 3).sum())

# ---- 2. paper figure prep ----------------------------------------------------------
paper_img = Image.open(f'{OUT}/slide014_fig1.png')
if paper_img.mode == 'RGBA':
    bg = Image.new('RGB', paper_img.size, (255, 255, 255))
    bg.paste(paper_img, mask=paper_img.split()[3])
    paper_img = bg
paper = np.asarray(paper_img).astype(int)
PH, PW = paper.shape[:2]

# paper box comps (fills) from measure3/recolor v1: >=800 px
pm = paper.max(axis=2) - paper.min(axis=2)
psat = pm > 18
plab, pn_ = ndimage.label(psat)
sizes = ndimage.sum(psat, plab, range(1, pn_ + 1))
comps = []
for i in range(pn_):
    if sizes[i] >= 800:
        m = plab == i + 1
        me = ndimage.binary_erosion(m, iterations=2)
        if me.sum() < 200:
            me = m
        yy, xx = np.where(me)
        core = np.median(paper[yy, xx], axis=0)
        yya, xxa = np.where(m)
        comps.append({'id': i + 1, 'core': core, 'n': int(sizes[i]),
                      'x': (int(xxa.min()), int(xxa.max())), 'y': (int(yya.min()), int(yya.max()))})
comps.sort(key=lambda c: (c['y'][0], c['x'][0]))
print(f'\npaper comps: {len(comps)}')

# map each comp's own fill pixels (eroded) to the frame; target = median there
Sx, Sy = 277 / PW, 408 / PH
FX0, FY0 = 598, 115
for c in comps:
    m = plab == c['id']
    me = ndimage.binary_erosion(m, iterations=2)
    if me.sum() < 200:
        me = m
    yy, xx = np.where(me)
    fx = np.round(FX0 + xx * Sx).astype(int)
    fy = np.round(FY0 + yy * Sy).astype(int)
    ok = (fx >= 0) & (fx < 960) & (fy >= 0) & (fy < 540)
    vals = f15[fy[ok], fx[ok]]
    q = (vals // 4) * 4
    uq, cnt = np.unique(q, axis=0, return_counts=True)
    mode = uq[np.argmax(cnt)] + 2
    c['target'] = mode
    c['target_med'] = np.median(vals, axis=0)
    c['frect'] = (int(fx.min()), int(fx.max()), int(fy.min()), int(fy.max()))
    x0, x1 = c['x']; y0, y1 = c['y']
    print(f"  comp n={c['n']} paper core=({c['core'][0]:.0f},{c['core'][1]:.0f},{c['core'][2]:.0f}) "
          f"paper x[{x0},{x1}] y[{y0},{y1}] frect x[{c['frect'][0]},{c['frect'][1]}] y[{c['frect'][2]},{c['frect'][3]}] "
          f"target=({c['target'][0]:.0f},{c['target'][1]:.0f},{c['target'][2]:.0f}) med=({c['target_med'][0]:.0f},{c['target_med'][1]:.0f},{c['target_med'][2]:.0f})")

# ---- 3. compose canvas at 600 dpi ---------------------------------------------------
K = 600 / 72.0
CW, CH = int(round(IW * K)), int(round(IH * K))
CLS_COL = np.array([[255, 255, 255], [253, 237, 221], [206, 255, 225], [255, 255, 255]], dtype=np.uint8)
bg_img = Image.fromarray(CLS_COL[cls].astype(np.uint8)).resize((CW, CH), Image.NEAREST)

# paper overlay with alpha
FIGW, FIGH = 277, 408
fw, fh = int(round(FIGW * K)), int(round(FIGH * K))
fig = np.asarray(paper_img.resize((fw, fh), Image.LANCZOS)).astype(float)
flat = fig.reshape(-1, 3)
mx = flat.max(axis=1); mn = flat.min(axis=1)
sat = mx - mn

# classify against comp cores, RESTRICTED by bbox position (several comps share
# identical paper fill colors — global nearest-core would cross-assign columns)
fh_, fw_ = fig.shape[:2]
ys_px = (np.arange(fh_) + 0.5) / (K * Sy)  # paper y for each overlay row
xs_px = (np.arange(fw_) + 0.5) / (K * Sx)  # paper x for each overlay col
best_d = np.full((fh_, fw_), 1e9)
best_i = np.full((fh_, fw_), -1, int)
for k, c in enumerate(comps):
    x0, x1 = c['x']; y0, y1 = c['y']
    sel = ((xs_px[None, :] >= x0 - 6) & (xs_px[None, :] <= x1 + 6) &
           (ys_px[:, None] >= y0 - 6) & (ys_px[:, None] <= y1 + 6))
    if not sel.any():
        continue
    d = np.linalg.norm(fig - c['core'][None, None, :], axis=2)
    upd = sel & (d < best_d)
    best_d[upd] = d[upd]
    best_i[upd] = k
cd = best_d.reshape(-1)
ci = best_i.reshape(-1)
neutral = sat < 18
# ink alpha for neutral pixels: alpha from darkness
alpha = np.where(neutral, (255.0 - mn) / 255.0, 0.0)
# colored: remap to comp target, blended by distance (solid below 40, fade to 110)
t = np.clip((cd - 40.0) / 70.0, 0, 1)
targets = np.stack([c['target'] if c['target'] is not None else c['core'] for c in comps])
colored = ~neutral
alpha_c = np.where(colored, 1.0 - t, 0.0)
alpha = np.maximum(alpha, alpha_c)
color = flat.copy()
tgt = targets[np.maximum(ci, 0)]
valid = colored & (ci >= 0)
color[valid] = tgt[valid]
# pixels beyond bbox reach keep their paper color, fully opaque
far = colored & (ci < 0)
alpha[far] = 1.0
# where alpha<1 and colored: blend handled by compositing over bg (color stays fill)
overlay = np.empty((flat.shape[0], 4), float)
overlay[:, :3] = color
overlay[:, 3] = alpha * 255
ov_img = Image.fromarray(overlay.reshape(fh, fw, 4).astype(np.uint8), 'RGBA')
fx = int(round((FX0 - IX0) * K)); fy = int(round((FY0 - IY0) * K))
print('overlay paste at canvas px:', fx, fy, 'size', ov_img.size)
bg_img = bg_img.convert('RGBA')
bg_img.alpha_composite(ov_img, (fx, fy))
final = bg_img.convert('RGB')
final.save(f'{OUT}/slide015_fig1_color.png')
print('saved slide015_fig1_color.png', final.size)
sidecar = {
    'file': 'slide015_fig1_color.png', 'dpi': 600,
    'canvas_frame_rect': [IX0, IY0, IX1, IY1], 'w_in': IW / 72, 'h_in': IH / 72,
    'figure_rect_frame': [FX0, FY0, FX0 + FIGW - 1, FY0 + FIGH - 1],
    'panel_border_rect_pt': [573, 105, 894, 524], 'border_pt': 2, 'border_color': '00B050',
    'peach': [253, 237, 221], 'green': [206, 255, 225],
}
json.dump(sidecar, open(f'{OUT}/slide015_fig1_color.json', 'w'), indent=1)
print(json.dumps(sidecar))

# ---- 4. up arrows (background-relative redness alpha) -------------------------------
for tag, (x0, x1, y0, y1) in {'up1': (654, 666, 487, 513), 'up2': (740, 750, 116, 140)}.items():
    crop = f15[y0:y1 + 1, x0:x1 + 1].astype(float)
    redness = crop[:, :, 0] - np.maximum(crop[:, :, 1], crop[:, :, 2])
    alpha_a = np.clip((redness - 20) / 150.0, 0, 1)
    w_, h_ = x1 - x0 + 1, y1 - y0 + 1
    aim = Image.fromarray((alpha_a * 255).astype(np.uint8)).resize(
        (int(round(w_ * K)), int(round(h_ * K))), Image.BILINEAR)
    oim = Image.new('RGBA', aim.size, (204, 0, 0, 0))
    oim.putalpha(aim)
    oim.save(f'{OUT}/slide015_{tag}.png')
    print(f'saved {tag}: rect x[{x0},{x1}] y[{y0},{y1}] {w_}x{h_}pt -> {oim.size}')
