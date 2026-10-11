from PIL import Image
import numpy as np
a = np.asarray(Image.open("unique_slides/slide_043.jpg").convert("RGB"), dtype=np.int16)
b = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("RGB"), dtype=np.int16)
d = np.abs(a-b).max(axis=2); mask = d>30
# vecbox label zone
ys,xs = np.where(mask[45:80, 395:560])
print("vecbox zone delta px:", len(xs), "x", (395+xs.min(), 395+xs.max()) if len(xs) else "", "y", (45+ys.min(), 45+ys.max()) if len(xs) else "")
# column histogram of the vecbox delta
import collections
colc = collections.Counter(395+xs)
print("cols:", sorted(colc.items())[:40])
# visible line2 text end on 44: ink in x600..740
for name in ["slide_043","slide_044"]:
    L = np.asarray(Image.open(f"unique_slides/{name}.jpg").convert("L"))
    m = (L<120)[78:100, 600:745]
    ys2,xs2 = np.where(m)
    print(name, "line2 visible ink x", (600+xs2.min(), 600+xs2.max()) if len(xs2) else "none", "n=",len(xs2))
# where does the inset cover line2? check 43's ink at x735..800 y78..101
L43 = np.asarray(Image.open("unique_slides/slide_043.jpg").convert("L"))
m43 = (L43<120)[78:101, 700:810]
ys3,xs3 = np.where(m43)
print("43 line2 ink x700..810:", (700+xs3.min(), 700+xs3.max()) if len(xs3) else "none", "n=", len(xs3))
# title line1 right end (does inset occlude line1 too? line1 ink to x867, y54..76; inset top at y80 -> NO overlap)
# h=5 badge position on 43: tag x = 563+46*4=747, y=280-20.5*4=198 -> tag (747..777, 198..212.5). Hmm inset is x738..908 y80..298!
# so the h=5 tag at (747,198) is FULLY inside the inset region -> occluded on 44. check.
print("43 h5-tag zone ink check:", L43[198:213, 747:778].min())
print("44 h5-tag zone:", np.asarray(Image.open("unique_slides/slide_044.jpg").convert("L"))[198:213, 747:778].min())
