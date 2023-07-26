from PIL import Image
import os

# 输入和输出文件夹路径
input_folder = r"D:\zsh\biaozhu\5.5_ytxs\images\2person_wai"
output_folder = r"D:\zsh\biaozhu\5.5_ytxs\images\2_w_img"

# 循环遍历文件夹中的每个图像文件
for filename in os.listdir(input_folder):
    # 检查文件类型是否为图像
    if filename.endswith(".jpg") or filename.endswith(".png"):
        filepath = os.path.join(input_folder, filename)
        # 使用 Image.open() 创建一个图像对象
        with Image.open(filepath) as im:
            # 获取图像的原始宽度和高度
            width, height = im.size
            # 将图像裁剪为左半部分并保存到输出文件夹中
            left_half = im.crop((0, 0, width/2, height))
            left_output_path = os.path.join(output_folder, "left_" + filename)
            left_half.save(left_output_path)
            # 将图像裁剪为右半部分并保存到输出文件夹中
            right_half = im.crop((width/2, 0, width, height))
            right_output_path = os.path.join(output_folder, "right_" + filename)
            right_half.save(right_output_path)
