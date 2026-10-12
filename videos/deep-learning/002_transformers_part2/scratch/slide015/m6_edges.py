from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)

def hx(t): return '#%02X%02X%02X' % tuple(t)

# h1 card: horizontal scan at y=400 (below ellipses) for salmon run
row = im[400]
sal = [x for x in range(960) if abs(row[x][0]-241)+abs(row[x][1]-139)+abs(row[x][2]-150) < 60]
print('y=400 salmon x-run:', min(sal), '..', max(sal))
row = im[190]
sal = [x for x in range(960) if abs(row[x][0]-241)+abs(row[x][1]-139)+abs(row[x][2]-150) < 60]
print('y=190 salmon x-run:', min(sal), '..', max(sal))
# vertical scan at x=620 (right of interior elements) for salmon run
col = im[:,620]
sal = [y for y in range(540) if abs(col[y][0]-241)+abs(col[y][1]-139)+abs(col[y][2]-150) < 60]
print('x=620 salmon y-run:', min(sal), '..', max(sal))
col = im[:,110]
sal = [y for y in range(540) if abs(col[y][0]-241)+abs(col[y][1]-139)+abs(col[y][2]-150) < 60]
print('x=110 salmon y-run:', (min(sal), max(sal)) if sal else None)

# top slivers: scan column x=300 (through plane region?) y 40..200
print('col x=300, y40..205:', ' '.join(f'{y}:{hx(im[y,300])}' for y in range(40, 206, 15)))
print('col x=450, y40..205:', ' '.join(f'{y}:{hx(im[y,450])}' for y in range(40, 206, 15)))
print('col x=700, y40..205:', ' '.join(f'{y}:{hx(im[y,700])}' for y in range(40, 206, 15)))
print('col x=850, y40..205:', ' '.join(f'{y}:{hx(im[y,850])}' for y in range(40, 206, 15)))
# query row area scan y=405 row
print('row y=405, x180..420:', ' '.join(f'{x}:{hx(im[405,x])}' for x in range(180, 421, 20)))
# W(1-4) zone scan
print('row y=360..425 col x=612:', ' '.join(f'{y}:{hx(im[y,612])}' for y in range(340, 431, 10)))
print('row y=390, x580..680:', ' '.join(f'{x}:{hx(im[390,x])}' for x in range(580, 681, 10)))
# title zone
print('row y=470, x330..670:', ' '.join(f'{x}:{hx(im[470,x])}' for x in range(330, 671, 20)))
