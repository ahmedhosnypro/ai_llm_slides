from PIL import Image
import numpy as np
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
a = np.asarray(F).astype(int)
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

def bbox(mask, label):
    ys, xs = np.where(mask)
    if len(xs)==0: print(label, ": none"); return
    print("%-22s x %4d..%4d  y %4d..%4d  n=%d" % (label, xs.min(), xs.max(), ys.min(), ys.max(), len(xs)))

# green dashed border (00B050-ish strong green)
grn = (g>120)&(r<130)&(b<130)&(g-r>40)&(g-b>40)
# legend zone
m = np.zeros_like(grn); m[420:522, 640:915] = grn[420:522, 640:915]
bbox(m, "legend green dash")
# mint fill E8FCE8 in legend zone
mint = (np.abs(r-232)<16)&(np.abs(g-252)<12)&(np.abs(b-232)<16)
m2 = np.zeros_like(mint); m2[420:522, 640:915] = mint[420:522, 640:915]
bbox(m2, "legend mint fill")
# W(e) chip: yellow FBE8B8-ish / gold above legend
gold = (r>230)&(g>190)&(g<230)&(b<190)
m3 = np.zeros_like(gold); m3[415:460, 640:760] = gold[415:460, 640:760]
bbox(m3, "W(e) chip gold")
# wochips: white boxes with red/green/blue borders in right zone x 590..800 y 350..520
# blue border 2F55C8-ish
blu = (np.abs(r-47)<50)&(np.abs(g-85)<50)&(b>140)&(b-r>60)
m4 = np.zeros_like(blu); m4[340:520, 590:800] = blu[340:520, 590:800]
bbox(m4, "wochips blue bord")
# headpanels dashed boxes: white fill regions x 600..800 y 240..470
wht = (r>244)&(g>244)&(b>244)
m5 = np.zeros_like(wht); m5[230:470, 596:800] = wht[230:470, 596:800]
bbox(m5, "headpanels white")
# vecbox: blue border 2222CC top center
m6 = np.zeros_like(blu); m6[40:90, 380:520] = blu[40:90, 380:520]
bbox(m6, "vecbox blue bord")
# input container mint fill x 90..140 y 300..430
m7 = np.zeros_like(mint); m7[295:435, 88:145] = mint[295:435, 88:145]
bbox(m7, "input container mint")
# token container mint fill x 150..370 y 465..505
m8 = np.zeros_like(mint); m8[460:505, 145:375] = mint[460:505, 145:375]
bbox(m8, "token container mint")
# gold boxes left: exact columns at row bands
goldF = (np.abs(r-245)<14)&(np.abs(g-194)<20)&(np.abs(b-66)<30)
m9 = np.zeros_like(goldF); m9[300:430, 125:180] = goldF[300:430, 125:180]
bbox(m9, "W_k gold boxes")
m10 = np.zeros_like(goldF); m10[300:430, 490:545] = goldF[300:430, 490:545]
bbox(m10, "W_v gold container")
# query W_q box red border x 215..255 y 438..468
red = (r>150)&(g<110)&(b<110)&(r-g>60)
m11 = np.zeros_like(red); m11[435:470, 210:260] = red[435:470, 210:260]
bbox(m11, "W_q box red")
# q strip pale cells x 235..285 y 428..445
cream = (r>235)&(g>225)&(b>190)&(b<235)
m12 = np.zeros_like(cream); m12[425:450, 230:290] = cream[425:450, 230:290]
bbox(m12, "q strip cells")
# concat bar: stadium outline dark 3A3A3A at y 120..150
dk = (r<90)&(g<90)&(b<90)
m13 = np.zeros_like(dk); m13[118:152, 180:700] = dk[118:152, 180:700]
bbox(m13, "concat bar dark px")
# LT box orange border D26900
org = (np.abs(r-210)<35)&(np.abs(g-105)<35)&(b<60)
m14 = np.zeros_like(org); m14[80:120, 300:580] = org[80:120, 300:580]
bbox(m14, "LT box orange border")
