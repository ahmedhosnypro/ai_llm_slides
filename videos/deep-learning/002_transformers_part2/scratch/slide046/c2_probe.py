from PIL import Image
import numpy as np
R = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide046/render_1.png').convert('RGB')).astype(int)
S = 150/72
def rpx(v): return int(round(v * S))
# 1. callout zone rows 95..130 render (slide 45.6..62.4), x 125..333
print('callout zone: per-row pinkish (FFCCCC tol 30) counts, x 125..333:')
for y in range(95, 132, 2):
    seg = R[y, rpx(60):rpx(158)]
    n = int((np.abs(seg - np.array([0xFF,0xCC,0xCC])).max(axis=1) <= 30).sum())
    print(f'  y={y} (slide {y/S:.1f}): pinkish={n} sample@x150={tuple(R[y, rpx(100)])}')
# 2. caption text: red-ink test below X row
red = (R[:,:,0]>120)&(R[:,:,1]<90)&(R[:,:,2]<90)
seg = red[rpx(526):rpx(543), f2r_x(270):f2r_x(550)] if False else red[int(526*S):int(543*S), 280*S.__int__() if False else int((280-17.582)/0.962329*S):int((545-17.582)/0.962329*S)]
rows = np.where(seg.sum(axis=1) > 3)[0]
print('caption red-ink rows (render):', (rows.min()+int(526*S), rows.max()+int(526*S)) if len(rows) else None, ' expected ~', int(530.65*S))
# 3. RELU: dump tile-1 region classified (slide x 157..232, y 238..272)
def classify(p):
    r,g,b = int(p[0]), int(p[1]), int(p[2])
    if r>140 and g<85 and b<85: return 'R'
    if max(r,g,b)>=246 and max(r,g,b)-min(r,g,b)<12: return '.'
    if max(r,g,b)-min(r,g,b)<16: return 'G' if max(r,g,b)<228 else 'g'
    if g>110 and r<115 and b<115: return 'n'
    if r>150 and b>150 and g<130: return 'm'
    if r>200 and g>200 and b<190: return 'y'
    return '?'
print('tile1 zone (slide x 157..232 step 2, y 238..272 step 2):')
for y in range(rpx(238), rpx(272), 3):
    print(f'  y={y} ({y/S:.0f}pt): ' + ''.join(classify(R[y, x]) for x in range(rpx(157), rpx(232), 2)))
