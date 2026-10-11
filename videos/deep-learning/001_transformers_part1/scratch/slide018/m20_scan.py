from PIL import Image
import collections
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
px = im.load()
def mode(x0,y0,x1,y1,tag):
    c=collections.Counter()
    for y in range(y0,y1):
        for x in range(x0,x1): c[px[x,y]]+=1
    print(tag, c.most_common(4))
mode(59,300,62,400,"frameA left border")
mode(120,246,150,249,"frameB top border")
mode(112,296,165,311,"topMatMul fill")
mode(85,431,160,444,"botMatMul fill")
mode(95,399,130,408,"Scale fill")
mode(82,365,140,376,"Mask fill")
mode(85,332,138,344,"SoftMax fill")
mode(368,314,406,325,"Concat fill")
mode(370,270,405,285,"topLinear fill")
mode(313,363,465,389,"SDPA mauve fill")
mode(660,360,715,384,"encMHA fill")
mode(755,282,812,305,"decMHA fill")
mode(115,110,450,142,"banner1 fill+text")
mode(120,165,400,195,"banner2 fill+text")
mode(88,470,96,478,"Q fill A")
mode(122,468,134,478,"K fill A")
mode(160,468,172,478,"V fill A")
mode(325,493,336,503,"V fill B")
mode(382,493,393,503,"K fill B")
