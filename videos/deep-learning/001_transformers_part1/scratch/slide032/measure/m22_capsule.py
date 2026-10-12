from PIL import Image
import numpy as np
fr = np.array(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg').convert('RGB')).astype(int)
def hexc(p): return '#%02X%02X%02X' % tuple(p)

# capsule row extents: for each y, find dark border pixels (sum<400) in x405..455
print("== capsule row extents (dark border px x405..455) ==")
for y in range(84, 262, 4):
    row = fr[y, 405:456]
    dk = np.where(row.sum(axis=1) < 430)[0] + 405
    print('  y=%3d dark@%s' % (y, list(dk) if len(dk) else '-'))
# fine near top/bottom
print("== top rows fine ==")
for y in range(84, 100):
    row = fr[y, 405:456]
    dk = np.where(row.sum(axis=1) < 430)[0] + 405
    print('  y=%3d dark@%s' % (y, list(dk) if len(dk) else '-'))
print("== bottom rows fine ==")
for y in range(248, 262):
    row = fr[y, 405:456]
    dk = np.where(row.sum(axis=1) < 430)[0] + 405
    print('  y=%3d dark@%s' % (y, list(dk) if len(dk) else '-'))

# capsule pink fill extents at y=110 (avoid chip): outer pink start/end incl. border
print("== pink extent at y=110, y=100, y=90 (first/last px with R>230,G 160..225) ==")
for y in [90, 95, 100, 110, 170, 240, 250, 254]:
    row = fr[y, 400:460]
    m = np.where((row[:,0] > 225) & (row[:,1] > 150) & (row[:,1] < 230) & (row[:,2] > 150) & (row[:,2] < 235))[0] + 400
    print('  y=%3d pink x %d..%d' % (y, m.min(), m.max()) if len(m) else '  y=%d none' % y)

# lavender fill: radial profile circle 1 (center 97,126.5)
print("== circle1 radial lavender profile (exclude dark text sum<420) ==")
for r in range(2, 11):
    vals = []
    for a in range(0, 360, 15):
        x = int(round(97 + r*np.cos(np.radians(a)))); yv = int(round(126.5 + r*np.sin(np.radians(a))))
        p = fr[yv, x]
        if p.sum() > 420: vals.append(p)
    if vals:
        m = np.array(vals).mean(axis=0).astype(int)
        print('  r=%2d n=%2d mean %s' % (r, len(vals), hexc(m)))

# interior median at r 3..5 across all 4 circles
allv = []
for cx in [97, 122, 148, 173]:
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            if dx*dx + dy*dy <= 18:
                p = fr[int(126.5)+dy, cx+dx]
                if p.sum() > 430 and not (p[0]>225 and p[1]>225 and p[2]<215):
                    allv.append(p)
allv = np.array(allv)
print("== interior median (r<=4.2, excl dark) %s n=%d ==" % (hexc(np.median(allv, axis=0).astype(int)), len(allv)))

# chip geometry fine: chip1 bbox rows/cols with yellow
print("== chip1 exact bbox ==")
sub = fr[95:125, 410:455]
ys, xs = np.where((sub[:,:,0] > 235) & (sub[:,:,1] > 235) & (sub[:,:,2] < 220))
print('  chip1 y%d..%d x%d..%d' % (ys.min()+95, ys.max()+95, xs.min()+410, xs.max()+410))
# chip color median
vals = sub[ys, xs]
print('  chip median %s' % hexc(np.median(vals, axis=0).astype(int)))
# chip border? sample just outside chip left edge
print('  left-of-chip y110 x414..419:', ' '.join(hexc(fr[110, x]) for x in range(413, 420)))
print('  right-of-chip y110 x436..441:', ' '.join(hexc(fr[110, x]) for x in range(435, 442)))
print('  above-chip x427 y101..106:', ' '.join(hexc(fr[y, 427]) for y in range(100, 107)))
