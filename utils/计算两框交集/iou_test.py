def calculate_iou(box1, box2):
    # 解包边界框的坐标和尺寸
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    # 计算交集区域的坐标
    intersection_x = max(x1, x2)
    intersection_y = max(y1, y2)

    # 计算交集区域的宽度和高度
    intersection_w = min(x1 + w1, x2 + w2) - intersection_x
    intersection_h = min(y1 + h1, y2 + h2) - intersection_y

    # 计算交集区域的面积
    intersection_area = max(intersection_w, 0) * max(intersection_h, 0)

    # 计算并集区域的面积
    union_area = w1 * h1 + w2 * h2 - intersection_area

    # 计算IOU并返回
    iou = intersection_area / union_area if union_area > 0 else 0
    return iou

# 示例使用
bbox1 = (50, 50, 100, 100)  # 第一个边界框，(x, y, width, height)
bbox2 = (70, 80, 120, 150)  # 第二个边界框，(x, y, width, height)

iou = calculate_iou(bbox1, bbox2)
print("IOU:", iou)
