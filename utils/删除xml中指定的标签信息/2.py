import os
import xml.etree.ElementTree as ET

# -----------------------------------
# 删除xml中指定的标签信息
# -----------------------------------
# 设置原始标签路径
origin_ann_dir = r'D:\zsh\726\new_xml'
# 设置新标签路径
new_ann_dir = r'D:\zsh\726\new_xml'

if not os.path.exists(new_ann_dir):
    os.makedirs(new_ann_dir)

k = 0
# os.walk游走遍历目录名
for dirpaths, dirnames, filenames in os.walk(origin_ann_dir):
    for filename in filenames:
        print("process...")
        k = k + 1
        print(k)
        # 获取原始xml文件绝对路径，isfile()检测是否为文件 isdir检测是否为目录
        print(r'%s\%s' % (origin_ann_dir, filename))
        # if os.path.isfile(r'%s%s' % (origin_ann_dir, filename)):
            # 如果是，获取绝对路径（重复代码）
        origin_ann_path = os.path.join(r'%s\%s' % (origin_ann_dir, filename))
        new_ann_path = os.path.join(r'%s\%s' % (new_ann_dir, filename))
        # ET是一个xml文件解析库，ET.parse（）打开xml文件。parse--"解析"
        tree = ET.parse(origin_ann_path)
        # 获取根节点
        root = tree.getroot()
        # 找到根节点下所有“object”节点
        for object in root.findall('object'):
            # 找到object节点下name子节点的值（字符串）
            name = str(object.find('name').text)
            # 如果name等于str，则删除该节点
            if (name in ["1"]):
                root.remove(object)
            if (name in ["player"]):
                root.remove(object)
            # if (name in ["basket_net"]):
                # root.remove(object)
            if (name in ["table"]):
                root.remove(object)
            if (name in ["umpire"]):
                root.remove(object)
            if (name in ["racket"]):
                root.remove(object)
            if (name in ["15"]):
                root.remove(object)
            # if (name in ["bucket"]):
            #     root.remove(object)
            # if (name in ["air_fryer"]):
            #     root.remove(object)

        # tree为文件，write写入新的文件中。
        tree.write(new_ann_path)
