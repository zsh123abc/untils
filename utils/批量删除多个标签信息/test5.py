import os
import xml.etree.ElementTree as ET

def remove_keypoints(xml_file, to_delete):
    # 加载XML文件
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 查找需要删除的关键点
    for keypoint in root.findall("./keypoints/keypoint"):
        if keypoint.get('name') in to_delete:
            root.find("./keypoints").remove(keypoint)

    # 保存修改后的XML文件
    tree.write(xml_file)

# 遍历整个目录，对所有XML文件进行批量处理
root_dir = r'D:\zsh\biaozhu\3\info'
to_delete = {'R_Knee', 'L_Knee', 'L_Ankle', 'R_Ankle'}

for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.xml'):
            xml_path = os.path.join(subdir, file)
            remove_keypoints(xml_path, to_delete)