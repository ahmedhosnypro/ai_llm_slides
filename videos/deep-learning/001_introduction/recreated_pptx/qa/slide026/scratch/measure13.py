from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)

# panel edges via long gray runs per row
def gray_runs(y):
    row = a[y]
    g = (np.abs(row[:,0]-233)<14)&(np.abs(row[:,1]-233)<14)&(np.abs(row[:,2]-231)<16)
    idx = np.where(g)[0]
    out=[]
    if len(idx):
        s=p=idx[0]
        for i in idx[1:]:
            if i>p+2: out.append((int(s),int(p))); s=i
            p=i
        out.append((int(s),int(p)))
    return [r for r in out if r[1]-r[0]>50]

for y in (60, 150, 300, 450, 515):
    print('y',y,'gray runs:', gray_runs(y))
# unquantized modals
def modal_exact(region,label):
    px = region.reshape(-1,3)
    q = Counter(map(tuple,px))
    print(label, q.most_common(3))
modal_exact(a[340:360, 640:750],'yellow-fill')
modal_exact(a[470:495, 700:830],'tan2-fill')
modal_exact(a[130:150, 500:640],'tan1-fill')
modal_exact(a[45:49, 200:800],'top-red-border-row')
