from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')
a = np.asarray(im).astype(int)
SX, OX, SY, OY = 0.962329, 17.582, 0.955556, 0.0
def sx(fx): return (fx - OX) / SX
def sy(fy): return fy / SY
def fx(v): return v * SX + OX
def fy(v): return v * SY
COLS = [194.9, 270.3, 346.3, 422.8, 499.8, 574.1, 771.8, 848.8]
FCOLS = [round(fx(c),1) for c in COLS]
print('col centers frame px:', FCOLS)

# --- token row band extents per column-1 x-range (x 185..225) ---
def rowband(ylo, yhi, xlo, xhi):
    seg = a[ylo:yhi, xlo:xhi]
    nonwhite = (seg.max(axis=2) < 245) | ((np.abs(seg[:,:,0]-seg[:,:,1])>25))
    rows = np.where(nonwhite.sum(axis=1) > 15)[0]
    return (rows.min()+ylo, rows.max()+ylo) if len(rows) else None
for name, yc in [('final',73),('postFFN',180.5),('postLN',286.5),('outatt',392),('X',495)]:
    bb = rowband(int(yc)-14, int(yc)+16, 185, 225)
    print(f'row {name}: frame y {bb} -> slide y {sy(bb[0]):.1f}..{sy(bb[1]):.1f} (h={sy(bb[1])-sy(bb[0]):.1f})')

# --- segment colors: sample each row at col1: 4 segments ---
for name, yc in [('final',73),('postFFN',180.5),('postLN',286.5),('outatt',392),('X',495)]:
    y = int(yc)+6  # below label text
    samples = [tuple(a[y, int(FCOLS[0]+dx)]) for dx in (-17,-6,6,17)]
    print(f'row {name} col1 segments @y={y}:', samples)

# --- MHA bar bounds ---
sub = a[400:500, 100:900]
navy = (sub[:,:,2]>100) & (sub[:,:,0]<90) & (sub[:,:,1]<90)
rows = np.where(navy.sum(axis=1) > 500)[0]; cols = np.where(navy.sum(axis=0) > 30)[0]
print('MHA bar frame: y', rows.min()+400, rows.max()+400, ' x', cols.min()+100, cols.max()+100)
print('  -> slide y', round(sy(rows.min()+400),1), round(sy(rows.max()+400),1), ' x', round(sx(cols.min()+100),1), round(sx(cols.max()+100),1))
print('  bar fill sample:', tuple(a[445, 300]), tuple(a[445, 700]))

# --- FFN box bounds (fill DDEBF7 + border) ---
sub = a[195:275, 100:900]
f7 = (np.abs(sub - np.array([0xDD,0xEB,0xF7])).max(axis=2) <= 12)
rows = np.where(f7.sum(axis=1) > 300)[0]; cols = np.where(f7.sum(axis=0) > 20)[0]
print('FFN fill frame: y', rows.min()+195, rows.max()+195, ' x', cols.min()+100, cols.max()+100)
# border: blue-ish lines around
blueish = (sub[:,:,2]>120) & (sub[:,:,0]<80) & (sub[:,:,1]<80)
br = np.where(blueish.sum(axis=1) > 400)[0]; bc = np.where(blueish.sum(axis=0) > 30)[0]
print('FFN border rows:', [int(r+195) for r in br], ' cols:', [int(c+100) for c in bc])
print('  -> slide y fill', round(sy(rows.min()+195),1), round(sy(rows.max()+195),1), ' x', round(sx(cols.min()+100),1), round(sx(cols.max()+100),1))

# --- LN bars (neutral gray 175..235, R~G~B) restricted x 220..380 (left of text) ---
for name, ylo, yhi in [('top', 90, 145), ('bottom', 300, 355)]:
    seg = a[ylo:yhi, 220:380]
    g = (np.abs(seg[:,:,0]-seg[:,:,1])<=8) & (np.abs(seg[:,:,1]-seg[:,:,2])<=8) & (seg[:,:,0]>=170) & (seg[:,:,0]<=235)
    rows = np.where(g.sum(axis=1) > 100)[0]
    print(f'graybar {name}: frame y {rows.min()+ylo}..{rows.max()+ylo} -> slide {sy(rows.min()+ylo):.1f}..{sy(rows.max()+ylo):.1f}')
    # x extent at bar middle
    ymid = (rows.min()+rows.max())//2 + ylo
    row = a[ymid]
    gm = (np.abs(row[:,0]-row[:,1])<=8) & (np.abs(row[:,1]-row[:,2])<=8) & (row[:,0]>=170) & (row[:,0]<=235)
    xs = np.where(gm)[0]
    xs = xs[(xs>100)&(xs<910)]
    print(f'  graybar {name} x extent @y={ymid}: {xs.min()}..{xs.max()} -> slide {sx(xs.min()):.1f}..{sx(xs.max()):.1f}; mid color {tuple(a[ymid,300])}')

# --- containers: green dash rows + fill extent ---
for name, ylo, yhi in [('top', 85, 175), ('bottom', 290, 390)]:
    seg = a[ylo:yhi, 140:900]
    gr = (seg[:,:,1]>110) & (seg[:,:,0]<120) & (seg[:,:,2]<120)
    rows = np.where(gr.sum(axis=1) > 30)[0]
    cf = (np.abs(seg - np.array([0xE2,0xEF,0xDA])).max(axis=2) <= 14)
    crows = np.where(cf.sum(axis=1) > 200)[0]
    print(f'container {name}: green-dash rows {[int(r+ylo) for r in rows[:6]]}...{[int(r+ylo) for r in rows[-6:]] if len(rows)>6 else ""} ; fill rows {crows.min()+ylo}..{crows.max()+ylo}')
    # container x extent at a dash row
    if len(rows):
        yd = rows[0]+ylo
        grf = (a[yd,:,1]>110) & (a[yd,:,0]<120) & (a[yd,:,2]<120)
        xs = np.where(grf)[0]; xs = xs[(xs>100)&(xs<910)]
        print(f'  top-dash row {yd} x: {xs.min()}..{xs.max()} -> slide {sx(xs.min()):.1f}..{sx(xs.max()):.1f}')

# --- plus discs: column 1 (fcx 205) ---
for name, ylo, yhi in [('top', 135, 165), ('bottom', 345, 375)]:
    seg = a[ylo:yhi, 185:226]
    dr = (np.abs(seg - np.array([0x99,0x00,0x00])).max(axis=2) <= 60) | ((seg[:,:,0]>100)&(seg[:,:,1]<60)&(seg[:,:,2]<60))
    ys, xs = np.where(dr)
    if len(ys):
        print(f'plus {name}: frame y {ys.min()+ylo}..{ys.max()+ylo} x {xs.min()+185}..{xs.max()+185} cy={sy((ys.min()+ys.max())/2+ylo):.1f} slide, d_frame={ys.max()-ys.min()+1}')
        print('   center color', tuple(a[(ys.min()+ys.max())//2+ylo, (xs.min()+xs.max())//2+185]))
