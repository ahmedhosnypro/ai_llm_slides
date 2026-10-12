from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_059.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def mask(lo, hi):
    return ((r>=lo[0])&(g>=lo[1])&(b>=lo[2])&(r<=hi[0])&(g<=hi[1])&(b<=hi[2]))

def bbox(m, label):
    ys, xs = np.where(m)
    if len(xs)==0: print(label, "EMPTY"); return None
    print(f"{label}: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  (n={len(xs)})")
    return (xs.min(), xs.max(), ys.min(), ys.max())

# tan softmax bar ~ F5CBA7 (245,203,167)
bbox(mask((235,185,150),(252,215,185)), "tan bar")
# rose container ~ CD5C5C (205,92,92)
bbox(mask((185,75,75),(225,115,115)), "rose container")
# dark red bars ~ B22222 (178,34,34) - deep red, g<70
bbox(mask((150,15,20),(200,75,75)), "dark-red bars region")
# navy circles ~ 1A237E (26,35,126)
bbox(mask((10,20,100),(70,70,160)), "navy")
# pink container ~ FADBD8
bbox(mask((242,205,200),(255,232,228)), "pink container")
# light blue D6EAF8
bbox(mask((200,222,240),(235,245,255)), "light blue (output row)")
# peach FDEBD0
bbox(mask((245,222,195),(255,242,220)), "peach (position row)")
