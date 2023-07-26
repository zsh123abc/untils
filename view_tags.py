import os
from unicodedata import name
import xml.etree.ElementTree as ET
import glob


def count_num(indir):
    os.chdir(indir)
    annotations = os.listdir('.')
    annotations = glob.glob(str(annotations) + '*.xml')

    dict = {} 
    for i, file in enumerate(annotations):  

        # actual parsing
        in_file = open(file, encoding='utf-8')
        tree = ET.parse(in_file)
        root = tree.getroot()

        # 遍历文件的所有标签
        for obj in root.iter('object'):
            name = obj.find('name').text
            if (name in dict.keys()):
                dict[name] += 1 
            else:
                dict[name] = 1 
        print(file)
    print("n:")
    for key in dict.keys():
        print(key + ': ' + str(dict[key]))


indir = r'C:\ann\annotations'  # xml文件所在的目录 

count_num(indir) 