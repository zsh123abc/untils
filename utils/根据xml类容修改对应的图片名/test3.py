import os
import xml.etree.ElementTree as ET

# 根据xml filename修改对应图片名和xml一致，并修改filename值
# 指定存放 XML 文件的目录路径
xml_dir = r"D:\zsh\7_5_paddle\data\train\xml"
image_folder = r"D:\zsh\7_5_paddle\data\train\img"
image_extension = ".jpg"

for xml_name in os.listdir(xml_dir):
    if xml_name.endswith(".xml"):
        # 指定 XML 文件路径
        xml_file = os.path.join(xml_dir, xml_name)

        # 解析 XML 文件
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # 获取 <filename> 元素的值
        filename_element = root.find("filename")
        filename_value = filename_element.text

        # 构建原始图片路径和目标图片路径
        original_image_path = os.path.join(image_folder, filename_value)
        new_img_name = xml_name[:-4]
        new_image_path = os.path.join(image_folder, new_img_name + image_extension)

        # 修改图片名
        try:
            os.rename(original_image_path, new_image_path)
        except:
            continue

        # 修改 XML 文件中的 <filename> 元素值为新的图片名
        filename_element.text = new_img_name + image_extension

        # 保存修改后的 XML 文件
        tree.write(xml_file)

print("完成图片名和 XML 文件的修改。")
