from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def classify(y, x):
    R,G,B = r[y,x], g[y,x], b[y,x]
    if R>120 and R-G>45 and R-B>45: return 'R'   # red
    if B-R>60 and B-G>45: return 'B'             # blue
    if R<110 and G<110 and B<110: return 'K'     # black/dark
    if R>238 and G>238 and B>238: return 'w'     # white
    if abs(R-204)<30 and abs(G-204)<30 and B>235: return 'l'  # lavender
    if R>235 and abs(G-224)<22 and abs(B-224)<22: return 'p'  # pink
    if abs(R-233)<14 and abs(G-233)<14 and abs(B-231)<16: return '.' # bg gray
    if R>200 and G>120 and G<200 and B<90: return 'O'  # orange
    return '?'

def show(y0, y1, x0, x1, ystep=2, xstep=4, label=""):
    print(f"--- {label} rows {y0}..{y1} cols {x0}..{x1} (ystep {ystep}, xstep {xstep})")
    hdr = "     " + "".join(str((x0+i*xstep)//100%10) for i in range(0, (x1-x0)//xstep+1))
    print(hdr)
    for y in range(y0, y1+1, ystep):
        line = "".join(classify(y, x0+i*xstep) for i in range(0, (x1-x0)//xstep+1))
        print(f"{y:4d} {line}")

show(108, 168, 60, 905, label="ROW1")
