from PIL import Image
import collections
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
px = im.load()

print("== pink/light-red thin curve pixels x410..660 y85..380 ==")
pts=[(x,y) for y in range(85,385) for x in range(410,665) if px[x,y][0]>190 and 90<px[x,y][1]<210 and 90<px[x,y][2]<215 and px[x,y][0]-px[x,y][1]>30]
print("n=",len(pts))
cc=collections.Counter()
for x,y in pts: cc[(x//10*10, y//10*10)]+=1
for k in sorted(cc): print(k, cc[k])
