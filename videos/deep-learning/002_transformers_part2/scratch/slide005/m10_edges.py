# m10 (slide005): directed edge scans for the two orange bands using the alpha-fit
# tint map (windowed fraction), plus my frame's own yellow-band mask vs 017's rects.
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
tint = (res < 26) & (a > 0.42) & (a < 0.88)

def to_build_x(fx): return (fx - 18.0787) / 0.961084
def to_build_y(fy): return (fy - 0.4700) / 0.957187
def to_frame_x(bx): return 18.0787 + 0.961084 * bx
def to_frame_y(by): return 0.4700 + 0.957187 * by

def frac(fx, fy, rad=3):
    x0, x1 = int(fx - rad), int(fx + rad + 1)
    y0, y1 = int(fy - rad), int(fy + rad + 1)
    return tint[y0:y1, x0:x1].mean()

def scan_axis(fixed, lo, hi, axis, name, thresh=0.5):
    """find first/last position where tint fraction > thresh"""
    hits = []
    for t in range(lo, hi):
        fx, fy = (t, fixed) if axis == 'x' else (fixed, t)
        if frac(fx, fy) > thresh:
            hits.append(t)
    if not hits:
        print(f'  {name}: NO tint above {thresh}')
        return
    print(f'  {name}: tint frames {hits[0]}..{hits[-1]}  build {to_build_x(hits[0]) if axis=="x" else to_build_y(hits[0]):.1f}..{to_build_x(hits[-1]) if axis=="x" else to_build_y(hits[-1]):.1f}')

print('== band b edges ==')
for by in (365, 380, 395):
    scan_axis(int(to_frame_y(by)), 500, 620, 'x', f'b_left  y={by}')
for bx in (600, 650, 700):
    scan_axis(int(to_frame_x(bx)), 310, 370, 'y', f'b_top   x={bx}')
    scan_axis(int(to_frame_x(bx)), 390, 430, 'y', f'b_bot   x={bx}')
for by in (365, 385):
    scan_axis(int(to_frame_y(by)), 700, 760, 'x', f'b_right y={by}')

print('== band c edges ==')
for by in (285, 300):
    scan_axis(int(to_frame_y(by)), 840, 910, 'x', f'c_right y={by}')
    scan_axis(int(to_frame_y(by)), 720, 770, 'x', f'c_left  y={by}')
for bx in (770, 800, 830, 860):
    scan_axis(int(to_frame_x(bx)), 240, 290, 'y', f'c_top   x={bx}')
    scan_axis(int(to_frame_x(bx)), 390, 440, 'y', f'c_bot   x={bx}')

# my frame's own yellow-band mask (bright yellow pixels)
yel = (my[..., 0] > 200) & (my[..., 1] > 200) & (my[..., 2] < 150)
inner = np.zeros(yel.shape, bool); inner[50:512, 64:896] = True
yel &= inner
print('== my-frame yellow mask: rows with >20px ==')
rows = np.where(yel.sum(axis=1) > 20)[0]
if len(rows):
    # group into runs
    runs = []
    s = rows[0]; p = rows[0]
    for r in rows[1:]:
        if r - p > 4:
            runs.append((s, p)); s = r
        p = r
    runs.append((s, p))
    for (r0, r1) in runs:
        cols = np.where(yel[r0:r1 + 1].sum(axis=0) > 2)[0]
        print(f'  y {r0}..{r1} (build {to_build_y(r0):.0f}..{to_build_y(r1):.0f})  x {cols.min()}..{cols.max()} (build {to_build_x(cols.min()):.0f}..{to_build_x(cols.max()):.0f})')
