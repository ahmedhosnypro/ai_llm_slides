from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_036.jpg').convert('RGB')
a = np.asarray(im).astype(int)
def cls(px):
    r,g,b=px
    if r>230 and g>200 and b<190: return 'T'   # tan fill
    if r>180 and g<90 and b<90: return 'R'     # red border
    if r<100 and g<100 and b<100: return 'k'   # dark text
    if b>r+40: return 'B'
    if r>235 and g>235 and b>235: return '.'
    return '?'
print('FC1 left stack column samples (x=307..334):')
print('  y   x307  x312  x318  x324  x330')
for y in range(393, 520, 3):
    print('%4d  %s' % (y, '   '.join('%s%s%s' % cls(a[y,x]) for x in (307,312,318,324,330))))
print()
print('exact colors: (312,400):',tuple(a[400,312]),'(312,410):',tuple(a[410,312]),'(318,404):',tuple(a[404,318]))
print('(312,430):',tuple(a[430,312]),'(318,436):',tuple(a[436,318]),'(330,464):',tuple(a[464,330]))
