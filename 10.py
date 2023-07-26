#根据图片删除多余的xml
import os


img_dir = r'C:\Users\cwj\Documents\WXWork\1688856502407527\Cache\File\2023-05\zsh_labels\images'
xml_dir = r'C:\Users\cwj\Documents\WXWork\1688856502407527\Cache\File\2023-05\zsh_labels\info'


allusedxmls = []
file_imgs = os.listdir(img_dir)
file_xmls = os.listdir(xml_dir)
for file_name in file_imgs:

    file_name = file_name[:-4] + '_0.xml'#删图片改.jpg或删xml改.xml
    # print(file_name)
    allusedxmls.append(file_name)

for file_name in file_xmls:
    print(file_name)
    if file_name not in allusedxmls:
        path = xml_dir +'/'+ file_name
        os.remove(path)