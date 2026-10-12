# m31_crops.py — cut matched crop pairs for the fixed arrow regions
from PIL import Image
FR = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg").convert("RGB")
RD = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide005/render_4.png").convert("RGB")
Q = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide005/"
SX, SY = 2.16770, 2.17684  # frame px -> render px
def cut(name, fx0, fy0, fx1, fy1):
    ox0,oy0,ox1,oy1 = int(fx0),int(fy0),int(fx1),int(fy1)
    rx0,ry0,rx1,ry1 = round((fx0-18.0787)*SX), round((fy0-0.4700)*SY), round((fx1-18.0787)*SX), round((fy1-0.4700)*SY)
    oc = FR.crop((ox0,oy0,ox1,oy1)).resize((rx1-rx0, ry1-ry0), Image.LANCZOS)
    rc = RD.crop((rx0,ry0,rx1,ry1))
    oc.save(Q+f"afix_{name}_orig.png"); rc.save(Q+f"afix_{name}_render_4.png")
    print(name, "orig", oc.size, "render", rc.size)
cut("hassembly", 448, 315, 532, 400)     # h circle + head + curve + gray line
cut("corridor", 412, 160, 534, 268)      # banner2 -> inset top border (connect_tan + junction)
cut("d1end",   596, 326, 668, 378)       # d1 tail under band -> enc box border
cut("d2end",   276, 328, 330, 382)       # d2 tail -> red rect left border
cut("d3zone",  188, 398, 268, 478)       # d3 fragment + inset bottom-right corner
