from PIL import Image
import numpy as np
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
W,H = img.size
print("size", W, H)
a = np.asarray(img).astype(int)

def colorat(x,y):
    print(f"  ({x},{y}) = {tuple(a[y,x])}")

# Sample chrome
print("canvas corner (10,10):", tuple(a[10,10]))
print("panel (60,300):", tuple(a[300,60]))
# scan for red border on left edge
for x in range(35,60):
    r,g,b = a[300,x]
    if r>150 and g<80 and b<80:
        print("red border left col at x=",x, (r,g,b)); break
# badge: find yellow circle region top-right
sub = a[40:110, 850:940]
ys,xs = np.where((sub[:,:,0]>200)&(sub[:,:,1]>200)&(sub[:,:,2]<160))
if len(xs): print("badge yellow bbox in full coords: x",xs.min()+850,"..",xs.max()+850," y",ys.min()+40,"..",ys.max()+40)
# title ink: find dark pixels in y 40..90
band = a[40:95, 100:860]
ys,xs = np.where(band.sum(axis=2) < 200)
if len(xs): print("title ink bbox: x",xs.min()+100,"..",xs.max()+100," y",ys.min()+40,"..",ys.max()+40)
