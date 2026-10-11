from PIL import Image
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
px = im.load()

print("== ASCII map x720..800 y250..335: R=strong red, Y=yellow, P=purple-ish, t=tan, .=bg ==")
for y in range(250,336):
    row=""
    for x in range(720,801):
        r,g,b = px[x,y]
        if r>150 and g<85 and b<85: row+="R"
        elif r>200 and g>200 and b<120: row+="Y"
        elif abs(r-205)<25 and abs(g-138)<30 and abs(b-220)<30: row+="P"
        elif abs(r-200)<20 and abs(g-168)<20 and abs(b-136)<20: row+="t"
        else: row+="."
    print(f"{y:3d} {row}")

print()
print("== red pixels x500..748 y120..380 (corridor between insets and arch) ==")
import collections
pts=[(x,y) for y in range(120,385) for x in range(500,749) if px[x,y][0]>150 and px[x,y][1]<85 and px[x,y][2]<85]
print("n=",len(pts))
cc=collections.Counter((x//12*12, y//12*12) for x,y in pts)
for k in sorted(cc): print(k, cc[k])
