from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg').convert('RGB')).astype(int)
def amap(y0, y1, x0, x1):
    print(f"== y[{y0},{y1}] x[{x0},{x1}] ==")
    print("    " + "".join(str((x//10)%10) for x in range(x0, x1)))
    for y in range(y0, y1):
        line = []
        for x in range(x0, x1):
            r,g,b = im[y,x]
            if r<100 and g<100: ch='K'
            elif r-b>60 and r-g>60: ch='O' if (g>110 and b<110) else 'R'
            elif r-g>40 and r-b>40: ch='r'
            elif b-r>50 and b-g>25: ch='B'
            elif r>235 and g>225 and b<212: ch='Y'
            elif abs(r-g)<20 and abs(g-b)<20: ch = '.' if r>238 else ('-' if r>150 else '#')
            else: ch='?'
            line.append(ch)
        print(f"{y:3d} " + "".join(line))
amap(286, 308, 262, 300)   # first +delta glyph region
print()
amap(286, 308, 826, 852)   # last +delta glyph region
# glyph core colors
print("glyph colors:", im[298,276].tolist(), im[299,352].tolist(), im[299,424].tolist(), im[298,838].tolist())
print("box1 digit color:", im[282,207].tolist(), im[280,208].tolist())
print("row1 label text px:", im[130,100].tolist(), im[136,90].tolist())
print("row2 label text px:", im[196,90].tolist(), im[200,100].tolist())
print("row3 label text px:", im[270,90].tolist(), im[276,85].tolist())
