#!/usr/bin/env python3
# m12_iso.py — isolated-window subpixel edges for each highlight rectangle.
import numpy as np
from PIL import Image
from scipy import ndimage

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
frame_im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB")
render = np.asarray(Image.open(S + "/base-1.png").convert("RGB"), dtype=np.float64)
warp = np.asarray(Image.open(S + "/frame_warped_contentfit.png").convert("RGB"), dtype=np.float64)
ax, sx, ay, sy = np.load(S + "/fit_content.npy")

d = np.abs(warp - render).sum(axis=2)

def measure(name, x0, x1, y0, y1, thr=110):
    win = d[y0:y1, x0:x1] > thr
    win = ndimage.median_filter(win, 3)
    colcov = win.mean(axis=0); rowcov = win.mean(axis=1)
    def cross(prof, off):
        idx = np.where(prof > 0.5)[0]
        if len(idx) == 0: return None
        i0, i1 = idx[0], idx[-1]
        def interp(i, up):
            j = i - 1 if up else i + 1
            if j < 0 or j >= len(prof) or prof[i] == prof[j]: return off + i
            t = (0.5 - prof[j]) / (prof[i] - prof[j])
            return off + j + t
        return interp(i0, True), interp(i1, False)
    lx, rx_ = cross(colcov, x0)
    ty, by = cross(rowcov, y0)
    f = 0.48
    print(f"{name}: window x{x0}..{x1} y{y0}..{y1}")
    print(f"  colcov head {colcov[:26].round(2)}")
    print(f"  colcov tail {colcov[-26:].round(2)}")
    print(f"  rowcov head {rowcov[:22].round(2)}")
    print(f"  rowcov tail {rowcov[-22:].round(2)}")
    print(f"  -> render edges L {lx:.1f} R {rx_:.1f} T {ty:.1f} B {by:.1f}")
    print(f"  -> BUILD PT x {lx*f:.2f}..{rx_*f:.2f} (w {(rx_-lx)*f:.2f})  y {ty*f:.2f}..{by*f:.2f} (h {(by-ty)*f:.2f})")
    return (lx * f, rx_ * f, ty * f, by * f)

# H1: encoder-side highlight (window stops before the column gap's connector noise)
h1 = measure("H1 (encoder MHA + left ext)", 1195, 1548, 715, 880)
# H2: decoder-side highlight
h2 = measure("H2 (decoder-side + right ext)", 1548, 1880, 545, 700)
# H1 right-edge refinement in the gap: use only rows deep inside H1's y-band
win = (d[760:830, 1490:1575] > 110)
colcov = ndimage.median_filter(win, 3).mean(axis=0)
print("\nH1 right-edge colcov x1490..1575:", colcov.round(2))
# H2 left-edge: rows deep inside H2's band
win = (d[590:650, 1500:1600] > 110)
colcov = ndimage.median_filter(win, 3).mean(axis=0)
print("H2 left-edge colcov x1500..1600:", colcov.round(2))
np.save(S + "/rects_iso.npy", np.array([h1, h2]))
