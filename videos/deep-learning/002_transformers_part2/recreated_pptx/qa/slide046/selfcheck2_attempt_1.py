from PIL import Image
import numpy as np
R = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide046/render_1.png').convert('RGB')).astype(int)
S = 150/72
def rpx(v): return int(round(v * S))
def f2r_x(fx): return int(round((fx-17.582)/0.962329 * S))
def f2r_y(fy): return int(round(fy/0.955556 * S))
ok = True
def check(name, cond, detail=""):
    global ok
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")
    if not cond: ok = False

print("== corrected checks ==")
# MHA bar: full-width navy rows (count>500) in the bar zone
navy_t = lambda s: (s[:,:,2]>110)&(s[:,:,0]<100)&(s[:,:,1]<100)
seg = R[f2r_y(415):f2r_y(495), f2r_x(200):f2r_x(850)]
m = navy_t(seg)
rows = np.where(m.sum(axis=1) > 500)[0]
b = (rows.min()+f2r_y(415), rows.max()+f2r_y(415)) if len(rows) else None
check('MHA bar full-width band', b and abs(b[0]-f2r_y(419))<=9 and abs(b[1]-f2r_y(468))<=9, f'{b} vs {f2r_y(419)}..{f2r_y(468)}')
# FFN box fill: sample between tiles (x=235 slide: gap between tile1 229.9 and tile2 239) at y=250
got = tuple(R[rpx(250), rpx(235)])
check('FFN box fill (inter-tile gap)', all(abs(int(g)-e)<=25 for g,e in zip(got,(221,235,247))), f'{got}')
# tile cream: sample between green-dot row and tile top (y=243, x between dots cx-18)
got = tuple(R[rpx(243), rpx(193.5-18)])
check('tile cream (clean spot)', all(abs(int(g)-e)<=40 for g,e in zip(got,(255,230,153))), f'{got}')
# house gray panel: sample inside panel near left edge (x=50 slide, y=20)
got = tuple(R[rpx(20), rpx(50)])
check('house gray panel (x=50)', all(abs(int(g)-e)<=12 for g,e in zip(got,(233,233,231))), f'{got}')
# callout box: dense pink rows (count>60) in the callout x-range
pk = (np.abs(R - np.array([0xFF,0xCC,0xCC])).max(axis=2) <= 30)
seg = pk[f2r_y(48):f2r_y(112), rpx(60):rpx(158)]
rows = np.where(seg.sum(axis=1) > 60)[0]
b = (rows.min()+f2r_y(48), rows.max()+f2r_y(48)) if len(rows) else None
check('callout box (dense pink)', b and abs(b[0]-f2r_y(54))<=12 and abs(b[1]-f2r_y(101))<=12, f'{b} vs {f2r_y(54)}..{f2r_y(101)}')
# caption text: dark ink strictly below the X row (y>527 slide)
dk = (R.max(axis=2)<150)
seg = dk[rpx(527):rpx(542), f2r_x(280):f2r_x(545)]
rows = np.where(seg.sum(axis=1) > 3)[0]
b = (rows.min()+rpx(527), rows.max()+rpx(527)) if len(rows) else None
check('caption text ink (below X row)', b and abs(b[0]-f2r_y(506))<=14, f'{b} vs ~{f2r_y(506)}..{f2r_y(513)}')
# annotation pair #1: orange ink with x narrowed to 50..138 slide (excludes col1 curve at 142.9+)
oran = (np.abs(R[:,:,0]-0xE8)<55)&(np.abs(R[:,:,1]-0xA0)<55)&(R[:,:,2]<110)
seg = oran[f2r_y(222):f2r_y(262), rpx(50):rpx(138)]
rows = np.where(seg.sum(axis=1) > 2)[0]
b = (rows.min()+f2r_y(222), rows.max()+f2r_y(222)) if len(rows) else None
check('ann Residual#1 (narrow x)', b and abs(b[0]-f2r_y(223))<=12, f'{b} vs ~{f2r_y(223)}..{f2r_y(255)}')
# bar texts: dark ink inside bars at 423..604 frame-x
for tag, f0, f1 in [('top bar text',108,122),('bottom bar text',319,332)]:
    seg = dk[f2r_y(f0)-4:f2r_y(f1)+4, f2r_x(423):f2r_x(604)]
    rows = np.where(seg.sum(axis=1) > 3)[0]
    check(tag, len(rows)>0 and abs(rows.min()+f2r_y(f0)-4-f2r_y(f0))<=12, f'rows {rows.min() if len(rows) else None}..{rows.max() if len(rows) else None}')
# MHA white text present
wh = (R[:,:,0]>190)&(R[:,:,1]>190)&(R[:,:,2]>190)
seg = wh[f2r_y(455):f2r_y(475), f2r_x(390):f2r_x(660)]
check('MHA bar white text', int(seg.sum())>400, f'{int(seg.sum())} white px')
# FFN title blue ink
blu = (R[:,:,2]>110)&(R[:,:,0]<90)&(R[:,:,1]<90)
seg = blu[f2r_y(218):f2r_y(236), f2r_x(290):f2r_x(760)]
check('FFN title blue ink', int(seg.sum())>200, f'{int(seg.sum())} px')
# green dots + magenta dots rows in the FFN box (col1)
gd = (R[:,:,1]>110)&(R[:,:,0]<115)&(R[:,:,2]<115)
seg = gd[f2r_y(232):f2r_y(268), rpx(180):rpx(230)]
rows = np.where(seg.sum(axis=1) > 2)[0]
check('FFN icon green dot band', len(rows)>0 and abs(rows.min()+f2r_y(232)-f2r_y(236))<=12, f'{rows.min() if len(rows) else None}..{rows.max() if len(rows) else None} vs ~{f2r_y(236)}..{f2r_y(241)}')
mg = (R[:,:,0]>150)&(R[:,:,2]>150)&(R[:,:,1]<130)
seg = mg[f2r_y(244):f2r_y(272), rpx(180):rpx(230)]
rows = np.where(seg.sum(axis=1) > 2)[0]
check('FFN icon magenta band', len(rows)>0 and abs(rows.min()+f2r_y(244)-f2r_y(247))<=12, f'{rows.min() if len(rows) else None}..{rows.max() if len(rows) else None} vs ~{f2r_y(247)}..{f2r_y(252)}')
# RELU tags: red ink in the tile top-right zones (8 tiles)
redr = (R[:,:,0]>140)&(R[:,:,1]<90)&(R[:,:,2]<90)
tiles = [193.5, 275.3, 356.6, 439.7, 520.3, 601.9, 769.5, 850.5]
cnt = 0
for cx in tiles:
    seg = redr[f2r_y(241):f2r_y(252), rpx(cx+8):rpx(cx+34)]
    if seg.sum() > 4: cnt += 1
check('RELU tags present', cnt>=6, f'{cnt}/8 tiles')
print()
print('SELFCHECK-2 RESULT:', 'ALL PASS' if ok else 'FAILURES PRESENT')
