from PIL import Image

# matrix region crop: frame coords (612, 375) - (854, 514) with margin
RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide031/render_3.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_031.jpg"
QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide031"
X0, Y0, X1, Y1 = 612, 375, 854, 514

r = Image.open(RENDER).convert("RGB")
S = r.size[0] / 960.0
rc = r.crop((int(X0*S), int(Y0*S), int(X1*S), int(Y1*S)))
rc = rc.resize((rc.size[0]*2, rc.size[1]*2), Image.LANCZOS)
rc.save(f"{QA}/crop_render_matrix.png")

o = Image.open(ORIG).convert("RGB")
oc = o.crop((X0, Y0, X1, Y1))
oc = oc.resize((oc.size[0]*2, oc.size[1]*2), Image.LANCZOS)
oc.save(f"{QA}/crop_original_matrix.png")
print("crops:", rc.size, oc.size)
