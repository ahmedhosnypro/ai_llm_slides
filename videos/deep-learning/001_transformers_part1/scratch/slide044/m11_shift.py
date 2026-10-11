from PIL import Image
import numpy as np
A = np.asarray(Image.open("unique_slides/slide_043.jpg").convert("L"), dtype=np.float32)
B = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("L"), dtype=np.float32)
def best_shift(x0,x1,y0,y1,r=8):
    a = A[y0:y1, x0:x1]
    best=(1e18,0,0)
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            b = B[y0+dy:y1+dy, x0+dx:x1+dx]
            e = np.abs(a-b).mean()
            if e<best[0]: best=(e,dx,dy)
    return best
print("cards region (quiet):", best_shift(100,700,300,500))
print("title line1:", best_shift(510,880,52,78))
print("title line2 (left of inset):", best_shift(600,735,78,100))
print("vecbox:", best_shift(398,505,48,76))
print("legend:", best_shift(736,908,462,530))
