# slide 015: build the recolored Figure-1 asset + arrow PNGs, with diagnostics.
# Canvas = shading union (peach|green) baked in; paper figure unmixed/composited on top.
import json
import numpy as np
from PIL import Image, ImageDraw

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1'
FR = f'{BASE}/unique_slides/slide_015.jpg'
OUT = f'{BASE}/recreated_pptx/build/assets'
f15 = np.asarray(Image.open(FR).convert('RGB')).astype(int)
r, g, b = f15[:, :, 0], f15[:, :, 1], f15[:, :, 2]

# ---- 0. paper prep -------------------------------------------------------------
paper_img = Image.open(f'{OUT}/slide014_fig1.png')
if paper_img.mode == 'RGBA':
    bg = Image.new('RGB', paper_img.size, (255, 255, 255))
    bg.paste(paper_img, mask=paper_img.split()[3])
    paper_img = bg
paper = np.asarray(paper_img).astype(int)
PH, PW = paper.shape[:2]  # 2239 x 1520

# ---- 1. precise shading edges ---------------------------------------------------
def peachy(px):
    rr, gg, bb = int(px[0]), int(px[1]), int(px[2])
    return rr > 238 and 215 < gg < 250 and 195 < bb < 240 and (rr - bb) > 15

def greenish(px):
    rr, gg, bb = int(px[0]), int(px[1]), int(px[2])
    return 185 < rr < 235 and gg > 235 and 195 < bb < 240

# vertical extents at pure-shading columns
colP = 583  # between peach left edge and figure paste left (598)
ysP = [y for y in range(95, 535) if peachy(f15[y, colP])]
colG = 882  # right of figure ink (858..874)
ysG = [y for y in range(95, 535) if greenish(f15[y, colG])]
print('peach col', colP, 'rows', ysP[0], '..', ysP[-1], ' n=', len(ysP))
print('green col', colG, 'rows', ysG[0], '..', ysG[-1], ' n=', len(ysG))
top = min(ysP[0], ysG[0]); bot = max(ysP[-1], ysG[-1])

# horizontal extents at a pure row (below boxes? use y=500 — below stacks, above panel bottom)
row = 500
xsP = [x for x in range(565, 900) if peachy(f15[row, x]) or (577 <= x <= 740 and f15[row, x][0] > 238 and f15[row, x][1] > 200)]
# simpler: scan transitions
def runs(mask_row):
    out = []
    inrun = False
    for i, v in enumerate(mask_row):
        if v and not inrun:
            s = i; inrun = True
        elif not v and inrun:
            out.append((s, i - 1)); inrun = False
    if inrun:
        out.append((s, len(mask_row) - 1))
    return out

rowP = [peachy(f15[row, x]) for x in range(560, 910)]
rowG = [greenish(f15[row, x]) for x in range(560, 910)]
print(f'row {row} peach runs:', [(a + 560, b_ + 560) for a, b_ in runs(rowP) if b_ - a > 5])
print(f'row {row} green runs:', [(a + 560, b_ + 560) for a, b_ in runs(rowG) if b_ - a > 5])
row2 = 150
rowP2 = [peachy(f15[row2, x]) for x in range(560, 910)]
rowG2 = [greenish(f15[row2, x]) for x in range(560, 910)]
print(f'row {row2} peach runs:', [(a + 560, b_ + 560) for a, b_ in runs(rowP2) if b_ - a > 5])
print(f'row {row2} green runs:', [(a + 560, b_ + 560) for a, b_ in runs(rowG2) if b_ - a > 5])

# flat cores over pure zones
peach_zone = f15[400:470, 578:592].reshape(-1, 3)
green_zone = f15[400:470, 878:890].reshape(-1, 3)
pq = np.median(peach_zone, axis=0); gq = np.median(green_zone, axis=0)
print('peach flat core:', pq, ' green flat core:', gq)
# uniformity
print('peach std:', peach_zone.std(axis=0), ' green std:', green_zone.std(axis=0))

# ---- 2. diagnostics: circles / keep-colors at mapped positions ------------------
S = 277 / PW   # 0.18224
Sy = 408 / PH
def to_frame(pxx, pyy):
    return 598 + pxx * S, 115 + pyy * Sy

