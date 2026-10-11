from PIL import Image
import numpy as np
A = np.asarray(Image.open("unique_slides/slide_043.jpg").convert("L"))
B = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("L"))
def iou_at(y0,y1,x0,x1,dx,dy=0):
    a = (A[y0:y1, x0:x1] < 120)
    b = (B[y0+dy:y1+dy, x0+dx:x1+dx] < 120)
    return (a&b).sum()/max(1,(a|b).sum())
print("line1 IoU at dx -9:", iou_at(52,78,515,865,-9))
print("line1 IoU at dx 0:", iou_at(52,78,515,865,0))
for dx in (-4,-5,-6,-7,-8,-9,-10):
    print(f"line2 IoU dx={dx}:", round(iou_at(80,100,600,736,dx),3))
# vertical: row profiles of line1 on both (x515..865)
for name,L in [("43",A),("44",B)]:
    rows=(L[48:104, 515:865]<120).sum(axis=1)
    nz=[(48+i,int(v)) for i,v in enumerate(rows) if v>3]
    print(name, "line rows:", nz[:6], "...", nz[-6:])
