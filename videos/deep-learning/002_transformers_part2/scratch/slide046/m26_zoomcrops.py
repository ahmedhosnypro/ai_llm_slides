from PIL import Image
im = Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')
# rightmost two columns' label zones: col7 cx=760.3, col8 cx=834.4 ; rows: final(65-81), postLN(278-295), X(487-503)
crops = {
 'zoom_xrow_col7_col8.png': (735, 485, 860, 505),
 'zoom_final_col7_col8.png': (735, 63, 860, 83),
 'zoom_xrow_col1_col2.png': (180, 485, 305, 505),
}
for name, box in crops.items():
    c = im.crop(box)
    c = c.resize((c.width*6, c.height*6), Image.LANCZOS)
    c.save(f'videos/deep-learning/002_transformers_part2/scratch/slide046/{name}')
    print(name, c.size)
