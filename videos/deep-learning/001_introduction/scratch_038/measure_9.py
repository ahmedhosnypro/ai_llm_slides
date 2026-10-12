from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[...,0], a[...,1], a[...,2]

def classify(y0,y1,x0,x1):
    sub_r, sub_g, sub_b = r[y0:y1, x0:x1], g[y0:y1, x0:x1], b[y0:y1, x0:x1]
    n = (y1-y0)*(x1-x0)
    tests = {
      'K': ((sub_r<90)&(sub_g<90)&(sub_b<90)),                       # black ink
      'R': ((sub_r>150)&(sub_g<100)&(sub_b<100)),                    # red
      'C': ((sub_g>120)&(sub_b>120)&(sub_r<110)),                    # cyan
      'G': ((sub_g>110)&(sub_r<110)&(sub_b<110)),                    # green
      'Y': ((sub_r>170)&(sub_g>170)&(sub_b<110)),                    # yellow
      'P': ((sub_r>80)&(sub_r<180)&(sub_b>80)&(sub_b<190)&(sub_g<90)),# purple
      'B': ((sub_b>190)&(sub_r>60)&(sub_r<170)&(sub_g>100)),         # light blue
      'N': ((sub_r>140)&((sub_r-sub_g)>35)&((sub_g-sub_b)>20)),      # brown/tan
      'W': ((sub_r>235)&(sub_g>235)&(sub_b>235)),                    # white
    }
    best, cnt = '.', 0
    for k, m in tests.items():
        c = m.sum()
        if c > cnt: best, cnt = k, c
    if cnt < n*0.25: return '.'
    return best

print("    " + "".join(str((x//100)%10) for x in range(60, 815, 8)))
print("    " + "".join(str((x//10)%10) for x in range(60, 815, 8)))
for y in range(255, 515, 5):
    row = []
    for x in range(60, 815, 8):
        row.append(classify(y, y+5, x, x+8))
    print(f"{y:3d} " + "".join(row))
