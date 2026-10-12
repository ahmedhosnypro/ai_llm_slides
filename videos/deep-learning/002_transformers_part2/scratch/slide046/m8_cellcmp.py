from PIL import Image
import numpy as np
f46 = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')).astype(int)
f45 = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_045.jpg').convert('RGB')).astype(int)
# 045 frame rows (frame y): top 167.2, mid 273.3, cont 377.3, X 480.3 ; col1 bar x 181..229
# 046 frame rows: final 73, postFFN 178, postLN 286, outatt 390, X 496 ; same cols
def segmean(a, y, x0, x1):
    seg = a[y-3:y+4, x0:x1].reshape(-1,3)
    return tuple(np.median(seg, axis=0).astype(int))
print('SEGMENT MEANS (median over 7xN window), col1 bar:')
print('frame | seg1(x183-191) | seg2(x195-203) | seg3(x207-215) | seg4(x219-227)')
for name, a, ys in [('045 top', f45, 167), ('045 mid', f45, 273), ('045 cont', f45, 377), ('045 X', f45, 480),
                    ('046 final', f46, 73), ('046 postFFN', f46, 178), ('046 postLN', f46, 286), ('046 outatt', f46, 390), ('046 X', f46, 496)]:
    print(name, [segmean(a, ys, x0, x1) for x0,x1 in [(183,192),(195,204),(207,216),(219,228)]])
# also sample col8 (frame cx 834.4): segments x 810..858
print('col8:')
for name, a, ys in [('045 top', f45, 167), ('046 final', f46, 73), ('046 X', f46, 496)]:
    print(name, [segmean(a, ys, x0, x1) for x0,x1 in [(812,821),(824,833),(836,845),(848,857)]])
