import os
from collections import Counter
import xml.etree.ElementTree as ET
import glob
from multiprocessing import Pool, cpu_count, freeze_support


def process_file(file):
    dict = {}
    in_file = open(file, encoding='utf-8')
    tree = ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        name = obj.find('name').text
        dict[name] = dict.get(name, 0) + 1

    in_file.close()
    return dict


def count_num(indir):
    os.chdir(indir)
    annotations = os.listdir('.')
    annotations = glob.glob('*.xml')

    dict = Counter()
    pool = Pool(cpu_count())  # 使用多进程池

    results = pool.map(process_file, annotations)  # 并行处理文件

    for result in results:
        dict.update(result)

    pool.close()
    pool.join()

    print("n:")
    for key, value in dict.items():
        print(key + ': ' + str(value))

# 多线程运行，代码运行更快
if __name__ == '__main__':
    freeze_support()  # 添加 freeze_support() 函数调用
    indir = r'D:\zsh\726\new_xml'  # xml文件所在的目录
    count_num(indir)