print('\nmapped diagnostics (frame coords -> frame color):')
for tag, (pxx, pyy) in {
    'plus circle enc (490,1560)': (490, 1560),
    'sine circle enc (330,1560)': (330, 1560),
    'plus circle dec (1030,1560)': (1030, 1560),
    'enc MHA center (490,1400)': (490, 1400),
    'enc FF center (490,1035)': (490, 1035),
    'enc AddNorm1 (490,910)': (490, 910),
    'enc AddNorm2 (490,1280)': (490, 1280),
    'dec AddNorm (1030,540)': (1030, 540),
    'dec FF (1030,670)': (1030, 670),
    'dec MHA (1030,980)': (1030, 980),
    'dec AddNorm2 (1030,1220)': (1030, 1220),
    'dec maskedMHA (1030,1375)': (1030, 1375),
}.items():
    fx, fy = to_frame(pxx, pyy)
    c = f15[int(round(fy)), int(round(fx))]
    pc = paper[pyy, pxx]
    print(f'  {tag}: frame({fx:.0f},{fy:.0f}) frame_rgb={tuple(c)} paper_rgb={tuple(pc)}')

# find paper embedding/linear/softmax boxes: colored comps 800..3000 px
from scipy import ndimage
pm = paper.max(axis=2) - paper.min(axis=2)
psat = pm > 18
plab, pn_ = ndimage.label(psat)
sizes = ndimage.sum(psat, plab, range(1, pn_ + 1))
print('\npaper colored comps 800..60000 px:')
for i in range(pn_):
    if 800 <= sizes[i] <= 60000:
        yy, xx = np.where(plab == i + 1)
        core = tuple(int(v) for v in np.median(paper[yy, xx], axis=0))
        print(f'  n={int(sizes[i])} x[{xx.min()},{xx.max()}] y[{yy.min()},{yy.max()}] core={core}')

# ---- 3. ink inventory outside known zones ---------------------------------------
dark = (r < 110) & (g < 110) & (b < 110)
print('\nink outside known zones:')
zones = np.zeros((540, 960), bool)
zones[40:100, 120:840] = True      # title
zones[45:100, 855:925] = True      # badge
zones[100:530, 85:420] = True      # left panel
zones[98:530, 565:900] = True      # right panel
zones[290:325, 450:535] = True     # block arrow
outside = dark & ~zones
print('  dark px outside zones:', outside.sum())
ys, xs = np.where(outside)
if len(ys):
    print('  bbox x[%d,%d] y[%d,%d]' % (xs.min(), xs.max(), ys.min(), ys.max()))

# ---- 4. build canvas asset -------------------------------------------------------
CX0, CY0 = 577, int(top)          # canvas origin (frame px)
CW, CH = 891 - 577 + 1, int(bot) - int(top) + 1
GX = 733 - CX0                    # green zone starts (canvas x)
PX1 = 735 - CX0                   # peach ends
print(f'\ncanvas: origin=({CX0},{CY0}) size {CW}x{CH} green_from_x={GX} peach_to_x={PX1}')
DPI = 600
K = DPI / 72.0  # 8.3333 px per pt
cv = Image.new('RGB', (int(round(CW * K)), int(round(CH * K))), (255, 255, 255))
d = ImageDraw.Draw(cv)
peach_c = tuple(int(v) for v in pq)
green_c = tuple(int(v) for v in gq)
d.rectangle([0, 0, int(round(PX1 * K)) - 1, cv.size[1] - 1], fill=peach_c)
d.rectangle([int(round(GX * K)), 0, cv.size[0] - 1, cv.size[1] - 1], fill=green_c)

# paste paper figure at (598,115) size 277x408 pt -> canvas coords
FIGW, FIGH = 277, 408
fig = paper_img.resize((int(round(FIGW * K)), int(round(FIGH * K))), Image.LANCZOS)
figa = np.asarray(fig).astype(float)
ox = int(round((598 - CX0) * K)); oy = int(round((115 - CY0) * K))
print('figure paste at canvas px:', ox, oy, 'fig size', fig.size)

sh_peach = np.array(peach_c, float); sh_green = np.array(green_c, float)
Hc, Wc = cv.size[1], cv.size[0]
zone_green = np.zeros((figa.shape[0], figa.shape[1]), bool)
xs_ = np.arange(figa.shape[1]) + ox
zone_green[:] = (xs_[None, :] >= int(round(GX * K)))

pal = {
    'orange': np.array([255, 226, 187], float),
    'blue': np.array([194, 232, 247], float),
    'yellow': np.array([242, 244, 193], float),
    'pink': np.array([248, 201, 212], float),
    'lavender': np.array([201, 201, 233], float),
    'green': np.array([198, 224, 198], float),
}
# refine pink/lavender/green cores from the paper itself later if needed; measure now:
for nm, c_ in pal.items():
    dd = np.abs(paper - c_).sum(axis=2)
    m = dd < 30
    if m.sum() > 500:
        print(f'palette {nm}: paper core', np.median(paper[m], axis=0), 'n=', m.sum())

