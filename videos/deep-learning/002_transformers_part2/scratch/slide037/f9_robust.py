# f9: rebuild slide space with the CONVERGED f37 fit; robust per-box color sampling.
from PIL import Image
import numpy as np

A, Bx, C, D = 21.15, 0.95635, 2.00, 0.95695
SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide037/my_slide_space.png"
img = Image.open(SRC).convert("RGB")
coeffs = (1.0/Bx, 0.0, -A/Bx, 0.0, 1.0/D, -C/D)
out = img.transform((960, 540), Image.AFFINE, coeffs, resample=Image.BILINEAR)
out.save(OUT)
print("wrote", OUT)

o = np.asarray(out).astype(int)

def robust(x0, x1, y0, y1, label):
    z = o[y0:y1, x0:x1].reshape(-1, 3).astype(float)
    s = z.sum(axis=1)
    lo, hi = np.percentile(s, [25, 75])
    core = z[(s >= lo) & (s <= hi)]
    med = np.median(core, axis=0)
    print(f"{label}: robust median ({med[0]:.0f},{med[1]:.0f},{med[2]:.0f})  hex #{int(med[0]):02X}{int(med[1]):02X}{int(med[2]):02X}  n={len(core)}")

print("== encoder stack (orig slide space) ==")
robust(632, 650, 320, 340, "container left strip (parent tan C8A888)")
robust(656, 716, 275, 286, "enc_addn_top (parent 6D99B4)")
robust(656, 716, 291, 312, "enc_ff (parent 807560)")
robust(660, 716, 345, 352, "enc_addn_bot (parent 6C99B4)")
robust(660, 670, 396, 405, "enc V circle zone (parent green 55A044)")
robust(637, 641, 300, 340, "green bus strip (parent 7FB421)")
print("== decoder stack ==")
robust(747, 752, 230, 258, "dec container left strip (parent olive B0B070)")
robust(756, 814, 208, 217, "dec_addn_top (parent 5C9CB7)")
robust(756, 814, 226, 247, "dec_ff (parent 6E7E62)")
robust(756, 814, 265, 273, "dec_addn_mid (parent 5C9CB6)")
robust(756, 814, 331, 342, "dec_indigo (parent 6E87E0)")
robust(747, 752, 328, 346, "dec low-left margin (parent panelGreen C8F8E0)")
robust(818, 830, 328, 346, "dec low-right margin (parent khaki B5BB97)")
robust(748, 820, 279, 308, "dec MHA box (parent B28659)")
print("== misc ==")
robust(682, 726, 253, 265, "yellow band over-stack zone (parent yellow)")
robust(728, 744, 255, 320, "yellow band right strip")
robust(752, 818, 152, 165, "softmax (parent A8ECBC)")
robust(752, 818, 178, 190, "linear (parent B0E4CE)")
robust(664, 706, 494, 509, "Inputs label zone")
robust(655, 665, 496, 512, "enc red arrow shaft")
