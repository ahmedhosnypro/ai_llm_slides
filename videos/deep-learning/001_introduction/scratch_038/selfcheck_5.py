from PIL import Image
import numpy as np
R = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide038/render_3.png').convert('RGB')).astype(int)
S = R.shape[1]/960.0
r, g, b = R[...,0], R[...,1], R[...,2]
ink = (r<175)&(g<175)&(b<175)
def fb(y0,y1,x0,x1):
    m = ink[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    ys, xs = np.nonzero(m)
    if len(xs)==0: return None
    return (round(x0+xs.min()/S,1), round(x0+xs.max()/S,1), round(y0+ys.min()/S,1), round(y0+ys.max()/S,1))
print("RGB:", fb(256, 289, 280, 370), "exp (294,358,267,283)")
print("arrow3d:", fb(300, 342, 276, 324), "exp (287,320,308,332) tip")
print("line1:", fb(128, 168, 95, 880), "exp (102,774,139,158)")
print("735text:", fb(464, 504, 366, 560), "exp (378,546,470,496)")
# also prepare crops for the pre-judge dense-region comparisons
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
D = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide038/'
# formula box crop: frame x 85..885, y 112..240
im.crop((85, 112, 885, 240)).resize((1600, 256), Image.LANCZOS).save(D+'orig_fbox_2x.png')
Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide038/render_3.png').convert('RGB').crop((int(85*S), int(112*S), int(885*S), int(240*S))).resize((1600,256), Image.LANCZOS).save(D+'render_fbox_2x.png')
# diagram crop: frame x 175..815, y 245..516
im.crop((175, 245, 815, 516)).resize((1600, 677), Image.LANCZOS).save(D+'orig_diag_25x.png')
Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide038/render_3.png').convert('RGB').crop((int(175*S), int(245*S), int(815*S), int(516*S))).resize((1600,677), Image.LANCZOS).save(D+'render_diag_25x.png')
print("crops saved")
