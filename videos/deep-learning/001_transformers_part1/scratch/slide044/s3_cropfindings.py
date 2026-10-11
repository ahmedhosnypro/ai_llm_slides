from PIL import Image
import numpy as np
L = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("L")).astype(int)
print("=== F2: concat-feeding arrows, y144..172, x780..850 (thr<150) ===")
for y in range(144,173):
    row = L[y,780:850]<150
    runs=[];s=None
    for i,v in enumerate(row):
        if v and s is None: s=i
        if not v and s is not None: runs.append((780+s,780+i-1)); s=None
    if s is not None: runs.append((780+s,849))
    print(y, runs)
print("=== F3: stack left corners, x742..775, y152..176 (chars: #<110, +<150, .<200) ===")
for y in range(152,177):
    print(y, "".join("#" if L[y,x]<110 else ("+" if L[y,x]<150 else ("." if L[y,x]<200 else " ")) for x in range(742,776)))
print("=== F1: behind-box right sliver extent, box A x783..793, y203..245 ===")
for y in range(203,246):
    print(y, "".join("#" if L[y,x]<110 else ("+" if L[y,x]<150 else ("." if L[y,x]<200 else " ")) for x in range(783,794)))
