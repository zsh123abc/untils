#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 移动标签为空的xml，并同步移动相应图片
import os
import xml.etree.ElementTree as ET
import shutil
# G:/person/images/'
# xml_dir = 'G:/person/new_annotations/
origin_ann_dir = r'D:\zsh\biaozhu\bilibli\download\table_tennis\7.18\7.18_ping-pang_xml/'  # 设置原始标签路径为 Annos
new_ann_dir = r'D:\zsh\biaozhu\bilibli\download\table_tennis\7.18\new_xml/'  # 设置新标签路径 Annotations
origin_pic_dir = r'D:\zsh\biaozhu\bilibli\download\table_tennis\7.18\7.18_ping-pang_img/'
new_pic_dir = r'D:\zsh\biaozhu\bilibli\download\table_tennis\7.18\new_img/'
k = 0
p = 0
q = 0
for dirpaths, dirnames, filenames in os.walk(origin_ann_dir):  # os.walk游走遍历目录名
    for filename in filenames:
        print("process...")
        k = k + 1
        print(k)
        if os.path.isfile(r'%s%s' % (origin_ann_dir, filename)):  # 获取原始xml文件绝对路径，isfile()检测是否为文件 isdir检测是否为目录
            origin_ann_path = os.path.join(r'%s%s' % (origin_ann_dir, filename))  # 如果是，获取绝对路径（重复代码）
            new_ann_path = os.path.join(r'%s%s' % (new_ann_dir, filename))
            tree = ET.parse(origin_ann_path)  # ET是一个xml文件解析库，ET.parse（）打开xml文件。parse--"解析"
            root = tree.getroot()  # 获取根节点
            if len(root.findall('object')):
                p = p + 1
            else:
                print(filename)
                old_xml = origin_ann_dir + filename
                new_xml = new_ann_dir + filename
                old_pic = origin_pic_dir + filename.replace("xml", "jpg")
                new_pic = new_pic_dir + filename.replace("xml", "jpg")
                q = q + 1
                shutil.move(old_pic, new_pic)
                shutil.move(old_xml, new_xml)
print("ok, ", p)
print("empty, ", q)