from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def core(y0,y1,x0,x1,fn,label):
    px = im[y0:y1+1, x0:x1+1].reshape(-1,3)
    sel = np.array([fn(p) for p in px])
    if sel.sum()==0: print(label, "none"); return
    avg = px[sel].mean(axis=0)
    print(f"{label}: ({avg[0]:.0f},{avg[1]:.0f},{avg[2]:.0f}) n={int(sel.sum())}")

# darkest-quartile sampler for text cores
def darkq(y0,y1,x0,x1,label):
    luma = (0.299*im[y0:y1+1,x0:x1+1,0]+0.587*im[y0:y1+1,x0:x1+1,1]+0.114*im[y0:y1+1,x0:x1+1,2]).reshape(-1)
    px = im[y0:y1+1, x0:x1+1].reshape(-1,3)
    idx = np.argsort(luma)[:max(4,len(luma)//8)]
    avg = px[idx].mean(axis=0)
    print(f"{label}: darkest-1/8 avg ({avg[0]:.0f},{avg[1]:.0f},{avg[2]:.0f})")

darkq(60,80,340,690,"title")
darkq(86,106,367,675,"subtitle")
darkq(114,158,69,151,"R1 label (gray)")
darkq(192,220,68,143,"R2 label (blue)")
darkq(263,289,65,148,"R3 label (red)")
darkq(132,141,185,225,"R1 box1 text")
darkq(198,212,180,225,"R2 box1 text")
darkq(277,290,190,215,"R3 box1 text")
darkq(368,384,80,109,"lead 'Use' (blue)")
darkq(368,384,120,249,"lead red seg")
darkq(391,403,80,155,"Problems red")
darkq(413,428,113,344,"bullet1 blue")
darkq(434,450,370,460,"bullet2 red seg")
darkq(456,471,99,343,"bullet2 L2 magenta")
darkq(478,494,113,545,"bullet3 blue")
darkq(313,328,218,235,"+delta label red")
# dot cores
darkq(412,425,97,107,"bullet dot")
darkq(134,142,624,632,"row1 dot gray")
darkq(203,212,624,633,"row2 dot blue")
# fills
def avg(y0,y1,x0,x1,label):
    px = im[y0:y1+1,x0:x1+1].reshape(-1,3).mean(axis=0)
    print(f"{label}: ({px[0]:.0f},{px[1]:.0f},{px[2]:.0f})")
avg(200,214,255,300,"lavender fill (no text zone)")
avg(282,290,244,262,"pink fill (gap zone)")
avg(495,499,300,700,"hlbox fill bottom strip")
avg(356,364,300,700,"hlbox fill top strip")
avg(150,155,300,340,"row1 container interior (between boxes)")
# orange stroke core
darkq(295,304,263,273,"orange stroke")
