#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import cv2
import numpy as np
import os
import sys
import argparse
import matplotlib.pyplot as plt
from sys import platform
from scipy.optimize import curve_fit

from object_detect_basketball_court_paddle import ObjectDetectBasketballCourtPaddle


objDetector = ObjectDetectBasketballCourtPaddle(0.5)

def batch_cutout(court_img_dir_path, outout_dir_path):
    img_file_list = os.listdir(court_img_dir_path) # 获取目录下的所有场地图片文件
    n = 0
    for img_file in img_file_list: # 循环对每一个场地图片进行处理
        frame = os.path.join(court_img_dir_path, img_file)
        print(frame)
        objBoxes = objDetector.detect(frame, 0, 0)
        for i, box in enumerate(objBoxes):
            if box is None or len(box)==0:
                n+=1
                continue
            cls, conf, xmin, ymin, xmax, ymax = box
            cls = int(cls)
           
            if(cls == objDetector.CLASS_ID_F_COURT):
               image = cv2.imread(frame)
               x1 = int(xmin)
               y1 = int(ymin)
               x2 = int(xmax)
               y2 = int(ymax)
               sub_image = image[y1:y2, x1:x2]
               #sub_image = [int(xmin),int(ymin),int(xmax),int(ymax)]
                
               output_file = os.path.join(outout_dir_path, img_file)
               print(sub_image)
               cv2.imwrite(output_file, sub_image)
    print(n)


court_img_dir_path = "/data2/PaddleDetection2.6/datasets/normal_court"
output_dir_path = "/data2/PaddleDetection2.6/datasets/normal_court_kotu"
print('k')
batch_cutout(court_img_dir_path, output_dir_path)

