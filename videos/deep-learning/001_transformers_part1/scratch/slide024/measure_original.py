# PIL measurement of the ORIGINAL frame slide_024.jpg (960x540, 1px = 1pt = 1/72in)
# Prints bounding boxes of color-classified regions. Scratch-only tool.
from PIL import Image
import numpy as np
import sys

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_024.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

def near(hexcolor, tol):
    r, g, b = int(hexcolor[0:2], 16), int(hexcolor[2:4], 16), int(hexcolor[4:6], 16)
    d = np.abs(a - np.array([r, g, b])).sum(axis=2)
    return d <= tol

def bbox(mask, label, minpx=30):
    ys, xs = np.nonzero(mask)
    if len(xs) < minpx:
        print(f"{label:28s} : ABSENT ({len(xs)} px)")
        return None
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    print(f"{label:28s} : x[{x0:4d},{x1:4d}] y[{y0:4d},{y1:4d}] center=({cx:.0f},{cy:.0f}) px={len(xs)}  in: x[{x0/72:.2f},{x1/72:.2f}] y[{y0/72:.2f},{y1/72:.2f}] ctr=({cx/72:.2f},{cy/72:.2f})in")
    return (x0, x1, y0, y1)

# --- big circle: pale cyan fill E4F7F7
bbox(near('E4F7F7', 24), 'BIG CIRCLE fill E4F7F7')
# --- sentence box: pure white (inside frame area) -- white margin + box both white
bbox(near('FFFFFF', 12), 'WHITE (margin+sentbox)')
# --- word nodes pale yellow FBF9CF
bbox(near('FBF9CF', 20), 'YELLOW nodes FBF9CF')
# --- green Boy nodes C9F29B
bbox(near('C9F29B', 24), 'GREEN Boy nodes C9F29B')
# --- red arrows EE0000
bbox(near('EE0000', 90), 'RED arrows EE0000 (loose)')
# --- blue vector outline 4472C4
bbox(near('4472C4', 60), 'BLUE outline 4472C4')
# --- light blue bars 8FBCE6
bbox(near('8FBCE6', 45), 'LTBLUE bars 8FBCE6')
# --- orange bars FF6600
bbox(near('FF6600', 70), 'ORANGE bars FF6600')
# --- orange outline FF4000
bbox(near('FF4000', 60), 'ORANGE outline FF4000')
# --- pink hatch F2B8B8
bbox(near('F2B8B8', 40), 'PINK hatch F2B8B8')
# --- badge FDFD96
bbox(near('FDFD96', 40), 'BADGE FDFD96')

# --- per-cluster analysis: label connected components of key masks with scipy
try:
    from scipy import ndimage
    def clusters(hexcolor, tol, label, minpx=40):
        m = near(hexcolor, tol)
        lab, n = ndimage.label(m)
        print(f"--- clusters {label} (n={n}) ---")
        out = []
        for i in range(1, n + 1):
            ys, xs = np.nonzero(lab == i)
            if len(xs) < minpx:
                continue
            x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            print(f"  {label}[{i:2d}] x[{x0:4d},{x1:4d}] y[{y0:4d},{y1:4d}] w={x1-x0+1:3d} h={y1-y0+1:3d} ctr=({cx:.0f},{cy:.0f}) px={len(xs)}")
            out.append((cx, cy, x0, x1, y0, y1, len(xs)))
        return out
    clusters('FBF9CF', 24, 'YELLOW', 100)
    clusters('C9F29B', 30, 'GREEN', 100)
    clusters('8FBCE6', 60, 'LTBLUE', 25)
    clusters('FF6600', 90, 'ORANGE', 25)
    clusters('F2B8B8', 60, 'PINK', 200)
    clusters('E4F7F7', 30, 'CYAN', 500)
except ImportError:
    print("scipy unavailable")
