# 复制
import os
import shutil

path = r'D:\zsh\biaozhu\jianzi_kicking' # 存放图片文件夹的路径
jpg_path = r'D:\zsh\biaozhu\img'  # 图片复制后存放路径
if not os.path.exists(jpg_path):
    os.makedirs('images', jpg_path)  # 不存在就递归生成目录

for root, dirs, files in os.walk(path):
    for i in range(len(files)):
        if (files[i][-3:] == 'jpg'):  # 判断后缀是否是jpg
            file_path = root + '/' + files[i]  # 图片目录加上图片名字
            new_file_path = jpg_path + '/' + files[i]  # 新图片目录加上图片名字
            shutil.copy(file_path, new_file_path)
