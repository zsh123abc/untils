
from PIL import Image
import os
import xml.etree.ElementTree as ET

def flip_images_and_annotations_in_folder(input_folder, output_folder, annotation_folder, output_annotation_folder):

    image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    # 遍历每个图片文件
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        output_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + '_overturn' + os.path.splitext(image_file)[1])

        # 打开图片文件
        image = Image.open(image_path)

        # 左右翻转图片
        flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)

        # 保存翻转后的图片到输出文件夹中，保持原有格式和信息不变
        flipped_image.save(output_path, format=image.format)

        # 获取对应的标注数据xml文件
        annotation_file = os.path.splitext(image_file)[0] + '.xml'
        annotation_path = os.path.join(annotation_folder, annotation_file)
        output_annotation_path = os.path.join(output_annotation_folder, os.path.splitext(annotation_file)[0] + '_overturn' + os.path.splitext(annotation_file)[1])

        # 打开并解析xml文件
        tree = ET.parse(annotation_path)
        root = tree.getroot()

        # 翻转标注数据
        for object in root.findall('object'):
            bndbox = object.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            xmax = int(bndbox.find('xmax').text)
            bndbox.find('xmin').text = str(image.width - xmax)
            bndbox.find('xmax').text = str(image.width - xmin)

        # 保存翻转后的标注数据到输出文件夹中
        tree.write(output_annotation_path)

        print(f"翻转完成：{image_file}")

# 输入文件夹路径和输出文件夹路径
input_folder_path = r'D:\zsh\biaozhu\basketball_count\F_field\labelimg\voc\JPEGImages'
output_folder_path = r'D:\zsh\biaozhu\basketball_count\F_field\labelimg\voc\fz_JPEGImages'
annotation_folder_path = r'D:\zsh\biaozhu\basketball_count\F_field\labelimg\voc\Annotations'
output_annotation_folder_path = r'D:\zsh\biaozhu\basketball_count\F_field\labelimg\voc\fz_Annotations'

# 执行批量左右翻转图片和标注数据的函数
flip_images_and_annotations_in_folder(input_folder_path, output_folder_path, annotation_folder_path, output_annotation_folder_path)


