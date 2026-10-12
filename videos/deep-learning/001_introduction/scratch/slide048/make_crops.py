from PIL import Image
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')
A = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets'
# 1. meme photo (NN row): x247..361, y189..254  -> crop box (l,t,r,b) exclusive right/bottom
meme = im.crop((247,189,361,254)); meme.save(f'{A}/s048_meme.png'); print('s048_meme', meme.size)
# 2. siamese parallelogram photo (CNN row): x123..228, y313..431
sia = im.crop((123,313,228,431)); sia.save(f'{A}/s048_siamese.png'); print('s048_siamese', sia.size)
# 3. CNN slab chain incl Conv labels, gap arrows, NL labels: x228..693, y312..440
chain = im.crop((228,312,693,440)); chain.save(f'{A}/s048_cnn_chain.png'); print('s048_cnn_chain', chain.size)
# 4. combined dense crop for vision build-input: x235..430, y150..250, x2
dense = im.crop((235,150,430,250))
dense = dense.resize((dense.width*2, dense.height*2), Image.LANCZOS)
dense.save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide048/dense_crop_2x.png')
print('dense', dense.size)
