from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_036.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

def sat(px):
    r,g,b = px
    return max(r,g,b) - min(r,g,b)

# Border stroke detection: a pixel is "stroke" if saturated OR dark (luminance < 140)
lum = a.mean(axis=2)
s = a.max(axis=2) - a.min(axis=2)
stroke = (s > 60) | (lum < 150)

# vertical strokes: columns with long runs inside a y-window
def vedges(x0, x1, y0, y1, minrun=30):
    res=[]
    for x in range(x0, x1):
        col = stroke[y0:y1, x]
        # longest run
        best=0; cur=0
        for v in col:
            cur = cur+1 if v else 0
            best = max(best,cur)
        if best >= minrun:
            res.append((x,best))
    return res

def hedges(y0, y1, x0, x1, minrun=30):
    res=[]
    for y in range(y0, y1):
        row = stroke[y, x0:x1]
        best=0; cur=0
        for v in row:
            cur = cur+1 if v else 0
            best = max(best,cur)
        if best >= minrun:
            res.append((y,best))
    return res

def sample(x,y):
    return tuple(a[y,x])

print("== VECTOR CONTAINER (expect ~x48..269 y97..367) ==")
print(' v-edges:', vedges(40, 90, 110, 350, 60)[:8], '...', vedges(250, 285, 110, 350, 60)[:8])
print(' h-edges top:', hedges(85, 115, 60, 250, 60)[:8])
print(' h-edges bot:', hedges(350, 380, 60, 250, 60)[:8])
print("== EQUATIONS BOX (expect ~x307..662 y108..227) ==")
print(' v-edges L:', vedges(295, 325, 120, 215, 40)[:8], ' R:', vedges(640, 675, 120, 215, 40)[:8])
print(' h top:', hedges(95, 120, 330, 640, 100)[:8], ' bot:', hedges(215, 240, 330, 640, 100)[:8])
print(' border color samples:', [sample(x,160) for x in range(305,318)], [sample(655,y) for y in range(150,165)])
print("== BELL BOX (expect ~x682..893 y108..221) ==")
print(' v-edges L:', vedges(670, 695, 115, 215, 30)[:6], ' R:', vedges(885, 905, 115, 215, 30)[:6])
print(' h top:', hedges(95, 120, 700, 880, 80)[:6], ' bot:', hedges(210, 235, 700, 880, 80)[:6])
print(' border color:', [sample(x,170) for x in range(680,692)], [sample(890,y) for y in range(150,160)])
print("== REMEMBER BOX (expect ~x48..230 y383..508) ==")
print(' v-edges L:', vedges(40, 65, 395, 500, 30)[:6], ' R:', vedges(220, 245, 395, 500, 30)[:6])
print(' h top:', hedges(370, 400, 60, 210, 60)[:6], ' bot:', hedges(495, 525, 60, 210, 60)[:6])
print(' border color:', [sample(x,450) for x in range(48,60)], [sample(225,y) for y in range(430,442)])
print("== FLOWCHART2 MAGENTA (expect ~x518..902 y373..518) ==")
print(' v-edges L:', vedges(505, 540, 390, 510, 40)[:8], ' R:', vedges(890, 915, 390, 510, 40)[:8])
print(' h top:', hedges(360, 390, 560, 880, 80)[:6], ' bot:', hedges(505, 530, 560, 880, 80)[:6])
print(' border color:', [sample(518+dx, 450) for dx in range(-4,5)], [sample(x,375+dy) for x in range(700,706) for dy in range(-3,4)][:4])
print("== FORMULA BOXES ==")
print(' box1 v:', vedges(275, 300, 315, 350, 20)[:6], vedges(430, 455, 315, 350, 20)[:6])
print(' box1 h:', hedges(295, 320, 300, 430, 50)[:6], hedges(350, 375, 300, 430, 50)[:6])
print(' box2 v:', vedges(488, 512, 300, 355, 25)[:6], vedges(645, 668, 300, 355, 25)[:6])
print(' box2 h:', hedges(285, 305, 510, 640, 50)[:6], hedges(358, 380, 510, 640, 50)[:6])
print(' box3 v:', vedges(672, 695, 315, 345, 20)[:6], vedges(825, 850, 315, 345, 20)[:6])
print(' box3 h:', hedges(300, 322, 690, 820, 50)[:6], hedges(348, 370, 690, 820, 50)[:6])
