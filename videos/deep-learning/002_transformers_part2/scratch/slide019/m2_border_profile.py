# m2: profile colors across expected border positions
from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_019.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def hprofile(y, x0, x1, label):
    row = a[y, x0:x1]
    s = ' '.join(f"{x}:{r},{g},{b}" for (x,(r,g,b)) in zip(range(x0,x1), row))
    print(f'H y={y} {label}: {s}')

def vprofile(x, y0, y1, label):
    col = a[y0:y1, x]
    s = ' '.join(f"{y}:{r},{g},{b}" for (y,(r,g,b)) in zip(range(y0,y1), col))
    print(f'V x={x} {label}: {s}')

hprofile(300, 52, 70, 'left border zone')      # expect panel-left red line ~x59
hprofile(300, 893, 912, 'right border zone')   # expect ~x902
vprofile(480, 35, 52, 'top border zone')       # expect ~y43
vprofile(480, 508, 525, 'bottom/letterbox zone') # expect ~y516 border, then black
