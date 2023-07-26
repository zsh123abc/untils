import re,requests
import os
from urllib import parse
import cv2


def download_img(url, download_path):
    try:
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47"}
        rs=requests.get(url, headers=headers)
    except:
        for i in range(4):
            # 延长等待时间，超时设置为20秒
            rs=requests.get(url, headers=headers)
            if rs.status_code == 200:
                break

    parse_res=parse.urlparse(url)
    print(parse_res.path)
    file_parts = os.path.split(parse_res.path)
    filename = file_parts[1]

    path = os.path.join(download_path, filename)
    with open(path,'wb') as f:   #以wb类型保存，i[-2]为图片名称
        f.write(rs.content)
    return filename


def draw_content(img, rect, content):
    x, y, width, height = rect
    bg_color = (255,255,255) #白色
    cv2.rectangle(img, (x, y), (x + width, y + height), bg_color, -1)
    # txt_color =  #橙色
    cv2.putText(img, content, (x + 10, y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,165,255), 2)
    return img

def process_item(item, new_image_dir):
    for i in range(3):
        origin_txt = item[i] + "m" #跳远的距离
        origin_img_url = item[i+3] #对应的图片

        #下载并加载图片
        download_filename = download_img(origin_img_url, new_image_dir)
        origin_img_filepath = os.path.join(new_image_dir, download_filename)
        origin_img = cv2.imread(origin_img_filepath)

        #重新绘制跳远距离并写入新的文件
        draw_rect = [585, 40, 180, 80]
        new_img = draw_content(origin_img, draw_rect, origin_txt)
        new_img_filepath = os.path.join(new_image_dir, download_filename)
        cv2.imwrite(new_img_filepath,new_img)

        item[i+3] = new_img_filepath

def load_csv_data(csv_file):
    with open(csv_file, "r") as f:
        res = f.readlines()
        items = list()
        num = 0
        for cur in res:
            num = num + 1
            if num == 1:
                continue
            # strip方法去除每一行的换行符
            line = cur.strip("\n")
            item = line.split(",")
            if len(item) < 6:
                continue
            for i in range(len(item)):
                item[i] = item[i].strip(" ")
            items.append(item)
        return items

def save_csv_data(new_csv_file):
    with open(new_csv_file, "a") as f:
        #每一行写入一项数据,逗号分隔
        f.write(f"{item[0]},{item[1]},{item[2]},{item[3][8:]},{item[4][8:]},{item[5][8:]}\n")


csv_file = r"D:\new_ldty\立定跳远修改new.csv"
new_csv_file = r"D:\new_ldty\new_csv\立定跳远修改new.csv"
new_image_dir = r"D:\new_ldty\new_img_ldty"

with open(new_csv_file, "a") as f:
        #每一行写入一项数据,逗号分隔
        f.write(f"{'第一投'},{'第二投'},{'第三投'},{'地址一'},{'地址二'},{'地址三'}\n")

csv_data = load_csv_data(csv_file)
n=0
for item in csv_data:
    n+=1
    process_item(item, new_image_dir)
    save_csv_data(new_csv_file)
    print(n)