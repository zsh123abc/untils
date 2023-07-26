import os
import shutil

# 源文件夹路径列表
path = r'D:\zsh\biaozhu\骨骼点\引体向上\4.23引体向上_背身\ytxs'
path_list = os.listdir(path)
# source_folders = [path_list]

# 目标文件夹路径
destination_folder = r"D:\zsh\biaozhu\骨骼点\引体向上\4.23引体向上_背身\img"

# 遍历源文件夹中的所有文件
for source_folder in path_list:
    source_folder = path +'/'+ source_folder
    for filename in os.listdir(source_folder):
        # 如果文件是图片
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # 拼接源文件路径
            source_file_path = os.path.join(source_folder, filename)
            # 拼接目标文件路径
            destination_file_path = os.path.join(destination_folder, filename)
            # 复制文件到目标文件夹
            shutil.copyfile(source_file_path, destination_file_path)



