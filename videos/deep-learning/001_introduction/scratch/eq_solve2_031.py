import sys
sys.path.insert(0, "/home/ahmed/Projects/ai_llm_slides/scripts")
import render_eq
from PIL import Image
import numpy as np

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/matrix_test"

# Targets (frame pt): theta glyph w16 h18 (y 401..418, baseline=bottom~418);
# sub digit w~12 h~11, bottom ~5.5 below baseline; row ink total 23 (top..sub bottom).

def split_ink(png):
    im = Image.open(png).convert("RGBA")
    a = np.asarray(im).astype(int)
    ink = a[:, :, 3] > 40
    colc = ink.sum(axis=0)
    onc = colc > 0
    runs = []; s = None
    for x, v in enumerate(onc):
        if v and s is None: s = x
        if not v and s is not None: runs.append((s, x - 1)); s = None
    if s is not None: runs.append((s, len(onc) - 1))
    # theta = first run cluster; sub = last runs (gap >= 4px separates them)
    # find the largest horizontal gap
    gaps = [(runs[i+1][0] - runs[i][1], i) for i in range(len(runs)-1)]
    gaps.sort()
    if gaps and gaps[-1][0] >= 4:
        i = gaps[-1][1]
        th = (runs[0][0], runs[i][1]); su = (runs[i+1][0], runs[-1][1])
    else:
        th = (runs[0][0], runs[-1][1]); su = None
    def yext(x0, x1):
        rows = np.where(ink[:, x0:x1+1].any(axis=1))[0]
        return (rows[0], rows[-1]) if len(rows) else None
    thy = yext(*th)
    suy = yext(*su) if su else None
    return th, thy, su, suy

for fs in [34, 36, 38, 40, 42]:
    p = f"{OUT}_solve_{fs}.png"
    info = render_eq.render(r"\theta_1", p, fs, "#000000")
    im = Image.open(p)
    W, H = im.size
    th_x, th_y, su_x, su_y = split_ink(p)
    to_pt = lambda v: v / 600 * 72
    print(f"fs={fs}: PNG {W}x{H} baseline_frac={info['baseline_frac']}")
    print(f"  theta: w={to_pt(th_x[1]-th_x[0]+1):.1f} h={to_pt(th_y[1]-th_y[0]+1):.1f}pt (targets w16 h18)")
    if su_x:
        print(f"  sub:   w={to_pt(su_x[1]-su_x[0]+1):.1f} h={to_pt(su_y[1]-su_y[0]+1):.1f}pt "
              f"below-baseline={to_pt(su_y[1] - info['baseline_px']):.1f} (targets w12 h11 below 5.5)")
    rows_all = np.where((np.asarray(Image.open(p).convert("RGBA"))[:, :, 3] > 40).any(axis=1))[0]
    print(f"  total ink h={to_pt(rows_all[-1]-rows_all[0]+1):.1f}pt (target 23)")
