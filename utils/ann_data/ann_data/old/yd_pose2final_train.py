import os
import numpy as np
import json
import argparse


parser = argparse.ArgumentParser(description='convert yd pose to final train.')
parser.add_argument('-json_name', metavar='json_name', type=str, required=False,
                    help='filename for annotations json file.')
parser.add_argument('-img_path', metavar='yd_pose_label_data_path', type=str, required=False,
                    help='path to the yd pose annotations files.')
args = parser.parse_args()

KP_Names = ['R_Ankle', 'R_Knee', 'R_Hip', 'L_Hip', 'L_Knee', 'L_Ankle', '', '', 'Neck', 'B_Head', 'R_Wrist', 'R_Elbow',
            'R_Shoulder', 'L_Shoulder', 'L_Elbow', 'L_Wrist']
# 关键点顺序映射
order_map = {0: 13, 1: 11, 2: 9, 3: 8, 4: 10, 5: 12, 6: 1, 7: 0, 8: 7, 9: 5, 10: 3, 11: 2, 12: 4, 13: 6}


def check_empty(list, name):
    try:
        if not list:
            return True
        list[name]
    except ValueError:
        return True

    if len(list[name]) > 0:
        return False
    else:
        return True


def csvdata(csv_file_path):
    print(csv_file_path)
    file = open(csv_file_path, 'r')
    try:
        idx = 0
        data = []
        while True:
            text_line = file.readline()
            # print(text_line)
            if text_line:
                if idx == 0:
                    idx = idx + 1
                    continue
                items = text_line.split(",")
                data.append(items)
            else:
                break
    finally:
        file.close()

    return data


def loadcsv(video_path):
    group_csvdata = {}
    video_result_paths = os.listdir(video_path)
    for result_path in video_result_paths:
        if result_path[-4:] == ".csv":
            csv_file_path = os.path.join(video_path, result_path)
            result_path = video_path.split('/')[-1]
            data = csvdata(csv_file_path)
            group_csvdata[result_path] = data
        else:
            if result_path == '.':
                continue
            if not os.path.isdir(os.path.join(video_path, result_path)):
                continue
            files = os.listdir(os.path.join(video_path, result_path))
            for f in files:
                if f[-4:] != ".csv":
                    continue
                csv_file_path = os.path.join(video_path, result_path, f)
                data = csvdata(csv_file_path)
                group_csvdata[result_path] = data

    return group_csvdata


def do_convert(args):
    db_type = args.json_name
    img_path = args.img_path
    # db_type = 'add-2'
    # img_path = 'C:/Users/laozhenyao/Desktop/aug_test/add-2'
    annot_group_data = loadcsv(img_path)
    save_path = os.path.join(img_path, 'annotations')
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    json_save_path = os.path.join(save_path, db_type + '.json')

    joint_num = 14

    anno_data = list()
    for group, group_data in annot_group_data.items():
        print(group, len(group_data))
        for item_data in group_data:
            if len(item_data) < 33:
                continue

            # kps
            kps = np.zeros((joint_num, 3))  # xcoord, ycoord, vis
            annot_joint_num = len(KP_Names)
            annot_jid = 0
            for jid in range(annot_joint_num):
                # remove 6, 7 keypoint
                if KP_Names[jid] == "":
                    continue
                kps[annot_jid][0] = float(item_data[jid * 3 + 1])
                kps[annot_jid][1] = float(item_data[jid * 3 + 2])
                kps[annot_jid][2] = int(item_data[jid * 3 + 3])
                annot_jid = annot_jid + 1

            filename = item_data[0]
            if db_type == 'add-2':
                img_name = os.path.join(db_type, group, "images", filename).replace('\\', '/')
            else:
                img_name = os.path.join(group, "images", filename).replace('\\', '/')

            # 关键点排序
            points, kps = [], kps.tolist()
            for x, y, v in kps:
                if v != 0:
                    points.append([x, y])
                else:
                    points.append([-1, -1])
            points = sorted([i for i in zip(order_map.values(), points)], key=lambda k: k[0])
            points = [i[1] for i in points]

            anno_data.append({'image': img_name, 'points': points})

    with open(json_save_path, 'w') as f:
        json.dump(anno_data, f)


if __name__ == "__main__":
    do_convert(args)
