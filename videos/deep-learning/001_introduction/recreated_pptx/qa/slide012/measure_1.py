from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print("size", W, "x", H)

def modal(px_block):
    vals = [tuple(p) for p in px_block.reshape(-1,3)]
    from collections import Counter
    return Counter(vals).most_common(3)

# 1. Find chrome panel + top rule region: column profile of red-ish pixels rows 0..60
print("\n== rows 30..60 red-ish (R>120, G<60, B<60) count per row ==")
for y in range(30, 62):
    red = sum(1 for x in range(W) if a[y,x,0]>120 and a[y,x,1]<70 and a[y,x,2]<70)
    if red > 50: print(" row", y, "red px:", red, "sample", tuple(a[y,480]))

# 2. Black footer bar rows
print("\n== dark rows (y>480): count of very dark px per row ==")
for y in range(480, H):
    dark = sum(1 for x in range(W) if a[y,x].sum() < 150)
    if dark > 50: print(" row", y, "dark:", dark, "x-range:", end=" ")
    if dark > 50:
        xs = [x for x in range(W) if a[y,x].sum() < 150]
        print(xs[0], "..", xs[-1])

# 3. Scan for title box + content box: find rows/cols with blue-ish border (navy/blue)
print("\n== bluish border px (B>90, B-R>30, B-G>30) per row 50..450 ==")
rows = {}
for y in range(50, 460):
    bl = [x for x in range(W) if a[y,x,2]>90 and a[y,x,2]-a[y,x,0]>30 and a[y,x,2]-a[y,x,1]>30]
    if len(bl) > 20: rows[y] = (len(bl), bl[0], bl[-1])
for y in sorted(rows): print(" row", y, rows[y])
