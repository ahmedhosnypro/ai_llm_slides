from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_014.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

def bbox(mask, label):
    ys, xs = np.nonzero(mask)
    if len(xs)==0: print(f"{label}: EMPTY"); return None
    print(f"{label}: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  n={len(xs)}")
    return (xs.min(), xs.max(), ys.min(), ys.max())

# letterbox rows (near-black)
dark = (r<40)&(g<40)&(b<40)
rows_dark = np.nonzero(dark.sum(axis=1) > 400)[0]
print("letterbox dark rows:", rows_dark.min() if len(rows_dark) else None, "..", rows_dark.max() if len(rows_dark) else None)

# blue panel borders (strong blue, darkish): b>120, b-r>60, b-g>60
blue = (b-r>60)&(b-g>50)&(b>110)
print("--- blue structure (panel borders / lines / text) ---")
bbox(blue, "all blue ink")
# columns where blue count is high (vertical borders)
colsum = blue.sum(axis=0)
print("blue col peaks (>=200):", [int(x) for x in np.nonzero(colsum>=200)[0]])
rowsum = blue.sum(axis=1)
print("blue row peaks (>=200):", [int(x) for x in np.nonzero(rowsum>=200)[0]])

# wheat design box F2DEB8
wheat = (abs(r-242)<28)&(abs(g-222)<28)&(abs(b-184)<30)&(r>g)&(g>b)
print("--- wheat box ---")
bbox(wheat, "wheat fill")

# peach Y rows F5CBA7
peach = (abs(r-245)<20)&(abs(g-203)<24)&(abs(b-167)<26)
print("--- peach Y rows ---")
bbox(peach, "peach fill")
rows_peach = np.nonzero(peach.sum(axis=1) > 30)[0]
# group into runs
runs=[]
if len(rows_peach):
    s=rows_peach[0]; p=rows_peach[0]
    for y in rows_peach[1:]:
        if y-p>3: runs.append((s,p)); s=y
        p=y
    runs.append((s,p))
print("peach row runs:", runs)

# pink input nodes FFB6C1
pink = (abs(r-255)<20)&(abs(g-182)<30)&(abs(b-193)<30)
print("--- pink X nodes (left panel) ---")
bbox(pink, "pink")
rows_pink = np.nonzero(pink.sum(axis=1) > 8)[0]
runs=[]
if len(rows_pink):
    s=rows_pink[0]; p=rows_pink[0]
    for y in rows_pink[1:]:
        if y-p>6: runs.append((s,p)); s=y
        p=y
    runs.append((s,p))
print("pink row runs:", runs)
cols_pink = np.nonzero(pink.sum(axis=0) > 5)[0]
print("pink col range:", cols_pink.min() if len(cols_pink) else None, cols_pink.max() if len(cols_pink) else None)

# matrix panel D5F5D5 pale green
mgreen = (abs(r-213)<22)&(abs(g-245)<15)&(abs(b-213)<22)&(g>r)&(g>b)
print("--- matrix panel (pale green) ---")
bbox(mgreen, "palegreen fill")

# red-ish (C00000/CC0000) — title, Σ rims, +, y labels
red = (r>150)&(r-g>90)&(r-b>90)
print("--- red ink ---")
bbox(red[:200,:], "red top band (title, y<200)")

# title text: red in top band
tb = red[40:130,:]
cols_t = np.nonzero(tb.sum(axis=0)>0)[0]
rows_t = np.nonzero(tb.sum(axis=1)>0)[0]
if len(cols_t): print("title red ink: x", cols_t.min(), "..", cols_t.max(), " y", 40+rows_t.min(), "..", 40+rows_t.max())

# dark text (black labels) top band
darktxt = (r<90)&(g<90)&(b<90)
tb2 = darktxt[40:135, :]
ct = np.nonzero(tb2.sum(axis=0)>0)[0]
print("dark ink top band cols:", ct.min() if len(ct) else None, ct.max() if len(ct) else None)
