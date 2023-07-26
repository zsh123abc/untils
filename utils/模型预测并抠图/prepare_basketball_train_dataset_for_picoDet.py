import os
import random

trainval_percent = 0.15
train_percent = 0.85
dataset_path = './'
xmlfilepath = './xml/'  #换成自己标签存放的路径
txtsavepath = '/dataset/VOCdevkit/VOC2007'
imgfilepath = './images/'  #换成自己图片存放的路径
#label_paths = {"./xml/": "./images/", "./xml_aug/": "./images_aug/", "./big_xml/": "./big_images/", "./big_xml_aug/": "./big_images_aug/"}
#label_paths = {"./xml/": "./images/"}
label_paths = {"./xml/": "./images/", "./old_xml/": "./old_images/"}

ftrainval = open(dataset_path + '/trainval.txt', 'w')
ftest = open(dataset_path + '/test.txt', 'w')
ftrain = open(dataset_path + '/train.txt', 'w')
fval = open(dataset_path + '/val.txt', 'w')

total_num = 0
for xmlfilepath in label_paths:
    imgfilepath = label_paths[xmlfilepath]
    total_xml = os.listdir(xmlfilepath)

    num = len(total_xml)
    total_num = total_num + num
    print("num:", num)
    id_list = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(id_list, tv)
    train = random.sample(trainval, tr)


    for i in id_list:
        name = total_xml[i][:-4]
        if i in trainval:
            ftrainval.write(imgfilepath + name + '.jpg' + ' ' + xmlfilepath + name + '.xml' + '\n')
            if i in train:
                ftest.write(imgfilepath + name + '.jpg' + ' ' + xmlfilepath + name + '.xml' + '\n')
            else:
                fval.write(imgfilepath + name + '.jpg' + ' ' + xmlfilepath + name + '.xml' + '\n')
        else:
            ftrain.write(imgfilepath + name + '.jpg' + ' ' + xmlfilepath + name + '.xml' + '\n')

print("total num:", total_num)
ftrainval.close()
ftrain.close()
fval.close()
ftest.close()

