from PIL import Image
import numpy as np

im = Image.open("videos/deep-learning/001_introduction/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print("size", W, H)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

# color masks
red    = (R>150) & (G<90) & (B<90)                       # C00000-ish (title, bullets, box border, frame)
blue   = (B>120) & (B-R>60) & (B-G>60)                   # 1F1FB4-ish (body, borders)
dark   = (R<90) & (G<90) & (B<90)                        # black-ish (matrix glyphs, bottom bar)
graybg = (abs(R-236)<14) & (abs(G-236)<14) & (abs(B-236)<14)  # ECECEC field
white  = (R>240) & (G>240) & (B>240)

def bbox(mask, name, x0=0, x1=W, y0=0, y1=H):
    m = mask[y0:y1, x0:x1]
    rows = np.where(m.any(axis=1))[0]; cols = np.where(m.any(axis=0))[0]
    if len(rows)==0:
        print(f"{name}: EMPTY in region"); return None
    r = (x0+cols[0], y0+rows[0], x0+cols[-1], y0+rows[-1])
    print(f"{name}: x {r[0]}..{r[2]}  y {r[1]}..{r[3]}  (w={r[2]-r[0]+1}, h={r[3]-r[1]+1})")
    return r

print("\n--- whole-slide structure ---")
bbox(graybg, "gray ECECEC field")
bbox(white, "white pixels")
bbox(red & (np.arange(H)[:,None]<150), "red ink y<150 (title band?)")

# title band: strong red rows in top third
rowred = red[:200].sum(axis=1)
tr = np.where(rowred>8)[0]
print("rows with >8 red px in y<200:", tr.min() if len(tr) else None, "..", tr.max() if len(tr) else None)

print("\n--- title ink bbox (y 55..130) ---")
bbox(red, "title red ink", 0, W, 55, 130)

print("\n--- content box (blue border) search y 110..380 ---")
bbox(blue, "blue ink y110..380", 0, W, 110, 380)
# blue border lines: rows/cols with many blue px
sub = blue[110:380]
rowb = sub.sum(axis=1); colb = sub.sum(axis=0)
br = np.where(rowb>200)[0]+110
print("blue border rows (>200px):", br[:12], "...", br[-12:] if len(br)>12 else "")
bc = np.where(colb>100)[0]
print("blue border cols (>100px):", bc[:12], "...", bc[-12:] if len(bc)>12 else "")

print("\n--- blue text lines inside content box ---")
# inside borders, find text rows
if len(br)>=2 and len(bc)>=2:
    y_top, y_bot = br[0], br[-1]
    x_l, x_r = bc[0], bc[-1]
    inner = blue[y_top+4:y_bot-4, x_l+4:x_r-4]
    rowi = inner.sum(axis=1)
    on = rowi > 3
    # find contiguous bands
    bands=[]; s=None
    for i,v in enumerate(on):
        if v and s is None: s=i
        if not v and s is not None:
            if i-s>3: bands.append((s+y_top+4, i-1+y_top+4))
            s=None
    if s is not None: bands.append((s+y_top+4, len(on)-1+y_top+4))
    print("content box border bbox:", (x_l, y_top, x_r, y_bot))
    for b in bands:
        m = blue[b[0]:b[1]+1, x_l+4:x_r-4]
        cols2 = np.where(m.any(axis=0))[0]
        print(f"  blue text band y {b[0]}..{b[1]}  x {x_l+4+cols2[0]}..{x_l+4+cols2[-1]}")

print("\n--- red bullet text (y 300..380, x 90..700) ---")
bbox(red, "red bullets", 90, 700, 280, 385)

print("\n--- bottom area: label box + matrix box (y 380..540) ---")
bbox(blue, "blue ink y380..540", 0, W, 380, 540)
bbox(red,  "red ink y360..540", 0, W, 360, 540)
sub2 = red[360:540]
rowr = sub2.sum(axis=1)
rr = np.where(rowr>60)[0]+360
print("red border rows (>60px) in y360..540:", rr)
sub3 = red[380:520, 590:870]
colr = sub3.sum(axis=0)
rc = np.where(colr>40)[0]+590
print("red border cols (>40px) in x590..870:", rc)
sub4 = blue[400:500, 350:620]
colb2 = sub4.sum(axis=0); rowb2 = sub4.sum(axis=1)
print("label box blue cols (>25px):", (np.where(colb2>25)[0]+350))
print("label box blue rows (>25px):", (np.where(rowb2>25)[0]+400))

print("\n--- matrix black ink inside red box ---")
if len(rr)>=2 and len(rc)>=2:
    my0, my1 = rr[0], rr[-1]; mx0, mx1 = rc[0], rc[-1]
    bbox(dark, "matrix dark ink", mx0+3, mx1-3, my0+3, my1-3)
    bbox(dark, "any dark ink y360..530 x560..900", 560, 900, 360, 530)

print("\n--- bottom black bar ---")
bbox(dark & (np.arange(H)[:,None]>500), "dark y>500")
rowdark = dark[500:540].sum(axis=1)
for y in range(500, 540):
    if dark[y].sum() > 800: print("full-width dark row at y", y); break

print("\n--- tooltip region (x 0..170, y 480..525) ---")
tt = a[480:525, 0:170]
print("mean color tooltip region:", tt.reshape(-1,3).mean(axis=0).round(1))

print("\n--- color samples ---")
def sample(x,y,n=2): print(f"({x},{y}) ->", a[y,x], " region mean:", a[max(0,y-n):y+n, max(0,x-n):x+n].reshape(-1,3).mean(axis=0).round(0))
sample(480, 30)   # top outside panel
sample(480, 95)   # title area bg
sample(480, 200)  # inside content box
sample(480, 420)  # between label and bottom
sample(200, 480)  # gray field lower left
sample(30, 300)   # left margin outside panel
sample(940, 300)  # right margin outside panel
sample(480, 530)  # very bottom
