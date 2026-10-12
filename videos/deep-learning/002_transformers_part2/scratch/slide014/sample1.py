from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_014.jpg').convert('RGB')
A = np.asarray(im).astype(int)
def px(x,y): return tuple(A[y,x])
def runs_along(vals, coords):
    out=[]; s=0
    for i in range(1,len(vals)+1):
        if i==len(vals) or vals[i]!=vals[i-1]:
            out.append((vals[i-1], coords[s], coords[i-1])); s=i
    return out
def scanrow(y, x0, x1, step=1, label=""):
    print(f"--- row y={y} {label} ---")
    prev=None; start=x0
    for x in range(x0, x1, step):
        c = tuple(A[y,x])
        key = (c[0]//24, c[1]//24, c[2]//24)
        if key != prev:
            print(f"  x{x}: {c}")
            prev = key; start = x
def scancol(x, y0, y1, step=1, label=""):
    print(f"--- col x={x} {label} ---")
    prev=None
    for y in range(y0, y1, step):
        c = tuple(A[y,x])
        key = (c[0]//24, c[1]//24, c[2]//24)
        if key != prev:
            print(f"  y{y}: {c}")
            prev = key

# Y5 row band: scan row y=470 across fx 300..620
scanrow(470, 300, 625, 1, "Y5/X5 band")
