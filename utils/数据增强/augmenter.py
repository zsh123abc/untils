#增强数据
import xml.etree.ElementTree as ET
import pickle
import os
from os import getcwd
import numpy as np
from PIL import Image
import glob

import imgaug as ia
from imgaug import augmenters as iaa

ia.seed(1)

def read_xml_annotation(root, image_id):
    in_file = open(os.path.join(root, image_id), encoding='UTF-8')
    tree = ET.parse(in_file)
    root = tree.getroot()
    bndboxlist = []

    for object in root.findall('object'):  # 找到root节点下的所有country节点
        bndbox = object.find('bndbox')  # 子节点下节点rank的值

        xmin = int(bndbox.find('xmin').text)
        xmax = int(bndbox.find('xmax').text)
        ymin = int(bndbox.find('ymin').text)
        ymax = int(bndbox.find('ymax').text)
        # print(xmin,ymin,xmax,ymax)
        bndboxlist.append([xmin,ymin,xmax,ymax])
        # print(bndboxlist)

    #bndbox = root.find('object').find('bndbox')
    return bndboxlist
# (506.0000, 330.0000, 528.0000, 348.0000) -> (520.4747, 381.5080, 540.5596, 398.6603)
def change_xml_annotation(root, image_id, new_target):
    new_xmin = new_target[0]
    new_ymin = new_target[1]
    new_xmax = new_target[2]
    new_ymax = new_target[3]

    in_file = open(os.path.join(root, str(image_id) + '.xml'))  # 这里root分别由两个意思
    tree = ET.parse(in_file)
    xmlroot = tree.getroot()
    object = xmlroot.find('object')
    bndbox = object.find('bndbox')
    xmin = bndbox.find('xmin')
    xmin.text = str(new_xmin)
    ymin = bndbox.find('ymin')
    ymin.text = str(new_ymin)
    xmax = bndbox.find('xmax')
    xmax.text = str(new_xmax)
    ymax = bndbox.find('ymax')
    ymax.text = str(new_ymax)
    tree.write(os.path.join(root, str(image_id) + "_aug" + '.xml'))

def change_xml_list_annotation(root, image_id, new_target, saveroot, aug_name, id):

    in_file = open(os.path.join(root, str(image_id) + '.xml'), encoding='UTF-8')  # 这里root分别由两个意思
    tree = ET.parse(in_file)
    xmlroot = tree.getroot()
    index = 0

    for object in xmlroot.findall('object'):  # 找到root节点下的所有country节点
        bndbox = object.find('bndbox')  # 子节点下节点rank的值

        # xmin = int(bndbox.find('xmin').text)
        # xmax = int(bndbox.find('xmax').text)
        # ymin = int(bndbox.find('ymin').text)
        # ymax = int(bndbox.find('ymax').text)

        new_xmin = new_target[index][0]
        new_ymin = new_target[index][1]
        new_xmax = new_target[index][2]
        new_ymax = new_target[index][3]

        xmin = bndbox.find('xmin')
        xmin.text = str(new_xmin)
        ymin = bndbox.find('ymin')
        ymin.text = str(new_ymin)
        xmax = bndbox.find('xmax')
        xmax.text = str(new_xmax)
        ymax = bndbox.find('ymax')
        ymax.text = str(new_ymax)

        index = index + 1

    tree.write(os.path.join(saveroot, str(image_id) + aug_name + str(id) + '.xml'))


if __name__ == "__main__":

    category = '6.13_court_voc'
    IMG_DIR = "./dataset/{}/old_images".format(category)      #图片文件夹路径
    XML_DIR = "./dataset/{}/old_xml".format(category)     #xml文件夹路径

    AUG_IMG_DIR = "./dataset/{}/old_images_aug".format(category)  # 存储增强后的影像文件夹路径
    AUG_XML_DIR = "./dataset/{}/old_xml_aug".format(category)  # 存储增强后的XML文件夹路径

    os.makedirs(AUG_IMG_DIR, exist_ok=True)
    os.makedirs(AUG_XML_DIR, exist_ok=True)

    boxes_img_aug_list = []
    new_bndbox = []
    new_bndbox_list = []

    # 增强方式
    aug_seq = [
        iaa.Flipud(1),  # 翻转：上下对称
        iaa.Fliplr(1),  # 镜像: 左右对称
        iaa.Multiply((0.8, 1.2)),  # 改变亮度
        iaa.GaussianBlur(sigma=(1, 3)),  # 模糊
        iaa.AddToHueAndSaturation((-15, 15)),  # 改变色调和饱和度
        iaa.Affine(
            translate_px={"x": (-10, 10), "y": (-10, 10)},  # 平移
            scale=(0.3, 0.7),  # 缩放
            # rotate=(-10, 10)  # 旋转
        )
    ]
    # 增强方式组合，{'增强名字': {增强次数: [增强组合]}}
    aug_orders = {
#         '_Flipud_': {1: [0]},
                  '_Fliplr_': {1: [1]},
                   '_Multiply_': {1: [2]},
#                   '_GaussianBlur_': {1: [3]},
                   '_AddToHueAndSaturation_': {1: [4]},
                 #'_Affine_': {1: [5]},
                   '_Mix_': {1: [1, 2, 4]}}
    # 增强
    for aug_name, aug_order in aug_orders.items():
        AUGLOOP = list(aug_order.items())[0][0]  # 每张影像增强的数量
        aug_seq_tmp = [aug_seq[j] for j in list(aug_order.items())[0][1]]
        print(aug_name)

        seq = iaa.Sequential(aug_seq_tmp)

        for root, sub_folders, files in os.walk(XML_DIR):

            for name in files:

                bndbox = read_xml_annotation(XML_DIR, name)

                for epoch in range(AUGLOOP):
                    seq_det = seq.to_deterministic()  # 保持坐标和图像同步改变，而不是随机

                    image_path = glob.glob(os.path.join(IMG_DIR,name[:-4]+'.???'))[0]
                    suffix = image_path[-4:]
                    # 读取图片
                    img = Image.open(image_path)
                    print(image_path)
                    img = np.array(img)

                    # bndbox 坐标增强
                    for i in range(len(bndbox)):
                        bbs = ia.BoundingBoxesOnImage([
                            ia.BoundingBox(x1=bndbox[i][0], y1=bndbox[i][1], x2=bndbox[i][2], y2=bndbox[i][3]),
                        ], shape=img.shape)

                        bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]
                        boxes_img_aug_list.append(bbs_aug)

                        # new_bndbox_list:[[x1,y1,x2,y2],...[],[]]
                        new_bndbox_list.append([int(bbs_aug.bounding_boxes[0].x1),
                                                int(bbs_aug.bounding_boxes[0].y1),
                                                int(bbs_aug.bounding_boxes[0].x2),
                                                int(bbs_aug.bounding_boxes[0].y2)])
                    # 存储变化后的图片
                    image_aug = seq_det.augment_images([img])[0]
                    path = os.path.join(AUG_IMG_DIR, str(name[:-4]) + aug_name + str(epoch) + suffix)
                    # image_auged = bbs.draw_on_image(image_aug, thickness=0)
                    Image.fromarray(image_aug).save(path)

                    # 存储变化后的XML
                    change_xml_list_annotation(XML_DIR, name[:-4], new_bndbox_list, AUG_XML_DIR, aug_name, epoch)
                    print(str(name[:-4]) + aug_name + str(epoch) + suffix)
                    new_bndbox_list = []
