#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import cv2
import os
import numpy as np
import xml.etree.ElementTree as ET
import xml.dom.minidom
# from shapely.geometry import Polygon


# In[ ]:


def decodeVocAnnotation(voc_xml_path,ord_img_path):
    """
    voc数据集格式的文件解析，将一个文件解析成一个字符串，
    字符串的格式是:x1,y1,x2,y2,class x1,y1,x2,y2,class ...
    使用空格间隔不同对象
    注意:返回的类别不是整型，而是字符串的类别名称
    注意判断返回值是否为 空，如果是空说明没有目标，是一张背景图
    :param voc_xml_path:
    :return:
    """
    assert voc_xml_path.endswith(".xml"), "voc_xml_path must endswith .xml" # 确定文件是否是xml格式

    xml_file = open(voc_xml_path, 'r', encoding='utf-8') # 打开文件
    # 打开xml文件，并返回根节点
    root = ET.ElementTree().parse(xml_file) # 读取根节点

    # 定义一个列表，专门保存目标
    information = []
    # 定义一个列表，用来存放当前图片的所有标签
    tag_list = []
    # 个别xml文件没有path和filename
    if root.find('path') is None:
        filepath = os.path.splitext(ord_img_path)[0]+'.jpg'
    else:    
        filepath = root.find('path').text # 读取root节点的子节点path的值

    filename = root.find('filename').text # 读取root节点的子节点filename的值 

    width = 0
    height = 0
    for size_item in root.iter('size'):
        width = int(size_item.find('width').text)
        height = int(size_item.find('height').text)

    # 查找root节点下所有目标信息
    for obj in root.iter('object'):
        # 目标的名称
        name = obj.find('name').text
        # 目标的bbox坐标，一般voc是保存的corner格式的bbox
        box = obj.find('bndbox')
        xmin = int(box.find('xmin').text)
        ymin = int(box.find('ymin').text)
        xmax = int(box.find('xmax').text)
        ymax = int(box.find('ymax').text)

        tag_list.append(name)
        # 添加一个目标的信息
        information.append({"rect": [xmin,ymin,xmax,ymax],"tag": name, "path": filepath, "filename": filename, "width":width, "height": height})

    xml_file.close() # 关闭文件
    return  [information,tag_list]


# In[ ]:


def writeVocAnnotation(folder: str, img_name: str, path: str, img_width: int, img_height: int, labels: list):
    #tag_num: int, tag_name: str, box_list:list
    '''
    VOC标注xml文件生成函数
    :param folder: 文件夹名
    :param img_name:
    :param path:
    :param img_width:
    :param img_height:
    :param tag_num: 图片内的标注框数量
    :param tag_name: 标注名称
    :param box_list: 标注坐标,其数据格式为[[xmin1, ymin1, xmax1, ymax1],[xmin2, ymin2, xmax2, ymax2]....]
    :return: a standard VOC format .xml file, named "img_name.xml"
    '''
    # 创建dom树对象
    doc = xml.dom.minidom.Document()
 
    # 创建root结点annotation，并用dom对象添加根结点
    root_node = doc.createElement("annotation")
    doc.appendChild(root_node)
 
    # 创建结点并加入到根结点
    folder_node = doc.createElement("folder")
    folder_value = doc.createTextNode(folder)
    folder_node.appendChild(folder_value)
    root_node.appendChild(folder_node)
 
    filename_node = doc.createElement("filename")
    filename_value = doc.createTextNode(img_name)
    filename_node.appendChild(filename_value)
    root_node.appendChild(filename_node)
 
    path_node = doc.createElement("path")
    path_value = doc.createTextNode(path)
    path_node.appendChild(path_value)
    root_node.appendChild(path_node)
 
    source_node = doc.createElement("source")
    database_node = doc.createElement("database")
    database_node.appendChild(doc.createTextNode("Unknown"))
    source_node.appendChild(database_node)
    root_node.appendChild(source_node)
 
    size_node = doc.createElement("size")
    for item, value in zip(["width", "height", "depth"], [img_width, img_height, 3]):
        elem = doc.createElement(item)
        elem.appendChild(doc.createTextNode(str(value)))
        size_node.appendChild(elem)
    root_node.appendChild(size_node)
 
    seg_node = doc.createElement("segmented")
    seg_node.appendChild(doc.createTextNode(str(0)))
    root_node.appendChild(seg_node)
 
    for label in labels:
        tag_name = label["tag"]
        bndbox = label["rect"]

        obj_node = doc.createElement("object")
        name_node = doc.createElement("name")
        name_node.appendChild(doc.createTextNode(tag_name))
        obj_node.appendChild(name_node)
 
        pose_node = doc.createElement("pose")
        pose_node.appendChild(doc.createTextNode("Unspecified"))
        obj_node.appendChild(pose_node)
 
        trun_node = doc.createElement("truncated")
        trun_node.appendChild(doc.createTextNode(str(0)))
        obj_node.appendChild(trun_node)
 
        trun_node = doc.createElement("difficult")
        trun_node.appendChild(doc.createTextNode(str(0)))
        obj_node.appendChild(trun_node)
 
        bndbox_node = doc.createElement("bndbox")
        for item, value in zip(["xmin", "ymin", "xmax", "ymax"], bndbox):
            elem = doc.createElement(item)
            elem.appendChild(doc.createTextNode(str(value)))
            bndbox_node.appendChild(elem)
        obj_node.appendChild(bndbox_node)
        root_node.appendChild(obj_node)
    
    xml_name = img_name[:-4]
    xml_path = os.path.join(folder, xml_name + ".xml")

    xml_path = xml_path.replace('\\','/')
    # output_filename = os.path.join(xml_path, urllib.quote(html, safe='+/'))

    
    with open(xml_path, "w", encoding="utf-8") as f:
        # writexml()第一个参数是目标文件对象，第二个参数是根节点的缩进格式，第三个参数是其他子节点的缩进格式，
        # 第四个参数制定了换行格式，第五个参数制定了xml内容的编码。
        
        doc.writexml(f, indent='', addindent='\t', newl='\n', encoding="utf-8")


