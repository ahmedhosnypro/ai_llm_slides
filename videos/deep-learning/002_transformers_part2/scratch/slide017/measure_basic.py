from PIL import Image
import numpy as np

# My original frame
im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
print("frame size:", im.size)
a = np.asarray(im).astype(int)

# Parent frame (001 slide 043) for reference
im2 = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg").convert("RGB")
print("parent frame size:", im2.size)
b = np.asarray(im2).astype(int)

def col_runs(arr, x, label):
    col = arr[:, x]
    # find dark red border rows (C00000-ish): r>120, g<80, b<80
    red = (col[:,0]>120)&(col[:,1]<90)&(col[:,2]<90)
    runs=[]
    y=0
    H=arr.shape[0]
    while y<H:
        if red[y]:
            y0=y
            while y<H and red[y]: y+=1
            runs.append((y0,y-1))
        else: y+=1
    print(label, "red runs at x=%d:"%x, runs[:12])

def row_runs(arr, y, label):
    row = arr[y]
    red = (row[:,0]>120)&(row[:,1]<90)&(row[:,2]<90)
    runs=[]; x=0; W=arr.shape[1]
    while x<W:
        if red[x]:
            x0=x
            while x<W and red[x]: x+=1
            runs.append((x0,x-1))
        else: x+=1
    print(label, "red runs at y=%d:"%y, runs[:12])

for im_, arr, name in ((im,a,"FRAME"),(im2,b,"PARENT")):
    print("===",name,"===")
    H,W = arr.shape[:2]
    col_runs(arr, W//2, "midcol")
    col_runs(arr, 30, "x30")
    col_runs(arr, W-30, "xlast30")
    row_runs(arr, H//2, "midrow")
