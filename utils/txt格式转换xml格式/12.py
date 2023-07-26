import time
import os
from PIL import Image
import cv2
import numpy as np

'''人为构造xml文件的格式'''
out0 = '''<annotation>
    <folder>%(folder)s</folder>
    <filename>%(name)s</filename>
    <path>%(path)s</path>
    <source>
        <database>None</database>
    </source>
    <size>
        <width>%(width)d</width>
        <height>%(height)d</height>
        <depth>3</depth>
    </size>
    <segmented>0</segmented>
'''
out1 = '''    <object>
        <name>%(class)s</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%(xmin)d</xmin>
            <ymin>%(ymin)d</ymin>
            <xmax>%(xmax)d</xmax>
            <ymax>%(ymax)d</ymax>
        </bndbox>
    </object>
'''

out2 = '''</annotation>
'''

# 创建字典用来对类型进行转换
label_map = {0: 'F_field'}

'''txt转xml函数'''


def translate(image_dir, txt_dir, xml_dir):
    source = {}
    label = {}
    for jpg in os.listdir(image_dir):
        if jpg[-4:] == '.jpg':
            image_path = os.path.join(image_dir, jpg)
            image = cv2.imread(image_path)
            h, w, _ = image.shape

            xml_path = os.path.join(xml_dir, jpg.replace('.jpg', '.xml'))
            fxml = open(xml_path, 'w')
            imgfile = jpg.split('/')[-1]
            source['name'] = imgfile
            source['path'] = image_path
            source['folder'] = os.path.basename(image_dir)

            source['width'] = w
            source['height'] = h

            fxml.write(out0 % source)

            txt_path = os.path.join(txt_dir, jpg.replace('.jpg', '.txt'))
            lines = np.loadtxt(txt_path)

            for box in lines:
                if box.shape != (5,):
                    box = lines

                class_num = int(box[0])
                class_text = label_map[class_num]
                label['class'] = class_text

                xmin = float(box[1] - 0.5 * box[3]) * w
                ymin = float(box[2] - 0.5 * box[4]) * h
                xmax = float(xmin + box[3] * w)
                ymax = float(ymin + box[4] * h)

                label['xmin'] = xmin
                label['ymin'] = ymin
                label['xmax'] = xmax
                label['ymax'] = ymax

                fxml.write(out1 % label)
            fxml.write(out2)


if __name__ == '__main__':
    image_dir = r'C:\Users\cwj\Documents\WXWork\1688856502407527\Cache\Video\2023-07\7.3_court_img\7_3_court1\img'
    txt_dir = r'C:\Users\cwj\Documents\WXWork\1688856502407527\Cache\Video\2023-07\7.3_court_img\7_3_court1\out_txt'
    xml_dir = r'C:\Users\cwj\Documents\WXWork\1688856502407527\Cache\Video\2023-07\7.3_court_img\7_3_court1\xml'

    translate(image_dir, txt_dir, xml_dir)
    print('---------------Done!!!--------------')
