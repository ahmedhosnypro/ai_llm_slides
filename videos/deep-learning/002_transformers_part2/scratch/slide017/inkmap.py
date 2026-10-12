from PIL import Image
import numpy as np

F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
a = np.asarray(F).astype(int)
H, W = a.shape[:2]

# "content" = pixel that is NOT salmon card, NOT panel gray, NOT white-ish, NOT black pill/text? (keep dark as content)
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]
salmon = (np.abs(r-240)<26)&(np.abs(g-136)<30)&(np.abs(b-144)<30)
grayish = (np.abs(r-g)<12)&(np.abs(g-b)<14)&(r>200)   # white/panel/light gray
dark = (r<110)&(g<110)&(b<110)                         # dark ink/text (content!)
content = (~salmon) & (~grayish) | dark

# restrict to front card zone: x 60..620, y 260..510 (frame px)
zone = np.zeros_like(content); zone[260:512, 60:625] = True
cm = content & zone

colprof = cm.sum(axis=0)
print("column ink profile (x: count), bucketed x/6:")
for x0 in range(60, 624, 6):
    v = colprof[x0:x0+6].sum()
    bar = "#" * int(v/12)
    print("%3d %4d %s" % (x0, v, bar))
