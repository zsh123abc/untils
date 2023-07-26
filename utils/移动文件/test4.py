# 移动一半文件到另外的文件夹中
import os
import shutil
import threading
import time

def move_file(img_path,new_img_path):
    con = 0
    for path in os.listdir(img_path):
        if con%2==0:
            file_path = img_path + '/' + path # 图片目录加上图片名字
            new_file_path = new_img_path + '/' + path  # 新图片目录加上图片名字
            shutil.move(file_path, new_file_path)
        con+=1

if __name__ == "__main__":
    img_path = r'D:\zsh\biaozhu\3.28toulan_5tag\images'  # 存放图片文件夹的路径
    new_img_path = r'D:\zsh\biaozhu\3.28toulan_5tag\images2'  # 图片复制后存放路径

    xml_path = r'D:\zsh\biaozhu\3.28toulan_5tag\xml'
    new_xml_path = r'D:\zsh\biaozhu\3.28toulan_5tag\xml2'
    start = time.time()
    t1 = threading.Thread(target=move_file, args=(img_path,new_img_path))
    t2 = threading.Thread(target=move_file, args=(xml_path,new_xml_path))
    t1.start()
    t2.start()
    end = time.time()

    print('运行耗时：{}'.format(end-start))