from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[...,0], a[...,1], a[...,2]
black = (r<110)&(g<110)&(b<110)

def show(y0,y1,x0,x1,cell=2,label=""):
    print(f"--- {label} y{y0}..{y1} x{x0}..{x1} cell={cell} ---")
    print("     " + "".join(str(((x0+c*cell)//10)%10) for c in range((x1-x0)//cell)))
    for y in range(y0, y1, cell):
        row=""
        for x in range(x0, x1, cell):
            row += "#" if black[y:y+cell, x:x+cell].sum()>0 else "."
        print(f"{y:4d} {row}")

show(326, 352, 396, 440, 2, "above-stack 7")
show(548, 620, 0, 0, 2, "") if False else None
# right-side 7: x 550..618, y 320..420
print("--- right-side 7 (x550..618, y320..420) ---")
print("     " + "".join(str((x//10)%10) for x in range(550, 618, 2)))
for y in range(320, 420, 2):
    row=""
    for x in range(550, 618, 2):
        row += "#" if black[y:y+2, x:x+2].sum()>0 else "."
    print(f"{y:4d} {row}")
print("--- 3 + pencil (x382..440, y392..452) ---")
print("     " + "".join(str((x//10)%10) for x in range(382, 440, 2)))
for y in range(392, 452, 2):
    row=""
    for x in range(382, 440, 2):
        row += "#" if black[y:y+2, x:x+2].sum()>0 else "."
    print(f"{y:4d} {row}")

# modal colors
def modal(y0,y1,x0,x1,name):
    c = Counter(tuple(a[y,x]) for y in range(y0,y1) for x in range(x0,x1))
    print(f"modal {name}: {c.most_common(3)}")
modal(116, 120, 300, 500, "fbox border top")
modal(66, 102, 340, 630, "title red")
modal(210, 224, 116, 150, "line3 red 7*7")
modal(210, 224, 172, 190, "line3 blue 3")
modal(210, 224, 212, 226, "line3 green 5")
modal(139, 158, 300, 700, "line1 black")
modal(292, 440, 262, 336, "brown slab face")
modal(358, 396, 394, 419, "cyan face")
modal(358, 396, 512, 548, "purple face")
modal(361, 377, 617, 634, "circle cyan")
modal(358, 382, 608, 642, "ring+tan region")
modal(571, 593, 572, 592, "eq blue")
