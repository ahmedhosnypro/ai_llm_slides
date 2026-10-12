from PIL import Image
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg").convert("RGB")
px = F.load()
# dash-under-band would read ~(208,46,18): dark red-orange, g<110, r>170
# band over gray panel reads ~(234,192,163): g>150
# band over the salmon box (200,126,87) -> (0.63*200+0.37*237, 0.63*126+0.37*125, 0.63*87+0.37*49)=(215,126,72): g~126
print("band region x600..660 y338..372: classify per row")
for y in range(338, 373):
    dark=[]; 
    for x in range(600, 661):
        r,g,b = px[x,y]
        if r>170 and g<110 and (r-g)>80: dark.append(x)
    if dark: print(" y",y,"dark-red-orange:",dark)
# Also: the enc box border zone for context rows 339-372 x640-650
print("enc box left border cols (r>170,g<110):")
for y in range(336, 375, 2):
    dark=[]
    for x in range(638, 655):
        r,g,b = px[x,y]
        if r>150 and g<110 and (r-g)>60: dark.append(x)
    print(" y",y,dark)
