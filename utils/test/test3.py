import os

folder_path = r'D:\zsh\biaozhu\3.28toulan_5tag\images2'  # 要删除文件所在的文件夹路径

file_list = os.listdir(folder_path)  # 获取文件夹中的所有文件名

for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)  # 拼接文件路径
    os.remove(file_path)  # 删除文件