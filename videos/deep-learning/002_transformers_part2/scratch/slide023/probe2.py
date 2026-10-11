from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
blue = (b-r>45)&(b-g>25)
red  = (r-g>45)&(r-b>45)
mag  = (r-g>60)&(b-g>60)
luma = (0.299*r+0.587*g+0.114*b)

print("bullet1 rows 410..430, blue cols 90..135 per row:")
for y in range(410,431):
    cs = [x for x in range(90,136) if blue[y,x]]
    if cs: print(f"  y{y}: {cs}")
print()
print("rows 388..410 (Problems band), ink cols x75..250:")
for y in range(386,412):
    cs = [x for x in range(75,260) if luma[y,x]<195]
    if cs: print(f"  y{y}: {cs[0]}..{cs[-1]} n={len(cs)}")
print()
print("Problems colors: red cols:", [x for x in range(75,260) if red[391:404,x].any()], )
print("blue cols:", [x for x in range(75,260) if blue[391:404,x].any()])
print()
print("lead line rows 366..388, underline check: per-row long runs (luma<195):")
for y in range(378,389):
    row = luma[y,75:885]<195
    runs=[]; inr=False
    for i,v in enumerate(row):
        if v and not inr: s=i; inr=True
        elif not v and inr:
            if i-s>=15: runs.append((75+s,75+i-1))
            inr=False
    if inr and len(row)-s>=15: runs.append((75+s,884))
    if runs: print(f"  y{y}: {runs}")
