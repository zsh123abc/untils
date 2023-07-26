# 根据xml删除多余的图片
import os


img_dir = r'D:\zsh\biaozhu\4.25erfenxian\img2'
xml_dir = r'D:\zsh\biaozhu\4.25erfenxian\json'

xmls = []
for xml in os.listdir(xml_dir):

    xmls.append(xml.split('.xml')[0])

for image_name in os.listdir(img_dir):
    image_name = image_name.split('.jpg')[0]
    if image_name not in xmls:
        image_name = image_name + '.jpg'

        print(image_name)
        os.remove(os.path.join(img_dir, image_name))