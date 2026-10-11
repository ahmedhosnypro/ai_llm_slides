from PIL import Image
R = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide018/render_1.png').convert('RGB')
O = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
S = R.size[0]/960.0
D = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide018/'
regions = {
  'rc_banner':  (20, 88, 560, 230),
  'rc_sdpa':    (30, 205, 215, 525),
  'rc_mhainset':(283, 203, 535, 532),
  'rc_encmha':  (596, 318, 748, 402),
  'rc_decmha':  (655, 238, 862, 342),
}
for name,(x0,y0,x1,y1) in regions.items():
    # render crop (150dpi space) resized to 2x original-crop scale for parity
    rc = R.crop((int(x0*S), int(y0*S), int(x1*S), int(y1*S)))
    oc = O.crop((x0,y0,x1,y1))
    target = (oc.width*2, oc.height*2)
    rc = rc.resize(target, Image.LANCZOS)
    oc = oc.resize(target, Image.LANCZOS)
    rc.save(D+name+'_render.png'); oc.save(D+name+'_orig.png')
    print(name, rc.size)