# In[ ]:


def rect_intersection(a,b):
    poly_a = Polygon.from_bounds(a[0], a[1], a[2], a[3])
    ploy_b = Polygon.from_bounds(b[0], b[1], b[2], b[3])
    intersection = poly_a.intersection(ploy_b)
    if intersection.is_empty:
        return ()
    else:
        return intersection.bounds


def rect_is_inner(outer, inner):
    if outer[0]<=inner[0] and outer[1]<=inner[1] and outer[2]>=inner[2] and outer[3]>=inner[3]:
        return True
    return False

def rect_union(a,b):
    union = [0, 0, 0, 0]
    union[0] = min(a[0], b[0])
    union[1] = min(a[1], b[1])
    union[2] = max(a[2], b[2])
    union[3] = max(a[3], b[3])
    return union


# In[ ]:

def fetch_a_group_label(images_path, filename, new_annos_path, new_images_path, sub_img_rect, new_labels):
    image_path = os.path.join(images_path, filename) #需要赋值
    print("image path:", image_path)
    image = cv2.imread(image_path)
    if image is None:
        return
    x1,y1, x2,y2 = sub_img_rect
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)

    height, width, _ = image.shape
    #width = sp[1]#width(colums) of image

    #抠图超出边界
    if x1<0:
        x1 = 0
    if y1<0:
        y1 = 0

    if x2>=width:
        x2 = width-1
    if y2>=height:
        y2 = height-1
    
    sub_img_width = int(x2-x1)
    sub_img_height = int(y2-y1)
    #抠图
    sub_image = image[y1:y2, x1:x2]
    #保存扣出来的图
    img_filename = filename
    new_img_path = os.path.join(new_images_path, img_filename)
    
    if sub_image is None or sub_image.size==0:
        print("sub image is empty:", img_filename)
        return
    print([y1,y2, x1,x2])
    cv2.imwrite(new_img_path, sub_image)
    #保存标注文件
    sub_img_height, sub_img_width, sub_img_channels = sub_image.shape
    '''
    VOC标注xml文件生成函数
    :param folder: 文件夹名
    :param img_name: xml文件名
    :param path: 文件路径
    :param img_width:
    :param img_height:
    :param tag_num: 图片内的标注框数量
    :param tag_name: 标注名称
    :param box_list: 标注坐标,其数据格式为[[xmin1, ymin1, xmax1, ymax1],[xmin2, ymin2, xmax2, ymax2]....]
    :return: a standard VOC format .xml file, named "img_name.xml"
    '''
    #                   folder        , img_name  , path: , img_width:, img_height:, tag_num:    ,tag_name, box_list:list
    writeVocAnnotation(new_annos_path, filename, new_img_path, sub_img_width, sub_img_height, new_labels)
    # writeVocAnnotation(new_annos_path, anno_file, filepath, filename, sub_img_width, sub_img_height, 1, new_label, [union_rect])


def distance(x, y):
    return ((y[0] - x[0]) ** 2 + (y[1] - x[1]) ** 2) ** (1/2)

def getBoxCenterCoord( box):
    xmin, ymin, xmax, ymax = box
    xCoord = int(np.mean([xmin, xmax]))
    yCoord = int(np.mean([ymin, ymax]))
    return (xCoord, yCoord)

