# -*- coding: utf-8 -*-
import glob

import tensorflow as tf
import cv2
import numpy as np
import os
import csv
import matplotlib.pyplot as plt
import argparse
# import torch
import time

'''
D:\project\data\dance_test_0630_img
D:\project\data\dance_test_tflite_img
D:\project\TNN_Model_result\blaze_pose\blaze_gpose.tflite
'''

parse = argparse.ArgumentParser('description: infer and generate blaze format csv file.')
parse.add_argument('img_dir', metavar= 'img_dir', type=str, help='directory to input images.')
parse.add_argument('tflite_path', metavar= 'tflite_path', type=str, help='tflite path to blaze model.')

def time_synchronized():
    # pytorch-accurate time
    # torch.cuda.synchronize() if torch.cuda.is_available() else None
    return time.time()


def padding_img(img, dest_size=None, color=(255, 255, 255)):
    ori_h, ori_w, _ = img.shape                                 #原图尺寸

    if dest_size is None:
        if ori_h >= ori_w:
            dest_size = (ori_h, ori_h)                        #fixme   按长边填充
        else:
            dest_size = (ori_w, ori_w)

    if dest_size[0] < ori_w and dest_size[1] < ori_h:
        raise Exception("The dest size must small than origin image")

    w_offset = max(0, int((dest_size[0] - ori_w) // 2))
    h_offset = max(0, int((dest_size[1] - ori_h) // 2))

    dest_img = cv2.copyMakeBorder(img, h_offset, h_offset, w_offset, w_offset, cv2.BORDER_CONSTANT,
                                  color)                         #填充目标图片    按边扩充
    dest_img = cv2.resize(dest_img, (int(dest_size[0]), int(dest_size[1])))
    return (dest_img, w_offset, h_offset)


def draw_2d_line(img, points, conn):
    """

    :param img:
    :param points:
    :param conn: [(0, 1), (1, 2), (3, 4),...]
    :return:
    """
    dup = img.copy()
    h, w, _ = dup.shape
    thickness = int(5 / 640 * h)

    colors = [0, 0, 0]
    for ind, (start_ind, end_ind) in enumerate(conn):
        xmin, ymin = points[start_ind]
        xmax, ymax = points[end_ind]

        colors[ind % 2] += 32
        colors[0] = min(0, 256)
        colors[1] = min(0, 256)
        colors[2] = min(0, 256)
        colors = [0,255,0]
        cv2.line(dup,
                 (int(xmin), int(ymin)),
                 (int(xmax), int(ymax)),
                 colors,
                 thickness)               #fixme      可视化输出图片
    return dup

def show_kps(image, points):
    for i, p in enumerate(points):
        x, y, visibility = p
        color = (0, 0, 255) if (visibility>0.2) else (255, 0, 0)
        cv2.circle(image, center=(int(x), int(y)), color=(255, 0, 0), radius=3, thickness=2)
        image = cv2.putText(image, str(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 1, cv2.LINE_AA)

    return image


class PoseEstimator:
    def __init__(self, model_path):
        self.interpreter = tf.lite.Interpreter(model_path)
        self.inp_len = self.interpreter.get_input_details()[0]['shape'][2]
        self.interpreter.allocate_tensors()
        # print('outputs:%s'%self.interpret.get_outputs()[0])
        self.out_len = 48

    def predict(self, frame):
        inp_frame, w_offset, h_offset = padding_img(frame)
        tmp_img = cv2.resize(inp_frame, (self.inp_len, self.inp_len))

        pad_h, pad_w, _ = inp_frame.shape
        h_scale, w_scale = pad_h / self.out_len, pad_w / self.out_len

        # tmp_img = tmp_img / 127.5 - 1
        tmp_img = tmp_img
        # img_transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
        # tmp_img = img_transform(tmp_img).numpy()

        # inp_img = tmp_img.transpose((2, 0, 1))
        inp_img = tmp_img
        inp_img = inp_img[np.newaxis, :, :, :]
        inp_img = inp_img.astype(np.float32)

        input_details = self.interpreter.get_input_details()
        # print(input_details)
        output_details = self.interpreter.get_output_details()
        # print(output_details)

        self.interpreter.set_tensor(input_details[0]['index'], inp_img)
        t1 = time_synchronized()
        self.interpreter.invoke()
        pred = [self.interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
        t2 = time_synchronized()
        FPS = 1/(t2-t1)
        # print(pred)
        coords = []
        pred = np.squeeze(pred)              #输出形状转换output: [17, 3]
        conf = []
        avg_conf = 0

        for i in range(pred.shape[0]):
            xy = pred[i,:]

            raw_x = xy[1]*self.out_len
            raw_y = xy[0]*self.out_len  # 找到最大位置所在行-->   x坐标值
            y = int(raw_y * h_scale - h_offset)  # 返回原图所在位置
            x = int(raw_x * w_scale - w_offset)
            coords.append([x, y])
            conf.append([x, y, xy[2]])
            avg_conf += xy[2]
        neck = [(coords[5][0]+coords[6][0])/2, (coords[5][1]+coords[6][1])/2]

        coords.insert(6,neck)
        # coords[6]
        avg_conf = avg_conf / pred.shape[0]

        return coords,pred, conf, avg_conf, FPS


def getPersonKeypoints(name, results):
    '''
        results forat
        "keypoints": {
            0: "nose",
            1: "left_eye",
            2: "right_eye",
            3: "left_ear",
            4: "right_ear",
            5: "left_shoulder",
            6: "neck",
            7: "right_shoulder",
            8: "left_elbow",
            9: "right_elbow",
            10: "left_wrist",
            11: "right_wrist",
            12: "left_hip",
            13: "right_hip",
            14:"left_knee",
            15:"right_knee",
            16:"left_ankle",
            17:"right_ankle"
        }
    '''
    person = {}
    person['image'] = name
    person['keypoints'] = {}
    person['keypoints']['R_Ankle'] = {}
    person['keypoints']['R_Ankle']['x'] = results[17][0]
    person['keypoints']['R_Ankle']['y'] = results[17][1]
    person['keypoints']['R_Ankle']['visible'] = '2'
    person['keypoints']['R_Knee'] = {}
    person['keypoints']['R_Knee']['x'] = results[15][0]
    person['keypoints']['R_Knee']['y'] = results[15][1]
    person['keypoints']['R_Knee']['visible'] = '2'
    person['keypoints']['R_Hip'] = {}
    person['keypoints']['R_Hip']['x'] = results[13][0]
    person['keypoints']['R_Hip']['y'] = results[13][1]
    person['keypoints']['R_Hip']['visible'] = '2'
    person['keypoints']['L_Hip'] = {}
    person['keypoints']['L_Hip']['x'] = results[12][0]
    person['keypoints']['L_Hip']['y'] = results[12][1]
    person['keypoints']['L_Hip']['visible'] = '2'
    person['keypoints']['L_Knee'] = {}
    person['keypoints']['L_Knee']['x'] = results[14][0]
    person['keypoints']['L_Knee']['y'] = results[14][1]
    person['keypoints']['L_Knee']['visible'] = '2'
    person['keypoints']['L_Ankle'] = {}
    person['keypoints']['L_Ankle']['x'] = results[16][0]
    person['keypoints']['L_Ankle']['y'] = results[16][1]
    person['keypoints']['L_Ankle']['visible'] = '2'

    person['keypoints']['R_Wrist'] = {}
    person['keypoints']['R_Wrist']['x'] = results[11][0]
    person['keypoints']['R_Wrist']['y'] = results[11][1]
    person['keypoints']['R_Wrist']['visible'] = '2'
    person['keypoints']['R_Elbow'] = {}
    person['keypoints']['R_Elbow']['x'] = results[9][0]
    person['keypoints']['R_Elbow']['y'] = results[9][1]
    person['keypoints']['R_Elbow']['visible'] = '2'
    person['keypoints']['R_Shoulder'] = {}
    person['keypoints']['R_Shoulder']['x'] = results[7][0]
    person['keypoints']['R_Shoulder']['y'] = results[7][1]
    person['keypoints']['R_Shoulder']['visible'] = '2'
    person['keypoints']['L_Shoulder'] = {}
    person['keypoints']['L_Shoulder']['x'] = results[5][0]
    person['keypoints']['L_Shoulder']['y'] = results[5][1]
    person['keypoints']['L_Shoulder']['visible'] = '2'
    person['keypoints']['L_Elbow'] = {}
    person['keypoints']['L_Elbow']['x'] = results[8][0]
    person['keypoints']['L_Elbow']['y'] = results[8][1]
    person['keypoints']['L_Elbow']['visible'] = '2'
    person['keypoints']['L_Wrist'] = {}
    person['keypoints']['L_Wrist']['x'] = results[10][0]
    person['keypoints']['L_Wrist']['y'] = results[10][1]
    person['keypoints']['L_Wrist']['visible'] = '2'

    person['keypoints']['B_Head'] = {}
    person['keypoints']['B_Head']['x'] = results[0][0]
    person['keypoints']['B_Head']['y'] = results[0][1]
    person['keypoints']['B_Head']['visible'] = '2'
    person['keypoints']['Neck'] = {}
    person['keypoints']['Neck']['x'] = results[6][0]
    person['keypoints']['Neck']['y'] = results[6][1]
    person['keypoints']['Neck']['visible'] = '2'

    return person

def convert(img_dir, onnx_path):
    # yd pose keypoint order
    KP_Names = ['R_Ankle', 'R_Knee', 'R_Hip', 'L_Hip', 'L_Knee', 'L_Ankle', '', '', 'Neck', 'B_Head', 'R_Wrist',
                'R_Elbow', 'R_Shoulder', 'L_Shoulder', 'L_Elbow', 'L_Wrist']
    csv_output_rows = []

    p = PoseEstimator(model_path=onnx_path)
    names = os.listdir(img_dir)
    names.sort()
    for name in names:
        file = os.path.join(img_dir, name)
        img = cv2.imread(file)
        if img is None:
            continue
        res = p.predict(img)
        person = getPersonKeypoints(name, res[0])
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
            # if kp["visible"] == "0":
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

        imgPath = os.path.join(img_dir, person["image"])
        print(imgPath)
        image_bgr = cv2.imread(imgPath, cv2.IMREAD_COLOR)
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
            bbox[0] = (xmin + xmax) / 2. - width / 2 * width_ratio
            if bbox[0] < 0:
                bbox[0] = 0
            bbox[1] = (ymin + ymax) / 2. - height / 2 * height_ratio
            if bbox[1] < 0:
                bbox[1] = 0
            bbox[2] = width * width_ratio
            if bbox[2] > image_bgr.shape[0]:
                bbox[2] = image_bgr.shape[0] - bbox[0]
            bbox[3] = height * height_ratio
            if bbox[3] > image_bgr.shape[1]:
                bbox[3] = image_bgr.shape[1] - bbox[1]

        data.extend(bbox)
        csv_output_rows.append(data)

    headers = ["frame"]
    for i in range(len(KP_Names)):
        headers.extend(["%s_x" % KP_Names[i].lower(), "%s_y" % KP_Names[i].lower(), "%s_v" % KP_Names[i].lower()])
    headers.extend(["bbox_top_x", "bbox_top_y", "bbox_bottom_x", "bbox_bottom_y"])

    par_dir = os.path.abspath(os.path.dirname(img_dir))
    with open(os.path.join(par_dir, "pose-data_blaze.csv"), 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows(csv_output_rows)
        csvfile.close()

if __name__ == '__main__':
    args = parse.parse_args()
    convert(args.img_dir, args.tflite_path)

