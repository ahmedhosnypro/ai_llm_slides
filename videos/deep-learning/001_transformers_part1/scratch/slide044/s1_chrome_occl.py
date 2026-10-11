from PIL import Image
import numpy as np
def badge_yellow_extent(path, scale_to_frame):
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    r,g,b = im[...,0], im[...,1], im[...,2]
    yel = (r>200)&(g>200)&(b<190)
    cx, cy, d = 893*scale_to_frame, 71*scale_to_frame, 36*scale_to_frame
    y0 = int(cy-d)
    win = yel[y0:int(cy+d), int(cx-d):int(cx+d)]
    ys,xs = np.where(win)
    return ((y0+ys.min())/scale_to_frame, (y0+ys.max())/scale_to_frame, int(len(ys)))
print("orig 44 yellow y-extent (frame px):", badge_yellow_extent("unique_slides/slide_044.jpg", 1.0))
print("orig 43 yellow y-extent (frame px):", badge_yellow_extent("unique_slides/slide_043.jpg", 1.0))
print("render1 yellow y-extent (frame px):", badge_yellow_extent("recreated_pptx/qa/slide044/render_1.png", 1125/540.0))
