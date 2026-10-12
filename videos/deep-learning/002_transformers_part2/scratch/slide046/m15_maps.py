from PIL import Image
import numpy as np
a = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')).astype(int)
def classify(p):
    r,g,b = int(p[0]), int(p[1]), int(p[2])
    mx, mn = max(r,g,b), min(r,g,b)
    if r>140 and g<85 and b<85: return 'R'
    if mx>=248 and mx-mn<10: return '.'
    if mx-mn<16: return 'g' if mx<228 else 'G'
    if b>110 and r<100 and g<100: return 'N'   # navy/blue
    if g>110 and r<115 and b<115: return 'n'   # green
    if r>200 and g>200 and b<190: return 'y'
    if r>190 and b>150 and g<r-15: return 'm'  # pink/magenta
    if r>170 and g<r-40 and b<r-40: return 'o' # orange
    if b>r and b>g: return 'l'
    return '?'
bands = [('A: final row + red arrows + container top', 62, 105),
         ('B: bar/green/plus/navy/postFFN/FFNtop', 126, 210),
         ('C: FFNbot/block?/postLN/red?/conttop/bar', 258, 320),
         ('D: bar/plus/navy/outatt/MHA', 338, 424),
         ('E: MHA/Xrow/caption', 462, 516)]
for bname, y0, y1 in bands:
    print(f'===== {bname} =====')
    hdr = '     ' + ''.join(str(x//100%10) if x%20==0 else ' ' for x in range(140, 912, 4))
    print(hdr)
    for y in range(y0, y1, 2):
        print(f'{y:4d} ' + ''.join(classify(a[y,x]) for x in range(140, 912, 4)))
