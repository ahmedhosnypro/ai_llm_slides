from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
# looser red text mask
red = (r - g > 35) & (r - b > 35) & (r > 120)
# title rows: profile
sub = red[55:84, 61:900]
prof = sub.sum(axis=1)
print("title row profile 55..83:", {55+i: int(v) for i, v in enumerate(prof) if v>0})
cols = np.where(sub.any(axis=0))[0]
print("title x extent (loose):", 61+cols.min(), "..", 61+cols.max())
# column profile endpoints
cp = sub.sum(axis=0)
nz = [61+i for i,v in enumerate(cp) if v>0]
print("first 12 ink cols:", nz[:12], " last 12:", nz[-12:])

blue = (b - r > 35) & (b - g > 25) & (b > 120)
sub2 = blue[82:112, 61:900]
rows2 = np.where(sub2.any(axis=1))[0]
cp2 = sub2.sum(axis=0)
nz2 = [61+i for i,v in enumerate(cp2) if v>0]
print("subtitle rows:", 82+rows2.min(), "..", 82+rows2.max(), " x:", nz2[0], "..", nz2[-1])
