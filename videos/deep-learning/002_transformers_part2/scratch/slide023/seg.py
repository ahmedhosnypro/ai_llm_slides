from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
X0, X1 = 62, 899

def bbox(mask, y0, y1, label):
    m = mask[y0:y1+1, :].copy()
    m[:, :X0]=False; m[:, X1:]=False
    rows = np.where(m.any(axis=1))[0]; cols = np.where(m.any(axis=0))[0]
    if len(rows)==0: print(f"  {label}: EMPTY"); return None
    print(f"  {label}: y {y0+rows.min()}..{y0+rows.max()}  x {cols.min()}..{cols.max()}  (w {cols.max()-cols.min()+1}, h {rows.max()-rows.min()+1})")
    return (y0+rows.min(), y0+rows.max(), cols.min(), cols.max())

# color masks
lav   = (abs(r-204)<28)&(abs(g-204)<28)&(b>235)&(b-r>25)
pink  = (r>235)&(abs(g-224)<20)&(abs(b-224)<20)&(r-g>18)&(r-b>18)
black = (r<110)&(g<110)&(b<110)
redm  = (r>130)&(r-g>60)&(r-b>60)
bluem = (b>150)&(b-r>60)&(b-g>60)
white = (r>238)&(g>238)&(b>238)

print("ROW1 108..168")
black_r1 = black.copy(); black_r1[:108]=False; black_r1[169:]=False
bb = bbox(black_r1, 108, 168, "black(dashed container+?)")
# white boxes row1
bbox(white, 112, 162, "white boxes row1")
bbox(redm, 112, 162, "red ink row1")
print("ROW2 178..238")
bbox(lav, 178, 238, "lavender fill(container)")
bbox(white, 182, 232, "white boxes row2")
bbox(bluem, 182, 232, "blue ink row2")
print("ROW3 253..315")
bbox(pink, 253, 315, "pink fill(container)")
bbox(white, 257, 310, "white boxes row3")
bbox(redm, 257, 310, "red ink row3")
