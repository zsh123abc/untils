import os
import glob
import xml.etree.ElementTree as ET
import shutil
import xml.dom.minidom as minidom

# def format_object_elements(xml_file):
#     # 读取XML文件
#     tree = ET.parse(xml_file)
#     root = tree.getroot()

#     # 遍历所有的<object>元素
#     for obj_elem in root.findall('object'):
#         # 将<object>元素转换为字符串
#         obj_str = ET.tostring(obj_elem, encoding='utf-8').decode('utf-8')

#         # 使用minidom解析<object>字符串并重新格式化
#         dom = minidom.parseString(obj_str)
#         formatted_obj = dom.toprettyxml(indent='  ')

#         # 替换原始<object>元素内容为格式化后的内容
#         obj_elem.clear()
#         obj_elem.append(ET.fromstring(formatted_obj))

#     # 将整理后的XML保存到文件中
#     tree.write(xml_file, encoding='utf-8')


# 定义XML模板数据
template_xml_path = r"D:\zsh\7.7_court\part1\all_court\7.8_basket_all_img\test\VID_20230706_134317_0000.xml"

# 定义目标文件夹路径和保存路径
source_xml_folder = r"D:\zsh\7.7_court\part1\all_court\7.8_basket_all_img\test\xml"
output_xml_folder = r"D:\zsh\7.7_court\part1\all_court\7.8_basket_all_img\test\new_xml"

# 获取目标文件夹下所有XML文件的路径
xml_files = os.listdir(source_xml_folder)

# 遍历所有XML文件
for xml_file in xml_files:
    # 构建目标文件的路径
    source_xml_path = os.path.join(source_xml_folder, xml_file)
    output_xml_path = os.path.join(output_xml_folder, xml_file)

    # 解析目标文件
    tree = ET.parse(source_xml_path)
    root = tree.getroot()

    # 清空目标文件的标注信息
    root.findall("object")
    for obj in root.findall("object"):
        root.remove(obj)

    # 解析模板XML文件
    template_tree = ET.parse(template_xml_path)
    template_root = template_tree.getroot()

    # 复制模板数据的标注信息并添加到目标文件
    for template_object in template_root.findall("object"):
        obj = ET.Element("object")
        obj.append(ET.Element("name"))
        obj.find("name").text = template_object.find("name").text
        print(template_object.find("name").text)
        obj.append(ET.Element("bndbox"))
        bndbox = obj.find("bndbox")
        bndbox.append(ET.Element("xmin"))
        bndbox.append(ET.Element("ymin"))
        bndbox.append(ET.Element("xmax"))
        bndbox.append(ET.Element("ymax"))
        bndbox.find("xmin").text = template_object.find("bndbox").find("xmin").text
        bndbox.find("ymin").text = template_object.find("bndbox").find("ymin").text
        bndbox.find("xmax").text = template_object.find("bndbox").find("xmax").text
        bndbox.find("ymax").text = template_object.find("bndbox").find("ymax").text
        root.append(obj)

    # 保存修改后的XML文件到输出目录
    tree.write(output_xml_path)
    # format_object_elements(output_xml_path)


# 调用函数来格式化XML文件


    # 复制源文件夹中的其他文件到输出目录
    # source_file_path = os.path.join(source_xml_folder, os.path.splitext(os.path.basename(xml_file))[0] + ".*")
    # for source_file in glob.glob(source_file_path):
    #     output_file_path = os.path.join(output_xml_folder, os.path.basename(source_file))
    #     shutil.copy(source_file, output_file_path)

print("替换完成！")
