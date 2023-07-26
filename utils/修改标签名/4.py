"""
使用python xml解析树解析xml文件，批量修改xml文件里object节点下name节点的text
"""
import glob
import xml.etree.ElementTree as ET
path = r'D:\zsh\biaozhu\bilibli\download\table_tennis\badminton\bo\new_xml'    # xml文件夹路径
i = 0
for xml_file in glob.glob(path + '/*.xml'):
    # print(xml_file)
    tree = ET.parse(xml_file)
    obj_list = tree.getroot().findall('object')
    for per_obj in obj_list:
        pre = per_obj[1]
        if per_obj[0].text == 'volant':    # 错误的标签“33”
            per_obj[0].text = 'shuttle'    # 修改成“44”
            i = i+1

    tree.write(xml_file)
print('共完成了{}处替换'.format(i))
