from PIL import Image
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_018.jpg').convert('RGB')
W,H = im.size
px = im.load()
def isred(r,g,b): return r>150 and g<80 and b<80
def isreddish(r,g,b): return r>100 and r-g>40 and r-b>40

# vertical profile at several columns: classify each row 40..120
for col in [200, 480, 800]:
    seq=[]
    prev=None
    for y in range(40,130):
        r,g,b = px[col,y]
        c = 'R' if isreddish(r,g,b) else ('W' if r>245 and g>245 else ('G' if 215<r<245 and 215<g<245 else '?'))
        if c!=prev: seq.append(f"{y}{c}"); prev=c
    print(f"col{col} y40..130:", " ".join(seq))

# horizontal profile at several rows
for row in [50, 75, 105, 130]:
    seq=[]; prev=None
    for x in range(30,940):
        r,g,b = px[x,row]
        c = 'R' if isreddish(r,g,b) else ('W' if r>245 and g>245 else ('G' if 215<r<245 and 215<g<245 else '?'))
        if c!=prev: seq.append(f"{x}{c}"); prev=c
    print(f"row{row}:", " ".join(seq))
