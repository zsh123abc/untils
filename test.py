import os

# 定义要检查的字符串列表
keywords = ['_Fliplr_', '_Multiply_', '_AddToHueAndSaturation_', '_Mix_']

# 定义要遍历的文件夹路径
dir_path = '/path/to/folder'

# 遍历文件夹和文件
for root, dirs, files in os.walk(dir_path):
    for file_name in files:
        # 检查文件名是否包含指定字符串
        for keyword in keywords:
            if keyword in file_name:
                # 删除文件
                os.remove(os.path.join(root, file_name))
                print(f"删除文件：{os.path.join(root, file_name)}")
