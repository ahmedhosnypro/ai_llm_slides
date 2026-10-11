from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_036.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def classify(px):
    r,g,b = px
    l = (r+g+b)/3
    if l>235: return '.'
    if b > r+40 and b>90: return 'B'   # blue
    if r > g+50 and r>100 and g<150: return 'R'  # red/maroon
    if r>180 and 80<g<190 and b<120: return 'O'  # orange
    if g > r+25 and g > b+15: return 'G'  # green
    if r>200 and g>180 and b<140: return 'Y'  # yellow
    return 'k'  # dark/other

# coarse map of vector container: x46..270 y99..373, downsample x2
print('VEC container (x46-270, y99-373), 2px cells; B=blue R=red O=orange G=green k=dark')
hdr = '    ' + ''.join(str((46+i*2)//100%10) for i in range(113))
print(hdr)
for y in range(99, 373, 4):
    row = ''
    for x in range(46, 270, 2):
        block = a[y:y+4, x:x+2].reshape(-1,3)
        l = block.mean(axis=1)
        # prefer the most saturated ink pixel in block
        sat = block.max(axis=1)-block.min(axis=1)
        i = int(np.argmax(sat*0.7 + (255-l)))
        c = classify(block[i])
        row += c if c!='.' else ('.' if l.mean()>235 else ':')
    print('%3d %s' % (y, row))
