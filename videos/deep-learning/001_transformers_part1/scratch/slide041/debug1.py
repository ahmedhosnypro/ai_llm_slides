import numpy as np
from PIL import Image
from scipy import ndimage

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide041/render/slide-1.png"
im = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
S = 150/72.0

# 1) where are the containment strays?
diff_panel = (np.abs(r-233)+np.abs(g-233)+np.abs(b-231)) > 90
diff_white = (np.abs(r-255)+np.abs(g-255)+np.abs(b-255)) > 90
ink = diff_panel & diff_white
zone = np.zeros((H, W), bool); zone[100:1120, 94:1906] = True
ring = np.zeros((H, W), bool)
ring[93:105, 85:1915] = True; ring[1115:1125, 85:1915] = True
ring[93:1125, 85:99] = True; ring[93:1125, 1901:1915] = True
out = ink & ~zone & ~ring
lab, n = ndimage.label(out)
print("stray clusters:", n)
for i in range(1, n+1):
    ys, xs = np.where(lab == i)
    if len(xs) < 20: continue
    print(f"  cluster n={len(xs)}: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}  (frame px x {xs.min()/S:.0f}..{xs.max()/S:.0f} y {ys.min()/S:.0f}..{ys.max()/S:.0f})  rgb~{tuple(int(v) for v in im[ys[len(ys)//2], xs[len(xs)//2]])}")

# 2) highlights with looser mask (blend-aware)
ylw = (r>215)&(g>240)&(b<150)
for (label, x0,y0,x1,y1) in [("hl-outputProb", 750,100,825,140), ("hl-outputs", 750,485,825,515), ("hl-MHA-band", 660,240,760,340)]:
    m = np.zeros((H,W),bool); m[int(y0*S):int(y1*S)+1, int(x0*S):int(x1*S)+1] = True
    ys, xs = np.where(ylw & m)
    print(f"{label}: {'EMPTY' if len(xs)==0 else f'x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(xs)}'}")

# 3) dark red arc search: any dark-red ink anywhere right of x=800*S
drk = (np.abs(r-139)<55)&(g<80)&(b<80)
m = np.zeros((H,W),bool); m[:, int(800*S):] = True
ys, xs = np.where(drk & m)
print("dark-red right of 800:", "EMPTY" if len(xs)==0 else f"x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(xs)}")
# any ink at all in the arc's expected bbox (800..888 frame px x, 106..506 y)?
m2 = np.zeros((H,W),bool); m2[int(106*S):int(506*S)+1, int(800*S):int(888*S)+1] = True
anyink = (np.abs(r-204)+np.abs(g-250)+np.abs(b-220) > 90)  # vs dec green
ys, xs = np.where(anyink & m2)
print("any-ink in arc bbox:", "EMPTY" if len(xs)==0 else f"x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(xs)} sample rgb {tuple(int(v) for v in im[ys[0], xs[0]]) if len(xs) else None}")
