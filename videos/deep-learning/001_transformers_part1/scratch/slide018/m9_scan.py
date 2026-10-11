from PIL import Image
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
px = im.load()

print("== ASCII x798..880 y255..330 ==")
for y in range(255,331):
    row=""
    for x in range(798,881):
        r,g,b = px[x,y]
        if r>150 and g<85 and b<85: row+="R"
        elif r>200 and g>200 and b<120: row+="Y"
        else: row+="."
    print(f"{y:3d} {row}")

print()
print("== red x190..505 y235..540 (between/around insets) ==")
import collections
pts=[(x,y) for y in range(235,541) for x in range(190,506) if px[x,y][0]>150 and px[x,y][1]<85 and px[x,y][2]<85]
print("n=",len(pts))
cc=collections.Counter((x//14*14, y//14*14) for x,y in pts)
for k in sorted(cc):
    if cc[k]>=2: print(k, cc[k])
