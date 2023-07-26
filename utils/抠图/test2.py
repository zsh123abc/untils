import os, paddlehub as hub
from PIL import Image

huseg = hub.Module(name='deeplabv3p_xception65_humanseg') 

path = 'images/' 

files = [path + i for i in os.listdir(path)]

print(files)

results = huseg.segmentation(data={'image': files}) 

for i, result in enumerate(results):
    img = Image.open(files[i])
    img = img.convert('RGBA')
    label = result['label_map']
    label = Image.fromarray(label, mode='P')
    label = label.resize(img.size, resample=Image.NEAREST)
    mask = label.convert('L')
    img.putalpha(mask)
    img.save(f"segmented_{i}.png")