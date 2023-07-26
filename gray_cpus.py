import os
import cv2 as cv
from concurrent.futures import ThreadPoolExecutor
import time

img_path = "dataset/615_flip_data/images"
new_img_path = "dataset/6.19_gray_court_voc/images"

def process_image(filename):
    img = cv.imread(os.path.join(img_path, filename), 0)
    filename_sp = filename.split(".")
    new_filename = filename_sp[0] + "_gray." + filename_sp[1]
    cv.imwrite(os.path.join(new_img_path, new_filename), img)

# 获取系统的CPU核心数
num_cpus = os.cpu_count()
# 增大线程池大小为CPU核心数的2倍
max_workers = num_cpus * 2

start_time = time.time()

# 使用增大的线程池大小处理图像
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(process_image, os.listdir(img_path))

end_time = time.time()
execution_time = end_time - start_time

print("Total execution time: ", execution_time, "seconds")
