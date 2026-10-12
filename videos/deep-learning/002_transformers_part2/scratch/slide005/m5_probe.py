# m5 (slide005): numeric probes.
# A) Grid of median my/warp colors over the architecture area (build pt grid).
# B) Box-state table: certified base box rects -> median my color + best tint fit.
# C) Probe strips: chevrons zone1/2/3, gap shafts, legend/leader positions, pin/band
#    absence, 'Output' yellow highlight, N x circle.
from PIL import Image
import numpy as np

A, Bx, C, D = 20.9473, 0.95679, 2.2031, 0.95651
def to_frame(bx, by):
    return 18.0787 + 0.961084 * bx, 0.4700 + 0.957187 * by

myI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg').convert('RGB')
wI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/warped_001_f21.png')
my = np.asarray(myI).astype(np.float32)
w = np.asarray(wI).astype(np.float32)

def med(img, bx, by, bw, bh):
    fx, fy = to_frame(bx, by)
    fw, fh = 0.961084 * bw, 0.957187 * bh
    x0, y0 = int(fx), int(fy)
    x1, y1 = int(fx + fw), int(fy + fh)
    reg = img[y0:y1, x0:x1].reshape(-1, 3)
    return np.median(reg, axis=0)

def tintfit(mycol, warpcol):
    best = ('none', 0.0, 999.0)
    for name, tint in (('Y', (255, 255, 0)), ('O', (237, 125, 49))):
        t = np.array(tint, np.float32)
        d = t - warpcol
        den = (d * d).sum()
        if den < 1e-3:
            continue
        a = float(np.clip(((mycol - warpcol) * d).sum() / den, 0, 1))
        res = float(np.abs(warpcol + a * d - mycol).max())
        if res < best[2]:
            best = (name, a, res)
    return best

print('== B) box-state table (build coords; median my; median warp; fit) ==')
boxes = [
    ('enc_addn_top', 653, 273, 67, 14.5), ('enc_ff', 653, 288, 67, 27),
    ('enc_addn_bot', 656, 343.5, 64, 10), ('enc_mha', 652, 354, 68, 35),
    ('enc_bus_x637', 633, 290, 8, 100), ('enc_panel_top', 620, 200, 80, 20),
    ('dec_addn_top', 753, 206.5, 64, 12.5), ('dec_ff', 753, 223.5, 64, 26.5),
    ('dec_addn_mid', 753, 263.5, 64, 11), ('dec_mha_cross', 752, 280, 66, 27),
    ('dec_masked_mha', 753, 313, 64, 14), ('dec_low_indigo', 753, 331, 64, 11),
    ('dec_trunk_x834', 831, 290, 7, 100), ('Nx_circle', 843, 302, 22, 22),
    ('output_hl', 760, 112, 48, 16), ('outputs_shifted_hl', 764, 497, 44, 12),
    ('between_panels', 722, 250, 20, 20), ('enc_panel_gap', 600, 300, 20, 20),
    ('left_of_enc_panel', 585, 370, 20, 20), ('right_of_dec_panel', 880, 280, 14, 20),
]
for name, bx, by, bw, bh in boxes:
    m = med(my, bx, by, bw, bh); wr = med(w, bx, by, bw, bh)
    fit = tintfit(m, wr)
    print(f'  {name:22s} my=({m[0]:5.0f},{m[1]:5.0f},{m[2]:5.0f})  warp=({wr[0]:5.0f},{wr[1]:5.0f},{wr[2]:5.0f})  fit={fit[0]} a={fit[1]:.2f} res={fit[2]:.0f}')

print('== C) probe strips ==')
# chevrons: zone1 (783.5,197/202), zone2 (783.5,255.5/259.5), zone3 (772,313/318) build
for name, cx, cy in [('chev_z1', 783.5, 197), ('chev_z1b', 783.5, 202), ('chev_z2', 783.5, 255.5),
                     ('chev_z2b', 783.5, 259.5), ('chev_z3', 772, 313), ('chev_z3b', 772, 318)]:
    m = med(my, cx - 4, cy - 3, 8, 6); wr = med(w, cx - 4, cy - 3, 8, 6)
    print(f'  {name:10s} my=({m[0]:5.0f},{m[1]:5.0f},{m[2]:5.0f}) warp=({wr[0]:5.0f},{wr[1]:5.0f},{wr[2]:5.0f})')

# gap shafts: build x784.7 y193.6-206.4 and y250.5-263.5 (from 002:19 drawGapShafts)
for name, x0, y0, x1, y1 in [('shaft_gap1', 783, 194, 787, 206), ('shaft_gap2', 783, 251, 787, 263),
                             ('shaft_cont', 783, 230, 787, 245)]:
    m = med(my, x0, y0, x1 - x0, y1 - y0); wr = med(w, x0, y0, x1 - x0, y1 - y0)
    print(f'  {name:10s} my=({m[0]:5.0f},{m[1]:5.0f},{m[2]:5.0f}) warp=({wr[0]:5.0f},{wr[1]:5.0f},{wr[2]:5.0f})')

# legend/leader absence probes (001 build coords) -> my frame should be panel gray / callout peach
for name, x0, y0, x1, y1 in [
    ('legend1_zone', 141, 102, 342, 130), ('legend2_zone', 311, 143, 514, 171),
    ('legend3_zone', 264, 181, 465, 209), ('leader1_mid', 500, 130, 700, 160),
    ('leader5_mid', 540, 250, 590, 330), ('pin_zone', 531, 334, 603, 406),
    ('band_zone', 570, 420, 900, 490)]:
    m = med(my, x0, y0, x1 - x0, y1 - y0); wr = med(w, x0, y0, x1 - x0, y1 - y0)
    print(f'  {name:14s} my=({m[0]:5.0f},{m[1]:5.0f},{m[2]:5.0f}) warp=({wr[0]:5.0f},{wr[1]:5.0f},{wr[2]:5.0f})')

print('== A) grid medians (build pt, 20pt cells, x560-900 y190-500): my|warp, tint flag ==')
hdr = '      ' + ''.join(f'x{bx:4d}           ' for bx in range(560, 900, 40))
print(hdr)
for by in range(190, 500, 20):
    row = f'y{by:4d} '
    for bx in range(560, 900, 40):
        m = med(my, bx, by, 20, 20); wr = med(w, bx, by, 20, 20)
        fit = tintfit(m, wr)
        flag = '.' if fit[2] < 18 else (fit[0] if fit[2] < 40 else '?')
        row += f'{int(m[0]):3d},{int(m[1]):3d},{int(m[2]):3d}{flag} '
    print(row)
