from PIL import Image
import numpy as np
a = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')).astype(int)
print('raw colors x=100..160 (step 12), y=41..53:')
for y in range(41, 54):
    print(f'  y={y}: ' + ' '.join(f'{tuple(a[y,x])}' for x in range(100, 161, 12)))
print('raw colors x=56..70 (step 2), y=44..60:')
for y in range(44, 61, 2):
    print(f'  y={y}: ' + ' '.join(f'{tuple(a[y,x])}' for x in range(56, 71, 2)))
print('callout bottom rows y=98..106, x=100..160:')
for y in range(98, 107):
    print(f'  y={y}: ' + ' '.join(f'{tuple(a[y,x])}' for x in range(100, 161, 12)))
