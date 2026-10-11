from PIL import Image
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
px = im.load()
print("== ASCII x485..575 y92..150: R=red-ish, p=pink-ish, .=other ==")
for y in range(92,151):
    row=""
    for x in range(485,576):
        r,g,b = px[x,y]
        if r>150 and g<85 and b<85: row+="R"
        elif r>200 and 130<g<215 and 130<b<215 and r-g>25: row+="p"
        else: row+="."
    print(f"{y:3d} {row}")
