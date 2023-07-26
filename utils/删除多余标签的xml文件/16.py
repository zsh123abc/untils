import os
import xml.etree.ElementTree as ET

path = 'D:/zsh/biaozhu/3.1/xml'
for file in os.listdir(path):
    if file.endswith('.xml'):
        xml_path = os.path.join(path, file)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        if len(root.findall('object')) > 1:  # 超过一个标签
            os.remove(xml_path)  # 删除XML文件