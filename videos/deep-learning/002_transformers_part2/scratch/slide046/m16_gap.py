from PIL import Image
import numpy as np
a = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')).astype(int)
def probe(x0, x1, y0, y1, label):
    print(f'--- {label} (x{x0}..{x1}, y{y0}..{y1}) ---')
    for y in range(y0, y1):
        row = a[y, x0:x1]
        s = ''
        for p in row:
            r,g,b = int(p[0]),int(p[1]),int(p[2])
            if r>140 and g<85 and b<85: s+='R'
            elif max(r,g,b)>=246 and max(r,g,b)-min(r,g,b)<12: s+='.'
            elif b>110 and r<100 and g<100: s+='N'
            elif g>110 and r<115 and b<115: s+='n'
            elif r>170 and g<r-40 and b<r-40: s+='o'
            elif r>190 and b>140 and g<r-15: s+='m'
            elif max(r,g,b)-min(r,g,b)<16: s+='G' if max(r,g,b)<228 else 'g'
            else: s+='?'
        print(f'{y:4d} {s}')
# bottom unit gap bar->postLN, columns 1,3,5 (cx 205,351,499)
probe(199, 212, 293, 315, 'bottom gap col1 cx=205')
probe(345, 358, 293, 315, 'bottom gap col3 cx=351')
# top unit red gap, col1 and col3
probe(199, 212, 80, 104, 'top red gap col1')
probe(345, 358, 80, 104, 'top red gap col3')
