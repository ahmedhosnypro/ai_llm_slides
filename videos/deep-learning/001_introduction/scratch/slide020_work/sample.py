from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_020.jpg').convert('RGB')
a = np.asarray(im)
def med(x0,y0,x1,y1,label):
    r = a[y0:y1, x0:x1].reshape(-1,3)
    m = np.median(r, axis=0).astype(int)
    print(f"{label:34s} ({x0},{y0})-({x1},{y1}) median={tuple(m)} #{m[0]:02X}{m[1]:02X}{m[2]:02X}")
med(20,20,40,40,"outer background")
med(300,120,340,140,"ellipse fill (center)")
med(100,220,140,240,"Input Samples box fill")
med(220,220,260,230,"Pre processing fill")
med(320,220,360,230,"Feature Extraction fill?")
med(420,220,460,230,"Feature Selection fill?")
med(560,230,600,250,"Classification fill (darkred)")
med(660,220,700,240,"Predicted Labels fill?")
med(760,200,785,240,"Prediction Error box fill")
med(850,220,890,240,"Samples Labels fill?")
med(600,180,620,190,"white inner region 586-763x237-318?")
med(300,80,600,95,"title band")
med(480,490,520,510,"below canvas / above black strip")
med(300,390,600,430,"green annotation box area")
med(760,400,820,410,"starburst area")
# column profile of red border row
row = a[210,:,:]
print("row210 non-gray transitions:")
prev=None
for x in range(0,960):
    r,g,b = row[x]
    is_red = r>130 and g<90 and b<90
    if is_red and prev!=True:
        print("  red start x=",x, tuple(row[x]))
    if not is_red and prev==True:
        print("  red end   x=",x)
    prev=is_red
