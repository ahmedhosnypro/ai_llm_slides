from PIL import Image
QA="/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide026"
RENDER=f"{QA}/render_1.png"
ORIG="/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg"
CROPS={  # name: (x0,y0,x1,y1) frame px
 'crop1_eq1':   (95,118,505,182),
 'crop2_eq23':  (90,188,600,300),
 'crop3_chain': (95,300,615,372),
 'crop4_final': (95,378,830,500),
}
r=Image.open(RENDER).convert("RGB"); S=r.size[0]/960.0
o=Image.open(ORIG).convert("RGB")
for name,(x0,y0,x1,y1) in CROPS.items():
    rc=r.crop((int(x0*S),int(y0*S),int(x1*S),int(y1*S)))
    rc=rc.resize((rc.size[0]*2,rc.size[1]*2), Image.LANCZOS)
    rc.save(f"{QA}/crop_render_{name}.png")
    oc=o.crop((x0,y0,x1,y1)).resize(((x1-x0)*2,(y1-y0)*2), Image.LANCZOS)
    oc.save(f"{QA}/crop_original_{name}.png")
    print(name, rc.size, oc.size)
