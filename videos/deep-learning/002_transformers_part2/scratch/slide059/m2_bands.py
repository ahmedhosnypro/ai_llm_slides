from PIL import Image
import numpy as np
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

def bbox(mask, name):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(name, 'EMPTY'); return None
    print(f'{name}: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}  (n={len(xs)})')
    return xs.min(), xs.max(), ys.min(), ys.max()

# 1) pink input container FADBD8 (light pink): R~250 G~219 B~216
pink = (abs(R-250)<18) & (abs(G-219)<18) & (abs(B-216)<18)
bbox(pink[380:540, :], 'pink container (y offset 380)')  # will re-add offset
ys, xs = np.where(pink)
print('pink full: x', xs.min(), xs.max(), 'y', ys.min(), ys.max())

# 2) peach position-row fill FDEBD0
peach = (abs(R-253)<12) & (abs(G-235)<14) & (abs(B-208)<16)
ys, xs = np.where(peach)
print('peach: x', xs.min(), xs.max(), 'y', ys.min(), ys.max(), 'n', len(xs))

# 3) light-blue output row fill D6EAF8
lblu = (abs(R-214)<16) & (abs(G-234)<16) & (abs(B-248)<16)
ys, xs = np.where(lblu)
print('lightblue D6EAF8: x', xs.min(), xs.max(), 'y', ys.min(), ys.max(), 'n', len(xs))

# 4) muted-red encoder container CD5C5C
mred = (abs(R-205)<25) & (abs(G-92)<25) & (abs(B-92)<25)
ys, xs = np.where(mred)
print('muted red CD5C5C: x', xs.min(), xs.max(), 'y', ys.min(), ys.max(), 'n', len(xs))

# 5) dark-red bars B22222 (178,34,34)
dred = (abs(R-178)<28) & (abs(G-34)<30) & (abs(B-34)<30)
ys, xs = np.where(dred)
print('darkred B22222: x', xs.min(), xs.max(), 'y', ys.min(), ys.max(), 'n', len(xs))
# per-row profile to find the 3 bars
cnt = dred.sum(axis=1)
rows = [y for y in range(540) if cnt[y] > 100]
print('darkred bar rows:', rows)

# 6) tan softmax bar F5CBA7
tan = (abs(R-245)<14) & (abs(G-203)<16) & (abs(B-167)<18)
ys, xs = np.where(tan)
print('tan F5CBA7: x', xs.min(), xs.max(), 'y', ys.min(), ys.max(), 'n', len(xs))

# 7) navy circles 1A237E
navy = (abs(R-26)<25) & (abs(G-35)<25) & (abs(B-126)<35)
ys, xs = np.where(navy)
print('navy 1A237E: x', xs.min(), xs.max(), 'y', ys.min(), ys.max(), 'n', len(xs))

# 8) GAP box: white with black border — find black border rows in band y 160..230
blk = (R<90)&(G<90)&(B<90)
cnt = blk[:, 150:850].sum(axis=1)
print('black rows y150..240:', {y:int(cnt[y]) for y in range(150, 241) if cnt[y] > 100})

# 9) pooled row: yellow F4D03F
pyl = (abs(R-244)<20)&(abs(G-208)<20)&(abs(B-63)<35)
ys, xs = np.where(pyl)
print('pool yellow F4D03F: x', xs.min(), xs.max(), 'y', ys.min(), ys.max(), 'n', len(xs))
