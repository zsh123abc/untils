import os
import json
import math


# Initialize counters for Left, Right, and Cannot_determine
left_count = 0
right_count = 0
cannot_determine_count = 0
left_angle = 0
right_angle = 0
zj_angel = 0

# 判断左右斜角的图片数量
# def determine_basket_position(left_top_1, left_bottom_1):
#     global left_count, right_count, cannot_determine_count,left_angle, right_angle
#     if abs(left_top_1[0] - left_bottom_1[0]) < 100:
#         cannot_determine_count += 1
#         return "Cannot_determine"
#     elif left_top_1[0] < left_bottom_1[0]:
#         left_count += 1
#         angle = calculate_angle(left_top_1, left_bottom_1)
#         if  angle >=150 and angle <= 180:
#             right_angle += 1
#         return "Left"
#     elif left_top_1[0] > left_bottom_1[0]:
#         right_count += 1
#         angle = calculate_angle(left_top_1, left_bottom_1)
#         print(angle)
#         if  angle >=0 and angle <= 30:
#             left_angle += 1
#         return "Right"


# 用角度判断球场朝向左或右
def determine_basket_position(left_top_1, left_bottom_1):
    global left_count, right_count, cannot_determine_count,left_angle, right_angle, zj_angel

    angle = calculate_angle(left_top_1, left_bottom_1)
    if angle == None:
        zj_angel += 1
    else:
        if left_top_1[0] < left_bottom_1[0]:
            if  angle >= 340 and angle <= 360:
                right_angle += 1
        elif left_top_1[0] > left_bottom_1[0]:
            if  (angle >=0 and angle <= 20) or angle >=350:
                left_angle += 1



# 求角度
def calculate_angle(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    # 计算斜率
    if (y2-y1==0) or (x2-x1==0):
        return None
    else:
        slope = (y2 - y1) / (x2 - x1)

    # 计算角度
    angle = math.degrees(math.atan(slope))
    if angle < 0:
        angle += 360
    print(angle)
    return angle


# def determine_position_and_angle(left_top_1, left_bottom_1):
#     global left_angle, right_angle
#     position = ""
#     if left_top_1[0] < left_bottom_1[0]:
#         position = "left_top_1 在 left_bottom_1 的左边"
#         angle = calculate_angle(left_top_1, left_bottom_1)
#         print(angle)
#         if  angle >=0 and angle <= 30:
#             left_angle += 1

#     elif left_top_1[0] > left_bottom_1[0]:
#         position = "left_top_1 在 left_bottom_1 的右边"
#         angle = calculate_angle(left_top_1, left_bottom_1)
#         if  angle >=150 and angle <= 180:
#             right_angle += 1
#     else:
#         position = "left_top_1 和 left_bottom_1 在同一垂直线上"

#     return position



def process_json_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            json_file_path = os.path.join(folder_path, filename)
            process_json_file(json_file_path)

def process_json_file(json_file_path):
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
            # right_top_1 = points['right_top_1']
            left_bottom_1 = points['left_bottom_1']
            # right_bottom_1 = points['right_bottom_1']
            # central_top_1 = points['central_top_1']
            print("Processed:", json_file_path)
            # basket_position = determine_basket_position(left_top_1, right_top_1, left_bottom_1, right_bottom_1, central_top_1)
            basket_position = determine_basket_position(left_top_1, left_bottom_1)

            # 求角度
            # determine_position_and_angle(left_top_1, left_bottom_1)
            
            # print("Basket position:", basket_position)
        
        except KeyError as e:
            
            print("Invalid JSON file:", json_file_path)

folder_path = r'D:\zsh\biaozhu\basketball_count\wx_all_court_test_train\json'
# folder_path = r'D:\zsh\biaozhu\basketball_count\F_field\labelme\test'

process_json_folder(folder_path)

# print('Left:', left_count)
# print('Right:', right_count)
# print('Cannot_determine:', cannot_determine_count)

print(f"左 边球场的数量：{left_angle} ")
print(f"右 边球场的数量：{right_angle} ")
print(f"刚好中间 球场的数量：{zj_angel} ")

