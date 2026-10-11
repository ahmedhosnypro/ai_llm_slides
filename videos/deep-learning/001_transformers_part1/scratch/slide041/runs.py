import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_041.jpg").convert("RGB")).astype(int)

def runs_along(axis_vals, coords, label, tol=14):
    print(f"--- {label} ---")
    out = []
    start = 0
    cur = axis_vals[0]
    for i in range(1, len(axis_vals)):
        if abs(axis_vals[i][0]-cur[0])>tol or abs(axis_vals[i][1]-cur[1])>tol or abs(axis_vals[i][2]-cur[2])>tol:
            out.append((coords[start], coords[i-1], tuple(int(v) for v in cur)))
            start = i; cur = axis_vals[i]
        else:
            cur = [(cur[j]*0.8 + axis_vals[i][j]*0.2) for j in range(3)]
    out.append((coords[start], coords[-1], tuple(int(v) for v in cur)))
    for s,e,c in out:
        if e-s >= 2:
            print(f"  {s:4d}..{e:4d} rgb{c}")

y = 300
runs_along(im[y,:,:], list(range(im.shape[1])), f"row y={y}")
y = 480
runs_along(im[y,:,:], list(range(im.shape[1])), f"row y={y}")
x = 420
runs_along(im[:,x,:], list(range(im.shape[0])), f"col x={x}")
x = 660
runs_along(im[:,x,:], list(range(im.shape[0])), f"col x={x}")
