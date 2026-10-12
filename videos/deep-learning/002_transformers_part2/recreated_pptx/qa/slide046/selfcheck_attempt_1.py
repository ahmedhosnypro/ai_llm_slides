from PIL import Image
import numpy as np
R = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide046/render_1.png').convert('RGB')).astype(int)
F = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')).astype(int)
S = 150/72  # render px per slide pt
def rpx(v): return int(round(v * S))
def f2r_x(fx): return int(round((fx-17.582)/0.962329 * S))
def f2r_y(fy): return int(round(fy/0.955556 * S))
ok = True
def check(name, cond, detail=""):
    global ok
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")
    if not cond: ok = False

print("== 1. structure bands (render vs measured frame positions, tol 8.3 rpx = 4pt) ==")
def inkband(img, x0, x1, y0, y1, test, minc=3):
    seg = img[y0:y1, x0:x1]
    m = test(seg)
    rows = np.where(m.sum(axis=1) > minc)[0]
    return (int(rows.min())+y0, int(rows.max())+y0) if len(rows) else None
navy_t = lambda s: (s[:,:,2]>110)&(s[:,:,0]<100)&(s[:,:,1]<100)
gray_t = lambda s: (np.abs(s[:,:,0]-s[:,:,1])<=12)&(np.abs(s[:,:,1]-s[:,:,2])<=12)&(s[:,:,0]>=168)&(s[:,:,0]<=238)
lav_t  = lambda s: (np.abs(s - np.array([0xD8,0xBF,0xD8])).max(axis=2) <= 35)
dr_t   = lambda s: (s[:,:,0]>110)&(s[:,:,1]<70)&(s[:,:,2]<70)
grn_t  = lambda s: (s[:,:,1]>110)&(s[:,:,0]<115)&(s[:,:,2]<115)
# MHA bar: sample its fill color first
print('MHA bar fill sample @(1042,966):', tuple(R[966,1042]), ' expected ~00008B')
b = inkband(R, f2r_x(300), f2r_x(700), 880, 1060, navy_t)
check('MHA bar band', b and abs(b[0]-f2r_y(419))<=9 and abs(b[1]-f2r_y(468))<=9, f'{b} vs {f2r_y(419)}..{f2r_y(468)}')
for tag, f0, f1 in [('top LN bar',102,128.5),('bottom LN bar',312,338.5)]:
    bb = inkband(R, f2r_x(250), f2r_x(400), f2r_y(f0)-25, f2r_y(f1)+25, gray_t)
    check(tag, bb and abs(bb[0]-f2r_y(f0))<=9 and abs(bb[1]-f2r_y(f1))<=9, f'{bb} vs {f2r_y(f0)}..{f2r_y(f1)}')
for tag, f0, f1 in [('final row',65,81),('postFFN row',173,188),('postLN row',278,295),('outatt row',384,400),('X row',487,503)]:
    bb = inkband(R, f2r_x(216), f2r_x(228), f2r_y(f0)-12, f2r_y(f1)+12, lav_t)
    check(tag, bb and abs(bb[0]-f2r_y(f0))<=9, f'{bb} vs {f2r_y(f0)}..{f2r_y(f1)}')
for tag, cy in [('top plus',155.4),('bottom plus',376.25)]:
    yc = rpx(cy)
    bb = inkband(R, rpx(194.9-9), rpx(194.9+9), yc-22, yc+22, dr_t)
    check(tag, bb and abs((bb[0]+bb[1])/2 - yc)<=9, f'{bb} cy={(bb[0]+bb[1])/2 if bb else None} vs {yc}')
# containers: green dash rows
for tag, f0, f1 in [('top container',96,165),('bottom container',303,378)]:
    b0 = inkband(R, f2r_x(300), f2r_x(850), f2r_y(f0)-14, f2r_y(f0)+14, grn_t, minc=30)
    b1 = inkband(R, f2r_x(300), f2r_x(850), f2r_y(f1)-14, f2r_y(f1)+14, grn_t, minc=30)
    check(tag+' top dash', b0 and abs(b0[0]-f2r_y(f0))<=9, f'{b0} vs {f2r_y(f0)}')
    check(tag+' bottom dash', b1 and abs(b1[0]-f2r_y(f1))<=9, f'{b1} vs {f2r_y(f1)}')

print("== 2. color samples (render) ==")
samples = [
  ('navy bar', 966, 1042, (0,0,139), 60),
  ('gray bar top', rpx(120), rpx(300), (217,217,217), 30),
  ('container fill', rpx(160), rpx(300), (226,239,218), 25),
  ('FFN box fill', rpx(245), rpx(300), (221,235,247), 25),
  ('tile cream', rpx(252), rpx(193.5-25), (255,230,153), 40),
  ('callout fill', rpx(70), rpx(100), (255,204,204), 35),
  ('caption band', rpx(533), rpx(350), (255,182,193), 45),
  ('panel white', rpx(300), rpx(100), (255,255,255), 12),
  ('house gray panel', rpx(20), rpx(30), (233,233,231), 14),
]
for name, y, x, exp, tol in samples:
    got = tuple(R[y, x])
    check(name, all(abs(int(g)-e)<=tol for g,e in zip(got,exp)), f'{got} vs {exp}')

print("== 3. thin arrow families present (counts in gap bands, x 195..860 slide) ==")
red_t = lambda s: (s[:,:,0]>130)&(s[:,:,1]<85)&(s[:,:,2]<85)
blu_t = lambda s: (s[:,:,2]>110)&(s[:,:,0]<100)&(s[:,:,1]<100)
def gapcount(test, f_y0, f_y1, exclude_dash=True):
    y0, y1 = f2r_y(f_y0), f2r_y(f_y1)
    seg = R[y0:y1, f2r_x(200):f2r_x(855)]
    return int(test(seg).sum())
