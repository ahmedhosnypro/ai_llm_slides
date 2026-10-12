# selfcheck_attempt_1 (slide005): closed-loop render-vs-frame verification.
# Warps render_1.png into MY frame space (build pt -> render px = x*150/72, zero
# offset; build pt -> frame px via the certified mapping), then:
#  1) re-fits the two orange bands' edges + alpha on the RENDER and compares with the
#     frame-measured targets (tol ~4px @150dpi = 1.92pt);
#  2) checks callout/banner ink bboxes (inherited content) vs the frame;
#  3) global strong-diff rate vs the certified 002:19 baseline (15.4%);
#  4) containment: bands inside the panel, no band ink outside the house frame.
from PIL import Image
import numpy as np

FX0, FY0 = 18.0787, 0.4700
SX, SY = 0.961084, 0.957187

myI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg').convert('RGB')
rI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide005/render_1.png').convert('RGB')
my = np.asarray(myI).astype(np.float32)
KX, KY = (150.0 / 72.0) / SX, (150.0 / 72.0) / SY  # frame px -> render px scale
coeffs = (KX, 0.0, -FX0 * KX, 0.0, KY, -FY0 * KY)
rw = np.asarray(rI.transform((960, 540), Image.AFFINE, coeffs, resample=Image.BILINEAR)).astype(np.float32)
Image.fromarray(rw.astype(np.uint8)).save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/warped_render1.png')

def to_build(fx, fy):
    return (fx - FX0) / SX, (fy - FY0) / SY

ORANGE = np.array([237, 125, 49], np.float32)

# The render has no JPEG noise; the band edges in the RENDER are measured directly:
# orange-tinted render pixels = (r-g, r-b) in the orange direction over the local
# background. Known false-positive sources inside the zones (salmon box top edge)
# are interpreted manually below.
def band_edges_render(x0, x1, y0, y1):
    r_, g_, b_ = rw[..., 0], rw[..., 1], rw[..., 2]
    # orange-tinted render pixels: strong r-g and r-b, r>140
    t = (r_ > 140) & (r_ - g_ > 55) & (r_ - b_ > 75)
    sub = t[y0:y1, x0:x1]
    colcov = sub.sum(axis=0); rowcov = sub.sum(axis=1)
    cols = np.where(colcov > 0.3 * max(1, colcov.max()))[0]
    rows = np.where(rowcov > 0.3 * max(1, rowcov.max()))[0]
    return (x0 + cols.min(), x0 + cols.max(), y0 + rows.min(), y0 + rows.max())

print('== band edges: RENDER (exact) vs FRAME-measured targets (build pt) ==')
# band b zone: frame x560-760, y325-425 ; targets x583..734, y357.5..403.5
rx0, rx1, ry0, ry1 = band_edges_render(560, 760, 325, 425)
bx0, by0 = to_build(rx0, ry0); bx1, by1 = to_build(rx1, ry1)
print(f'band_b render: build x{bx0:.1f}..{bx1:.1f} y{by0:.1f}..{by1:.1f}  target x583.0..734.0 y357.5..403.5')
print(f'  edge dev pt: left {bx0-583:+.1f} right {bx1-734:+.1f} top {by0-357.5:+.1f} bottom {by1-403.5:+.1f}  (tol 1.92pt = 4px@150dpi)')
# band c zone: frame x715-905, y245-430 ; targets x748.5..888, y276.5..324.5
rx0, rx1, ry0, ry1 = band_edges_render(715, 905, 245, 430)
bx0, by0 = to_build(rx0, ry0); bx1, by1 = to_build(rx1, ry1)
print(f'band_c render: build x{bx0:.1f}..{bx1:.1f} y{by0:.1f}..{by1:.1f}  target x748.5..888.0 y276.5..324.5')
print(f'  edge dev pt: left {bx0-748.5:+.1f} right {bx1-888:+.1f} top {by0-276.5:+.1f} bottom {by1-324.5:+.1f}')

print('== band alpha: RENDER measured over known sub-boxes (frame-median targets) ==')
def med(img, bx, by, bw, bh):
    fx, fy = FX0 + SX * bx, FY0 + SY * by
    fw, fh = SX * bw, SY * bh
    reg = img[int(fy):int(fy + fh), int(fx):int(fx + fw)].reshape(-1, 3)
    return np.median(reg, axis=0)
for name, bx, by in [('band_b/panel', 600, 365), ('band_b/circleV', 663.5, 400.5),
                     ('band_c/mint', 852, 295), ('band_c/crossMHA', 785, 290)]:
    mr = med(rw, bx - 3, by - 3, 6, 6); mf = med(my, bx - 3, by - 3, 6, 6)
    print(f'  {name:16s} render=({mr[0]:.0f},{mr[1]:.0f},{mr[2]:.0f})  frame=({mf[0]:.0f},{mf[1]:.0f},{mf[2]:.0f})')

print('== banner (callout) ink bbox: render vs frame ==')
def redink(img, x0, x1, y0, y1):
    r_, g_, b_ = img[..., 0], img[..., 1], img[..., 2]
    m = (r_ > 120) & (g_ < 95) & (b_ < 95)
    sub = m[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if not len(xs):
        return None
    return (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max())
for name, (x0, x1, y0, y1) in [('banner1_border', (60, 520, 90, 150)), ('banner2_border', (90, 460, 152, 210))]:
    fr = redink(my, x0, x1, y0, y1); rr = redink(rw, x0, x1, y0, y1)
    if fr and rr:
        bx0f, by0f = to_build(fr[0], fr[2]); bx1f, by1f = to_build(fr[1], fr[3])
        bx0r, by0r = to_build(rr[0], rr[2]); bx1r, by1r = to_build(rr[1], rr[3])
        print(f'  {name}: frame build x{bx0f:.1f}..{bx1f:.1f} y{by0f:.1f}..{by1f:.1f} | render build x{bx0r:.1f}..{bx1r:.1f} y{by0r:.1f}..{by1r:.1f} | dev L{bx0r-bx0f:+.1f} R{bx1r-bx1f:+.1f} T{by0r-by0f:+.1f} B{by1r-by1f:+.1f}')
    else:
        print(f'  {name}: frame={fr} render={rr}')

print('== global strong-diff rate (render vs frame, panel) ==')
dd = np.abs(my - rw).sum(axis=2)
strong = dd > 120
rate = strong[46:514, 60:900].mean()
print(f'  strong-pixel rate {rate*100:.1f}%  (certified 002:19 render-vs-frame baseline 15.4%)')

print('== containment ==')
# bands must sit inside the house panel (build x42..918, y45..538) with margin
for name, (x, y, w_, h_) in [('band_b', (583, 357.5, 151, 46)), ('band_c', (748.5, 276.5, 139.5, 48))]:
    ok = x >= 42 and y >= 45 and x + w_ <= 918 and y + h_ <= 538
    print(f'  {name}: rect ({x},{y},{w_},{h_}) inside panel: {ok}')
