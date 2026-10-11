import numpy as np
from PIL import Image
from scipy import ndimage

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_041.jpg").convert("RGB")
im = np.asarray(IM).astype(int)
H, W = im.shape[:2]
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
print(f"frame {W}x{H}")

def comps(mask, label, k=6, minsize=25):
    lab, n = ndimage.label(mask)
    if n == 0:
        print(f"{label}: EMPTY"); return
    sizes = ndimage.sum(mask, lab, range(1, n+1))
    order = np.argsort(sizes)[::-1][:k]
    for i in order:
        if sizes[i] < minsize: continue
        ys, xs = np.where(lab == i+1)
        print(f"{label}[{i}] n={int(sizes[i])}: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  (in: x{xs.min()/72:.2f}..{xs.max()/72:.2f} y{ys.min()/72:.2f}..{ys.max()/72:.2f})")

# --- title: red text, band y 40..110 (no clip) ---
red = (r>130)&(g<80)&(b<80)
red[:40,:] = False; red[110:,:] = False
comps(red, "title-red", 3)
# title text height: rows containing red ink in x 200..760
band = red[:, 200:760]
rows = np.where(band.any(axis=1))[0]
cols = np.where(band.any(axis=0))[0]
print(f"title band rows {rows.min()}..{rows.max()}  cols {cols.min()}..{cols.max()}")

# --- center zoom container: tan EAC08F, tight ---
tan = (abs(r-234)<12)&(abs(g-192)<14)&(abs(b-143)<16)
tan[:, :280] = False; tan[:, 540:] = False  # left half of slide only
comps(tan, "tan-container-tight", 3, 500)

# --- right panel: encoder interior tan-brown E8D0B8, tight ---
enc = (abs(r-232)<10)&(abs(g-208)<10)&(abs(b-184)<12)
enc[:, :540] = False
comps(enc, "encoder-interior-tight", 3, 500)

# --- decoder interior pale green C8E8C0, tight ---
dec = (abs(r-200)<10)&(abs(g-232)<10)&(abs(b-192)<12)
dec[:, :540] = False
comps(dec, "decoder-interior-tight", 3, 500)

# --- left schematic: light green boxes C8E6C9 (SoftMax) in left area ---
c8e6 = (abs(r-200)<12)&(abs(g-230)<10)&(abs(b-201)<12)
c8e6[:, 300:] = False
comps(c8e6, "left-softmax-C8E6C9", 3)

# lavender MatMul C5CAE9
lav = (abs(r-197)<14)&(abs(g-202)<14)&(abs(b-233)<12)
lav[:, 300:] = False
comps(lav, "left-matmul-C5CAE9", 3)

# pale yellow Scale FFF9C4
pyl = (abs(r-255)<12)&(abs(g-249)<10)&(abs(b-196)<14)
pyl[:, 300:] = False
comps(pyl, "left-scale-FFF9C4", 3)

# pink Mask F8BBD0
pnk = (abs(r-248)<10)&(abs(g-187)<12)&(abs(b-208)<12)
pnk[:, 300:] = False
comps(pnk, "left-mask-F8BBD0", 3)

# --- center zoom internals (x 280..540) ---
# pale yellow Linear/Concat FFF8DC
py2 = (abs(r-255)<10)&(abs(g-248)<10)&(abs(b-220)<12)
py2[:, :280] = False; py2[:, 545:] = False
comps(py2, "center-linear-concat-FFF8DC", 6)

# salmon SDPA DE9284
sal = (abs(r-222)<16)&(abs(g-146)<18)&(abs(b-132)<18)
sal[:, :280] = False; sal[:, 545:] = False
comps(sal, "center-salmon-DE9284", 6)

# purple circles V/K 7B4FA0 in center
pur2 = (abs(r-123)<22)&(abs(g-79)<22)&(abs(b-160)<22)
pur2[:, :280] = False; pur2[:, 545:] = False
comps(pur2, "center-purple-VK-7B4FA0", 4)

# red circles q CC2222 center (big red circle = pin too)
red2 = (r>180)&(g<60)&(b<60)
red2[:, :280] = False; red2[:, 545:] = False
comps(red2, "center-red-q/pin", 8)

# --- right panel internals (x>540) ---
# purple masked MHA B39DDB tight
pur3 = (abs(r-179)<16)&(abs(g-157)<16)&(abs(b-219)<16)
pur3[:, :540] = False
comps(pur3, "right-maskedMHA-B39DDB", 3)

# gray blocks A8A8A8 tight
gry = (abs(r-168)<10)&(abs(g-168)<10)&(abs(b-168)<10)
gry[:, :540] = False
comps(gry, "right-gray-A8A8A8", 10)

# brown input embedding C89A6A
brn = (abs(r-200)<12)&(abs(g-154)<12)&(abs(b-106)<14)
brn[:, :540] = False
comps(brn, "right-inputemb-C89A6A", 3)

# maroon output embedding 8B4A4A
mro = (abs(r-139)<16)&(abs(g-74)<16)&(abs(b-74)<16)
mro[:, :540] = False
comps(mro, "right-outputemb-8B4A4A", 3)

# light green Linear/Softmax A8E8A8
lgn = (abs(r-168)<14)&(abs(g-232)<10)&(abs(b-168)<14)
lgn[:, :540] = False
comps(lgn, "right-linear-softmax-A8E8A8", 6)

# yellow highlights FFFF00
ylw = (r>240)&(g>240)&(b<120)
ylw[:, :540] = False
comps(ylw, "right-yellow-highlight", 8)
ylwc = ylw.copy(); ylwc[:, 545:] = False
comps(ylwc, "center-yellow-highlight", 4)

# bright green panel border 00A000 — column/row extents in right area
bg = (r<70)&(g>140)&(g<190)&(b<70)
bg[:, :540] = False
comps(bg, "right-panel-border-00A000", 4, 100)

# dark green brackets/borders 006400
dg = (r<70)&(g>85)&(g<125)&(b<70)
comps(dg, "darkgreen-006400", 8, 40)
