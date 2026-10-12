#!/usr/bin/env python3
"""Resume verification: re-derive the banked measurements straight from the ground-truth
frame before trusting them, + title font forensics (Arial-Bold vs serif, cap/advance fit)."""
from PIL import Image, ImageFont
import numpy as np

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_030.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = 0.299 * R + 0.587 * G + 0.114 * B
red = (R > 130) & (G < 90) & (B < 90)
black = lum < 60
print("frame size:", im.size)

def vres(name, got, want, tol=2):
    ok = all(abs(g - w) <= tol for g, w in zip(got, want))
    print(f"  {name}: got {got} want {want} {'OK' if ok else 'MISMATCH'}")

# ---- 1. left panel border (want x85..478, y235..476) ----
print("== left panel edges ==")
vres("left  x@y350", [int(np.where(red[350, 80:100])[0].min()) + 80, int(np.where(red[350, 80:100])[0].max()) + 80], [85, 86])
vres("right x@y350", [int(np.where(red[350, 470:490])[0].min()) + 470, int(np.where(red[350, 470:490])[0].max()) + 470], [478, 478])
vres("top   y@x300", [int(np.where(red[225:245, 300])[0].min()) + 225, int(np.where(red[225:245, 300])[0].max()) + 225], [235, 235])
vres("bot   y@x300", [int(np.where(red[465:485, 300])[0].min()) + 465, int(np.where(red[465:485, 300])[0].max()) + 465], [476, 476])

# ---- 2. right panel border (want top 270 x535..883, bottom 444 x534..884, right x884) ----
print("== right panel edges ==")
vres("top   y@x700", [int(np.where(red[260:280, 700])[0].min()) + 260, int(np.where(red[260:280, 700])[0].max()) + 260], [270, 270])
vres("bot   y@x700", [int(np.where(red[435:455, 700])[0].min()) + 435, int(np.where(red[435:455, 700])[0].max()) + 435], [444, 444])
vres("right x@y350", [int(np.where(red[350, 875:895])[0].min()) + 875, int(np.where(red[350, 875:895])[0].max()) + 875], [884, 884])
lb = np.where(red[350, 525:545])[0]
print("  left border @y350 x525..545:", "NONE" if len(lb) == 0 else f"x{[int(v)+525 for v in lb]}")
tb = red[270, 520:900]
xs = np.where(tb)[0]
print(f"  top border run @y270: x{int(xs.min())+520}..{int(xs.max())+520}")

# ---- 3. title (want x117..869 y83..116, cap 'A' y84..107) ----
print("== title ==")
tr = red[70:130, 100:900]
ys, xs = np.where(tr)
vres("title bbox", [int(xs.min()) + 100, int(xs.max()) + 100, int(ys.min()) + 70, int(ys.max()) + 70], [117, 869, 83, 116], tol=3)
cap = tr[:, 17:30]  # 'A' region (x117..130)
ys2 = np.where(cap.any(axis=1))[0]
print(f"  'A' rows y{int(ys2.min())+70}..{int(ys2.max())+70} (cap height {int(ys2.max()-ys2.min())+1}, want 24)")
tcol = a[100, 250]
print(f"  title ink sample @ (250,100): #{tcol[0]:02X}{tcol[1]:02X}{tcol[2]:02X} (JPEG-darkened C00000 family)")

# ---- 4. photo bbox (want x105..442 y284..454) ----
print("== left photo ==")
# non-white, non-red ink inside panel interior (x88..476, y240..474)
sub = a[240:474, 88:476]
sl = 0.299 * sub[:, :, 0] + 0.587 * sub[:, :, 1] + 0.114 * sub[:, :, 2]
sr = (sub[:, :, 0] > 130) & (sub[:, :, 1] < 90) & (sub[:, :, 2] < 90)
sw = (sl > 235) & (sub[:, :, 0] > 235) & (sub[:, :, 1] > 235) & (sub[:, :, 2] > 235)
dens = (~sw) & (~sr)
colc = dens.sum(axis=0); rowc = dens.sum(axis=1)
cx = np.where(colc > 40)[0]; ry = np.where(rowc > 40)[0]
vres("photo bbox", [int(cx.min()) + 88, int(cx.max()) + 88, int(ry.min()) + 240, int(ry.max()) + 240], [105, 442, 284, 454], tol=3)

