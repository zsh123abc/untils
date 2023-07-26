import os
import shutil

def compare_folders(folder1, folder2, output_folder, output_folder2):
    # 获取文件夹1中的所有图片文件
    files1 = get_image_files(folder1)
    # 获取文件夹2中的所有图片文件
    files2 = get_image_files(folder2)
    
    # 在输出文件夹中创建一个新文件夹，用于存放只存在于一个文件夹中的图片
    output_unique_folder = os.path.join(output_folder, 'unique_images')
    output_unique_folder2 = os.path.join(output_folder2, 'unique_images')
    os.makedirs(output_unique_folder, exist_ok=True)
    os.makedirs(output_unique_folder2, exist_ok=True)
    
    # 检查文件夹1中的每个文件是否也存在于文件夹2中
    for file1 in files1:
        file1_name = os.path.basename(file1)
        file2 = os.path.join(folder2, file1_name)
        if file2 in files2:
            # 图片在两个文件夹中都存在，跳过
            continue
        else:
            # 将只存在于文件夹1中的图片复制到输出文件夹中
            shutil.copy2(file1, output_unique_folder)
    
    # 检查文件夹2中的每个文件是否也存在于文件夹1中
    for file2 in files2:
        file2_name = os.path.basename(file2)
        file1 = os.path.join(folder1, file2_name)
        if file1 in files1:
            # 图片在两个文件夹中都存在，跳过
            continue
        else:
            # 将只存在于文件夹2中的图片复制到输出文件夹中
            shutil.copy2(file2, output_unique_folder2)

def get_image_files(folder):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']  # 可根据需求添加其他图片格式的扩展名
    image_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if any(file.lower().endswith(extension) for extension in image_extensions):
                image_files.append(os.path.join(root, file))
    return image_files

# 设置输入文件夹和输出文件夹的路径
folder1 = r'D:\zsh\biaozhu\basketball_count\zsh_all_court_test_train\images'   
# folder2 = r'D:\zsh\biaozhu\original_court_img\f_519_img'
folder2 = r'D:\zsh\biaozhu\basketball_count\wx_all_court_test_train\img'
output_folder = r'D:\zsh\biaozhu\basketball_count\zsh_all_court_test_train\new_images'
output_folder2 = r'D:\zsh\biaozhu\basketball_count\zsh_all_court_test_train\new_images2'

# 比较两个文件夹中的图片并将只存在于一个文件夹中的图片另存到输出文件夹
compare_folders(folder1, folder2, output_folder, output_folder2)
