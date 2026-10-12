from PIL import Image
import numpy as np
R = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide038/render_1.png').convert('RGB')).astype(int)
S = R.shape[1]/960.0
r, g, b = R[...,0], R[...,1], R[...,2]
# what is at frame (383..392, 395..408) that matched 'circ'?
for y in range(395, 409):
    row = []
    for x in range(380, 396):
        row.append(tuple(R[int(y*S), int(x*S)]))
    print(y, row[::3])
print("--- dash rows in x 376..390 (isolated from X) ---")
ink = (r<175)&(g<175)&(b<175)
for y in range(345, 395):
    m = ink[int(y*S):int((y+1)*S), int(376*S):int(390*S)]
    if m.sum()>2: print(" dash ink at frame y", y, m.sum())
print("--- stack png first-slab left edge: colored cols at y=370 ---")
cy = int(370*S)
for x in range(386, 400):
    print(x, tuple(R[cy, int(x*S)]))
print("--- title ink rows (render) ---")
red = ((r-g)>40)&((r-b)>40)&(r>110)
ys = np.nonzero(red[:, int(340*S):int(620*S)].sum(axis=1)>3)[0]
print("title ink render y", ys.min(), "..", ys.max(), "-> frame", ys.min()/S, ys.max()/S)
