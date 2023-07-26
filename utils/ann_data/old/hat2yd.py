# -*- coding: utf-8 -*-

import os
import csv
import cv2
import numpy as np
import xml.etree.ElementTree as ET

import argparse

parser = argparse.ArgumentParser(description='convert hat to yd pose format.')
parser.add_argument('hat_annotation_file_path', metavar='hat_annotation_file_path', type=str,
                    help='path to the hat annotations files, 分两级目录, 指到上级目录就行')

args = parser.parse_args()

def getPersonKeypoints(xmlPath, xmlFile):
    print(os.path.join(xmlPath, xmlFile))
    tree = ET.parse(os.path.join(xmlPath, xmlFile))
    root = tree.getroot()
    person = {}
    for obj in root.getchildren():
        if obj.tag == "image":
            person["image"] = obj.text
            
        if obj.tag == "keypoints":
            person["keypoints"] = {}
            for child in obj.getchildren():
                name = child.attrib["name"]
                person["keypoints"][name] = child.attrib
    return person

def convert(group_path):
    KP_Names = ['R_Ankle','R_Knee','R_Hip','L_Hip','L_Knee','L_Ankle','','','Neck','B_Head','R_Wrist','R_Elbow','R_Shoulder','L_Shoulder','L_Elbow','L_Wrist']
    group_result_paths = os.listdir(group_path)
    for result_path in group_result_paths:
        print(result_path)
        if result_path != 'info':
            continue

        csv_output_rows = []
        files = os.listdir(os.path.join(group_path, result_path))
        files.sort()
        for f in files:
            if f[-4:] != ".xml":
                continue
            person = getPersonKeypoints(os.path.join(group_path, result_path), f)
            data = [person["image"]]

            xmin = 0
            ymin = 0
            xmax = 0
            ymax = 0

            print(person["keypoints"].keys())
            for kp_name in KP_Names:
                if kp_name == "" or not kp_name in person["keypoints"]:
                    data.extend([0, 0, 0])
                    continue
                kp = person["keypoints"][kp_name]
                #if kp["visible"] == "0":
                #    data.extend([0, 0, 1])
                #    continue
                x = float(kp["x"])
                y = float(kp["y"])
                visible = 1 if kp["visible"] == "0" else 2
                data.extend([x, y, visible])

                if visible > 0:
                    if xmin > x or xmin == 0:
                        xmin = x
                    if xmax < x:
                        xmax = x
                    if ymin > y or ymin == 0:
                        ymin = y
                    if ymax < y:
                        ymax = y

            imgPath = os.path.join(group_path, "images", person["image"]) + ".jpg"
            print(imgPath)
            image_bgr = cv2.imread(imgPath, cv2.IMREAD_COLOR)
            if image_bgr is None:
                continue
            if image_bgr.size == 0:
                print('read fail:', imgPath)
                continue

            width = xmax - xmin + 1
            height = ymax - ymin + 1

            bbox = np.zeros((4))
            # corrupted bounding box
            if width <= 0 or height <= 0:
                continue
            # 20% extend
            else:
                width_ratio = 1.3 if width > height else 1.5
                height_ratio = 1.5 if width > height else 1.3
                bbox[0] = (xmin + xmax)/2. - width/2*width_ratio
                if bbox[0] < 0:
                    bbox[0] = 0
                bbox[1] = (ymin + ymax)/2. - height/2*height_ratio
                if bbox[1] < 0:
                    bbox[1] = 0
                bbox[2] = width*width_ratio
                if bbox[2] > image_bgr.shape[0]:
                    bbox[2] = image_bgr.shape[0] - bbox[0]
                bbox[3] = height*height_ratio
                if bbox[3] > image_bgr.shape[1]:
                    bbox[3] = image_bgr.shape[1] - bbox[1]

            data.extend(bbox)
            csv_output_rows.append(data)

        headers = ["frame"]
        for i in range(len(KP_Names)):
            headers.extend(["%s_x" % KP_Names[i].lower(), "%s_y" % KP_Names[i].lower(), "%s_v" % KP_Names[i].lower()])
        headers.extend(["bbox_top_x", "bbox_top_y", "bbox_bottom_x", "bbox_bottom_y"])

        with open(os.path.join(group_path, "pose-data.csv"), 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(headers)
            csvwriter.writerows(csv_output_rows)
            csvfile.close()

def convert_groups(groups_path):
    group_result_paths = os.listdir(groups_path)
    for group_path in group_result_paths:
        path_ = os.path.join(groups_path, group_path)
        if not os.path.isdir(path_):
            continue
        print(path_)
        convert(path_)


if __name__ == "__main__":
    # execute only if run as a script
    pose_path = args.hat_annotation_file_path  #"/data/yd_pose/exercise9/frames_labeled"
    convert_groups(pose_path)
