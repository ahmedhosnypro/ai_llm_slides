from PIL import Image
R = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide005/render_4.png").convert("RGB")
px = R.load()
def is_pinkp(x,y):
    r,g,b = px[x,y]
    return r>150 and 70<g<185 and (r-g)>25 and (r-b)>25
def grayp(x,y):
    r,g,b = px[x,y]
    return abs(r-g)<14 and abs(g-b)<14 and 140<(0.299*r+0.587*g+0.114*b)<215
# spurious-stroke corridor ABOVE connect_tan's path: x998-1024, y310-492
pts=[(x,y) for y in range(310,493) for x in range(998,1025) if is_pinkp(x,y) or grayp(x,y)]
print("connector-ink px in old spurious corridor (y310-492):", len(pts), pts[:10])
print("VERDICT:", "PASS - corridor clean" if len(pts)==0 else "FAIL")
