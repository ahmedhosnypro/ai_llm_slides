from PIL import Image
import numpy as np
import sys

path = sys.argv[1] if len(sys.argv) > 1 else 'recreated_pptx/qa/slide003/render_1.png'
im = Image.open(path).convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
K = 150/72.0  # render px per original px
r, g, b = a[...,0], a[...,1], a[...,2]
print(f"render {W}x{H}; scale K={K:.5f} (orig px -> render px)")

red = (r > 120) & (r - g > 50) & (r - b > 50)
blue = (b > 130) & (b - r > 60) & (b - g > 40)

def bands(mask, x0, x1, y0, y1, minpx=2):
    rows = mask[y0:y1, x0:x1].sum(axis=1)
    out, inb = [], False
    for i, v in enumerate(rows):
        if v >= minpx and not inb: st = i; inb = True
        elif v < minpx and inb: out.append((y0+st, y0+i-1)); inb = False
    if inb: out.append((y0+st, y0+len(rows)-1))
    return out

# TITLE
tb = bands(red, 100, W-100, 30, 200)
print("title bands (render px):", tb)
for (y0,y1) in tb:
    xs = np.where(red[y0:y1+1, 100:W-100].any(axis=0))[0] + 100
    print(f"  title ink y=[{y0},{y1}] x=[{xs.min()},{xs.max()}] cap_h={y1-y0+1} (target cap ~{29*K:.1f}, center_target={999.75:.0f})")
    if len(xs): print(f"  title center x={(xs.min()+xs.max())/2:.1f}")

# AGENDA
ab = bands(blue, 100, 1300, 250, 800)
print("agenda bands (render px):")
tops = []
for (y0,y1) in ab:
    xs = np.where(blue[y0:y1+1, 100:1300].any(axis=0))[0] + 100
    tops.append(y0)
    print(f"  band y=[{y0},{y1}] h={y1-y0+1} x=[{xs.min()},{xs.max()}] w={xs.max()-xs.min()+1}")
targets = [358.3, 445.8, 531.3, 616.7]
wt = [539.6, 562.5, 497.9, 412.5]
if len(tops) == 4:
    print("  band tops:", tops, "targets:", [f"{t:.1f}" for t in targets])
    print("  top deltas (render-target):", [f"{t-T:+.1f}" for t,T in zip(tops,targets)])
    pitches = [tops[i+1]-tops[i] for i in range(3)]
    print("  pitches:", pitches, f"(pinned {41.33*K:.2f}px = 41.33pt)")
    ws = [int(np.where(blue[y0:y1+1, 100:1300].any(axis=0))[0].max() - np.where(blue[y0:y1+1, 100:1300].any(axis=0))[0].min() + 1) for (y0,y1) in ab]
    print("  widths:", ws, "targets:", [f"{t:.1f}" for t in wt])
    xs_all = np.where(blue[250:800, :].any(axis=0))[0]
    print(f"  leftmost blue ink x={xs_all.min()} (target 231.25)")

# BOTTOM LINE
bl = bands(red, 100, W-100, 1050, H, minpx=3)
print("bottom red bands y>1050:", bl, "(target band ~[1118.8,1125])")
for (y0,y1) in bl:
    xs = np.where(red[y0:y1+1, :].any(axis=0))[0]
    print(f"  x=[{xs.min()},{xs.max()}] (target [79.2,1918.8])")

# HOUSE FRAME + containment
print("== containment (house frame: x in [22.5,1977], y in [22.5,1102.5]) ==")
ys, xs = np.where(blue)
print(f"  agenda ink bbox x=[{xs.min()},{xs.max()}] y=[{ys.min()},{ys.max()}]")
viol = ((xs < 22.5) | (xs > 1977) | (ys < 22.5) | (ys > 1102.5)).sum()
print(f"  agenda ink outside house frame: {viol} px")
ys2, xs2 = np.where(red[30:1050, :])
print(f"  title ink (y30-1050) bbox x=[{xs2.min()},{xs2.max()}] y=[{ys2.min()+30},{ys2.max()+30}]")

# BADGE (yellow)
yellow = (r > 200) & (g > 200) & (b < 200) & (b > 100)
ym = yellow[30:140, 1800:1990]
ys3, xs3 = np.where(ym)
if len(xs3): print(f"  badge fill x=[{xs3.min()+1800},{xs3.max()+1800}] y=[{ys3.min()+30},{ys3.max()+30}] (house target x[1872,1947] y[45,120])")

# DOUBLE SPACE check line 4: column gaps
(l4y0, l4y1) = ab[3]
cols = blue[l4y0:l4y1+1, :].sum(axis=0)
nz = np.where(cols > 0)[0]
gaps, start, prev = [], nz[0], nz[0]
for x in nz[1:]:
    if x - prev > 4: gaps.append((prev, x, x - prev))
    prev = x
print("  line4 word gaps (end,start,width):", [(int(gp[0]),int(gp[1]),int(gp[2])) for gp in gaps])
