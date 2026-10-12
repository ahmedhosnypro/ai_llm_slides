# selfcheck_attempt_2 (slide005): closed-loop verification of render_2.
# 1) Band edges via 1D color-step scans (immune to red-border/maroon false positives):
#    scan along a line for the step into/out of the orange blend vs the local base.
# 2) Band alpha via the B-channel lever over known backgrounds (frame vs render).
# 3) Banner border bboxes with a JPEG-tolerant red detector (record).
# 4) Global strong-diff rate + containment.
from PIL import Image
import numpy as np

FX0, FY0 = 18.0787, 0.4700
SX, SY = 0.961084, 0.957187

myI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg').convert('RGB')
rI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide005/render_2.png').convert('RGB')
my = np.asarray(myI).astype(np.float32)
KX, KY = (150.0 / 72.0) / SX, (150.0 / 72.0) / SY
rw = np.asarray(rI.transform((960, 540), Image.AFFINE, (KX, 0.0, -FX0 * KX, 0.0, KY, -FY0 * KY), resample=Image.BILINEAR)).astype(np.float32)
Image.fromarray(rw.astype(np.uint8)).save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/warped_render2.png')

def to_build(fx, fy):
    return (fx - FX0) / SX, (fy - FY0) / SY

def fpx(bx, by):
    return FX0 + SX * bx, FY0 + SY * by

def sample(img, bx, by, rad=2):
    fx, fy = fpx(bx, by)
    return img[int(fy - rad):int(fy + rad + 1), int(fx - rad):int(fx + rad + 1)].reshape(-1, 3).mean(axis=0)

def step_scan(img, bx0, by0, bx1, by1, n=60):
    """sample along a build-pt segment, return positions of large steps (band edges)"""
    vals = []
    for i in range(n + 1):
        t = i / n
        bx = bx0 + (bx1 - bx0) * t
        by = by0 + (by1 - by0) * t
        vals.append(sample(img, bx, by))
    vals = np.array(vals)
    d = np.abs(np.diff(vals, axis=0)).sum(axis=1)
    steps = [(i / n, bx0 + (bx1 - bx0) * (i + 0.5) / n, by0 + (by1 - by0) * (i + 0.5) / n, d[i]) for i in np.where(d > 60)[0]]
    return vals, steps

print('== 1) band edge step-scans (build pt; big steps = edges) ==')
scans = [
    ('b_top   col x620', 620, 340, 620, 375),
    ('b_top   col x700', 700, 340, 700, 375),
    ('b_bot   col x620', 620, 390, 620, 420),
    ('b_bot   col x700', 700, 390, 700, 420),
    ('b_left  row y380', 570, 380, 600, 380),
    ('b_right row y380', 725, 380, 748, 380),
    ('c_top   col x800', 800, 260, 800, 292),
    ('c_top   col x850', 850, 260, 850, 292),
    ('c_bot   col x800', 800, 310, 800, 340),
    ('c_bot   col x860', 860, 310, 860, 340),
    ('c_left  row y300', 738, 300, 762, 300),
    ('c_right row y300', 878, 300, 902, 300),
]
for name, *seg in scans:
    vals_r, steps_r = step_scan(rw, *seg)
    vals_f, steps_f = step_scan(my, *seg)
    def fmt(steps):
        return ' '.join(f'({t:.2f}@{bx:.1f},{by:.1f} d{d:.0f})' for t, bx, by, d in steps[:6]) or 'none'
    print(f'  {name}: R: {fmt(steps_r)}')
    print(f'  {name[0]*9}F: {fmt(steps_f)}' if False else f'  {" ":9s} F: {fmt(steps_f)}')

print('== 2) band alpha B-channel lever (alpha = (B_base - B_obs) / (B_base - 49)) ==')
# known bases from the certified base: peach panel F8DCC4 B=196 (band b zone outside
# boxes), mint panel D9F2D9 B=217 (band c zone right part), tan container C8A888 B=136
for name, bx, by, Bbase in [('b/peachPanel', 600, 365, 196), ('b/tanContainer', 640, 300 - 0 + 62, 136),
                            ('c/mintPanel', 852, 295, 217), ('c/tanBrownBox', 785, 292, 89)]:
    fr = sample(my, bx, by); rr = sample(rw, bx, by)
    af = (Bbase - fr[2]) / (Bbase - 49.0)
    ar = (Bbase - rr[2]) / (Bbase - 49.0)
    print(f'  {name:16s} frame B={fr[2]:.0f} alpha~{af:.2f} | render B={rr[2]:.0f} alpha~{ar:.2f}')

print('== 3) banner border bboxes (JPEG-tolerant red) ==')
def redink(img, x0, x1, y0, y1):
    r_, g_, b_ = img[..., 0], img[..., 1], img[..., 2]
    m = (r_ > 140) & (r_ - g_ > 45) & (r_ - b_ > 35)
    sub = m[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if not len(xs):
        return None
    return (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max())
for name, (x0, x1, y0, y1) in [('banner1_border', (60, 520, 90, 150)), ('banner2_border', (90, 460, 152, 212))]:
    fr = redink(my, x0, x1, y0, y1); rr = redink(rw, x0, x1, y0, y1)
    if fr and rr:
        bx0f, by0f = to_build(fr[0], fr[2]); bx1f, by1f = to_build(fr[1], fr[3])
        bx0r, by0r = to_build(rr[0], rr[2]); bx1r, by1r = to_build(rr[1], rr[3])
        print(f'  {name}: frame x{bx0f:.1f}..{bx1f:.1f} y{by0f:.1f}..{by1f:.1f} | render x{bx0r:.1f}..{bx1r:.1f} y{by0r:.1f}..{by1r:.1f} | dev L{bx0r-bx0f:+.1f} R{bx1r-bx1f:+.1f} T{by0r-by0f:+.1f} B{by1r-by1f:+.1f}')
    else:
        print(f'  {name}: frame={fr} render={rr}')

print('== 4) global + containment ==')
dd = np.abs(my - rw).sum(axis=2)
print('  strong-pixel rate %.1f%% (baseline 15.4%%)' % (100 * (dd[46:514, 60:900] > 120).mean()))
for name, (x, y, w_, h_) in [('band_b', (583, 357.5, 151, 46)), ('band_c', (748.5, 276.5, 139.5, 48))]:
    print(f'  {name}: inside panel {x >= 42 and y >= 45 and x + w_ <= 918 and y + h_ <= 538}')
