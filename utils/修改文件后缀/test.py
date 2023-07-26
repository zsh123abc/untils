import os
# 文件加上后缀
# path of the folder
folder_path = r'D:\zsh\biaozhu\4.26篮板图片\video'

# list of files in the folder
files_list = os.listdir(folder_path)

ext = ''#要替换的文件后缀

# change file extension
for file_name in files_list: 
    full_file_name = os.path.join(folder_path, file_name) 
    if os.path.isfile(full_file_name): 
        file_name, file_ext = os.path.splitext(full_file_name) 
    # if file_ext == '':
    #     new_file_name = file_name + '.mp4' 
    #     os.rename(full_file_name, new_file_name)
    if file_ext == ext:
        new_file_name = file_name[:-7] + '.mp4' 
        os.rename(full_file_name, new_file_name)