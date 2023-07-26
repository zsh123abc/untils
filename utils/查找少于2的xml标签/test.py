import os
import shutil
import xml.etree.ElementTree as ET

def count_xml_tags(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    tag = root.findall('object')
    return len(tag)

def move_files_with_few_tags(source_dir, destination_dir, new_img_path):
    for filename in os.listdir(source_dir):
        if filename.endswith('.xml'):
            xml_file_path = os.path.join(source_dir, filename)
            image_file_path = os.path.join(source_dir[:-3]+'img', os.path.splitext(filename)[0] + '.jpg')
            
            tag_count = count_xml_tags(xml_file_path)
            if tag_count < 3:
                shutil.move(xml_file_path, os.path.join(destination_dir, filename))
                if os.path.exists(image_file_path):
                    shutil.move(image_file_path, os.path.join(destination_dir, os.path.splitext(filename)[0] + '.jpg'))

# 设置源目录和目标目录
xml_path = r'D:\zsh\7.7_court\part1\all_court\7.8_basket_all_img\7.8_basket_all\xml'
new_xml_path = r'D:\zsh\7.7_court\part1\all_court\7.8_basket_all_img\7.8_basket_all\new_xml'
img_pth = r'D:\zsh\7.7_court\part1\all_court\7.8_basket_all_img\7.8_basket_all\img'
new_img_path = r'D:\zsh\7.7_court\part1\all_court\7.8_basket_all_img\7.8_basket_all\new_img'

# 调用函数移动文件
move_files_with_few_tags(xml_path, new_xml_path, new_img_path)
