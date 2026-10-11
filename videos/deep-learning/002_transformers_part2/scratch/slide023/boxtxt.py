from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
luma = (0.299*r+0.587*g+0.114*b)

def txtw(y0,y1,x0,x1,label,thr=195):
    m = luma[y0:y1+1, x0:x1+1] < thr
    cols = np.where(m.any(axis=0))[0]; rows = np.where(m.any(axis=1))[0]
    if len(cols)==0: print(label,"none"); return
    print(f"{label}: x {x0+cols.min()}..{x0+cols.max()} (w {cols.max()-cols.min()+1})  y {y0+rows.min()}..{y0+rows.max()} (h {rows.max()-rows.min()+1})")

txtw(130,144,180,228,"R1 box1 'Word 0'")
txtw(130,144,253,300,"R1 box2 'Word 1'")
txtw(130,144,735,786,"R1 box7 'Word N-2'")
txtw(130,144,810,862,"R1 box8 'Word N-1'")
txtw(198,214,175,222,"R2 box1 'Pos 0'")
txtw(198,214,740,782,"R2 box7 'Pos N-2'")
txtw(276,291,180,222,"R3 box1 '0'")
txtw(276,291,254,296,"R3 box2 'd'")
txtw(276,291,328,370,"R3 box3 '2d'")
txtw(276,291,740,782,"R3 box7 '1-d'")
txtw(276,291,812,858,"R3 box8 '1'")
