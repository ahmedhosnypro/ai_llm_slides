from PIL import Image
import numpy as np
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
a = np.asarray(img).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
white=(r>235)&(g>235)&(b>225)
blue=(b>110)&((b-r)>25)
# output stack col1: white box x-extent at box2 mid-height y=405
for y in [380, 405, 436, 468]:
    xs=np.where(white[y,235:320])[0]+235
    print(f"col1 output white row y={y}: {xs.min()}..{xs.max()}" if len(xs) else f"y={y} none")
# blue vertical strokes col1 x 240..320
lab_yes = blue[355:495, 235:325]
cols = lab_yes.sum(axis=0)
print("col1 blue per-x counts (x=235+i):", {235+i:int(c) for i,c in enumerate(cols) if c>30})
# same col2, col3
for x0,x1,lab in [(505,595,"col2"),(775,860,"col3")]:
    lab_yes = blue[355:495, x0:x1]
    cols = lab_yes.sum(axis=0)
    print(f"{lab} blue per-x counts:", {x0+i:int(c) for i,c in enumerate(cols) if c>30})
# input stacks: red verticals per-x
red=(r>140)&((r-g)>60)&((r-b)>60)
for x0,x1,lab in [(120,185,"col1"),(390,455,"col2"),(655,720,"col3")]:
    cols = red[350:495, x0:x1].sum(axis=0)
    print(f"{lab} red per-x:", {x0+i:int(c) for i,c in enumerate(cols) if c>30})
