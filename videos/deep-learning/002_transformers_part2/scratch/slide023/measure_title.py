from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
ink = (abs(r-233) + abs(g-233) + abs(b-231)) > 60
ink[:, :61] = False; ink[:, 900:] = False

def band(y0, y1, x0=61, x1=900, label=""):
    sub = ink[y0:y1+1, x0:x1]
    rows = np.where(sub.any(axis=1))[0]; cols = np.where(sub.any(axis=0))[0]
    if len(rows)==0: print(label, "EMPTY"); return
    print(f"{label}: y {y0+rows.min()}..{y0+rows.max()} (h {rows.max()-rows.min()+1})  x {x0+cols.min()}..{x0+cols.max()} (w {cols.max()-cols.min()+1}) cx {(x0+cols.min()+x0+cols.max())/2}")
    # row profile to split lines
    prof = sub.sum(axis=1)
    gaps = [y0+i for i,v in enumerate(prof) if v==0]
    print("   empty rows:", gaps[:50])

band(47, 80, label="title")
band(80, 112, label="subtitle")
# title only red
red = (r - g > 60) & (r - b > 60)
sub = red[40:80, 200:800]
rows = np.where(sub.any(axis=1))[0]; cols = np.where(sub.any(axis=0))[0]
print("title red ink: y", 40+rows.min(), "..", 40+rows.max(), " x", 200+cols.min(), "..", 200+cols.max())
# subtitle blue
blue = (b - r > 60) & (b - g > 40)
sub = blue[78:115, 200:800]
rows = np.where(sub.any(axis=1))[0]; cols = np.where(sub.any(axis=0))[0]
print("subtitle blue ink: y", 78+rows.min(), "..", 78+rows.max(), " x", 200+cols.min(), "..", 200+cols.max())
