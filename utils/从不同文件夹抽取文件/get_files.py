import os
import shutil
# 从不同的文件夹批量移动文件至指定文件夹并删除原有文件夹

# 设置抽取文件的根目录
root_dir = r'C:\Users\cwj\Documents\WXWork\1688856502407527\Cache\File\2023-07\download'

# 定义要抽取的文件后缀
extensions = ['.mp4']

# 定义保存抽取文件的目标文件夹
target_dir = r'C:\Users\cwj\Documents\WXWork\1688856502407527\Cache\File\2023-07\video'

# 遍历所有文件夹
for root, dirs, files in os.walk(root_dir):#迭代遍历每一层的文件夹
    # 遍历所有文件 
    for file in files: 
        # 检查文件的扩展名
        if file.endswith(tuple(extensions)): 
            # 拼接文件的完整路径 
            path = os.path.join(root, file) 

            # 复制文件到目标文件夹
            # shutil.copy2(path, target_dir)

            # 移动文件到目标文件夹
            shutil.move(path, target_dir)
            # os.rmtree(root)
            shutil.rmtree(str(root))