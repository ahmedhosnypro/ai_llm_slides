from PIL import Image
import numpy as np
R = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide046/render_1.png').convert('RGB')).astype(int)
S = 150/72
def rpx(v): return int(round(v * S))
ok = True
def check(name, cond, detail=""):
    global ok
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")
    if not cond: ok = False
# house gray panel visible strip (y 45..52 slide, x 46 slide — left of the diagram panel)
got = tuple(R[rpx(48), rpx(46)])
check('house gray panel strip (46,48)', all(abs(int(g)-e)<=12 for g,e in zip(got,(233,233,231))), f'{got}')
# callout box: FFCCCC rows between the panel top border (52.3) and box bottom (105.7)
pk = (np.abs(R - np.array([0xFF,0xCC,0xCC])).max(axis=2) <= 12)
seg = pk[rpx(56):rpx(104), rpx(60):rpx(158)]
rows = np.where(seg.sum(axis=1) > 100)[0]
b = (rows.min()+rpx(56), rows.max()+rpx(56)) if len(rows) else None
check('callout FFCCCC fill band', b and abs(b[0]-rpx(56.5))<=8 and abs(b[1]-rpx(104))<=8, f'{b} vs ~{rpx(56.5)}..{rpx(104)}')
# caption text: RED ink below the X row
red = (R[:,:,0]>120)&(R[:,:,1]<90)&(R[:,:,2]<90)
seg = red[rpx(527):rpx(542), rpx(270):rpx(545)]
rows = np.where(seg.sum(axis=1) > 3)[0]
b = (rows.min()+rpx(527), rows.max()+rpx(527)) if len(rows) else None
check('caption text (red ink)', b and abs(b[0]-rpx(530.6))<=9, f'{b} vs ~{rpx(530.6)}..{rpx(538)}')
# RELU tags: blended-red mask (7pt glyphs on cream)
redr = (R[:,:,0]>150)&(R[:,:,0]-R[:,:,1]>60)&(R[:,:,0]-R[:,:,2]>60)
tiles = [193.5, 275.3, 356.6, 439.7, 520.3, 601.9, 769.5, 850.5]
cnt = 0
for cx in tiles:
    seg = redr[rpx(243):rpx(253), rpx(cx+6):rpx(cx+34)]
    if seg.sum() > 4: cnt += 1
check('RELU tags present', cnt==8, f'{cnt}/8 tiles')
print()
print('SELFCHECK-3 RESULT:', 'ALL PASS' if ok else 'FAILURES PRESENT')
