from PIL import Image
im = Image.open('unique_slides/slide_059.jpg')
crops = {
 "top_band":    (320, 40, 700, 140),
 "softmax_left":(80, 70, 340, 125),
 "pooled_fan":  (360, 110, 660, 190),
 "gap_box":     (160, 175, 900, 220),
 "output_left": (160, 215, 560, 270),
 "encoder":     (130, 265, 880, 385),
 "input_left":  (130, 380, 560, 515),
 "input_right": (560, 380, 910, 515),
 "left_labels": (70, 125, 185, 515),
 "badge":       (845, 45, 910, 100),
 "output_right":(560, 215, 910, 270),
}
for name, box in crops.items():
    c = im.crop(box)
    c = c.resize((c.width*2, c.height*2), Image.LANCZOS)
    c.save(f'scratch/slide059/crop_{name}.png')
    print(name, box, '->', c.size)
