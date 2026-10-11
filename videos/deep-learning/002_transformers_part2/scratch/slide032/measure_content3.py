#!/usr/bin/env python3
"""Content measurement v3: profile-threshold rectangles for fills/borders + line bands."""
from PIL import Image
import numpy as np, json

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_032.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
FX0, SX, SY = 18.63, 0.96123, 0.95556
def to_slide(fx, fy): return ((fx - FX0) / SX, fy / SY)
def pr(label, fx0, fy0, fx1, fy1):
    s0 = to_slide(fx0, fy0); s1 = to_slide(fx1 + 1, fy1 + 1)
    print(f"{label:34s} frame x {fx0}..{fx1} y {fy0}..{fy1} -> slide x {s0[0]:.1f}..{s1[0]:.1f} y {s0[1]:.1f}..{s1[1]:.1f} (w {s1[0]-s0[0]:.1f} h {s1[1]-s0[1]:.1f})")
    return (s0[0], s0[1], s1[0], s1[1])

def near(c, tol):
    r, g, b = c
    return (np.abs(R - r) < tol) & (np.abs(G - g) < tol) & (np.abs(B - b) < tol)

def rect_from_profiles(mask, label, rthr, cthr):
    rowc = mask.sum(axis=1); colc = mask.sum(axis=0)
    rows = np.where(rowc >= rthr)[0]; cols = np.where(colc >= cthr)[0]
    if not len(rows) or not len(cols):
        print(f"{label}: no rectangle"); return None
    fx0, fx1, fy0, fy1 = int(cols.min()), int(cols.max()), int(rows.min()), int(rows.max())
    return pr(label, fx0, fy0, fx1, fy1)

out = {}
# cyan panel E0F7FA (233,254,249 measured)
out['panel'] = rect_from_profiles(near((233, 254, 249), 12), 'cyan main panel', 200, 120)
# callout fill: sample says (214,218,184)-ish; use distance-to-FFFFCC < 45 AND exclude gray by requiring B < 215 and R > 195
call = (np.abs(R - 255) < 55) & (np.abs(G - 255) < 55) & (B > 165) & (B < 225) & (R - B > 30)
out['callout'] = rect_from_profiles(call, 'callout fill', 120, 60)
# orange border CC6600
orange = (np.abs(R - 204) < 60) & (np.abs(G - 102) < 55) & (np.abs(B - 0) < 70) & (R - B > 110)
out['callout_border'] = rect_from_profiles(orange, 'callout orange border', 100, 30)
# vector box: white interior rect + red border. white inside x<215,y<210
white = (R > 240) & (G > 240) & (B > 240)
vm = np.zeros((H, W), bool); vm[95:210, 60:215] = white[95:210, 60:215]
out['vecbox'] = rect_from_profiles(vm, 'vector box white', 25, 12)
red = (R > 120) & (G < 90) & (B < 90)
rm = np.zeros((H, W), bool); rm[95:210, 60:215] = red[95:210, 60:215]
out['vecbox_red'] = rect_from_profiles(rm, 'vector box red border', 8, 3)

# navy panel border 000080
navy = (R < 110) & (G < 110) & (B > 90) & (B - R > 30) & (B - G > 30)
out['panel_border'] = rect_from_profiles(navy, 'navy border', 100, 30)

# title/subtitle
out['title'] = pr('title red ink', *[(int(v)) for v in (
    np.where((red[:, 150:850].sum(axis=1) > 0)[0][ (red[:, 150:850].sum(axis=1) > 0) & (np.arange(H) < 85) ].min()) if False else 0,)] ) if False else None
tr = red[30:80, 150:850]
ys, xs = np.where(tr)
pr('title red ink', 150 + xs.min(), 30 + ys.min(), 150 + xs.max(), 30 + ys.max())
blue = (R < 110) & (G < 110) & (B > 130)
bs = blue[78:112, 150:850]
ys, xs = np.where(bs)
pr('subtitle blue ink', 150 + xs.min(), 78 + ys.min(), 150 + xs.max(), 78 + ys.max())

# vector box inner red ink (excluding border box rows/cols): find red inside the white box
bx0, by0, bx1, by1 = 98, 115, 182, 181  # rough from earlier; refine below
inner_red = red[by0+6:by1-5, bx0+6:bx1-5]
ys, xs = np.where(inner_red)
pr('vector inner red ink', bx0 + 6 + xs.min(), by0 + 6 + ys.min(), bx0 + 6 + xs.max(), by0 + 6 + ys.max())

# --- text lines in main panel ---
ink = (R < 160) & ((B - R > 25) | (R - G > 60) | (G - R > 40) | ((R < 110) & (G < 110) & (B < 110)))
p = out['panel']
px0, py0, px1, py1 = 82, 208, 879, 511  # inside navy border, frame coords
m = np.zeros((H, W), bool); m[py0:py1, px0:px1] = ink[py0:py1, px0:px1]
rowc = m.sum(axis=1)
bands = []
inb = False
for r in range(H):
    if rowc[r] > 3 and not inb: inb, b0 = True, r
    elif rowc[r] <= 3 and inb:
        inb = False
        if r - b0 >= 2: bands.append((b0, r - 1))
print(f"\n== {len(bands)} line bands in main panel (inside x {px0}..{px1}) ==")
for i, (b0, b1) in enumerate(bands):
    xs = np.where(m[b0:b1 + 1].any(axis=0))[0]
    pr(f"line{i} ink", int(xs.min()), b0, int(xs.max()), b1)

# yellow highlight bands
ym = near((255, 255, 0), 65)
print("\n== yellow highlight rows (count>25) ==")
yc = ym[:, px0:px1].sum(axis=1)
inb = False
for r in range(H):
    if yc[r] > 25 and not inb: inb, y0 = True, r
    elif yc[r] <= 25 and inb:
        inb = False
        xs = np.where(ym[y0:r].any(axis=0))[0]
        if r - y0 >= 4 and (xs.max() - xs.min()) > 20:
            pr(f"highlight y {y0}..{r-1}", int(xs.min()), y0, int(xs.max()), r - 1)

# green ink bands
gm = (G > 110) & (R < 110) & (B < 110) & (G - R > 50) & (G - B > 50)
print("\n== green rows (count>8) ==")
gc = gm.sum(axis=1)
inb = False
for r in range(H):
    if gc[r] > 8 and not inb: inb, y0 = True, r
    elif gc[r] <= 8 and inb:
        inb = False
        xs = np.where(gm[y0:r].any(axis=0))[0]
        if r - y0 >= 4:
            pr(f"green y {y0}..{r-1}", int(xs.min()), y0, int(xs.max()), r - 1)

json.dump(out, open('content_measure3.json', 'w'), indent=1)
print("\nsaved content_measure3.json")
