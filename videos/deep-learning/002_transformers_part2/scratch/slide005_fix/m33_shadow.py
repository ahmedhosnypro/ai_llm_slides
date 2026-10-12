from PIL import Image
O = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide005/afix_hassembly_orig.png").convert("RGB")
R = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide005/afix_hassembly_render_4.png").convert("RGB")
po,pr = O.load(), R.load()
def midtone(p,x,y):
    r,g,b = p[x,y]; L = 0.299*r+0.587*g+0.114*b
    return 150<L<215 and abs(r-g)<15 and abs(g-b)<15
# shadow right border: crop x~64-66, rows 35..95; shadow top border: rows ~30-33, x28..64
for label,p in (("ORIG",po),("RENDER",pr)):
    n_right = sum(1 for y in range(35,96) for x in range(62,68) if midtone(p,x,y))
    n_top   = sum(1 for y in range(28,36) for x in range(28,64) if midtone(p,x,y))
    print(label, "shadow right-border midtone px:", n_right, " top-border px:", n_top)
