#利用标注生成txt，xml
# 复制blaze


# -*- coding: utf-8 -*-
import os
import os.path as osp
import numpy as np
import json

import argparse

parser = argparse.ArgumentParser(description='convert yd pose to hat format.')
parser.add_argument('yd_pose_path', metavar='yd_pose_label_data_path', type=str,
                    help='path to the yd pose annotations files.')
parser.add_argument('model_type', metavar='model_type', type=str,
                    help='model type to the yd pose annotations files.eg: blaze、hr')

args = parser.parse_args()

def convert_group(group_path, model_type):
    KP_Names = ['R_Ankle','R_Knee','R_Hip','L_Hip','L_Knee','L_Ankle','','','Neck','B_Head','R_Wrist','R_Elbow','R_Shoulder','L_Shoulder','L_Elbow','L_Wrist']
    anno_list_file = None
    files = os.listdir(group_path)
    for f in files:
        if os.path.isdir(os.path.join(group_path, f)):
            convert_group(os.path.join(group_path, f), model_type)
            continue
        if f[-4:] != ".csv":
            continue

        csv_file = f
        if not anno_list_file:
            anno_list_file = open(os.path.join(group_path, "annotation_list.txt"), 'w')
        csv_file_path = os.path.join(group_path, csv_file)
        file = open(csv_file_path, 'r')

        try:
            idx = 0
            while True:
                text_line = file.readline()
                if text_line:
                    if idx == 0:
                        idx = idx + 1
                        continue
                    items = text_line.split(",")
                    # if len(items) != 37:
                    #     continue
                    imgName = items[0][:-4]

                    anno_list_file.write('%s_0.xml\n' % imgName)

                    if not os.path.exists(os.path.join(group_path, 'info')):
                        os.mkdir(os.path.join(group_path, 'info'))

                    anno_file = open(os.path.join(group_path, 'info', '%s_0.xml' % (imgName)), 'w')

                    anno_file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
                    anno_file.write('<annotation>\n')
                    anno_file.write('<image>%s</image>\n' % imgName)
                    anno_file.write('<category>person</category>\n')
                    anno_file.write('<subcategory>male</subcategory>\n')
                    anno_file.write('<keypoints>\n')

                    print('%d items len:' % idx, len(items))
                    for kpid in range(16):
                        print('kpid:', kpid)
                        if KP_Names[kpid] == "":
                            continue
                        if 'hr' == model_type:
                            anno_file.write('<keypoint name="%s" visible="1" x="%s" y="%s" z="0.0" zorder="0"/>\n' % (KP_Names[kpid], items[kpid*2 + 1], items[kpid*2+1+1].strip('\n')))
                        elif 'blaze' == model_type:
                            anno_file.write('<keypoint name="%s" visible="1" x="%s" y="%s" z="0.0" zorder="0"/>\n' % (KP_Names[kpid], items[kpid * 3 + 1], items[kpid * 3 + 1 + 1].strip('\n')))

                    anno_file.write('</keypoints>\n')
                    anno_file.write('<segments>\n')
                    anno_file.write('</segments>\n')
                    anno_file.write('</annotation>\n')

                    anno_file.close()

                else:
                    break
                idx = idx + 1

        finally:
            file.close()


if __name__ == "__main__":
    # execute only if run as a script
    yd_pose_path = args.yd_pose_path #"/data/yd_pose/exercise9/frames_labeled"
    convert_group(yd_pose_path, args.model_type)
