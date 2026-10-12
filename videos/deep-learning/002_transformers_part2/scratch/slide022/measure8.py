from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg').convert('RGB')).astype(int)

print("== left edge columns x55..70, rows 115,130,200,280,360,460,505 ==")
for y in [115,130,200,280,360,460,505]:
    print(f" y={y}:", " ".join(f"x{x}:{im[y,x].tolist()}" for x in range(55,71,2)))
print("== right edge columns x886..906 ==")
for y in [115,130,200,280,360,460,505]:
    print(f" y={y}:", " ".join(f"x{x}:{im[y,x].tolist()}" for x in range(886,907,2)))
print("== boundary rows y336..356 at x=400,700 ==")
for y in range(334, 358):
    print(f" y={y} x400:{im[y,400].tolist()} x700:{im[y,700].tolist()}")
print("== bottom rows y496..508 at x=400,700 ==")
for y in range(496, 509):
    print(f" y={y} x400:{im[y,400].tolist()} x700:{im[y,700].tolist()}")
print("== fills: row1 container (x300,y140) row2 (x300,y205) row3 (x300,y285) cyan (x700,y440) boxes r1 (x200,y138) r2 (x200,y205) r3 (x200,y285)")
for lbl,(x,y) in {"r1fill":(300,146),"r1box":(200,138),"r2fill":(300,210),"r2box":(200,205),"r3fill":(300,290),"r3box":(200,285),"cyan":(700,440),"white?":(300,170)}.items():
    print(f" {lbl}: {im[y,x].tolist()}")
