from PIL import Image
NS = '/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure'
im = Image.open(NS + '/unique_slides/slide_010.jpg').convert('RGB')
im.crop((60, 255, 660, 385)).resize((1800, 390), Image.Resampling.LANCZOS).save('/tmp/s10_formula_crop.png')
im.crop((530, 285, 900, 515)).resize((1110, 690), Image.Resampling.LANCZOS).save('/tmp/s10_tree_crop.png')
im.crop((660, 40, 900, 300)).resize((960, 1040), Image.Resampling.LANCZOS).save('/tmp/s10_matrix_crop.png')
print('saved')
