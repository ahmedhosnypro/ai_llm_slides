from PIL import Image
import numpy as np
A = np.asarray(Image.open("unique_slides/slide_043.jpg").convert("L"))
B = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("L"))
a = (A[52:78, 500:880] < 120)
b = (B[52:78, 500:880] < 120)
# shift b left content: compare a[y,x] vs b[y,x+8]
b8 = (B[52:78, 508:888] < 120)
inter = (a & b8).sum(); union = (a | b8).sum()
print("IoU at -8 shift:", inter/union, "a n:", a.sum(), "b8 n:", b8.sum())
# residual pattern: which columns mismatch
mism = (a ^ b8)
colmis = mism.sum(axis=0)
print("mismatch by 20-col bucket:", [int(colmis[i:i+20].sum()) for i in range(0,380,20)])
rowmis = mism.sum(axis=1)
print("row mismatch:", list(enumerate([int(v) for v in rowmis])))
