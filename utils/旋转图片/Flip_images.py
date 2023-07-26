from PIL import Image
import os, shutil
xz = int('3')
def circle(srcPath, dstPath):
    for filename in os.listdir(srcPath):
        # 如果不存在目的目录则创建一个，保持层级结构
        if not os.path.exists(dstPath):
            os.makedirs(dstPath)

        # 拼接完整的文件或文件夹路径
        srcFile = os.path.join(srcPath, filename)
        dstFile = os.path.join(dstPath, filename)

        # 如果是文件就处理
        if os.path.isfile(srcFile):
            try:
                sImg = Image.open(srcFile)
                if xz == 1:
                    ss = sImg.transpose(Image.FLIP_LEFT_RIGHT)
                elif xz == 2:
                    ss = sImg.transpose(Image.FLIP_TOP_BOTTOM)   # 图像上下镜像
                elif xz == 3:
                    ss = sImg.transpose(Image.ROTATE_90)      # 图像逆时针旋转90°
                elif xz == 4:
                    ss = sImg.transpose(Image.ROTATE_180)     # 图像逆时针旋转180°
                elif xz == 5:
                    ss = sImg.transpose(Image.ROTATE_270)     # 图像逆时针旋转240°
                elif xz == 6:
                    ss = sImg.transpose(Image.TRANSPOSE)      # 图像顺时针旋转90°


                ss.save(dstFile)
                print(dstFile + " 转换成功！")
            except Exception:
                print(dstFile + "失败！")
        if os.path.isdir(srcFile):
            circle(srcFile, dstFile)


if __name__ == '__main__':
    # 遍历待加入图片
    dirss = (r'C:\Users\cwj\Documents\WXWork\1688856502407527\Cache\Video\2023-07\7.3_court_video\7_3_court2') # 图片路径
    dirss2 = (r'C:\Users\cwj\Documents\WXWork\1688856502407527\Cache\Video\2023-07\7.3_court_video\7_3_court2') # 图片反转后存放路径
    circle(dirss, dirss2)#翻转两次
    circle(dirss, dirss2)
    # circle(dirss, dirss2)
