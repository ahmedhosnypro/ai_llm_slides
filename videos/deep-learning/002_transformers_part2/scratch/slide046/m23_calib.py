from PIL import Image
import numpy as np
a = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')).astype(int)
a45 = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_045.jpg').convert('RGB')).astype(int)
def sx(fx): return (fx-17.582)/0.962329
def sy(fy): return fy/0.955556
def classify(p):
    r,g,b = int(p[0]), int(p[1]), int(p[2])
    mx, mn = max(r,g,b), min(r,g,b)
    if r>140 and g<85 and b<85: return 'R'
    if mx>=246 and mx-mn<12: return '.'
    if mx-mn<16: return 'g' if mx<228 else 'G'
    if b>100 and r<100 and g<100: return 'N'
    if g>110 and r<115 and b<115: return 'n'
    if r>200 and g>200 and b<190: return 'y'
    if r>190 and b>140 and g<r-15: return 'm'
    return '?'
print('== callout fine map (x 50..185, y 40..118) ==')
for y in range(40, 118):
    print(f'{y:4d} ' + ''.join(classify(a[y,x]) for x in range(50, 186)))