# ---- 5. right dark image (want dense x548..876 y278..434) ----
print("== right image ==")
sub2 = a[275:440, 540:880]
sl2 = 0.299 * sub2[:, :, 0] + 0.587 * sub2[:, :, 1] + 0.114 * sub2[:, :, 2]
dk = sl2 < 140
cx2 = np.where(dk.sum(axis=0) > 20)[0]; ry2 = np.where(dk.sum(axis=1) > 20)[0]
vres("dark dense bbox", [int(cx2.min()) + 540, int(cx2.max()) + 540, int(ry2.min()) + 275, int(ry2.max()) + 275], [548, 876, 278, 434], tol=4)

# ---- 6. arrow (want ink x484..534 y347..363) ----
print("== arrow ==")
aw = red[340:370, 480:545]
ys3, xs3 = np.where(aw)
print(f"  strong-red bbox x[{int(xs3.min())+480}..{int(xs3.max())+480}] y[{int(ys3.min())+340}..{int(ys3.max())+340}] (want 484..534 / 347..363)")
mid = a[354, 486:520]
print(f"  shaft interior @y354 x486..519 modal: #{np.bincount((mid[:,0]*65536+mid[:,1]*256+mid[:,2]).tolist()).argmax():06X}")

# ---- 7. chrome border presence in this frame ----
print("== chrome border presence (informational; chrome drawn by law regardless) ==")
for x in (41, 42, 43, 916, 917, 918):
    px_ = a[300, x]
    print(f"  x={x} y=300: #{px_[0]:02X}{px_[1]:02X}{px_[2]:02X}", end="")
print()
for y in (43, 44, 45, 46):
    px_ = a[y, 500]
    print(f"  y={y} x=500: #{px_[0]:02X}{px_[1]:02X}{px_[2]:02X}", end="")
print()

# ---- 8. title font forensics ----
print("== title font forensics ==")
TARGET_ADV = 869 - 117 + 1  # 753
words = [("Apply", 117, 211), ("filter", 224, 299), ("on", 312, 347), ("2-D", 362, 415),
         ("gray", 438, 507), ("image", 521, 612), ("(K=1", 635, 709), ("Channel)", 727, 869)]
CAP = 24
FONTS = {
    "LiberationSans-Bold (Arial)": "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
    "LiberationSerif-Bold (TNR)": "/usr/share/fonts/liberation/LiberationSerif-Bold.ttf",
    "LiberationSerif-Reg": "/usr/share/fonts/liberation/LiberationSerif-Regular.ttf",
    "LiberationSans-Reg": "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
}
for name, path in FONTS.items():
    # size such that cap height ('A') == 24 px
    best = None
    for size10 in range(200, 700):
        f = ImageFont.truetype(path, size10 / 10)
        bb = f.getbbox("A")
        cap = bb[3] - bb[1]
        if best is None or abs(cap - CAP) < best[1]:
            best = (size10 / 10, abs(cap - CAP), cap)
    size = best[0]
    f = ImageFont.truetype(path, int(round(size)))
    adv_total = 0
    wadv = []
    for w, x0, x1 in words:
        adv = f.getlength(w)
        wadv.append(adv)
        adv_total += adv
    # 7 gaps: singles 13,13,15,?,14,?,18 -> space ~ (2*13+15+14)/4 ~ 13.75*2? use measured gaps directly
    gaps = [224 - 211, 312 - 299, 347 - 362 + 15, 0, 0, 0, 0]  # not exact; just report advances
    tot = sum(wadv) + f.getlength(" ") * 7 + f.getlength(" ") * 2  # 7 word gaps + 2 extra (double spaces)
    print(f"  {name}: cap-size {size}pt  word-adv {[round(v) for v in wadv]}  total-with-spaces {round(tot)} (target ~753)")

EOF = None
