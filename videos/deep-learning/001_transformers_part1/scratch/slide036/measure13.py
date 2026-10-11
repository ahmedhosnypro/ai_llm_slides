from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_036.jpg').convert('RGB')
a = np.asarray(im).astype(int)
# print a fine map of x214..270, y128..240 at 2px
print('fine map right V2 (x214-270, y128-240), 2px cells: B=blue R=red .=bg')
for y in range(128, 242, 2):
    row=''
    for x in range(214, 272, 2):
        block = a[y:y+2, x:x+2].reshape(-1,3)
        sat = block.max(axis=1)-block.min(axis=1)
        l = block.mean(axis=1)
        i = int(np.argmax(sat*0.7 + (255-l)))
        r,g,b = block[i]
        c = '.'
        if l.mean() < 235:
            if b > r+40 and b>90: c='B'
            elif r > g+40 and r>80: c='R'
            else: c='k'
        row += c
    print('%3d %s' % (y,row))
print()
print('left V2 fine map (x92-152, y128-235):')
for y in range(128, 236, 2):
    row=''
    for x in range(92, 152, 2):
        block = a[y:y+2, x:x+2].reshape(-1,3)
        sat = block.max(axis=1)-block.min(axis=1)
        l = block.mean(axis=1)
        i = int(np.argmax(sat*0.7 + (255-l)))
        r,g,b = block[i]
        c = '.'
        if l.mean() < 235:
            if b > r+40 and b>90: c='B'
            elif r > g+40 and r>80: c='R'
            else: c='k'
        row += c
    print('%3d %s' % (y,row))
