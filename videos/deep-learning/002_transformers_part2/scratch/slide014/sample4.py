from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_014.jpg').convert('RGB')
A = np.asarray(im).astype(int)
def vscan(x, y0, y1, label):
    print(f"--- col x={x} {label} ---")
    prev=None
    for y in range(y0,y1):
        c=tuple(int(v) for v in A[y,x]); key=(c[0]//14,c[1]//14,c[2]//14)
        if key!=prev: print(f"  y{y}: {c}"); prev=key
def hscan(y, x0, x1, label):
    print(f"--- row y={y} {label} ---")
    prev=None
    for x in range(x0,x1):
        c=tuple(int(v) for v in A[y,x]); key=(c[0]//14,c[1]//14,c[2]//14)
        if key!=prev: print(f"  x{x}: {c}"); prev=key
vscan(311, 245, 512, "Y-box left edge strip (fx=311)")
vscan(446, 245, 512, "between Y box right edge & X labels (fx=446)")
hscan(290, 295, 630, "row1 band mid fy=290: Y squares -> X circles")
hscan(415, 295, 630, "row4 band mid fy=415")
