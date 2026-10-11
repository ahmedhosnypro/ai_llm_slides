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
    print(f'{label}: median {tuple(np.median(arr,axis=0).astype(int))}')

# FC2 box right border at x898-899?
stroke_color([(898,y) for y in range(390,510,12)], 'FC2 right x=898')
stroke_color([(899,y) for y in range(390,510,12)], 'FC2 right x=899')
stroke_color([(513,y) for y in range(390,510,12)], 'FC2 left x=513')
stroke_color([(x,373) for x in range(530,890,30)], 'FC2 top y=373')

# Formula box3: find v-edges in range x660..870, y315..350
lum = a.mean(axis=2); s = a.max(axis=2)-a.min(axis=2)
stroke = (s>60)|(lum<150)
for x in range(660, 870):
    col = stroke[315:350, x]
    best=0; cur=0
    for v in col:
        cur=cur+1 if v else 0; best=max(best,cur)
    if best>=20: print('box3 v-edge x=',x,'run',best, tuple(a[330,x]))
