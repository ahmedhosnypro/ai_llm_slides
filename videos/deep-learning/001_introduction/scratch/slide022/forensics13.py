from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_022.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

cyan = (g>200)&(b>200)&(r<210)&(g-r>25)
ys, xs = np.nonzero(cyan[380:470, 380:500])
print("cyan circle bbox:", (380+xs.min(), 380+ys.min(), 380+xs.max(), 380+ys.max()), "n=", len(xs))

# fine map of the flow zone x385..620 y400..445, cell 2: C=cyan R=red D=dark .=bg
print("   flow zone (C=cyan fill, R=red, D=dark):")
hdr = "     " + "".join(str(((385+i*2)//10)%10) for i in range((620-385)//2))
print(hdr)
for y in range(400, 446, 2):
    row = ""
    for x in range(385, 620, 2):
        cc = cyan[y:y+2, x:x+2].sum()
        px = a[y, x]
        isR = px[0]>130 and px[0]-px[1]>50 and px[0]-px[2]>40
        isD = px.sum() < 420
        n=4
        if cc >= 2: row += "C"
        elif isR: row += "R"
        elif isD: row += "D"
        else: row += "."
    print(f"{y:4d} " + row)
