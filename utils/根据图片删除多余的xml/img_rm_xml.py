import os


img_dir = r'D:\zsh\biaozhu\small_ball\ping-pang\7.18_ping-pang\7.20_ping-pang_xml'
xml_dir = r'D:\zsh\biaozhu\small_ball\ping-pang\7.18_ping-pang\img'


allusedxmls = []
file_imgs = os.listdir(img_dir)
file_xmls = os.listdir(xml_dir)
for file_name in file_imgs:

    file_name = file_name[:-4] + '.jpg'
    # print(file_name)
    allusedxmls.append(file_name)

for file_name in file_xmls:
    print(file_name)
    # if file_name not in allusedxmls:
    if file_name not in allusedxmls:
        path = xml_dir +'/'+ file_name
        os.remove(path) 