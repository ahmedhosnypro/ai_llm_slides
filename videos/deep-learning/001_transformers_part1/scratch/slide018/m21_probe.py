from PIL import Image
r = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide018/render_1.png').convert('RGB')
p = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide017/render_1.png').convert('RGB')
print("sizes:", r.size, p.size)
r9 = r.resize((960,540), Image.LANCZOS); p9 = p.resize((960,540), Image.LANCZOS)
pr, pp = r9.load(), p9.load()
print("== cluster (880-912, 96-116): render vs parent ==")
for y in range(94,118,3):
    print(y, [pr[x,y] for x in range(878,914,6)], "|", [pp[x,y] for x in range(878,914,6)])
print("== full-res badge zone ==")
for y in range(180,250,10):
    print(y, [r[x,y] for x in range(1830,1905,15)])
