import os
import shutil
import xml.etree.ElementTree as ET

def count_annotation_tags(xml_file):
    # 读取XML文件
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 获取标注信息标签数量
    annotation_tags = root.findall('object')
    return len(annotation_tags)

def move_files_with_less_tags(source_dir, destination_dir):
    # 确保目标目录存在
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # 遍历源目录中的文件
    for file_name in os.listdir(source_dir):
        if file_name.endswith('.xml'):
            file_path = os.path.join(source_dir, file_name)
            annotation_count = count_annotation_tags(file_path)
            
            # 判断标注信息标签数量是否小于三个
            if annotation_count < 3:
                # 移动文件到目标目录
                shutil.move(file_path, destination_dir)
                print(f"Moved {file_name} to {destination_dir}")

# 指定源目录和目标目录的路径
source_dir = r'D:\zsh\7.7_court\part1\all_court\7.8_basket_all_img\xml'
destination_dir = r'D:\zsh\7.7_court\part1\all_court\7.8_basket_all_img\new_xml'

# 调用函数进行移动操作
move_files_with_less_tags(source_dir, destination_dir)