check('red arrows top (bar->final)', gapcount(red_t, 86, 104) > 60, str(gapcount(red_t, 86, 104)))
check('green arrows top (plus->bar)', gapcount(grn_t, 128, 141) > 40, str(gapcount(grn_t, 128, 141)))
check('navy arrows top (row->plus)', gapcount(blu_t, 157, 172) > 40, str(gapcount(blu_t, 157, 172)))
check('red arrows bottom (bar->postLN)', gapcount(red_t, 297, 313) > 60, str(gapcount(red_t, 297, 313)))
check('green arrows bottom (plus->bar)', gapcount(grn_t, 340, 352) > 40, str(gapcount(grn_t, 340, 352)))
check('navy arrows bottom (row->plus)', gapcount(blu_t, 368, 383) > 40, str(gapcount(blu_t, 368, 383)))
# block arrows: per-column ink presence in the 4 gaps
for tag, f0, f1 in [('blk X->MHA', 470, 485), ('blk MHA->outatt', 402, 416), ('blk postLN->FFN', 266, 277), ('blk FFN->postFFN', 192, 205)]:
    y0, y1 = f2r_y(f0), f2r_y(f1)
    seg = R[y0:y1, f2r_x(196):f2r_x(860)]
    m = (seg[:,:,2]>110)&(seg[:,:,0]<110)&(seg[:,:,1]<110)
    cols = np.where(m.sum(axis=0)>1)[0]
    # cluster into arrows
    n = 0
    if len(cols):
        n = 1
        for i in range(1, len(cols)):
            if cols[i]-cols[i-1] > 6: n += 1
    check(tag, n >= 6, f'{n} arrow clusters')

print("== 4. callout + caption + annotations ==")
pk_t = lambda s: (np.abs(s - np.array([0xFF,0xCC,0xCC])).max(axis=2) <= 30)
bb = inkband(R, rpx(60), rpx(160), rpx(50), rpx(115), pk_t, minc=20)
check('callout box', bb and abs(bb[0]-f2r_y(54))<=12, f'{bb} vs ~{f2r_y(54)}..{f2r_y(101)}')
red_ink = lambda s: (s[:,:,0]>140)&(s[:,:,1]<85)&(s[:,:,2]<85)
bt = inkband(R, rpx(70), rpx(150), rpx(58), rpx(100), red_ink, minc=2)
check('callout text ink', bt and abs(bt[0]-f2r_y(62))<=12, f'{bt} vs ~{f2r_y(62)}..{f2r_y(92)}')
pkc = lambda s: (np.abs(s - np.array([0xFF,0xB6,0xC1])).max(axis=2) <= 35)
bc = inkband(R, rpx(280), rpx(545), rpx(522), rpx(542), pkc, minc=40)
check('caption pink band', bc, f'{bc} vs ~{f2r_y(504)}..{f2r_y(515)}')
dk = lambda s: (s.max(axis=2)<150)
bt = inkband(R, f2r_x(280), f2r_x(545), rpx(524), rpx(542), dk, minc=3)
check('caption text ink', bt and abs(bt[0]-f2r_y(506))<=12, f'{bt} vs ~{f2r_y(506)}..{f2r_y(513)}')
# annotations: orange pair #1 near 233/250, blue pair, orange #2, red pair
oran_t = lambda s: (np.abs(s[:,:,0]-0xE8)<55)&(np.abs(s[:,:,1]-0xA0)<55)&(s[:,:,2]<110)
bt = inkband(R, rpx(50), rpx(150), rpx(225), rpx(262), oran_t, minc=2)
check('ann Residual#1 orange', bt and abs(bt[0]-f2r_y(223))<=12, f'{bt} vs ~{f2r_y(223)}..{f2r_y(244)}')

print("== 5. containment (ink inside house panel x 42..918, y 45..539 slide; panel borders excl.) ==")
r0, r1 = rpx(46), rpx(534)
c0, c1 = rpx(46), rpx(914)
inner = R[r0:r1, c0:c1]
nonwhite = (inner.max(axis=2) < 200)
ys, xs = np.where(nonwhite)
check('no ink beyond panel bounds', len(ys)==0 or (ys.min()>2 and xs.min()>2), f'ink bbox in window: y {ys.min() if len(ys) else None}..{ys.max() if len(ys) else None}, x {xs.min() if len(xs) else None}..{xs.max() if len(xs) else None}')

print("== 6. ellipsis dots: 5 per row ==")
for tag, f0, f1, test, colr in [('final',65,81,blu_t,'blue'),('postFFN',173,188,blu_t,'blue'),('postLN',278,295,blu_t,'blue'),('outatt',384,400,blu_t,'blue'),('X',487,503,grn_t,'green')]:
    y0,y1 = f2r_y(f0), f2r_y(f1)
    seg = R[y0:y1, f2r_x(620):f2r_x(715)]
    m = test(seg)
    cols = np.where(m.sum(axis=0)>0)[0]
    n=0
    if len(cols):
        n=1
        for i in range(1,len(cols)):
            if cols[i]-cols[i-1]>3: n+=1
    check(f'dots {tag} ({colr})', n==5, f'{n} clusters')

print()
print('SELFCHECK RESULT:', 'ALL PASS' if ok else 'FAILURES PRESENT')
