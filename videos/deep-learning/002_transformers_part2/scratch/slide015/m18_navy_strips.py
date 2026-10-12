from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
# navy rule extent
for y in (60, 61, 62, 63, 64):
    row = im[y]
    navy = [x for x in range(60, 910) if abs(row[x][0]-58)<40 and abs(row[x][1]-50)<40 and abs(row[x][2]-149)<50]
    if navy: print(f'navy y={y}: x {min(navy)}..{max(navy)} n={len(navy)}')
# strip edges via runs on mid-rows
def runs(y, x0=380, x1=660):
    out=[]; cur=None; start=x0
    for x in range(x0,x1):
        r,g,b = im[y,x]
        cls = 'W' if r+g+b>705 else 'C'
        if cur is None: cur, start = cls, x
        elif cls != cur:
            out.append((cur, start, x-1)); cur, start = cls, x
    out.append((cur, start, x1-1))
    return [(c,a,b) for c,a,b in out if c=='C' and b-a>8]
for y,label in [(78,'h5'),(94,'h4'),(116,'h3'),(136,'h2'),(155,'h1')]:
    print(f'{label} strip y={y}: {runs(y)}')
# title ink bbox: dark pixels in y440..500, x260..700
tz = im[440:500, 260:700]
dark = (tz.sum(axis=2) < 420)
ys, xs = np.where(dark)
print('title ink bbox: x', 260+xs.min(), '..', 260+xs.max(), ' y', 440+ys.min(), '..', 440+ys.max(), ' n=', len(xs))
# red-ish title pixels (Multi Head + X2)
redt = (tz[:,:,0]>120) & (tz[:,:,1]<90) & (tz[:,:,2]<90)
ys2, xs2 = np.where(redt)
if len(xs2): print('title red ink: x', 260+xs2.min(), '..', 260+xs2.max(), ' y', 440+ys2.min(), '..', 440+ys2.max(), ' n=', len(xs2))
