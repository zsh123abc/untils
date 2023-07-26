import os
import shutil

#筛选出数据增强前后的图片

img_path = r'D:\篮球场1\梯形场地\增强前'
new_img_path = r'D:\篮球场1\梯形场地\增强后'

aug_orders = ['_Fliplr_','_Multiply_','_GaussianBlur_','_AddToHueAndSaturation_','_Affine_','_Mix_']
n=0
for img in os.listdir(img_path):
    for aug in aug_orders:
        if aug in img:
            new_img = img_path+'//'+img
            shutil.move(new_img,new_img_path)
print(n)