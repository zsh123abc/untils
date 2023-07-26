import cv2
import os
import shutil
import numpy as np
import tensorflow as tf


def nms(heat, kernel=3):
    hmax = tf.nn.max_pool2d(heat, kernel, 1, padding='SAME')
    keep = tf.cast(tf.equal(heat, hmax), tf.float32)
    return heat * keep


def find_keypoints_from_heatmap(batch_heatmaps, normalize=False):
    batch, height, width, n_points = tf.shape(batch_heatmaps)[0], tf.shape(
        batch_heatmaps)[1], tf.shape(batch_heatmaps)[2], tf.shape(batch_heatmaps)[3]

    batch_heatmaps = nms(batch_heatmaps)

    flat_tensor = tf.reshape(batch_heatmaps, (batch, -1, n_points))

    # Argmax of the flat tensor
    argmax = tf.argmax(flat_tensor, axis=1)
    argmax = tf.cast(argmax, tf.int32)
    scores = tf.math.reduce_max(flat_tensor, axis=1)

    # Convert indexes into 2D coordinates
    argmax_y = argmax // width
    argmax_x = argmax % width
    argmax_y = tf.cast(argmax_y, tf.float32)
    argmax_x = tf.cast(argmax_x, tf.float32)

    if normalize:
        argmax_x = argmax_x / tf.cast(width, tf.float32)
        argmax_y = argmax_y / tf.cast(height, tf.float32)

    # Shape: batch * 3 * n_points
    batch_keypoints = tf.stack((argmax_x, argmax_y, scores), axis=1)
    # Shape: batch * n_points * 3
    batch_keypoints = tf.transpose(batch_keypoints, [0, 2, 1])

    return batch_keypoints


def visualize_keypoints(image, keypoints, visibility=None, point_color=(0, 255, 0), text_color=(0, 0, 0)):
    draw = image.copy()
    edges = [[0, 1], [1, 2], [2, 4], [4, 6], [1, 3], [3, 5], [5, 7], [8, 10], [10, 12], [9, 11], [11, 13],
             [8, 9], [2, 8], [3, 9]]
    if visibility is not None:
        for edge_chain in edges:
            for i in range(len(edge_chain) - 1):
                if visibility[edge_chain[i]] and visibility[edge_chain[i + 1]]:
                    p1 = tuple(keypoints[edge_chain[i]])
                    p2 = tuple(keypoints[edge_chain[i + 1]])
                    cv2.line(draw, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), (0, 0, 255), 3)

    for i, p in enumerate(keypoints):
        x, y = p[0], p[1]
        tmp_point_color = point_color
        if visibility is not None and not int(visibility[i]):
            tmp_point_color = (100, 100, 100)
        draw = cv2.circle(draw, center=(int(x), int(y)),
                          color=tmp_point_color, radius=6, thickness=-1)
        draw = cv2.putText(draw, str(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX,
                           1, text_color, 2, cv2.LINE_AA)

    return draw


def tflite_keypoint(model_path, img_dir, config_path, vis_path=None, confidence=0.05):
    # Load model
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    im_size = input_details[0]['shape'][1]
    heatmap_size = im_size / 4

    kp_names = ['B_Head', 'Neck', 'L_Shoulder', 'R_Shoulder',
                'L_Elbow', 'R_Elbow', 'L_Wrist', 'R_Wrist',
                'L_Hip', 'R_Hip', 'L_Knee', 'R_Knee', 'L_Ankle', 'R_Ankle']
    
    info_path = os.path.join(img_dir, 'info')
    os.makedirs(info_path, exist_ok=True)
    img_path = os.path.join(img_dir, 'images')
    txt_file = ''
    for img_name in os.listdir(img_path):
        file_path = os.path.join(img_path, img_name)
        print(file_path)
        origin_frame = cv2.imread(file_path)
        scale = np.array([float(origin_frame.shape[1]) / im_size,
                          float(origin_frame.shape[0]) / im_size], dtype=float)
        img = cv2.resize(origin_frame, (im_size, im_size))

        # 预处理
        img = np.array([img])
        for i in range(img.shape[0]):
            img[i] = cv2.cvtColor(img[i], cv2.COLOR_BGR2RGB)
        images = np.array(img, dtype=np.float32)
        input_x = images / 127.5 - 1

        interpreter.set_tensor(input_details[0]['index'], input_x)
        interpreter.invoke()
        heatmap = interpreter.get_tensor(output_details[0]['index'])

        heatmap_kps = find_keypoints_from_heatmap(heatmap)[0]
        heatmap_kps = np.array(heatmap_kps)

        # Scale heatmap keypoint
        heatmap_stride = np.array([im_size / heatmap_size,
                                   im_size / heatmap_size], dtype=float)
        heatmap_kps[:, :2] = heatmap_kps[:, :2] * scale * heatmap_stride

        # Filter heatmap keypoint by confidence
        heatmap_kps_visibility = np.ones((len(heatmap_kps),), dtype=int)
        for i in range(len(heatmap_kps)):
            if heatmap_kps[i, 2] < confidence:
                heatmap_kps[i, :2] = [-1, -1]
                heatmap_kps_visibility[i] = 0

        # 可视化
        if vis_path is not None:
            draw = origin_frame.copy()
            draw = visualize_keypoints(draw, heatmap_kps[:, :2], visibility=heatmap_kps_visibility,
                                       point_color=(0, 255, 0), text_color=(255, 255, 255))
            cv2.imwrite(os.path.join(vis_path, img_name), draw)

        # xml文件保存
        xml_path = os.path.join(info_path, img_name.replace('.jpg', '_0.xml'))
        txt_file += img_name.replace('.jpg', '_0.xml\n')
        with open(xml_path, 'w', encoding='utf-8') as anno_file:
            anno_file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
            anno_file.write('<annotation>\n')
            anno_file.write('<image>%s</image>\n' % img_name.replace('.jpg', ''))
            anno_file.write('<category>person</category>\n')
            anno_file.write('<subcategory>male</subcategory>\n')
            anno_file.write('<keypoints>\n')

            for kp_name, heatmap_kp in zip(kp_names, heatmap_kps[:, :2]):
                anno_file.write('<keypoint name="%s" visible="1" x="%s" y="%s" z="0.0" zorder="0"/>\n' % (
                kp_name, heatmap_kp[0], heatmap_kp[1]))

            anno_file.write('</keypoints>\n')
            anno_file.write('<segments>\n')
            anno_file.write('</segments>\n')
            anno_file.write('</annotation>\n')

    # txt文件保存
    txt_path = os.path.join(img_dir, 'annotation_list.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(txt_file)

    # 标注配置文件
    shutil.copy(config_path, img_dir)


if __name__ == '__main__':
    model_path = r'D:\zsh\biaozhu\biaozhu_python\utils\ann_data\new\fp32_146_mobilenet_v2_all_block_aug_alpha1.tflite'  # 模型位置
    img_dir = r'D:\zsh\biaozhu\jianzi'# 图片上一级目录,图片目录名字要是"images"
    # vis_path = 'C:/Users/dell/Desktop/fsdownload/sit-up-1/img'
    config_path = r'D:\zsh\biaozhu\xml_congfig\config_person.xml'  # xml文件位置
    tflite_keypoint(model_path=model_path, img_dir=img_dir, config_path=config_path)
