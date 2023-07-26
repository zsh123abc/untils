import os
import glob

# 编写__init__.py 文件，把Tools设计成可导入的包
# import t.Flip_images
# path = ''
# t.Flip_images(path,path)

import utils

def getSeason(season):
    season = int(season)

    if season == 1:
        path = ''
        utils.view_tags(path)

    elif season == 2:
        path = input('翻转图片路径：')
        utils.Flip_images.circle(path,path)

    elif season == 3:
        video_path = input('视频路径：')
        img_path = input('抽帧图片存放路径：')
        utils.cap.cap_img(video_path,img_path)

    elif season == 4:
        path = input('图片路径：')
        jpg_path = input('图片复制路径：')
        utils.paste.test(path,jpg_path)

    elif season == 5:
        path = input('路径：')
        utils.t4.test(path)
    


if __name__ == '__main__':
    season = input('1,2,3,4,5 :')
    getSeason(season)