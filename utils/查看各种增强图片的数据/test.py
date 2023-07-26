import os
import shutil

def classify_and_move_images(image_paths, keywords):
    # 创建文件夹来存放不同分类的图片
    for keyword in keywords:
        folder_name = f"Category_{keyword}"
        os.makedirs(folder_name, exist_ok=True)

    # 统计各分类图片数量的字典
    category_counts = {keyword: 0 for keyword in keywords}

    # 遍历每张图片，并根据关键字移动到对应的文件夹，同时统计数量
    for image_path in image_paths:
        image_name = os.path.basename(image_path)

        for keyword in keywords:
            if keyword in image_name:
                folder_name = f"Category_{keyword}"
                destination_folder = os.path.join(folder_name, image_name)
                image_path = path+'/'+image_path
                destination_folder = path+'/'+destination_folder
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                # 移动图片到对应的文件夹
                shutil.move(image_path, destination_folder)

                # 增加对应分类的图片数量
                category_counts[keyword] += 1

    # 打印各分类的图片数量
    for keyword, count in category_counts.items():
        print(f"分类 {keyword} 的图片数量为: {count}")

# 示例数据
# image_paths = [
#     'image1_Fliplr_.jpg',
#     'image2_Multiply_.jpg',
#     'image3_GaussianBlur_.jpg',
#     'image4_AddToHueAndSaturation_.jpg',
#     'image5_Affine_.jpg',
#     'image6_Fliplr_Multiply_.jpg',
#     'image7_Fliplr_AddToHueAndSaturation_.jpg',
#     'image8_Multiply_AddToHueAndSaturation_.jpg',
# ]


path = r'C:\Users\cwj\Documents\WXWork\1688856502407527\Cache\File\2023-07\old_images_aug'
path_list=[]
for file_name in os.listdir(path):
    path_list.append(file_name)
keywords = [
    # '_Multiply_',
    # '_AddToHueAndSaturation_',
    # '_Mix_',
    '_Fliplr_Multiply_',
    '_Fliplr_AddToHueAndSaturation_',
    '_Multiply_AddToHueAndSaturation_',
]

classify_and_move_images(path_list, keywords)