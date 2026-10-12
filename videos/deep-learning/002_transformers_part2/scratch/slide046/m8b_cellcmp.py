from PIL import Image
import numpy as np
f46 = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')).astype(int)
f45 = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_045.jpg').convert('RGB')).astype(int)
def segmean(a, y, x0, x1):
    seg = a[y-2:y+3, x0:x1].reshape(-1,3)
    return tuple(np.median(seg, axis=0).astype(int))
wins = [(184,191),(196,203),(208,215),(220,227)]
print('045 rows at centers (certified: FFFF00 92D050 FF9999 D9D9D9):')
for name, y in [('045 top c=175.6', 176), ('045 mid c=281.3', 281), ('045 cont c=385.9', 386), ('045 X c=488.5', 488)]:
    print(' ', name, [segmean(f45, y, x0, x1) for x0,x1 in wins])
print('046 rows at centers:')
for name, y in [('046 final c=73', 73), ('046 postFFN c=180.5', 180), ('046 postLN c=286.5', 286), ('046 outatt c=392', 392), ('046 X c=495', 495)]:
    print(' ', name, [segmean(f46, y, x0, x1) for x0,x1 in wins])
