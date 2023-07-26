import cv2
import os
import argparse

def images_to_video(image_folder, video_name, frame_rate, width, height):
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    images.sort()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_name, fourcc, frame_rate, (width, height))

    for image in images:
        img = cv2.imread(os.path.join(image_folder, image))
        video.write(img)

    video.release()
    cv2.destroyAllWindows()

# 创建参数解析器
parser = argparse.ArgumentParser(description='Convert images to video')
parser.add_argument('--image_folder', type=str, default='路径/到/图像文件夹/', help='path to the folder containing images')
parser.add_argument('--video_name', type=str, default='输出视频名称.mp4', help='output video name')
parser.add_argument('--frame_rate', type=int, default=30, help='frame rate of the output video')
parser.add_argument('--width', type=int, default=1920, help='width of the output video')
parser.add_argument('--height', type=int, default=1080, help='height of the output video')

# 解析命令行参数
args = parser.parse_args()

# 执行函数
images_to_video(args.image_folder, args.video_name, args.frame_rate, args.width, args.height)
