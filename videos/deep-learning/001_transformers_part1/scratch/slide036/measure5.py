from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_036.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def stroke_color(pts, label):
    # take the most saturated/dark pixel within +-2px of each point
    best=[]
    for (x,y) in pts:
        cand = a[max(0,y-2):y+3, max(0,x-2):x+3].reshape(-1,3)
        lum = cand.mean(axis=1); sat = cand.max(axis=1)-cand.min(axis=1)
        score = sat*1.5 + (255-lum)
        i = int(np.argmax(score))
        best.append(tuple(cand[i]))
    arr = np.array(best)
    print(f'{label}: median {tuple(np.median(arr,axis=0).astype(int))}  samples {best[:6]}')

# Equations box border: edges x308, x659, y106, y226
stroke_color([(308,y) for y in range(115,215,10)], 'EQBOX left  x=308')
stroke_color([(659,y) for y in range(115,215,10)], 'EQBOX right x=659')
stroke_color([(x,106) for x in range(320,650,30)], 'EQBOX top   y=106')
stroke_color([(x,226) for x in range(320,650,30)], 'EQBOX bot   y=226')
# Bell box: x683..893, y110..219
stroke_color([(683,y) for y in range(115,215,10)], 'BELL left  x=683')
stroke_color([(893,y) for y in range(115,215,10)], 'BELL right x=893')
stroke_color([(x,110) for x in range(695,885,25)], 'BELL top   y=110')
stroke_color([(x,219) for x in range(695,885,25)], 'BELL bot   y=219')
# Vector container: x46..270, y99..373
stroke_color([(46,y) for y in range(110,365,20)], 'VEC left  x=46')
stroke_color([(270,y) for y in range(110,365,20)], 'VEC right x=270')
stroke_color([(x,99) for x in range(55,265,20)], 'VEC top   y=99')
stroke_color([(x,372) for x in range(55,265,20)], 'VEC bot   y=372')
# Statement boxes: x296..601 y238..279 ; x617..896 y238..280
stroke_color([(296,y) for y in range(244,275,5)], 'STMT1 left')
stroke_color([(601,y) for y in range(244,275,5)], 'STMT1 right')
stroke_color([(x,238) for x in range(305,595,25)], 'STMT1 top')
stroke_color([(617,y) for y in range(244,275,5)], 'STMT2 left')
stroke_color([(896,y) for y in range(244,275,5)], 'STMT2 right')
stroke_color([(x,280) for x in range(625,890,25)], 'STMT2 bot')
# Formula box1 x291..443 y306..363 ; box2 x503..655 y296..373 ; box3 x?..? y308..358
stroke_color([(291,y) for y in range(312,358,6)], 'FBOX1 left')
stroke_color([(443,y) for y in range(312,358,6)], 'FBOX1 right')
stroke_color([(x,306) for x in range(300,435,15)], 'FBOX1 top')
stroke_color([(x,363) for x in range(300,435,15)], 'FBOX1 bot')
stroke_color([(503,y) for y in range(302,368,8)], 'FBOX2 left')
stroke_color([(655,y) for y in range(302,368,8)], 'FBOX2 right')
stroke_color([(x,296) for x in range(512,648,15)], 'FBOX2 top')
stroke_color([(x,373) for x in range(512,648,15)], 'FBOX2 bot')
# box3: find edges first via scan
print()
# Remember box: x44..223 y386..507
stroke_color([(44,y) for y in range(395,500,10)], 'REMEMBER left')
stroke_color([(223,y) for y in range(395,500,10)], 'REMEMBER right')
stroke_color([(x,386) for x in range(55,215,15)], 'REMEMBER top')
stroke_color([(x,506) for x in range(55,215,15)], 'REMEMBER bot')
# Flowchart1 black box x286..502 y379..523
stroke_color([(286,y) for y in range(390,515,12)], 'FC1 left')
stroke_color([(502,y) for y in range(390,515,12)], 'FC1 right')
stroke_color([(x,379) for x in range(295,495,20)], 'FC1 top')
stroke_color([(x,523) for x in range(295,495,20)], 'FC1 bot')
# Flowchart2 box: v L 512-515, R 891-899, h top 372-374? bot 522-524
stroke_color([(513,y) for y in range(390,510,12)], 'FC2 left')
stroke_color([(894,y) for y in range(390,510,12)], 'FC2 right')
stroke_color([(x,373) for x in range(560,880,25)], 'FC2 top')
stroke_color([(x,523) for x in range(560,880,25)], 'FC2 bot')
