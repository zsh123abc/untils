import os
import json
import math
import shutil


# Initialize counters for Left, Right, and Cannot_determine
left_angle = 0
right_angle = 0
zj_angel = 0


# 用角度判断球场朝向左或右
def determine_basket_position(left_top_1, left_bottom_1, right_top_1,right_bottom_1,json_file_path, left_angle_path1, right_angle_path1, zj_angel_path1):
    global left_angle, right_angle, zj_angel
    angle = calculate_angle(right_top_1, right_bottom_1)
    if angle == None:
        zj_angel += 1
        shutil.copy(json_file_path, zj_angel_path1)
    else:
        if right_top_1[0] < right_bottom_1[0]:
            angle = calculate_angle_with_y_axis(right_top_1, right_bottom_1)
            # if  (angle >= 340 and angle <= 360) or (angle >=0 and angle <= 20):

            if  (angle >= -10 and angle <= 10):
                right_angle += 1
                # 把对应的文件存进单独的文件夹，方便查看
                shutil.copy(json_file_path, right_angle_path1)

        elif left_top_1[0] > left_bottom_1[0]:
            angle = calculate_angle_with_y_axis(left_top_1, left_bottom_1)

            if  (angle >=0 and angle <= 20) or angle >=-10:
                left_angle += 1
                shutil.copy(json_file_path, left_angle_path1)


def calculate_angle_with_y_axis(left_top_1, left_bottom_1):
    x1, y1 = left_top_1
    x2, y2 = left_bottom_1

    # 计算相对于新原点（left_top_1）的坐标偏移
    x2_rel = x2 - x1
    y2_rel = y2 - y1
    
    # 计算连线与 y 轴的夹角
    angle_rad = math.atan2(y2_rel, x2_rel)
    angle_deg = math.degrees(angle_rad)

    return angle_deg


# def calculate_angle_with_y_axis(left_top_1, left_bottom_1):
#     x1, y1 = left_top_1
#     x2, y2 = left_bottom_1

#     # 计算向量的坐标偏移
#     x_diff = x2 - x1
#     y_diff = y2 - y1
    
#     # 计算连线与 y 轴的夹角
#     angle_rad = math.atan2(y_diff, x_diff)
#     angle_deg = math.degrees(angle_rad) 

#     # 将角度转换为0到360度的范围
#     angle_deg = angle_deg if angle_deg >= 0 else angle_deg + 360
    
#     return angle_deg




# 求角度
def calculate_angle(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    # 计算斜率
    if (y2-y1==0) or (x2-x1==0): # 有些图片刚刚在正中间，导致被除数为0报错
        return None
    else:
        slope = (y2 - y1) / (x2 - x1)

    # 计算角度
    angle = math.degrees(math.atan(slope))
    if angle < 0:
        angle += 360
    print(angle)
    return angle


def process_json_folder(folder_path, left_angle_path1, right_angle_path1, zj_angel_path1):
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            json_file_path = os.path.join(folder_path, filename)
            process_json_file(json_file_path, left_angle_path1, right_angle_path1, zj_angel_path1)

def process_json_file(json_file_path, left_angle_path1, right_angle_path1, zj_angel_path1):
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    shapes = data['shapes']
    points = {}
    
    for shape in shapes:
        if shape['shape_type'] == 'point':
            points[shape['label']] = (shape['points'][0][0], shape['points'][0][1])

    if len(points) > 0:
        try:
            left_top_1 = points['left_top_1']
            left_bottom_1 = points['left_bottom_1']
            right_top_1 = points['right_top_1']
            right_bottom_1 = points['right_bottom_1']

            print("Processed:", json_file_path)
            determine_basket_position(left_top_1, left_bottom_1, right_top_1,right_bottom_1,json_file_path, left_angle_path1, right_angle_path1, zj_angel_path1)

        except KeyError as e:
            
            print("Invalid JSON file:", json_file_path)

# folder_path = r'D:\zsh\biaozhu\basketball_count\wx_all_court_test_train\json'
folder_path = r'D:\zsh\biaozhu\basketball_count\wx_all_court_test_train\left_angle\test'
# folder_path = r'D:\zsh\biaozhu\basketball_count\F_field\labelme\test'

left_angle_path1 = r'D:\zsh\biaozhu\basketball_count\wx_all_court_test_train\left_angle\json4'
right_angle_path1 = r'D:\zsh\biaozhu\basketball_count\wx_all_court_test_train\right_angle\json4'
zj_angel_path1 = r'D:\zsh\biaozhu\basketball_count\wx_all_court_test_train\zj_angel\json4'

# 如果文件夹不存在，就创建文件夹
if not os.path.exists(left_angle_path1):
    os.makedirs(left_angle_path1)
if not os.path.exists(right_angle_path1):
    os.makedirs(right_angle_path1)
if not os.path.exists(zj_angel_path1):
    os.makedirs(zj_angel_path1)

process_json_folder(folder_path, left_angle_path1, right_angle_path1, zj_angel_path1)

# print('Left:', left_count)
# print('Right:', right_count)
# print('Cannot_determine:', cannot_determine_count)

print(f"篮筐在左 边球场的数量：{left_angle} ")
print(f"篮筐在右 边球场的数量：{right_angle} ")
print(f"刚好在中间 球场的数量：{zj_angel} ")
