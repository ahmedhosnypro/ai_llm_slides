# stage 8: Final Result ellipse interior + label word widths
from PIL import Image, ImageFont
import numpy as np
from collections import Counter

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_009.jpg").convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[...,0], a[...,1], a[...,2]

def cls(p):
    R,G,B = p
    if R<120 and G<120 and B<120: return "K"
    if R>230 and G>230 and B>230: return "W"
    if R>170 and G>170 and B<100: return "y"
    return "?"

print("== Final Result ellipse interior map x786..882 y310..350 step1 ==")
print("     " + "".join(str((x//10)%10) for x in range(786,883)))
for y in range(310,351):
    print(f"y{y:3d} " + "".join(cls(a[y,x]) for x in range(786,883)))

# white pixels inside ellipse
whitem = (r>200)&(g>200)&(b>200)
sub = whitem[316:344, 800:866]
print("\nwhite px inside ellipse:", int(sub.sum()))
inkm = (r<120)&(g<120)&(b<120)
sub2 = inkm[316:344, 800:866]
ys,xs = np.nonzero(sub2)
if len(xs): print("dark px inside ellipse: n=%d x %d..%d y %d..%d" % (len(xs), xs.min()+800, xs.max()+800, ys.min()+316, ys.max()+316))
else: print("dark px inside ellipse: 0")
# mid pixel values
print("row y=330 x820..850:", [tuple(a[330,x]) for x in range(820,850,4)])
print("row y=325 x810..860:", [tuple(a[325,x]) for x in range(810,860,6)])

# label words at sizes
FB = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"
for s in (12,13,13.5,14,15):
    f = ImageFont.truetype(FB, int(s) if s==int(s) else 14)  # truetype needs int
for s in (12,13,14,15):
    f = ImageFont.truetype(FB, s)
    words = ["Cleaned","Data","Feature","Vectors","Final","Features","Predicted","Class"]
    print(f"\nlabel words @ {s}pt:", {w: round(f.getlength(w),1) for w in words})
# measured: Cleaned 53 / Data 29 / Feature 49 / Vectors 50 / Final 30 / Features 57 / Predicted 62 / Class 36
