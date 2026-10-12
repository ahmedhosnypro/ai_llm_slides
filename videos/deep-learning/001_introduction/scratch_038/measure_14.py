from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[...,0], a[...,1], a[...,2]
black = (r<110)&(g<110)&(b<110)

def show(y0,y1,x0,x1,cell=2,label=""):
    print(f"--- {label} y{y0}..{y1} x{x0}..{x1} cell={cell} ---")
    print("     " + "".join(str((x//10)%10) for x in range(x0, x1, cell)))
    for y in range(y0, y1, cell):
        row=""
        for x in range(x0, x1, cell):
            row += "#" if black[y:y+cell, x:x+cell].sum()>0 else "."
        print(f"{y:4d} {row}")

show(340, 404, 384, 560, 3, "slab region black-only (7s + outlines)")
show(320, 430, 548, 625, 3, "right-side 7 (ink<175 use black first)")
# right-side with lighter threshold
ink = (r<185)&(g<185)&(b<185)
print("--- right-side 7 ink<175: x548..625, y325..425 ---")
print("     " + "".join(str((x//10)%10) for x in range(548, 625, 3)))
for y in range(325, 425, 3):
    row=""
    for x in range(548, 625, 3):
        row += "#" if ink[y:y+3, x:x+3].sum()>0 else "."
    print(f"{y:4d} {row}")
print("--- 735 weights bbox ---")
ys, xs = np.nonzero(ink[465:505, 375:565])
print(f"x {375+xs.min()}..{375+xs.max()} y {465+ys.min()}..{465+ys.max()}")

def modal_masked(y0,y1,x0,x1,name,keep):
    c = Counter()
    for y in range(y0,y1):
        for x in range(x0,x1):
            px = tuple(a[y,x]); rr,gg,bb = px
            if keep(rr,gg,bb): c[px]+=1
    print(f"modal {name}: {c.most_common(3)}")
modal_masked(139, 158, 103, 774, "line1 text", lambda rr,gg,bb: rr<120 and gg<120 and bb<120)
modal_masked(174, 192, 119, 300, "line2 red term", lambda rr,gg,bb: (rr-gg)>50 and (rr-bb)>50)
modal_masked(174, 192, 380, 470, "line2 blue term", lambda rr,gg,bb: (bb-rr)>60)
modal_masked(174, 192, 500, 758, "line2 green term", lambda rr,gg,bb: (gg-rr)>40 and (gg-bb)>40)
modal_masked(66, 102, 335, 632, "title red", lambda rr,gg,bb: (rr-gg)>60)
modal_masked(571, 593, 571, 592, "eq bars", lambda rr,gg,bb: (bb-rr)>60)
# arrows fan region
show(400, 472, 388, 560, 4, "arrows fan (black)")
