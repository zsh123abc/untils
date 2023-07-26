import cv2
import os

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

# 输入参数
image_folder = r'D:\zsh\7_5_paddle\MOT16\train\MOT16-02\img1'
video_name = r'D:\zsh\7_5_paddle\MOT16\train\MOT16-02\img1.mp4'
frame_rate = 30  # 设置帧率
width, height = (1920, 1080)  # 设置视频尺寸

# 执行函数
images_to_video(image_folder, video_name, frame_rate, width, height)
