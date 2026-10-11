from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

# highlight box fill color sample
print("fill sample (400,460):", tuple(im[460,400]), tuple(im[420,200]), tuple(im[490,700]))
# border: strong blue rows
bl = (b-r>55)&(b>110)
rp = bl[340:515, 100:850].sum(axis=1)
print("strong-blue rows 340..514 (x100..850):", [(340+i,int(v)) for i,v in enumerate(rp) if v>=100])
# box bbox via fill color D6EAF8 ~ (214,234,248)
fill = (abs(r-214)<25)&(abs(g-234)<20)&(abs(b-248)<15)
rp = fill[340:515, :].sum(axis=1)
rows = [340+i for i,v in enumerate(rp) if v>=300]
print("fill rows:", rows[0], "..", rows[-1])
cp = fill[rows[0]:rows[-1], :].sum(axis=0)
cols = [x for x in range(960) if cp[x]>=100]
print("fill cols:", cols[0], "..", cols[-1])
# text lines inside: dark ink on light blue
luma = (0.299*r + 0.587*g + 0.114*b)
ink = luma < 190
sub = ink[350:505, 80:890]
rp = sub.sum(axis=1)
prev = False
for i,v in enumerate(rp):
    y = 350+i
    if v>=3 and not prev: start=y
    if v<3 and prev: print(f"  text line y {start}..{y-1}")
    prev = v>=3
if prev: print(f"  text line y {start}..{504}")
