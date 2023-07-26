import cv2

def flip_video(input_path, output_path):
    # 打开输入视频文件
    video = cv2.VideoCapture(input_path)

    # 获取输入视频的宽度、高度和帧率
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

    # 获取输入视频的编码器
    fourcc = int(video.get(cv2.CAP_PROP_FOURCC))

    # 创建输出视频的编码器和输出文件对象
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # 逐帧读取输入视频并进行左右翻转
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        
        # 水平翻转当前帧
        flipped_frame = cv2.flip(frame, 1)  # 参数 1 表示水平镜像翻转
        
        # 将翻转后的帧写入输出视频
        out.write(flipped_frame)

    # 释放视频对象和输出文件对象
    video.release()
    out.release()

# 输入视频文件路径和输出视频文件路径
input_video_path = r'C:\Users\cwj\Documents\WXWork\1688856502407527\Cache\Video\2023-07\left_two.mp4'
output_video_path = r'C:\Users\cwj\Documents\WXWork\1688856502407527\Cache\Video\2023-07\out_left_two.mp4'

# 左右翻转视频
flip_video(input_video_path, output_video_path)
