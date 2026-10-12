from PIL import Image
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_018.jpg').convert('RGB')
W,H = im.size
px = im.load()
# raw pixels along row 300, x 50..110 and x 870..930
print("row300 x50..110:", [(x,px[x,300]) for x in range(50,112)])
print("row300 x860..930:", [(x,px[x,300]) for x in range(860,931)])
# raw pixels along col 480, y 30..60 and y 455..480
print("col480 y28..60:", [(y,px[480,y]) for y in range(28,61)])
print("col480 y455..485:", [(y,px[480,y]) for y in range(455,486)])
