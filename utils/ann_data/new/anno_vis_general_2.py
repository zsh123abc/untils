# coding=UTF-8
import json
import cv2
import os
import argparse



parser = argparse.ArgumentParser(description='visualized annotations json file.')
parser.add_argument('-train_path', metavar='train_annotation_file_path', type=str,
                    help='path to the train annotations json file.', required=False)
parser.add_argument('-test_path', metavar='test_annotation_file_path', type=str,
                    help='path to the test annotations json file.', required=False)
parser.add_argument('-img_dir_path', metavar='image_directory_path', type=str,
                    help='path to the image directory.', required=False)
parser.add_argument('-save_path', metavar='image_save_path', type=str,
                    help='path to the image saving.', required=False)
args = parser.parse_args()

if __name__ == '__main__':
    # train_path = '/data2/tot_yd_data/add-2/annotations/merge_train.json'
    # test_path = '/data2/tot_yd_data/round_1-2/test_tf_yd_clear.json'
    # train_path = args.train_path
    # test_path = args.test_path
    # img_dir_path = args.img_dir_path
    # save_path = args.save_path
    # with open(train_path, 'r', encoding='utf-8') as f:
    #     train_data = json.load(f)
    # with open(test_path, 'r', encoding='utf-8') as f:
    #     test_data = json.load(f)
    # train_data.extend(test_data)
    # data = train_data

    # 关键点连接顺序
    edges = [[0, 1], [1, 2], [2, 4], [4, 6], [1, 3], [3, 5], [5, 7], [8, 10], [10, 12], [9, 11], [11, 13],
             [8, 9], [2, 8], [3, 9]]
    json_path = r'D:\zsh\biaozhu\zsh_labels\annotations\sit-up.json' # json路径
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # aic_imgs = os.listdir(os.path.join('G:/train/images/aic_imgs/train'))  # 检查aic数据打开
    for i in data:
        img_path = i['image']
        # 检查aic数据打开
        # if img_path.split('/')[-1] not in aic_imgs:
        #     continue
        # 检查通用数据集时打开
        # if '/'.join(img_path.split('/')[:2]) != 'pull-up-0/images':
        #     continue
        kps = i['points']
        img = cv2.imread(os.path.join(r'D:\zsh\biaozhu/', img_path)) #图片上两级路径
        # img = cv2.imread(os.path.join(img_dir_path + img_path))

        # print(img_path)
        # print(img_path)
        # 关键点按顺序连线，画线
        for edge_chain in edges:
            p1, p2 = kps[edge_chain[0]], kps[edge_chain[1]]
            if p1[0] == -1 or p2[0] == -1:
                continue
            cv2.line(img, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), (0, 0, 255), 3)
        # 画点
        for index, (x, y) in enumerate(kps):
            if x == -1:
                continue
            cv2.circle(img, (int(x), int(y)), radius=8, color=(0, 255, 0), thickness=-1)
            cv2.putText(img, str(index), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255), 2, cv2.LINE_AA)
        # cv2.namedWindow("img_cv", 0)
        # cv2.resizeWindow('img_cv', 800, 800)
        # cv2.imshow('img_cv', img)
        # cv2.waitKey(0)
        # output_path = os.path.join('G:/train/images/', '/'.join(img_path.split('/')[1:-1])) #图片上级路径
        # output_path = os.path.join('G:/train/aic_imgs/', '/'.join(img_path.split('/')[1:-1])) #输出可视化路径
        output_path = r'D:\zsh\biaozhu\zsh_labels\img'
        # output_path = os.path.join(save_path, '/'.join(img_path.split('/')[:-1]))
        os.makedirs(output_path, exist_ok=True)
        # print(output_path + '/' + img_path.split('/')[-1])
        cv2.imwrite(output_path + '/' + img_path.split('/')[-1], img)

