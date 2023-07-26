import json
import glob
import pandas as pd

keys = ['pic_dir', 'action',
        'b_head_x', 'b_head_y', 'b_head_v',
        'neck_x', 'neck_y', 'neck_v',
        'l_shoulder_x', 'l_shoulder_y', 'l_shoulder_v',
        'r_shoulder_x', 'r_shoulder_y', 'r_shoulder_v',
        'l_elbow_x', 'l_elbow_y', 'l_elbow_v',
        'r_elbow_x', 'r_elbow_y', 'r_elbow_v',
        'l_wrist_x', 'l_wrist_y', 'l_wrist_v',
        'r_wrist_x', 'r_wrist_y', 'r_wrist_v',
        'l_hip_x', 'l_hip_y', 'l_hip_v',
        'r_hip_x', 'r_hip_y', 'r_hip_v',
        'l_knee_x', 'l_knee_y', 'l_knee_v',
        'r_knee_x', 'r_knee_y', 'r_knee_v',
        'l_ankle_x', 'l_ankle_y', 'l_ankle_v',
        'r_ankle_x', 'r_ankle_y', 'r_ankle_v']
# 关键点顺序映射
order_map = {0: 13, 1: 11, 2: 9, 3: 8, 4: 10, 5: 12, 6: 1, 7: 0, 8: 7, 9: 5, 10: 3, 11: 2, 12: 4, 13: 6}
for file_name in ['sit-up']:
    output = dict()
    for i in keys:
        output[i] = list()

    index = 0
    paths = glob.glob('C:/Users/dell/Desktop/share_files/add-2/Apush-up/annotations/{}*.json'.format(file_name))
    for path in paths:
        print(path)
        name = path.split('\\')[1].split('.')[0]
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        images = data['images']
        annotations = data['annotations']

        for i in annotations:
            for j in images:
                if i['id'] == j['id']:
                    name = j['file_name'].split('/')[1]
                    pic_dir = j['file_name']

                    output['pic_dir'].append(pic_dir)
                    output['action'].append(name)
                    # print(pic_dir)

            # 关键点排序
            points = []
            for x, y in zip(i['keypoints'][0::3], i['keypoints'][1::3]):
                points.append([x, y, 0])
            points = sorted([i for i in zip(order_map.values(), points)], key=lambda k: k[0])
            points = [j for i in points for j in i[1]]
            for x, y, out_x, out_y, out_v in zip(points[0::3], points[1::3], keys[2::3], keys[3::3], keys[4::3]):
                if x == 0 and y == 0:
                    # x, y = None, None
                    print(index)
                output[out_x].append(int(x))
                output[out_y].append(int(y))
                output[out_v].append(0)

            index += 1

    # for i in output.values():
    #     print(len(i))
    df = pd.DataFrame(output)
    # print(df)
    df.to_csv('C:/Users/dell/Desktop/share_files/add-2/Apush-up/annotations/{}.csv'.format(file_name), index=0, header=0)
