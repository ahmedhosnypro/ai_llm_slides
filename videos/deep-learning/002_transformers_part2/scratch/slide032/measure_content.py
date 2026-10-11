#!/usr/bin/env python3
"""Full content-ink measurement of slide_032.jpg -> slide coordinates.

Mapping (from slide_002 certified build, confirmed by THIS frame's landmarks):
  frame_x = 18.63 + 0.96123 * slide_x ;  frame_y = 0.95556 * slide_y
  => slide_x = (frame_x - 18.63)/0.96123 ; slide_y = frame_y/0.95556
"""
from PIL import Image
import numpy as np, json

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_032.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

FX0, SX = 18.63, 0.96123
SY = 0.95556

def to_slide(fx, fy):
    return ((fx - FX0) / SX, fy / SY)

def bbox(mask, label, region=None):
    m = mask
    if region:
        x0, y0, x1, y1 = region
        mm = np.zeros_like(m)
        mm[y0:y1, x0:x1] = m[y0:y1, x0:x1]
        m = mm
    ys, xs = np.where(m)
    if not len(ys):
        print(f"{label}: NO INK")
        return None
    fx0, fx1, fy0, fy1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
    sx0, sy0 = to_slide(fx0, fy0)
    sx1, sy1 = to_slide(fx1 + 1, fy1 + 1)  # right/bottom edges exclusive -> +1
    print(f"{label}: frame x {fx0}..{fx1} y {fy0}..{fy1}  ->  slide x {sx0:.1f}..{sx1:.1f} y {sy0:.1f}..{sy1:.1f} (w {sx1-sx0:.1f} h {sy1-sy0:.1f})")
    return dict(frame=(fx0, fy0, fx1, fy1), slide=(sx0, sy0, sx1, sy1))

def near(color, tol=45):
    r, g, b = color
    return (np.abs(R - r) < tol) & (np.abs(G - g) < tol) & (np.abs(B - b) < tol)

out = {}
# --- big surfaces first ---
cyan = near((224, 247, 250), 22)
out['panel_fill'] = bbox(cyan, 'cyan panel fill E0F7FA')
callout = near((255, 255, 204), 18)
out['callout_fill'] = bbox(callout, 'callout fill FFFFCC')
orange = near((204, 102, 0), 60)
out['callout_border'] = bbox(orange, 'callout orange border CC6600')
navy = near((0, 0, 128), 60)
out['navy'] = bbox(navy, 'navy 000080 ink (panel border)')

# --- title (red) in top band ---
red = near((192, 0, 0), 70)
out['title'] = bbox(red, 'title red C00000', region=(150, 30, 800, 78))
# --- subtitle (blue) below title, above panel ---
blue = near((0, 0, 204), 70)
out['subtitle'] = bbox(blue, 'subtitle blue 0000CC', region=(150, 70, 850, 112))
# vector box: red border upper-left, white interior; region x<220, y<210
out['vecbox_red'] = bbox(red, 'vector-box red border+ink', region=(60, 95, 215, 205))
# check white inside vector box
white = near((255, 255, 255), 12)
out['vecbox_white'] = bbox(white, 'vector-box white interior', region=(70, 100, 210, 200))

# --- text lines inside the panel: row profile of dark ink (any of blue/green/red/black) ---
ink = (R < 150) & (G < 150) | (B < 100) & (R < 150)
# restrict to panel interior (fill bbox + margin)
if out['panel_fill']:
    fx0, fy0, fx1, fy1 = out['panel_fill']['frame']
else:
    fx0, fy0, fx1, fy1 = 77, 205, 883, 513
inner = np.zeros((H, W), bool)
inner[fy0 + 4:fy1 - 3, fx0 + 4:fx1 - 3] = True
inkp = ink & inner
rowc = inkp.sum(axis=1)
print("\npanel text row bands (rowc>3):")
bands = []
inb = False
for r in range(H):
    if rowc[r] > 3 and not inb:
        inb, b0 = True, r
    elif rowc[r] <= 3 and inb:
        inb = False
        bands.append((b0, r - 1))
for b0, b1 in bands:
    xs = np.where(inkp[b0:b1 + 1].any(axis=0))[0]
    s0 = to_slide(xs.min(), b0); s1 = to_slide(xs.max() + 1, b1 + 1)
    print(f"  band y {b0}..{b1} (h {b1-b0+1}) x {xs.min()}..{xs.max()} -> slide y {s0[1]:.1f}..{s1[1]:.1f} x {s0[0]:.1f}..{s1[0]:.1f}")

# --- per-band color analysis: yellow highlight, green, red, blue extents ---
yellow = near((255, 255, 0), 60)
green = near((0, 153, 0), 70)
darkred = near((192, 0, 0), 80)
for i, (b0, b1) in enumerate(bands):
    ym = yellow[b0:b1 + 1]
    gmask = green[b0:b1 + 1]
    rm = darkred[b0:b1 + 1]
    for name, mm in (('YELLOW', ym), ('GREEN', gmask), ('RED', rm)):
        ys2, xs2 = np.where(mm)
        if len(xs2) > 8:
            fx0b, fx1b = int(xs2.min()), int(xs2.max())
            s0 = to_slide(fx0b, 0); s1 = to_slide(fx1b + 1, 0)
            print(f"  band{i} {name}: frame x {fx0b}..{fx1b} -> slide x {s0[0]:.1f}..{s1[0]:.1f}")

# green/red ink overall (including panel)
out['green'] = bbox(green, 'green 009900 all')
out['red_all'] = bbox(darkred, 'red C00000 all')
ys, xs = np.where(darkred)
if len(xs):
    # red in lower half = closing warning
    sel = ys > 350
    if sel.any():
        bbox_of = (int(xs[sel].min()), int(ys[sel].min()), int(xs[sel].max()), int(ys[sel].max()))
        s0 = to_slide(bbox_of[0], bbox_of[1]); s1 = to_slide(bbox_of[2] + 1, bbox_of[3] + 1)
        print(f"red warning (y>350): frame x {bbox_of[0]}..{bbox_of[2]} y {bbox_of[1]}..{bbox_of[3]} -> slide x {s0[0]:.1f}..{s1[0]:.1f} y {s0[1]:.1f}..{s1[1]:.1f}")

# yellow highlight bbox overall
out['yellow'] = bbox(yellow, 'yellow FFFF00 all', region=(fx0, fy0, fx1, fy1))

json.dump(out, open('content_measure.json', 'w'), indent=1)
print("\nsaved content_measure.json")
