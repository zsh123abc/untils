import os
import xml.etree.ElementTree as ET
import shutil


def batch_remove_unwanted_labels(input_folder, output_folder):
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".xml"):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename)

            # 解析XML文件
            tree = ET.parse(input_file)
            root = tree.getroot()

            # 遍历所有的<object>元素
            for obj in root.findall('object'):
                name = obj.find('name').text

                # 如果标签不是"ball"或"Ball"，删除该<object>元素及其子元素
                if name == "ball":
                    
                    shutil.copy(input_file, output_file)
                    # root.remove(obj)

            # 将修改后的XML内容保存到输出文件夹下对应的文件中
            # tree.write(output_file)

# 使用示例
input_folder = r'D:\zsh\726\old_xml'  # 更改为你的输入文件夹路径
output_folder = r'D:\zsh\726\new_xml'  # 更改为你的输出文件夹路径
batch_remove_unwanted_labels(input_folder, output_folder)
