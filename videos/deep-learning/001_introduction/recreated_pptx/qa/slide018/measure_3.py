from PIL import Image
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_018.jpg').convert('RGB')
W,H = im.size
px = im.load()
def isred(r,g,b): return r>150 and g<80 and b<80

# find vertical red lines: for each x, count red pixels over y 100..470
counts = {}
for x in range(0,W):
    c = sum(1 for y in range(100,470) if isred(*px[x,y]))
    if c > 50: counts[x]=c
print("vertical red lines (x:count):", counts)

# horizontal red lines: for each y, count red pixels over x 100..860
hc = {}
for y in range(40,520):
    c = sum(1 for x in range(100,860) if isred(*px[x,y]))
    if c > 100: hc[y]=c
print("horizontal red lines (y:count):", hc)
