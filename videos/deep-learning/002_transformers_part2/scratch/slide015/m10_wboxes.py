from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
par = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
def hx(t): return '#%02X%02X%02X' % tuple(t)

print('CHILD red-ish scan x555..700, y330..430 (every 5px):')
for y in range(330, 431, 5):
    cells = []
    for x in range(555, 701, 5):
        r,g,b = im[y,x]
        cells.append('R' if (r>150 and g<110 and b<110) else ('.' if r+g+b>700 else ' '))
    print(f'  y={y}: {"".join(cells)}')

print('PARENT same-model region (x=(x-54.3)/.954, y=(y+86.1)/.960) sample:')
for (x,y) in [(600,460),(610,470),(620,480),(590,450),(600,440),(640,430)]:
    print(f'  parent({x},{y}) {hx(par[y,x])}  <-> child model ({0.954*x+54.3:.0f},{0.960*y-86.1:.0f}) {hx(im[int(0.960*y-86.1), int(0.954*x+54.3)])}')

print('PARENT red bar right of Probabilities oval (384..457, 244..258):')
for y in (246, 250, 254):
    print('  ', ' '.join(f'{x}:{hx(par[y,x])}' for x in range(380, 462, 10)))
print('CHILD mapped red bar (419..489, 148..162):')
for y in (150, 154, 158):
    print('  ', ' '.join(f'{x}:{hx(im[y,x])}' for x in range(415, 494, 10)))
