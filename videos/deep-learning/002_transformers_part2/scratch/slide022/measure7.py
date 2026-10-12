from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg').convert('RGB')).astype(int)

# color grid sample: y in steps, x in steps -> dominant hue class
def classify(c):
    r,g,b = c
    if abs(r-g)<18 and abs(g-b)<18 and abs(r-b)<18:
        if r>235: return '.'   # white
        if r>200: return ','   # light gray
        if r>120: return '-'   # mid gray
        return '#'             # dark
    if r>g and r>b:
        if r>200 and g>170: return 'y'  # yellow/cream
        if r>150 and g<120: return 'R'  # red
        return 'r'
    if b>r and b>=g:
        if r>150 and g>170: return 'b'  # light blue
        if b>130: return 'B'  # blue
        return 'n'  # navy
    if g>=r and g>=b: return 'g'
    return '?'

print("   " + "".join(str((x//100)%10) for x in range(45, 915, 10)))
for y in range(52, 518, 4):
    row = []
    for x in range(45, 915, 10):
        c = im[y-1:y+2, x-2:x+3].reshape(-1,3).mean(axis=0).astype(int)
        row.append(classify(c))
    print(f"{y:3d}" + "".join(row))