remap = {
    ('enc', 'orange'): np.array([241, 212, 170], float),
    ('enc', 'blue'): np.array([207, 219, 210], float),
    ('dec', 'orange'): np.array([198, 230, 174], float),
    ('dec', 'blue'): np.array([181, 229, 197], float),
}

flat = figa.reshape(-1, 3)
zg = np.repeat(zone_green.reshape(-1), 1)
mx = flat.max(axis=1); mn = flat.min(axis=1)
sat = mx - mn
neutral = sat < 18
# nearest palette
names = list(pal.keys())
P = np.stack([pal[n] for n in names])
dists = np.linalg.norm(flat[:, None, :] - P[None, :, :], axis=2)
ni = np.argmin(dists, axis=1); nd = dists[np.arange(len(flat)), ni]
out = flat.copy()
# neutral unmix
sh = np.where(zg[:, None], sh_green[None, :], sh_peach[None, :])
out_neutral = flat * sh / 255.0
out[neutral] = out_neutral[neutral]
# colored: remap orange/blue by zone; blend by distance for AA
colored = ~neutral
t = np.clip((nd - 40) / 70.0, 0, 1)  # 0 solid at d<=40, 1 at d>=110
for zi, zn in ((0, 'enc'), (1, 'dec')):
    zsel = colored & (zg == (zi == 1))
    for pi, pn_ in enumerate(names):
        if pn_ not in ('orange', 'blue'):
            continue
        sel = zsel & (ni == pi)
        if sel.sum() == 0:
            continue
        tgt = remap[(zn, pn_)]
        solid = np.ones_like(flat) * tgt[None, :]
        un = out_neutral[sel]
        blend = solid[sel] * (1 - t[sel, None]) + un * t[sel, None]
        out[sel] = blend
        print(f'remap {zn}/{pn_}: n={sel.sum()}')
out_img = Image.fromarray(out.reshape(figa.shape).astype(np.uint8))
cv.paste(out_img, (ox, oy))
cv.save(f'{OUT}/slide015_fig1_color.png')
print('saved slide015_fig1_color.png', cv.size)
sidecar = {
    'file': 'slide015_fig1_color.png', 'dpi': DPI,
    'canvas_frame_rect': [CX0, CY0, CX0 + CW - 1, CY0 + CH - 1],
    'w_in': CW / 72, 'h_in': CH / 72,
    'figure_rect_frame': [598, 115, 598 + FIGW - 1, 115 + FIGH - 1],
    'peach': list(peach_c), 'green': list(green_c),
    'green_from_canvas_x': GX, 'peach_to_canvas_x': PX1,
}
json.dump(sidecar, open(f'{OUT}/slide015_fig1_color.json', 'w'), indent=1)
print(json.dumps(sidecar))

# ---- 5. arrow PNGs ---------------------------------------------------------------
# block arrow: polygon in pt relative to (458,295): shaft (0,5)-(54,18); head (54,0),(67,11.5),(54,23)
bw, bh = 68, 24
bim = Image.new('RGBA', (int(round(bw * K)), int(round(bh * K))), (0, 0, 0, 0))
bd = ImageDraw.Draw(bim)
S6 = K
bd.polygon([(0 * S6, 5 * S6), (54 * S6, 5 * S6), (54 * S6, 18 * S6), (0 * S6, 18 * S6)], fill=(204, 0, 0, 255))
bd.polygon([(54 * S6, 0), (67 * S6, 11.5 * S6), (54 * S6, 23 * S6)], fill=(204, 0, 0, 255))
bim.save(f'{OUT}/slide015_blockarrow.png')
print('saved blockarrow', bim.size)

# up arrows: mask-extract from frame
for tag, (x0, x1, y0, y1) in {'up1': (653, 667, 486, 514), 'up2': (739, 751, 115, 141)}.items():
    crop = f15[y0:y1 + 1, x0:x1 + 1].astype(float)
    alpha = np.clip((255 - np.minimum(crop[:, :, 1], crop[:, :, 2])) / 255.0, 0, 1)
    w_, h_ = x1 - x0 + 1, y1 - y0 + 1
    aim = Image.fromarray((alpha * 255).astype(np.uint8)).resize(
        (int(round(w_ * K)), int(round(h_ * K))), Image.BILINEAR)
    oim = Image.new('RGBA', aim.size, (204, 0, 0, 0))
    oim.putalpha(aim)
    oim.save(f'{OUT}/slide015_{tag}.png')
    print(f'saved {tag}: frame rect x[{x0},{x1}] y[{y0},{y1}] size {w_}x{h_}pt ->', oim.size)
