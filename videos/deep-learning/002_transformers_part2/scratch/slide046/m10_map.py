from PIL import Image
import numpy as np
def classify(p):
    r,g,b = p
    mx, mn = max(p), min(p)
    if mx > 246 and mx-mn < 14: return '.'          # white
    if r>140 and g<90 and b<90: return 'R'          # red ink
    if mx-mn < 18: return 'g' if r<225 else 'G'     # gray dark/light
    if g>r and g>b: return 'n' if g<220 else 'v'    # green dark/pale
    if r>200 and g>200 and b<190: return 'y'        # yellow
    if r>200 and b>190 and g<r-20: return 'm'       # magenta/pink
    if r>180 and g<r-30 and b<r-30: return 'o'      # orange
    if b>r and b>g: return 'l'                      # lavender/blue
    return '?'
for fname, rows in [('045', [(165,190)]), ('046', [(60,88)])]:
    a = np.asarray(Image.open(f'videos/deep-learning/002_transformers_part2/unique_slides/slide_{fname}.jpg').convert('RGB')).astype(int)
    for y0,y1 in rows:
        print(f'--- {fname} rows {y0}..{y1}, x 175..235 ---')
        print('     ' + ''.join(str(x//10%10) for x in range(175,235)))
        print('     ' + ''.join(str(x%10) for x in range(175,235)))
        for y in range(y0,y1):
            print(f'{y:4d} ' + ''.join(classify(a[y,x]) for x in range(175,235)))
