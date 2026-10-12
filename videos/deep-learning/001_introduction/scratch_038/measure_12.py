from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[...,0], a[...,1], a[...,2]
ink = (r<175)&(g<175)&(b<175)

def bbox(mask, y0,y1,x0,x1,name):
    m = mask[y0:y1, x0:x1]
    ys, xs = np.nonzero(m)
    if len(xs)==0: print(f"{name}: EMPTY"); return
    print(f"{name}: x {x0+xs.min()}..{x0+xs.max()}  y {y0+ys.min()}..{y0+ys.max()}  n={len(xs)}")

# per-color row extents for slabs
masks = {
 'C': (g>120)&(b>120)&(r<110),
 'G': (g>110)&(r<110)&(b<110)&((g-b)>40),
 'R': (r>150)&(g<100)&(b<100),
 'Y': (r>170)&(g>170)&(b<110),
 'P': (r>80)&(r<180)&(b>80)&(b<190)&(g<90),
}
print("=== slab per-row extents (x380..565) ===")
for k, m in masks.items():
    print(f"-- {k}")
    for y in range(334, 404, 4):
        xs = np.nonzero(m[y, 380:565])[0]
        if len(xs): print(f"  y={y}: x {380+xs.min()}..{380+xs.max()} n={len(xs)}")

print("=== circles per-row extents (x595..812) ===")
for k, m in masks.items():
    xs_all = np.nonzero(m[330:420, 595:812].sum(axis=0))[0]
    if len(xs_all):
        # find segments
        segs=[]; s=p=None
        for x in xs_all:
            if s is None: s=p=x
            elif x<=p+3: p=x
            else: segs.append((595+s,595+p)); s=p=x
        segs.append((595+s,595+p))
        ys = np.nonzero(m[330:420, 595:812].sum(axis=1))[0]
        print(f"-- {k}: xsegs {segs} y {330+ys.min()}..{330+ys.max()}")

# tan ring around circles
tan = ((r-g)>25)&((g-b)>15)&(r>150)&(r<245)&(b<200)
print("=== tan ring rows (x595..812) ===")
for y in range(340, 410, 5):
    xs = np.nonzero(tan[y, 595:812])[0]
    if len(xs): print(f"  y={y}: n={len(xs)} x {595+xs.min()}..{595+xs.max()}")

# '=' sign
blue = (b>190)&(r>60)&(r<170)&(g>100)
print("=== blue = sign ===")
for y in range(320, 395, 3):
    xs = np.nonzero(blue[y, 548:615])[0]
    if len(xs): print(f"  y={y}: x {548+xs.min()}..{548+xs.max()} n={len(xs)}")

# samples of key colors
print("=== color samples ===")
pts = {
 'title_red': (480, 80), 'formula_black': (150, 148), 'formula_red7': (123, 217),
 'formula_blue3': (182, 217), 'formula_green5': (218, 216),
 'fbox_border': (400, 118), 'dbox_border': (400, 251),
 'slab_tan': (300, 360), 'slab_dark': (344, 320),
 'cyan_face': (400, 370), 'green_face': (440, 370), 'red_face': (462, 370),
 'yellow_face': (488, 370), 'purple_face': (525, 375),
 'circ_cyan': (628, 372), 'circ_green': (660, 372), 'circ_red': (698, 372),
 'circ_yellow': (736, 372), 'circ_purple': (776, 372),
 'ring1': (612, 370), 'ring2': (645, 370),
 'dash': (355, 366), 'eq_blue': (580, 368),
 'panel_gray': (480, 60), 'white_in_fbox': (500, 160), 'white_in_dbox': (650, 300),
}
for k,(x,y) in pts.items(): print(f"  {k} ({x},{y}) = {tuple(a[y,x])}")
