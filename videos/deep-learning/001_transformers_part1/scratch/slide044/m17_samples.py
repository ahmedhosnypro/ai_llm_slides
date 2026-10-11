from PIL import Image
import numpy as np
im = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("RGB"))
pts = {
 "panel fill (750,110)": (750,110), "panel fill (860,250)": (860,250),
 "top arrow shaft (808,90)": (808,90),
 "topLinear inside (810,106)": (810,106), "topLinear border (794,106)": (794,106),
 "concat fill (808,138)": (808,138), "concat border (786,138)": (786,138),
 "stack behind band (860,162)": (860,162), "stack behind (880,160)": (880,160),
 "stack front fill (800,180)": (800,180), "stack front fill (760,176)": (760,176),
 "stack front border row (800,170)": (800,170),
 "boxA fill (776,222)": (776,222), "boxB fill (822,222)": (822,222), "boxC fill (870,222)": (870,222),
 "boxA border (762,222)": (762,222),
 "arrow shaft (762,260)": (762,260), "arrow shaft (809,260)": (809,260),
 "VKQ label V (762,284)": (762,284), "VKQ label K (809,284)": (809,284),
 "badge ring (876,71)": (876,71), "badge fill (893,65)": (893,65),
 "green border (739,150)": (739,150), "green border top (800,81)": (800,81),
}
for k,(x,y) in pts.items():
    print(f"{k}: {tuple(int(v) for v in im[y,x])}")
