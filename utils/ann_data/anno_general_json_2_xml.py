import json
import os
import argparse
import shutil


parser = argparse.ArgumentParser(description='visualized annotations json file.')
parser.add_argument('-json_path', metavar='json_annotation_file_path', type=str,
                    help='path to the json annotations json file.', required=False)
parser.add_argument('-config_path', metavar='config_path', type=str,
                    help='path to the config directory.', required=False)
parser.add_argument('-save_path', metavar='image_save_path', type=str,
                    help='path to the image saving.', required=False)
args = parser.parse_args()


def json_2_xml(save_path, json_path, config_path):
    info_path = os.path.join(save_path, 'info')
    os.makedirs(info_path, exist_ok=True)
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    kp_names = ['B_Head', 'Neck', 'L_Shoulder', 'R_Shoulder',
                'L_Elbow', 'R_Elbow', 'L_Wrist', 'R_Wrist',
                'L_Hip', 'R_Hip', 'L_Knee', 'R_Knee', 'L_Ankle', 'R_Ankle']
    txt_file = ''
    for i in data:
        img_name = i['image'].split('/')[-1].replace('.jpg', '')
        kps = i['points']
        # xml文件保存
        xml_path = os.path.join(info_path, img_name + '_0.xml')
        txt_file += img_name + '_0.xml\n'
        with open(xml_path, 'w', encoding='utf-8') as anno_file:
            anno_file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
            anno_file.write('<annotation>\n')
            anno_file.write('<image>%s</image>\n' % img_name)
            anno_file.write('<category>person</category>\n')
            anno_file.write('<subcategory>male</subcategory>\n')
            anno_file.write('<keypoints>\n')

            for kp_name, heatmap_kp in zip(kp_names, kps):
                anno_file.write('<keypoint name="%s" visible="1" x="%s" y="%s" z="0.0" zorder="0"/>\n' % (
                    kp_name, heatmap_kp[0], heatmap_kp[1]))

            anno_file.write('</keypoints>\n')
            anno_file.write('<segments>\n')
            anno_file.write('</segments>\n')
            anno_file.write('</annotation>\n')
    # txt文件保存
    txt_path = os.path.join(save_path, 'annotation_list.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(txt_file)

    # 标注配置文件
    shutil.copy(config_path, save_path)


if __name__ == '__main__':
    json_path = args.json_path
    save_path = args.save_path
    config_path = args.config_path
    json_2_xml(save_path, json_path, config_path)
