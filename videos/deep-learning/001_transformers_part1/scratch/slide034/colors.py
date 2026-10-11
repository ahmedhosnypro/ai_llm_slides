from PIL import Image
import numpy as np
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
a = np.asarray(img).astype(int)
def darkest(x0,x1,y0,y1,label,n=5):
    reg = a[y0:y1,x0:x1].reshape(-1,3)
    idx = np.argsort(reg.sum(axis=1))[:n]
    print(label, [tuple(reg[i]) for i in idx])
darkest(318,338,128,146,"concept X core")       # X glyph
darkest(311,318,120,160,"concept [ bracket")
darkest(338,366,154,166,"concept 1xd subscript (green?)")
darkest(57,90,290,320,"emb box X + brackets")
darkest(91,122,322,340,"emb box 1xd subscript")
darkest(174,242,300,318,"SoftMax header label")
darkest(178,240,404,422,"col1 SoftMax orange label")
darkest(179,244,420,440,"col1 block arrow red")
darkest(93,120,323,340,"col1 header d")
darkest(152,166,323,352,"col1 header down-arrow")
darkest(400,430,320,350,"col2 header d-up")
darkest(62,92,176,206,"concept d-up label")
darkest(207,224,176,207,"concept block up-arrow")
darkest(71,266,222,238,"annot line1 blue")
darkest(271,365,222,238,"annot highlight1 area")
darkest(272,365,240,256,"annot line2 red-on-orange")
darkest(401,860,290,306,"warning text")
darkest(403,436,368,485,"col2 input box fill/border")
darkest(134,167,368,485,"col1 input box fill/border")
darkest(254,306,368,485,"col1 output box")
darkest(45,395,100,272,"concept box border")
# fills
def mode(x0,x1,y0,y1,label):
    reg=a[y0:y1,x0:x1].reshape(-1,3)
    print(label,"median",tuple(np.median(reg,axis=0).astype(int)))
mode(140,160,375,382,"col1 input box1 fill")
mode(410,430,375,382,"col2 input box1 fill")
mode(260,300,375,382,"col1 output box1 fill")
mode(600,700,450,470,"panel peach fill")
mode(100,180,125,150,"concept interior")
mode(75,190,120,155,"large eq box fill")
