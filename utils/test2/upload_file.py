import os
import shutil
from PIL import Image

# Define the source directory and destination directory
src_dir = r"D:\zsh\biaozhu\3.29_toulan\3.28_25000img\images_12349\4.21_篮球图片"
dst_dir = r"D:\zsh\biaozhu\3.29_toulan\3.28_25000img\images_12349\4.21_篮球图片2"

# Loop through all files in the source directory
for filename in os.listdir(src_dir):
    # Check if the file is an image
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        # Open the image file using PIL
        with Image.open(os.path.join(src_dir, filename)) as img:
            # Get the dimensions of the image
            width, height = img.size
            # Check if the dimensions are below 1500
        if width * height > 1500:
                # Get the size of the image in bytes
                size = os.path.getsize(os.path.join(src_dir, filename))
                # Check if the size is greater than 0
                if size > 0:
                    # Move the file to the destination directory
                    shutil.move(os.path.join(src_dir, filename), os.path.join(dst_dir, filename))





