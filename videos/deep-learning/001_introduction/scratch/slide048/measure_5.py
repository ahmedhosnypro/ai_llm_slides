from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')
W,H = im.size
a = np.asarray(im).astype(int)
R,G,B = a[...,0],a[...,1],a[...,2]
red = (R>120)&(R<235)&(G<80)&(B<80)
reddish = (R>140)&((R-G)>50)&((R-B)>50)

for y in [44,45,46,100,130,134,135,136,140,300,440,447,448,449,460,470,500,510,511,512,513,514,515,516]:
    xs = np.nonzero(red[y,:])[0]
    xs2 = np.nonzero(reddish[y,:])[0]
    s_red = str(xs.min())+'..'+str(xs.max())+f' n={len(xs)}' if len(xs) else '-'
    s_rd = str(xs2.min())+'..'+str(xs2.max())+f' n={len(xs2)}' if len(xs2) else '-'
    # list red x-clusters
    def clus(xs):
        out=[]; s=None; p=None
        for x in xs:
            if s is None: s=x
            elif x>p+3: out.append((s,p)); s=x
            p=x
        if s is not None: out.append((s,p))
        return out
    print(f'y={y:3d} red[{s_red}] clus={clus(xs)[:8]} reddish[{s_rd}]')
