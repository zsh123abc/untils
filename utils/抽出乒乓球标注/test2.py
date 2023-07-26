import os
from lxml import etree as ET
import shutil
import concurrent.futures


def process_file(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    for obj in root.findall('object'):
        name = obj.find('name').text

        if name in ["Racket", "shuttle", "shuttlecock", "volant"]:
            shutil.copy(input_file, output_file)
            break

    # 将修改后的XML内容保存到输出文件夹下对应的文件中
    tree.write(output_file)


def batch_remove_unwanted_labels(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for filename in os.listdir(input_folder):
            if filename.endswith(".xml"):
                input_file = os.path.join(input_folder, filename)
                output_file = os.path.join(output_folder, filename)
                executor.submit(process_file, input_file, output_file)


# 使用示例
input_folder = r'D:\zsh\biaozhu\bilibli\download\table_tennis\badminton\bo\xml'  # 更改为你的输入文件夹路径
output_folder = r'D:\zsh\biaozhu\bilibli\download\table_tennis\badminton\bo\new_xml'  # 更改为你的输出文件夹路径
batch_remove_unwanted_labels(input_folder, output_folder)
