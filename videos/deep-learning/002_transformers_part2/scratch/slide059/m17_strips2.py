from PIL import Image
import numpy as np
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

# cell-strip dark-border cols per row (vertical borders every ~12px)
def borders(y0, y1, x0, x1, name):
    dk = (R<190)&(G<185)&(B<190)
    cnt = dk[y0:y1, x0:x1].sum(axis=0)
    cols = [x0+i for i in range(x1-x0) if cnt[i] > (y1-y0)*0.55]
    # compress to ranges
    rngs = []
    for c in cols:
        if rngs and c - rngs[-1][1] <= 2: rngs[-1][1] = c
        else: rngs.append([c, c])
    print(name, 'border col ranges:', ['%d-%d' % (r[0], r[1]) for r in rngs])

borders(422, 436, 140, 920, 'word row')     # between top/bottom cell borders
borders(481, 496, 140, 920, 'position row')
borders(233, 249, 140, 920, 'output row')

# left labels: ink bboxes per color per band
def inkbox(mask, y0, y1, x0, x1, name):
    sub = np.zeros_like(mask); sub[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs)==0: print(name, 'EMPTY'); return
    print('%s: x %d..%d y %d..%d n%d' % (name, xs.min(), xs.max(), ys.min(), ys.max(), len(xs)))
    # line structure: rows with ink
    cnt = sub.sum(axis=1)
    rows = [y for y in range(y0,y1) if cnt[y]>3]
    if rows:
        # group contiguous
        grps = []
        for y in rows:
            if grps and y - grps[-1][1] <= 2: grps[-1][1] = y
            else: grps.append([y, y])
        print('   line bands:', ['%d-%d' % (g[0], g[1]) for g in grps])

red_t = (R>120)&(G<110)&(B<110)&(R-G>40)
grn_t = (G>100)&(G-R>25)&(G-B>15)
blu_t = (B>100)&(B-R>40)&(G<160)
inkbox(red_t, 125, 170, 55, 280, 'Single vector note (red italic)')
inkbox(red_t, 215, 262, 55, 280, 'Output/Sequence (red)')
inkbox(red_t, 378, 404, 55, 280, 'Input Sequence (red)')
inkbox(grn_t, 400, 448, 55, 280, 'Word/Embedding/Vectors (green)')
inkbox(blu_t, 458, 508, 55, 280, 'Position/Information/Vectors (blue)')
inkbox(blu_t, 44, 70, 280, 470, 'Output Classes (blue)')
inkbox(blu_t, 40, 66, 420, 640, 'C labels (blue)')
inkbox(red_t, 180, 215, 160, 880, 'GAP text?? (should be black - skip)')
# black text GAP
blk_t = (R<120)&(G<120)&(B<120)
inkbox(blk_t, 182, 210, 400, 700, 'GAP text (black)')
