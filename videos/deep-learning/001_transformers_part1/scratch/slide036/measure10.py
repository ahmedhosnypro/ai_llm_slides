from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_036.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def stroke_color(pts, label):
    best=[]
    for (x,y) in pts:
        cand = a[max(0,y-2):y+3, max(0,x-2):x+3].reshape(-1,3)
        lum = cand.mean(axis=1); sat = cand.max(axis=1)-cand.min(axis=1)
        score = sat*1.5 + (255-lum)
        i = int(np.argmax(score))
        best.append(tuple(cand[i]))
    arr = np.array(best)
    print(f'{label}: median {tuple(np.median(arr,axis=0).astype(int))} samples {best[:5]}')

# Left bracket tall stroke x51..62
stroke_color([(54,200),(56,250),(53,300),(55,170)], 'VEC tall stroke A x51-62')
# x60..83
stroke_color([(70,200),(75,250),(65,300)], 'VEC tall stroke B x60-83')
# X column entries x59..74
stroke_color([(66,148),(66,165),(66,182),(66,200)], 'VEC left column glyphs')
# bracket x170..182 / x191..202
stroke_color([(175,250),(176,300),(196,250),(197,300)], 'VEC right brackets x170/191')
# 5-X column? check x94..124 y131..214
stroke_color([(100,150),(110,150),(100,180),(118,160)], 'VEC x94-124 block')
stroke_color([(220,150),(230,160),(240,180)], 'VEC x215-244 block')
# orange divider: scan row 250 for orange
row=250
for x in range(110,175):
    r,g,b = a[row,x]
    if r>180 and 90<g<190 and b<110: print('orange px at x=%d color'%(x), (r,g,b))
# find the divider column: check multiple rows
cols=[]
for x in range(100,180):
    hits=0
    for y in range(120,350):
        r,g,b=a[y,x]
        if r>170 and 80<g<190 and b<120: hits+=1
    if hits>10: cols.append((x,hits))
print('orange-ish column hits:', cols[:12])
# white block arrow with blue outline at mid-height: scan y240..269 x115..168 (blue cc found x115..168 y240..269)
stroke_color([(140,245),(130,255),(150,255),(120,250)], 'arrow outline')
# fill of arrow
print('arrow fill samples:', [tuple(a[y,x]) for x,y in [(140,252),(135,260),(145,258),(138,248)]])
# container fill
print('container fill:', [tuple(a[y,x]) for x,y in [(130,120),(230,240),(150,340),(90,300)]])
# V1 header color
stroke_color([(60,115),(100,115),(180,115),(220,115)], 'V headers')
# M column glyphs color
stroke_color([(185,150),(185,250),(185,300),(230,150)], 'M glyphs right')
