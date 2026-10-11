from PIL import Image
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
S = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide018/'
crops = {
 'crop_banner':   (20, 88, 560, 230),
 'crop_encmha':   (596, 318, 748, 402),
 'crop_decmha':   (655, 238, 862, 342),
 'crop_sdpa':     (30, 208, 215, 525),
 'crop_mhainset': (283, 203, 535, 532),
}
for name,(x0,y0,x1,y1) in crops.items():
    c = im.crop((x0,y0,x1,y1))
    c = c.resize((c.width*2, c.height*2), Image.LANCZOS)
    c.save(S+name+'.png')
    print(name, c.size)
