from PIL import Image
r = Image.open('videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide046/render_1.png').convert('RGB')
f = Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')
S = 150/72
def crop_render(x0pt, y0pt, x1pt, y1pt):
    return r.crop((int(x0pt*S), int(y0pt*S), int(x1pt*S), int(y1pt*S)))
def crop_frame(fx0, fy0, fx1, fy1):
    return f.crop((int(fx0), int(fy0), int(fx1), int(fy1)))
# region A: rightmost columns labels, all rows (frame x 730..865, y 55..510)
# in slide pts: x (730-17.582)/0.962329=740.3 .. (865-17.582)/0.962329=880.5 ; y 57.5..533.7
crop_render(738, 57, 882, 536).resize((216*3, 379*3), Image.LANCZOS).save('videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide046/ccA_render.png')
crop_frame(730, 55, 865, 512).resize((135*5, 457*5), Image.LANCZOS).save('videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide046/ccA_orig.png')
# region B: top unit + final row + callout (frame x 55..900, y 38..200)
# slide: x 38.9..916.4, y 39.8..209.3
crop_render(39, 40, 916, 209).resize((877*2, 169*2), Image.LANCZOS).save('videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide046/ccB_render.png')
crop_frame(55, 38, 900, 200).resize((845*2, 162*2), Image.LANCZOS).save('videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide046/ccB_orig.png')
print('crops written')
