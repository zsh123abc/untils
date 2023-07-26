from PIL import Image
import numpy as np
import cv2
import os

# 定义文件夹路径和输出路径
folder_path = r'D:\zsh\biaozhu\4.20_jd_basetball\images'
output_path = r'D:\zsh\biaozhu\4.20_jd_basetball\img'

# 遍历文件夹中的所有图片
for filename in os.listdir(folder_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # 读取图片并转换为BGR格式
        img_path = os.path.join(folder_path, filename)
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # 进行背景分割
        mask = np.zeros(img.shape[:2], np.uint8)
        bgdModel = np.zeros((1,65),np.float64)
        fgdModel = np.zeros((1,65),np.float64)
        rect = (50,50,img.shape[1]-50,img.shape[0]-50)
        cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

        # 创建前景掩码
        mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')

        # 将前景与背景融合
        res = img*mask2[:,:,np.newaxis]
        res[np.where((res == [0, 0, 0]).all(axis=2))] = [255, 255, 255]
        # 保存结果
        output_name = os.path.join(output_path, filename)
        Image.fromarray(res).save(output_name)