#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import cv2
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom


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
        information.append({"rect": [xmin,ymin,xmax,ymax],"tag": name, "path": filepath, "filename": filename})

    xml_file.close() # 关闭文件
    return  [information,tag_list]


# In[ ]:


def writeVocAnnotation(folder: str, img_name: str, path: str, img_width: int, img_height: int, tag_num: int, tag_name: str, box_list:list):
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
 
    for i in range(tag_num):
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
        for item, value in zip(["xmin", "ymin", "xmax", "ymax"], box_list[i]):
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
  x = max(a[0], b[0])
  y = max(a[1], b[1])
  w = min(a[0]+a[2], b[0]+b[2]) - x
  h = min(a[1]+a[3], b[1]+b[3]) - y
  if w<0 or h<0: return ()
  return (x, y, w, h)

def rect_union(a,b):
    union = [0, 0, 0, 0]
    union[0] = min(a[0], b[0])
    union[1] = min(a[1], b[1])
    union[2] = max(a[2], b[2])
    union[3] = max(a[3], b[3])
    return union


# In[ ]:

def new_img_xml(annos_path,images_path,new_annos_path,new_images_path):

    con=0
    con2=0
    con3=0
    # con4=0
    # new_imgPath_list = []

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
        data = decodeVocAnnotation(os.path.join(annos_path, anno_file),os.path.join(images_path, anno_file))

        # 有一部分图片没有篮筐或者篮球
        lab = data[0] # 所有数据
        tag = data[1] # 当前图片所有标签列表
        
        if len(tag)==0:
            print('图片没有标注:{}'.format(anno_file))
            con3+=1

        elif ("basketball_frame" not in tag) or ("basketball" not in tag):
            print('图片没有筐或网:{}'.format(lab[0]['filename']))
            con2+=1

        
        for i in range(0, len(lab)):
            frame_label = lab[i]
            filepath = frame_label["path"]

            filename = frame_label["filename"]
            filepath = images_path+'\\'+filename

            if frame_label["tag"] == "basketball_frame":
                # 标注顺序可能不一样，篮球不一定标注在篮筐后面，如果在前面，那么i+1就会判断不到
                # for j in range(i+1, len(lab)):
                for j in range(0, len(lab)):
                    ball_label = lab[j]
                    if ball_label["tag"] == "basketball":
                        frame_rect = frame_label["rect"]
                        fx1, fy1, fx2, fy2 = frame_rect
                        frame_width = fx2-fx1
                        #扩大篮圈的范围
                        frame_outer_rect = [fx1-frame_width, fy1-int(frame_width/3), fx2+frame_width, fy2+frame_width]
                        
                        ball_rect = ball_label["rect"]
                        #求重叠区域
                        intersect_rect = rect_intersection(frame_outer_rect, ball_rect)
                        
                        # 可能有多个重复标签，
                        if len(intersect_rect) == 0:
                            if len(tag) == len(set(tag)):
                                print('图片名：{},图片中篮网和篮筐没有重叠区域！！！'.format(filename))
                                con+=1
                                # 没有重复标签并且篮筐和篮球不重叠，退出当前循环
                                break
                            # 有重复的标签就接着看重复标签有没有重叠，退出当次循环
                            continue       
                      
                        if intersect_rect[2]>0 and intersect_rect[3]>0:
                            image_path = filepath #需要赋值

                            image = cv2.imread(image_path)
                            #求篮筐和球的外框
                            union_rect = rect_union(frame_rect, ball_rect)
                            #求扣图框,然后抠图
                            sub_img_rect = rect_union(frame_outer_rect, ball_rect)
                            x1,y1, x2,y2 = sub_img_rect
                            
                            sp = image.shape
                            # width = sp[1]#width(colums) of image

                            #抠图超出边界
                            if x1<0:
                                x1 = 0
                            if y1<0:
                                y1 = 0

                            if x2<0:
                                x2 = 0
                            if y2<0:
                                y2 = 0
                            
                            #抠图
                            sub_image = image[y1:y2, x1:x2]
                            new_label = "success"
                            #如果球在篮筐左右两边，则判断为没投中
                            if ball_rect[2]<=frame_rect[0] or ball_rect[0]>=frame_rect[2]:
                                new_label = "miss"
                            #保存扣出来的图
                            img_filename = filename
                            new_img_path = os.path.join(new_images_path, img_filename)
                            # con4+=1
                            # new_imgPath_list.append(filename)
                            cv2.imwrite(new_img_path, sub_image)
                            #保存标注文件
                            sub_img_height, sub_img_width, sub_img_channels = sub_image.shape
                            ux1,uy1,ux2,uy2 = union_rect

                            new_label_rect = [ux1-x1, uy1-y1, ux2-x1, uy2-y1]
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
                            writeVocAnnotation(new_annos_path, filename, filepath, sub_img_width, sub_img_height, 1, new_label, [new_label_rect])
                            # writeVocAnnotation(new_annos_path, anno_file, filepath, filename, sub_img_width, sub_img_height, 1, new_label, [union_rect])

    print()
    print("篮筐和篮球没有重叠区域共有：{}张".format(con))
    print("没有篮筐或者没有篮球的图片共有：{}张".format(con2))
    print("没有标注图片共有：{}张".format(con3))


    # print()
    # # new_imgPath_list = list(set(new_imgPath_list))
    # list2 = []
    # for l1 in new_imgPath_list:
    #     if l1 not in list2:
    #         list2.append(l1)
    # print(list2)

    # print(len(list2))
    # images2 = r'C:\Users\cwj\zsh\ball_label\img2\images2'
    # img_list = os.listdir(images2)
    # for i in range(len(list2)):
    #     if list2[i]!=img_list[i]:
    #         print(img_list[i])
    #         print(list2[i])
    #         break


"""
有些图片没有篮筐篮网重叠部分，
    图片没有篮筐或篮网，
    图片有多个相同标签
"""
if __name__ == "__main__":
    annos_path = r"D:\zsh\biaozhu\3.8v\3.20_2000_img\lab" #xml路径
    images_path = r"D:\zsh\biaozhu\3.8v\3.20_2000_img\images" #img路径
    new_annos_path = r"C:\Users\cwj\zsh\ball_label\img2\lable2" # 新xml路径
    new_images_path = r"C:\Users\cwj\zsh\ball_label\img2\images2" # 新img路径

    new_img_xml(annos_path,images_path,new_annos_path,new_images_path)




