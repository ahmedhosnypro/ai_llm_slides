#!/usr/bin/env python3
"""m4_crops.py — zoom crops (z_*.png) of slide_048.jpg, nearest-neighbor upscales.
All crops banked in this dir. Crop rect = (x0, y0, x1, y1) inclusive, frame px."""
from PIL import Image

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_048.jpg'
im = Image.open(F).convert('RGB')

CROPS = [
    # name, (x0, y0, x1, y1) inclusive, upscale
    ('z_badge48',          (846, 42, 908, 96), 24),   # MAX-RES badge crop (occluded disc)
    ('z_badge48_wide',     (820, 40, 920, 110), 10),  # badge + inset corner context
    ('z_title48',          (78, 88, 128, 440), 6),    # vertical red title
    ('z_tag_out48',        (48, 40, 195, 84), 8),     # Block Output tag
    ('z_tag_in48',         (48, 474, 195, 522), 8),   # Block Input tag (+thumb edge)
    ('z_layer_top48',      (120, 82, 620, 200), 3),   # Y row + LayerNorm1 + plus row1
    ('z_layer_top48b',     (120, 82, 920, 200), 2),   # same, wider (incl. dots+badge zone)
    ('z_ffn_label48',      (120, 198, 620, 236), 4),  # Feed Forward Networks label
    ('z_mlp_row48',        (120, 228, 620, 272), 4),  # MLP boxes + captions
    ('z_layer_mid48',      (120, 268, 620, 420), 3),  # Y row + plus row2 + LayerNorm2
    ('z_layer_mid48b',     (120, 268, 920, 420), 2),
    ('z_mhsa48',           (120, 410, 620, 478), 3),  # maroon bar
    ('z_tokens_x48',       (120, 486, 920, 522), 3),  # bottom X token row + green dots
    ('z_tokens_y48',       (120, 48, 920, 84), 3),    # top Y token row + blue dots
    ('z_thumb48',          (40, 400, 175, 500), 8),   # thumbnail inset
    ('z_inset_top48',      (600, 60, 910, 260), 3),   # inset upper (Add&Norm, FF)
    ('z_inset_bot48',      (600, 300, 910, 500), 3),  # inset lower (Add&Norm, MHA, VKQ)
    ('z_blackband48',      (0, 495, 960, 540), 3),    # bottom black band
]

for name, (x0, y0, x1, y1), up in CROPS:
    c = im.crop((x0, y0, x1 + 1, y1 + 1))
    c = c.resize((c.width * up, c.height * up), Image.NEAREST)
    c.save(f'/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide048/{name}.png')
    print(name, 'rect', (x0, y0, x1, y1), 'x' + str(up), '->', c.size)
print('done')
