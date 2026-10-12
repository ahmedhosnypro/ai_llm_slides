from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg').convert('RGB')).astype(int)

def slice_run(y, x0=66, x1=892):
    row = im[y, x0:x1]
    # classify each px into: W(white/near), K(dark<100), R(red-ish), B(blue-ish), Y(yellow-ish cream), C(cyan-ish), G(gray)
    out = []
    for c in row:
        r,g,b = c
        if r<110 and g<110 and b<160: ch='K'
        elif r-g>40 and r-b>40: ch='R'
        elif b-r>40 and b-g>20: ch='B'
        elif r>235 and g>225 and b<215: ch='Y'
        elif r>215 and g>235 and b>235 and g-r>6: ch='C'
        elif abs(r-g)<18 and abs(g-b)<18: ch = 'W' if r>238 else ('g' if r>170 else 'G')
        else: ch='?'
        out.append(ch)
    # compress
    comp, s = [], 0
    for i in range(1, len(out)+1):
        if i==len(out) or out[i]!=out[s]:
            if i-s >= 2: comp.append(f"{out[s]}[{s+x0}-{i-1+x0}]")
            s = i
    return " ".join(comp)

for y, lbl in [(138,"ROW1 y138"), (205,"ROW2 y205"), (283,"ROW3 y283"), (297,"ROW3 y297 (+delta?)"), (305,"ROW3 y305"), (440,"PANEL y440")]:
    print(f"== {lbl} ==")
    print(slice_run(y))
    print()
