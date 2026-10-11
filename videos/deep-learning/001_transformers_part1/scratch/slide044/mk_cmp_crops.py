from PIL import Image
# same frame region from both, same output size: frame x726..916 y70..308
ren = Image.open("recreated_pptx/qa/slide044/render_1.png").convert("RGB")  # 2001x1125
org = Image.open("unique_slides/slide_044.jpg").convert("RGB")              # 960x540
S = 2000/960.0
box_r = (int(726*S), int(70*S), int(916*S), int(308*S))
box_o = (726, 70, 916, 308)
cr = ren.crop(box_r).resize((760, 952), Image.LANCZOS)
co = org.crop(box_o).resize((760, 952), Image.LANCZOS)
cr.save("recreated_pptx/qa/slide044/cmp_inset_render.png")
co.save("recreated_pptx/qa/slide044/cmp_inset_original.png")
print("saved", cr.size, co.size)
# full-slide pair for the judge is just render_1.png vs slide_044.jpg
