from PIL import Image
import numpy as np
from collections import Counter
O = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')).astype(int)
R = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide038/render_3.png').convert('RGB')).astype(int)
S = R.shape[1]/960.0
def modal(A, y0,y1,x0,x1, scale=1.0):
    yy0,yy1,xx0,xx1 = [int(v*scale) for v in (y0,y1,x0,x1)]
    c = Counter(tuple(A[y,x]) for y in range(yy0,yy1) for x in range(xx0,xx1))
    return c.most_common(2)
pts = {
 "title red":      (70, 95, 340, 360),
 "fbox border":    (117, 120, 300, 500),
 "dbox border":    (250, 253, 300, 500),
 "line2 red":      (176, 190, 120, 210),
 "line2 blue":     (176, 190, 400, 460),
 "line3 red":      (211, 222, 119, 149),
 "cyan face":      (365, 390, 396, 417),
 "purple face":    (365, 390, 512, 546),
 "brown face":     (355, 395, 270, 330),
 "circle cyan":    (364, 375, 618, 633),
 "circle ring":    (355, 362, 612, 640),
}
for nm, (y0,y1,x0,x1) in pts.items():
    print(f"{nm:14s} orig {modal(O,y0,y1,x0,x1)}")
    print(f"{'':14s} rend {modal(R,y0,y1,x0,x1,S)}")
