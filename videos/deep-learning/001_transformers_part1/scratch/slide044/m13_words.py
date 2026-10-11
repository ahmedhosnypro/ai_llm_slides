from PIL import Image
import numpy as np
def words(name, y0,y1, x0=505, x1=880):
    L = np.asarray(Image.open(f"unique_slides/{name}.jpg").convert("L"))
    colc = (L[y0:y1, x0:x1] < 120).sum(axis=0)
    runs=[]; s=None
    for i,v in enumerate(colc>0):
        if v and s is None: s=i
        if not v and s is not None:
            if i-s>=2: runs.append((x0+s, x0+i-1, i-s))
            s=None
    if s is not None: runs.append((x0+s, x0+len(colc)-1, len(colc)-s))
    # merge runs separated by <4px (letter gaps)
    merged=[runs[0]]
    for r in runs[1:]:
        if r[0]-merged[-1][1] <= 4:
            merged[-1]=(merged[-1][0], r[1], r[1]-merged[-1][0])
        else: merged.append(r)
    return merged
w43 = words("slide_043", 52,78)
w44 = words("slide_044", 52,78)
print("43 line1 words:", w43)
print("44 line1 words:", w44)
print()
w43b = words("slide_043", 80,100, 600, 740)
w44b = words("slide_044", 80,100, 600, 740)
print("43 line2 words (x600-740):", w43b)
print("44 line2 words (x600-740):", w44b)
