from PIL import Image
import numpy as np
a = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')).astype(int)
def classify(p):
    r,g,b = int(p[0]), int(p[1]), int(p[2])
    mx, mn = max(r,g,b), min(r,g,b)
    if r>140 and g<85 and b<85: return 'R'
    if mx>=248 and mx-mn<10: return '.'
    if mx-mn<16: return 'g' if mx<228 else 'G'
    if b>110 and r<100 and g<100: return 'N'
    if g>110 and r<115 and b<115: return 'n'
    if r>200 and g>200 and b<190: return 'y'
    if r>190 and b>150 and g<r-15: return 'm'
    if r>170 and g<r-40 and b<r-40: return 'o'
    if b>r and b>g: return 'l'
    return '?'
print('===== gap MHA->outatt (y 398..422) =====')
for y in range(398, 423, 1):
    print(f'{y:4d} ' + ''.join(classify(a[y,x]) for x in range(190, 320, 2)))
print('===== gap X->MHA (y 466..490) =====')
for y in range(466, 490, 1):
    print(f'{y:4d} ' + ''.join(classify(a[y,x]) for x in range(190, 320, 2)))
print('===== X row + caption (y 484..516) =====')
for y in range(484, 516, 1):
    print(f'{y:4d} ' + ''.join(classify(a[y,x]) for x in range(240, 420, 2)))
