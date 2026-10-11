from PIL import Image
import collections
r = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide018/render_1.png').convert('RGB')
r9 = r.resize((960,540), Image.LANCZOS)
pr = r9.load()
c=collections.Counter()
for y in range(280,308):
    for x in range(752,818):
        p = pr[x,y]
        c[p]+=1
print("dec box render modes:", c.most_common(6))
# text pixels (dark) inside dec box
dark=[(x,y) for y in range(280,308) for x in range(752,818) if sum(pr[x,y])<260]
print("dark text px:", len(dark))
