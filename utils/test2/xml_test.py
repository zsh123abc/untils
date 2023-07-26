#_*_ coding:utf-8 _*_
'''
XML是可扩展标记语言（Extensible Markup Language）的缩写，其中标记是关键部分。
用户可以创建内容，然后使用限定标记标记它，从而使每个单词、短语或块成为可识别、可分类的信息。
'''
#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
from xml.dom.minidom import parse
import xml.dom.minidom
import time
from xml.etree import ElementTree
import os    

def read_xml(path_name):            #传递文件路径
    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parse(path_name)
    collection = DOMTree.documentElement #获取文档根元素
    if collection.hasAttribute("shelf"): #获取根元素中shelf的名称
        print("Root element : %s" % collection.getAttribute("shelf"))
    # 获取所有关于movie节点下的标签内容
    movies = collection.getElementsByTagName("movie")  
    
    # 打印每部电影的详细信息i
    i = 1
    for movie in movies:   #循环movies所有节点，并读取对应标签中的内容数据 
        print("*****Movie*** %s **部" % i)
        if movie.hasAttribute("title"):
            # 获取title节点的名称
            print("Title: %s" % movie.getAttribute("title"))
        try:
            #获取标签中对应标签名称的内容
            type = movie.getElementsByTagName('type')[0]
            print("Type: %s" % type.childNodes[0].data)
            format = movie.getElementsByTagName('format')[0]
            print ("Format: %s" % format.childNodes[0].data)
            #修改标签中的内容格式如下：即重新赋值即可，后续标签皆如此写法
            # format.childNodes[0].data = "textt"
            rating = movie.getElementsByTagName('rating')[0]
            print("Rating: %s" % rating.childNodes[0].data)
             #修改标签中的内容格式如下：即重新赋值即可，后续标签皆如此写法
            # rating.childNodes[0].data = "textt"
            stars = movie.getElementsByTagName("stars")[0]
            print("stars: %s" % stars.childNodes[0].data)
            description = movie.getElementsByTagName('description')[0]
            print("Description: %s" % description.childNodes[0].data)
            i += 1
        except:
            pass

#XML文档中添加数据
def write_xml(path_name):
    xml_file = open(path_name)
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()

    tag_list = ['backboard','basket_net','basketball_frame']
    objects = root.findall('object')
    for object in objects:
        name = object.find('name').text
        if name in tag_list:
            pose = object.find('pose').text 
            truncated = object.find('truncated').text 
            difficult = object.find('difficult').text

            bndbox = object.find('bndbox')
            xmin=bndbox.find("xmin")
            ymin=bndbox.find("ymin")
            xmax=bndbox.find("xmax")
            ymax=bndbox.find("ymax")

            domTree = parse(path_name)
            # 文档根元素
            rootNode = domTree.documentElement
            # 新建一个customer节点
            customer_node = domTree.createElement("object")
            # customer_node.setAttribute("title", "fuchouzhe")

            # 创建name节点,并设置textValue
            name_node = domTree.createElement("name")
            print(name_node)
            name_text_value = domTree.createTextNode(name)
            name_node.appendChild(name_text_value)  # 把文本节点挂到name_node节点
            customer_node.appendChild(name_node)

            # 创建phone节点,并设置textValue
            phone_node = domTree.createElement("pose")
            phone_text_value = domTree.createTextNode(pose)
            phone_node.appendChild(phone_text_value)  # 把文本节点挂到name_node节点
            customer_node.appendChild(phone_node)

            # 创建comments节点,这里是CDATA
            comments_node = domTree.createElement("truncated")
            cdata_text_value = domTree.createTextNode(truncated)
            comments_node.appendChild(cdata_text_value)
            customer_node.appendChild(comments_node)
            rootNode.appendChild(customer_node)

            comments_node = domTree.createElement("difficult")
            cdata_text_value = domTree.createTextNode(difficult)
            comments_node.appendChild(cdata_text_value)
            customer_node.appendChild(comments_node)
            rootNode.appendChild(customer_node)

            comments_node = domTree.createElement("bndbox")

            xmin_node = domTree.createElement("xmin")
            ymin_node = domTree.createElement("ymin")
            xmax_node = domTree.createElement("xmax")
            ymax_node = domTree.createElement("ymax")

            cdata_text_value = domTree.createTextNode(xmin.text)
            cdata_text_value2 = domTree.createTextNode(ymin.text)
            cdata_text_value3 = domTree.createTextNode(xmax.text)
            cdata_text_value4 = domTree.createTextNode(ymax.text)

            xmin_node.appendChild(cdata_text_value)
            ymin_node.appendChild(cdata_text_value2)
            xmax_node.appendChild(cdata_text_value3)
            ymax_node.appendChild(cdata_text_value4)

            comments_node.appendChild(xmin_node)
            comments_node.appendChild(ymin_node)
            comments_node.appendChild(xmax_node)
            comments_node.appendChild(ymax_node)
            customer_node.appendChild(comments_node)
            rootNode.appendChild(customer_node)

            path = r'D:\zsh\biaozhu\4.1_img_3522\test_xml'
            for xml_patn in os.listdir(path):
                xml_patn = path+'\\'+xml_patn
                with open(xml_patn, 'a+') as f:
                    # 缩进 - 换行 - 编码
                    '''
                    file：要保存为的文件对象名
                    indent：根节点的缩进方式
                    allindent：子节点的缩进方式
                    newl：针对新行，指明换行方式
                    encoding：保存文件的编码方式
                    '''
                    domTree.writexml(f,indent="",addindent="",newl='',encoding='utf-8')
                '''整理xml文档的格式,否则xml添加数据,显示的是一行数据，不方便查看'''
                tree = ElementTree.parse(xml_patn)                       # 解析test.xml这个文件
                root = tree.getroot()                                # 得到根元素，Element类
                xiugai_xml(root, '\t', '\n')                          # 执行美化方法
                tree.write(xml_patn, encoding = 'utf-8')           # 保存文件

'''xml文档格式整理'''
def xiugai_xml(element, indent, newline, level = 0):
    # 判断element是否有子元素
    if element:
        # 如果element的text没有内容
        if element.text == None or element.text.isspace():
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
    temp = list(element) # 将elemnt转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):
            subelement.tail = newline + indent * (level + 1)
        else: 
            subelement.tail = newline + indent * level   
        xiugai_xml(subelement, indent, newline, level = level + 1)

if __name__ == "__main__":
    path_name = r"D:\zsh\biaozhu\4.1_img_3522\xml\fuishootingpractice.mp4_tl_4446.xml"
    # while True:
    #     change = input("选择执行的方法 read or write or break：")
    #     if change == "read" or change == "1":
    #         read_xml(path_name)
    #     elif change == "write" or change == "2":
    #         write_xml(path_name)
    #     elif change == "break" or change == "3":
    #         break
    #     time.sleep(2)
    #     break
    write_xml(path_name)