from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)

def classify(px):
    r,g,b = px
    if r>235 and g>235 and b>235: return '.'          # white
    if abs(r-233)<14 and abs(g-232)<14 and abs(b-231)<14: return ' '  # panel gray
    if r>200 and 100<g<190 and 100<b<190 and r-g>50: return 'S'       # salmon/pink card
    if 150<r<220 and 140<g<210 and b>200 and b-r>25: return 'L'       # lavender
    if r>220 and g>220 and 100<b<190: return 'Y'                      # yellow
    if 150<r<230 and g>215 and 150<b<220 and g-r>20: return 'G'       # pale green card
    if r>230 and 180<g<230 and 130<b<190 and r-b>60: return 'P'       # peach
    if r>220 and 120<g<200 and b<120: return 'O'                      # orange
    if r<180 and g>150 and b<180 and g-r>30: return 'K'               # green (key/strong)
    if r>180 and g<120 and b<120: return 'R'                          # red
    if r<100 and g<100 and b<100: return '#'                          # black
    if b>140 and b-r>40 and b-g>20: return 'B'                        # blue
    if abs(r-g)<25 and abs(g-b)<25 and 100<r<210: return 'm'          # gray/plane
    return '?'

print('    ' + ''.join(str((x//10)%10) for x in range(0,960,10)))
for y in range(40, 540, 10):
    line = []
    for x in range(0, 960, 10):
        # dominant class in 10x10 cell
        from collections import Counter
        c = Counter(classify(im[y+dy, x+dx]) for dy in (3,7) for dx in (3,7))
        line.append(c.most_common(1)[0][0])
    print(f'{y:3d} ' + ''.join(line))