def new_img_xml(annos_path,images_path,new_annos_path,new_images_path):

    con=0
    con2=0
    con3=0

    xml_list = os.listdir(annos_path) # 获取目录下的所有xml文件名
    for anno_file in xml_list: # 循环对每一个xml进行处理
        '''
        获取四个标注信息的数据集
        rect：在图片中的坐标，tag：标签名，path：文件路径，filename：文件名
        basketball_frame
        basket_net
        basketball
        backboard
        '''
        print(os.path.join(annos_path, anno_file))
        data = decodeVocAnnotation(os.path.join(annos_path, anno_file),os.path.join(images_path, anno_file))

        # 有一部分图片没有篮筐或者篮球
        lab = data[0] # 所有数据
        tag = data[1] # 当前图片所有标签列表
        
        if len(tag)==0:
            print('图片没有标注:{}'.format(images_path))
            con3+=1

        #elif ("basketball_frame" not in tag): # or ("basketball" not in tag):
        elif ("backboard" not in tag): # or ("basketball" not in tag):
            print('图片没有筐或网:{}'.format(lab[0]['filename']))
            con2+=1

        
        filepath = annos_path
        filename = anno_file

        sub_img_rect = []
        sub_img_width = 0
        sub_img_height = 0
        new_labels = []
        board_rect_list = []
        for i in range(0, len(lab)):
            board_label = lab[i]
            print(board_label)
            filename = board_label["filename"]
            img_width = board_label["width"]
            img_height = board_label["height"]
            print("tag:", board_label["tag"])
            if board_label["tag"] == "basketball":
                board_rect = board_label["rect"]
                fx1, fy1, fx2, fy2 = board_rect
                board_width = fx2-fx1
                board_heigh = fy2-fy1
                #扩大篮圈的范围
                sub_img_rect = [fx1-board_width/4, fy1-board_width/4, fx2+board_width/4, fy2+board_width/4]
                # sub_img_rect = [fx1+10,fy1+10,fx2+10,fy2+10]
                if sub_img_rect[0] < 0:
                    sub_img_rect[0] = 0
                if sub_img_rect[1] < 0:
                    sub_img_rect[1] = 0
                if sub_img_rect[2] > img_width:
                    sub_img_rect[2] = int(img_width - 1)
                if sub_img_rect[3] > img_height:
                    sub_img_rect[3] = int(img_height - 1)
                board_rect_list.append(sub_img_rect)

        if len(sub_img_rect) == 0:
            continue
        for sub_img_rect in board_rect_list:
            print(" go here sub_img_rect:", sub_img_rect)
            x1, y1, x2, y2 = sub_img_rect
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)
            sub_img_rect = [x1, y1, x2, y2]
            has_ball = False
            new_labels = []
            label1 = lab[0]
            l_filename = label1["filename"]
            l_filepath = label1["path"]
            label = dict(rect=[0, 0, x2-x1-1, y2-y1-1], width=x2-x1, height=y2-y1, tag="fail", path=l_filepath, filename=l_filename)
            new_labels.append(label)
            #if has_ball:
            fetch_a_group_label(images_path, filename, new_annos_path, new_images_path, sub_img_rect, new_labels)

    print("篮筐和篮球没有重叠区域共有：{}张".format(con))
    print("没有篮筐或者没有篮球的图片共有：{}张".format(con2))
    print("没有标注图片共有：{}张".format(con3))


"""
有些图片没有篮筐篮网重叠部分，
    图片没有篮筐或篮网，
    图片有多个相同标签
"""
if __name__ == "__main__":
    #annos_path = r"/data2/PaddleDetection2.6/datasets/basketball/xml" #xml路径
    annos_path = r"D:\zsh\biaozhu\3.29_toulan\3.28_25000img\images_12349\xml" #xml路径
    #images_path = r"/data2/PaddleDetection2.6/datasets/basketball/images" #img路径
    images_path = r"D:\zsh\biaozhu\3.29_toulan\3.28_25000img\images_12349\img" #img路径
    new_annos_path = r"D:\zsh\biaozhu\3.29_toulan\3.28_25000img\images_12349\new_xml" # 新xml路径
    new_images_path = r"D:\zsh\biaozhu\3.29_toulan\3.28_25000img\images_12349\new_img" # 新img路径
    #new_annos_path = r"/data2/action_localization/basketball-shot-detection/voc_hoop_ball_temp/xml" # 新xml路径
    #new_images_path = r"/data2/action_localization/basketball-shot-detection/voc_hoop_ball_temp/img" # 新img路径

    new_img_xml(annos_path,images_path,new_annos_path,new_images_path)




