from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg').convert('RGB')).astype(int)
R, G, B = im[:,:,0], im[:,:,1], im[:,:,2]
red = (R-G>45)&(R-B>45)
blue = (B-R>45)&(B-G>30)
grayish = (abs(R-G)<25)&(abs(G-B)<25)&(abs(R-B)<25)&(R<200)&(R>90)

def colruns(mask, y0, y1, x0=66, x1=892, minrun=2, frac=0.5):
    sub = mask[y0:y1, x0:x1]
    f = sub.mean(axis=0)
    on = f > frac
    runs, s = [], None
    for i, v in enumerate(on):
        if v and s is None: s = i
        if not v and s is not None:
            if i-s >= minrun: runs.append((s+x0, i-1+x0))
            s = None
    if s is not None: runs.append((s+x0, x1-1))
    return runs

def rowruns(mask, x0, x1, y0, y1, minrun=2, frac=0.5):
    sub = mask[y0:y1, x0:x1]
    f = sub.mean(axis=1)
    on = f > frac
    runs, s = [], None
    for i, v in enumerate(on):
        if v and s is None: s = i
        if not v and s is not None:
            if i-s >= minrun: runs.append((s+y0, i-1+y0))
            s = None
    if s is not None: runs.append((s+y0, y1-1))
    return runs

print("ROW1 red vertical strokes y[125,152]:", colruns(red, 125, 152))
print("ROW1 red horiz strokes x[170,560]:", rowruns(red, 170, 560, 118, 160))
print("ROW2 blue vertical strokes y[190,226]:", colruns(blue, 190, 226))
print("ROW2 blue horiz strokes x[170,560]:", rowruns(blue, 170, 560, 184, 232))
print("ROW3 red vertical strokes y[266,306]:", colruns(red, 266, 306))
print("ROW3 red horiz strokes x[170,560]:", rowruns(red, 170, 560, 260, 312))
print("ROW1 gray dots y[130,150]:", colruns(grayish, 130, 150, 560, 740, frac=0.25))
print("ROW2 blue dots y[195,225]:", colruns(blue, 195, 225, 560, 740, frac=0.25))
print("ROW3 orange: R>200,G 100-190,B<110")
orange = (R>200)&(G>90)&(G<200)&(B<120)&(R-B>90)
print("  orange vertical y[266,306]:", colruns(orange, 266, 306))
print("  orange horiz x[170,560]:", rowruns(orange, 170, 560, 260, 312, frac=0.3))
print("CYAN fill bbox:")
cyan = (B>235)&(G>240)&(R>215)&(R<245)&(G-R>8)
ys, xs = np.where(cyan)
print("  bbox x[%d,%d] y[%d,%d] n=%d" % (xs.min(), xs.max(), ys.min(), ys.max(), len(xs)))
print("cyan fill core color:", im[440, 300].tolist(), im[470, 500].tolist(), im[380, 600].tolist())
