#!/usr/bin/env python3
"""Content measurement v2: nearest-palette classification, then region bboxes."""
from PIL import Image
import numpy as np, json

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_032.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape

FX0, SX, SY = 18.63, 0.96123, 0.95556
def to_slide(fx, fy): return ((fx - FX0) / SX, fy / SY)

palette = {
    'white':   (255, 255, 255),
    'gray':    (233, 233, 231),
    'cyan':    (224, 247, 250),
    'callout': (255, 255, 204),
    'yellow':  (255, 255, 0),
    'navy':    (0, 0, 128),
    'blue':    (0, 0, 204),
    'green':   (0, 153, 0),
    'red':     (192, 0, 0),
    'orange':  (204, 102, 0),
    'black':   (60, 60, 60),
    'purple':  (106, 90, 205),
}
names = list(palette)
pal = np.array([palette[n] for n in names])
d = np.linalg.norm(a[:, :, None, :] - pal[None, None, :, :], axis=3)
cls = d.argmin(axis=2)
mind = d.min(axis=2)
cls[mind > 95] = -1  # unclassifiable

def bb(name, region=None, maxdist=None):
    m = (cls == names.index(name))
    if maxdist is not None:
        m &= (mind <= maxdist)
    if region:
        x0, y0, x1, y1 = region
        mm = np.zeros((H, W), bool); mm[y0:y1, x0:x1] = m[y0:y1, x0:x1]; m = mm
    ys, xs = np.where(m)
    if not len(ys): return None
    fx0, fy0, fx1, fy1 = int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())
    s0 = to_slide(fx0, fy0); s1 = to_slide(fx1 + 1, fy1 + 1)
    print(f"{name:8s} frame x {fx0}..{fx1} y {fy0}..{fy1}  -> slide x {s0[0]:.1f}..{s1[0]:.1f} y {s0[1]:.1f}..{s1[1]:.1f} (w {s1[0]-s0[0]:.1f} h {s1[1]-s0[1]:.1f}) n={len(ys)}")
    return (fx0, fy0, fx1, fy1, s0[0], s0[1], s1[0], s1[1])

out = {}
print("== global surfaces ==")
out['cyan'] = bb('cyan')
out['callout'] = bb('callout')
out['orange'] = bb('orange')
print("== top band ==")
out['title'] = bb('red', region=(150, 30, 850, 80))
out['subtitle'] = bb('blue', region=(150, 78, 850, 110))
print("== vector box area (x 60..215, y 95..205) ==")
out['vec_red'] = bb('red', region=(60, 95, 215, 205))
out['vec_white'] = bb('white', region=(75, 100, 210, 200))
print("== panel border navy ==")
out['navy'] = bb('navy')

# text-line bands inside cyan panel: dark ink = blue/red/green/black classes
panel = out['cyan'] or (77, 205, 883, 513, 0, 0, 0, 0)
px0, py0, px1, py1 = panel[0] + 5, panel[1] + 5, panel[2] - 4, panel[3] - 4
dark = np.isin(cls, [names.index('blue'), names.index('red'), names.index('green'), names.index('black'), names.index('navy')])
m = np.zeros((H, W), bool); m[py0:py1, px0:px1] = dark[py0:py1, px0:px1]
rowc = m.sum(axis=1)
bands = []
inb = False
for r in range(H):
    if rowc[r] > 3 and not inb: inb, b0 = True, r
    elif rowc[r] <= 3 and inb:
        inb = False
        if r - b0 >= 3: bands.append((b0, r - 1))
print(f"\n== {len(bands)} text-line bands in panel ==")
for i, (b0, b1) in enumerate(bands):
    xs = np.where(m[b0:b1 + 1].any(axis=0))[0]
    s0 = to_slide(xs.min(), b0); s1 = to_slide(xs.max() + 1, b1 + 1)
    print(f"band{i}: frame y {b0}..{b1} (h {b1-b0+1}) x {xs.min()}..{xs.max()} -> slide y {s0[1]:.1f}..{s1[1]:.1f} (h {s1[1]-s0[1]:.1f}) x {s0[0]:.1f}..{s1[0]:.1f}")
    # color spans in this band
    for cn in ('yellow', 'green', 'red', 'blue'):
        cm = (cls[b0:b1 + 1] == names.index(cn))
        ys2, xs2 = np.where(cm)
        if len(xs2) > 10:
            # spans: split columns into contiguous runs
            cols = np.unique(xs2)
            runs = []
            r0 = cols[0]
            for j in range(1, len(cols)):
                if cols[j] != cols[j - 1] + 1:
                    runs.append((r0, cols[j - 1])); r0 = cols[j]
            runs.append((r0, cols[-1]))
            runs = [(a1, b2) for a1, b2 in runs if b2 - a1 >= 3]
            if runs:
                ss = [(to_slide(a1, 0)[0], to_slide(b2 + 1, 0)[0]) for a1, b2 in runs]
                print(f"    {cn}: runs(frame x) {runs[:6]} -> slide x {[(round(a1,1), round(b2,1)) for a1, b2 in ss][:6]}")

json.dump(out, open('content_measure2.json', 'w'), indent=1)
print("\nsaved content_measure2.json")
