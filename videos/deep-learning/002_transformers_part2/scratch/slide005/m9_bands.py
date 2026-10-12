# m9 (slide005): precise orange band geometry. Alpha-fit ORANGE (ED7D31) of MY frame
# over the warped 001:18 reference; coverage profiles -> band rects + alpha.
# Also: verify the 537px strip (build x730-781) is border-phase artifact via pixel pairs.
from PIL import Image
import numpy as np

myI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg').convert('RGB')
wI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/warped_001_018.png')
my = np.asarray(myI).astype(np.float32)
w = np.asarray(wI).astype(np.float32)

ORANGE = np.array([237, 125, 49], np.float32)
d = ORANGE - w
den = (d * d).sum(axis=2) + 1e-6
a = np.clip(((my - w) * d).sum(axis=2) / den, 0, 1)
res = np.abs(w + a[..., None] * d - my).max(axis=2)
tint = (res < 20) & (a > 0.40) & (a < 0.85)
inner = np.zeros(tint.shape, bool); inner[50:512, 64:896] = True
tint &= inner

def to_build(fx, fy):
    return (fx - 18.0787) / 0.961084, (fy - 0.4700) / 0.957187

# Band b: left region x<740 frame, y 300..410 frame
# Band c: right region x>735 frame
def band_rect(x0, x1, y0, y1, name):
    sub = tint[y0:y1, x0:x1]
    colcov = sub.sum(axis=0)  # per frame-col
    rowcov = sub.sum(axis=1)
    # edges where coverage > 30% of the robust max
    cth = 0.35 * np.percentile(colcov[colcov > 5], 75) if (colcov > 5).any() else 0
    rth = 0.35 * np.percentile(rowcov[rowcov > 5], 75) if (rowcov > 5).any() else 0
    cols = np.where(colcov > cth)[0]
    rows = np.where(rowcov > rth)[0]
    fx0, fx1 = x0 + cols.min(), x0 + cols.max()
    fy0, fy1 = y0 + rows.min(), y0 + rows.max()
    bx0, by0 = to_build(fx0, fy0); bx1, by1 = to_build(fx1, fy1)
    # alpha stats inside the rect (exclude text ink: res<20 already)
    aa = a[fy0:fy1, fx0:fx1][tint[fy0:fy1, fx0:fx1]]
    print(f'{name}: frame x{fx0}..{fx1} y{fy0}..{fy1}  build x{bx0:.1f}..{bx1:.1f} y{by0:.1f}..{by1:.1f}'
          f'  alpha med {np.median(aa):.2f} p25 {np.percentile(aa,25):.2f} p75 {np.percentile(aa,75):.2f} n={aa.size}')
    return (bx0, by0, bx1, by1)

b = band_rect(520, 738, 300, 400, 'band_b(left)')
c = band_rect(738, 900, 200, 400, 'band_c(right)')
# band b full vertical extent (does it reach above y344? below y411?)
band_rect(520, 738, 250, 470, 'band_b_tall')
band_rect(738, 900, 150, 470, 'band_c_tall')

# strip check: pixel pairs in the 537px strip zone
print('== strip probe (my vs gt18-warp) ==')
for (bx, by) in [(733, 230), (737, 260), (740, 290), (735, 320), (760, 250), (770, 300), (750, 200), (745, 400)]:
    fx = int(18.0787 + 0.961084 * bx); fy = int(0.4700 + 0.957187 * by)
    print(f'  build({bx},{by}) my={tuple(int(v) for v in my[fy, fx])} gt18={tuple(int(v) for v in w[fy, fx])}')

# verify orange over specific known boxes (alpha sanity)
for name, bx, by in [('enc_V_circle', 663.5, 400.5), ('enc_K_circle', 695, 400.5), ('enc_Q_circle', 717.5, 400.5),
                     ('Nx_zone', 852, 295), ('crossMHA', 785, 290), ('maskedMHA', 785, 330),
                     ('dec_VKQ_masked', 770, 380), ('encMHA_box', 686, 370)]:
    fx = int(18.0787 + 0.961084 * bx); fy = int(0.4700 + 0.957187 * by)
    reg = slice(fy - 2, fy + 3), slice(fx - 2, fx + 3)
    aa = a[reg][tint[reg]]
    print(f'  {name:16s} my={tuple(int(v) for v in np.median(my[reg].reshape(-1,3),axis=0))} gt18={tuple(int(v) for v in np.median(w[reg].reshape(-1,3),axis=0))} alpha_med={np.median(aa) if aa.size else float("nan"):.2f}')
