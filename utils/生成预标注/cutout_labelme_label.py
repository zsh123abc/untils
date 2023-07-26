# -*- coding: utf-8 -*-
#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import cv2
import os
import copy
import base64
import numpy as np
import json
# from shapely.geometry import Polygon


# In[ ]:

def decodeAnnotation(json_file_path,ord_img_path):
    with open(json_file_path) as f:
        result=json.load(f)
        return result

# In[ ]:

def save_new_json(folder: str, json_file_name: str, labels: object,lab_new):
    json_path = os.path.join(folder, json_file_name)
    print("json_path:", json_path)

    json_path = json_path.replace('\\','/')
    """
    修改后json保存路径
    """
    new_json_path = r'D:\zsh\7.7_court\part1\all_court\new_json'+'/'+json_file_name
    # output_filename = os.path.join(xml_path, urllib.quote(html, safe='+/'))

    # lab = json.dumps(lab_new)
    x1,y1, x2,y2 = labels

    file_in = open(json_path, "r", encoding='utf-8')
    # json.load数据到变量json_data
    json_data = json.load(file_in)
    """
    命名，四个点画框
    """
    dic = {
            "label": "F_field", "points": [[x1,y1],[x2,y2]], 
               "group_id": None,
               "description": "",
               "shape_type": "rectangle",
               "flags": {}
               }
    json_data['shapes'] = [dic] # 修改标注数据，只要框
    file_in.close()
    # 保存至另外的一个json文件
    file_out = open(new_json_path, "w", encoding='utf-8')
    # 将修改后的数据写入文件
    file_out.write(json.dumps(json_data,indent=2))
    file_out.close()  


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

def load_base64_img(data):
    img_data = base64.b64decode(data)
    # 转换为np数组
    img_array = np.frombuffer(img_data, np.uint8)
    # 转换成opencv可用格式
    img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
    return img

# In[ ]:

def fetch_a_group_label(images_path, img_filename, anno_filename, new_annos_path, new_images_path, sub_img_rect, label_new, label_items):
    image_path = os.path.join(images_path, img_filename) #需要赋值
    print("image path:", image_path)
    image = cv2.imread(image_path)
    if image is None:
        return
    
    # 获取画框的四个点
    x1,y1, x2,y2 = sub_img_rect

    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    
    save_new_json(new_annos_path, anno_filename, sub_img_rect,label_new)

def distance(x, y):
    return ((y[0] - x[0]) ** 2 + (y[1] - x[1]) ** 2) ** (1/2)

def getBoxCenterCoord( box):
    xmin, ymin, xmax, ymax = box
    xCoord = int(np.mean([xmin, xmax]))
    yCoord = int(np.mean([ymin, ymax]))
    return (xCoord, yCoord)

def new_img_xml(annos_path,images_path,new_annos_path,new_images_path, label_items):


    xml_list = os.listdir(annos_path) # 获取目录下的所有xml文件名
    for anno_file in xml_list: # 循环对每一个xml进行处理
        # labelme img,json放在一起
        if anno_file[-4:] != "json":
            continue
        print("anno_file:", os.path.join(annos_path, anno_file))
        # 解码。解码之后变为字典格式
        label_data = decodeAnnotation(os.path.join(annos_path, anno_file), os.path.join(images_path, anno_file))

        if len(label_data["shapes"])==0:
            print('图片没有标注:{}'.format(images_path))

        img_filename = anno_file.replace(".json", ".jpg")

        sub_img_rect = []

        if "imageWidth" in label_data:
            img_width = label_data["imageWidth"]
            img_height = label_data["imageHeight"]
        label_new = copy.deepcopy(label_data)
        minx, miny, maxx, maxy = -1, -1, 0, 0
        for i in range(0, len(label_data["shapes"])):
            shape = label_data["shapes"][i]
            if shape["label"] not in label_items: #["left", "right", "front", "back"]:
                continue
            for point in shape["points"]:
                if minx < 0 or minx > point[0]:
                    minx = point[0]
                if miny < 0 or miny > point[1]:
                    miny = point[1]
                if maxx < point[0]:
                    maxx = point[0]
                if maxy < point[1]:
                    maxy = point[1]
        width = maxx - minx
        # 四个点扩大范围
        minx = int(minx - 10)
        if minx < 0:
            minx = 0
        miny = int(miny - 10)
        if miny < 0:
            miny= 0
        maxx = int(maxx + 10)
        if maxx > img_width:
            maxx = img_width
        maxy = int(maxy + 10)
        if maxy > img_height:
            maxy = img_height

        sub_img_rect = [minx, miny, maxx, maxy] #矩形框
                              
        #连线

        #if has_ball:
        fetch_a_group_label(images_path, img_filename, anno_file, new_annos_path, new_images_path, sub_img_rect, label_new, label_items)


if __name__ == "__main__":
    """
    都改成原json路径
    """
    annos_path = r"D:\zsh\7.7_court\part1\all_court\img" #json路径
    images_path = r"D:\zsh\7.7_court\part1\all_court\img" #img路径
    new_annos_path = r"D:\zsh\7.7_court\part1\all_court\img" #xml路径
    new_images_path = r"D:\zsh\7.7_court\part1\all_court\img" #img路径

    label_items = ["left_top_1", "left_bottom_1", "right_top_1", "right_bottom_1", "central_top_1"]
    #label_items = ["left", "right", "front", "back"]
    new_img_xml(annos_path,images_path,new_annos_path,new_images_path, label_items)





# %%
