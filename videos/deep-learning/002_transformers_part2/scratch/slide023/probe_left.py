from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
# columns 120..160: what's there across y 350..505?
red  = (r-g>45)&(r-b>45)
blue = (b-r>45)&(b-g>25)
dark = (0.299*r+0.587*g+0.114*b) < 150
for x in range(120, 165):
    rr = red[350:506, x].sum(); bb = blue[350:506, x].sum(); dd = dark[350:506, x].sum()
    if rr+bb+dd > 5: print(f"x{x}: red {rr} blue {bb} dark {dd}")
print()
# sample the two vertical strokes' colors
print("x132 colors y370..500:", [tuple(im[y,132]) for y in range(370,500,25)])
print("x146 colors y370..500:", [tuple(im[y,146]) for y in range(370,500,25)])
print("x133:", [tuple(im[y,133]) for y in range(370,500,25)])
print("x147:", [tuple(im[y,147]) for y in range(370,500,25)])
# bullet dots: look at rows 413..430, x 120..170
print()
print("bullet zone rows 410..432, x 120..175 nonbg:")
for y in range(410, 433, 2):
    row=[]
    for x in range(120,176):
        R,G,B = r[y,x],g[y,x],b[y,x]
        if R>120 and R-G>40: row.append((x,'R'))
        elif B-R>40: row.append((x,'B'))
    if row: print(y, row[:20])
