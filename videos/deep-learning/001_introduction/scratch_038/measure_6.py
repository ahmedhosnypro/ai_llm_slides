from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[...,0], a[...,1], a[...,2]

masks = {
 "brown(C08040/8B4513)": ((r-g)>40)&((g-b)>25)&(r>120)&(b<130),
 "cyan(00BFBF)": (g>130)&(b>130)&(r<110),
 "green(00A000)": (g>110)&(r<110)&(b<110)&((g-b)>40),
 "red(FF0000)": (r>180)&(g<90)&(b<90),
 "yellow(FFFF00)": (r>190)&(g>190)&(b<110),
 "purple(800080)": (r>90)&(r<170)&(b>90)&(b<180)&(g<90),
 "blue(6699FF)": (b>190)&(r>70)&(r<160)&(g>110)&(g<200),
}
# restrict to diagram region
for name, m in masks.items():
    mm = m.copy()
    mm[:256] = False; mm[512:] = False; mm[:, :60] = False; mm[:, 812:] = False
    ys, xs = np.nonzero(mm)
    if len(xs)==0: print(name, "EMPTY"); continue
    print(f"{name}: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} count {len(xs)}")

# brown detail: the slab
mm = masks["brown (C08040/8B4513)"]; mm[:256]=False; mm[512:]=False; mm[:,:60]=False; mm[:,812:]=False
ys, xs = np.nonzero(mm)
print("\nbrown row profile:")
import collections
rows = collections.Counter(ys)
for y in sorted(set(ys)):
    xr = xs[ys==y]
    print(y, len(xr), xr.min(), xr.max())
