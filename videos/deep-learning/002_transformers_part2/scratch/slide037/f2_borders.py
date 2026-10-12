# f2: border profiles + badge, to anchor the frame->build affine.
from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def hprofile(y, x0, x1, label):
    row = a[y, x0:x1]
    print(f'H y={y} {label}: ' + ' '.join(f"{x}:{r},{g},{b}" for (x, (r, g, b)) in zip(range(x0, x1), row)))

def vprofile(x, y0, y1, label):
    col = a[y0:y1, x]
    print(f'V x={x} {label}: ' + ' '.join(f"{y}:{r},{g},{b}" for (y, (r, g, b)) in zip(range(y0, y1), col)))

hprofile(300, 50, 68, 'left border zone')
hprofile(300, 900, 920, 'right border zone')
vprofile(480, 38, 58, 'top border zone')
vprofile(480, 505, 522, 'bottom/letterbox zone')
hprofile(500, 50, 68, 'left border low')
vprofile(60, 500, 520, 'bottom-left corner zone')
# darkness-based border detection: any px notably darker than panel (231,233,230)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
dark = (r + g + b) < 3 * 175
colcnt = dark[100:500, :].sum(axis=0)
rowcnt = dark[:, 100:900].sum(axis=1)
print('DARK cols x<100 with >=200:', [(x, int(colcnt[x])) for x in range(0, 100) if colcnt[x] >= 200])
print('DARK cols x>860 with >=200:', [(x, int(colcnt[x])) for x in range(860, 960) if colcnt[x] >= 200])
print('DARK rows y<100 with >=200:', [(y, int(rowcnt[y])) for y in range(0, 100) if rowcnt[y] >= 200])
print('DARK rows y>480 with >=200:', [(y, int(rowcnt[y])) for y in range(480, 540) if rowcnt[y] >= 200])
