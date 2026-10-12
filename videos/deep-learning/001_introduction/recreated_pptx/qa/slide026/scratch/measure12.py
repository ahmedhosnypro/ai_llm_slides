from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)
# gray panel left boundary at several rows
for y in (100, 200, 300, 450, 510):
    row = a[y]
    xs = [x for x in range(36, 100) if abs(row[x][0]-233)<12 and abs(row[x][1]-233)<12 and abs(row[x][2]-231)<12]
    print('y',y,'first gray x:', xs[:3], 'last of 36..100:', xs[-3:] if xs else None)
    print('   y',y,'x42..56:', [row[x].tolist() for x in range(42,57,2)])
# panel right boundary
for y in (300, 450):
    row = a[y]
    xs = [x for x in range(880, 930) if abs(row[x][0]-233)<12 and abs(row[x][1]-233)<12 and abs(row[x][2]-231)<12]
    print('y',y,'gray right:', xs[-3:] if xs else None, [row[x].tolist() for x in range(914,925,2)])
# yellow fill clean corner + tan2 fill corner
from collections import Counter
def modal(region,label):
    px = region.reshape(-1,3)
    q = Counter(map(tuple,(px//4*4)))
    print(label, q.most_common(4))
modal(a[340:360, 640:750],'yellow-fill-right')
modal(a[470:495, 700:830],'tan2-fill-right')
modal(a[130:150, 500:640],'tan1-fill-right')
# panel gray between container bottom (509) and footer (518)
modal(a[510:517, 200:800],'below-container gray')
