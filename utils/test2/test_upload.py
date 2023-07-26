
import requests

# cookies = {
#     'token': 'Bearer%20eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJxaXdlbi1jbXMiLCJleHAiOjE2ODEzNTQzNDQsInN1YiI6IntcInVzZXJJZFwiOjEwfSIsImF1ZCI6InFpd2Vuc2hhcmUiLCJpYXQiOjE2ODA3NDk1NDR9.X-jZKCa4ZW3AtALFRlD-S9-ZkOgjg0VAdx2z3FN6mNw',
#     'JSESSIONID': '02BC34C0BB65A4C1B5DC0AC42D943CCF',
# }

# headers = {
#     'Host': '192.168.100.98:1080',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
#     'Accept': '*/*',
#     'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#     'token': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJxaXdlbi1jbXMiLCJleHAiOjE2ODEzNTQzNDQsInN1YiI6IntcInVzZXJJZFwiOjEwfSIsImF1ZCI6InFpd2Vuc2hhcmUiLCJpYXQiOjE2ODA3NDk1NDR9.X-jZKCa4ZW3AtALFRlD-S9-ZkOgjg0VAdx2z3FN6mNw',
#     'Referer': 'http://192.168.100.98:1080/?filePath=%2Fzsh%2Flabel_data%2Fimages%2F&fileType=0',
#     # 'Cookie': 'token=Bearer%20eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJxaXdlbi1jbXMiLCJleHAiOjE2ODEzNTQzNDQsInN1YiI6IntcInVzZXJJZFwiOjEwfSIsImF1ZCI6InFpd2Vuc2hhcmUiLCJpYXQiOjE2ODA3NDk1NDR9.X-jZKCa4ZW3AtALFRlD-S9-ZkOgjg0VAdx2z3FN6mNw; JSESSIONID=02BC34C0BB65A4C1B5DC0AC42D943CCF',
# }

# params = {
#     'chunkNumber': '1',
#     'chunkSize': '1048576',
#     'currentChunkSize': '163134',
#     'totalSize': '163134',
#     'identifier': 'c7f5df281077967cab5dc238ed67c840',
#     'filename': 'chuan.jpg',
#     'relativePath': 'chuan.jpg',
#     'totalChunks': '1',
#     'filePath': '/zsh/label_data/images/',
#     'isDir': '0',
# }

# response = requests.get('http://192.168.100.98:1080/api/filetransfer/uploadfile', params=params, cookies=cookies, headers=headers)

# response


def test_upload_file():
    test_url = "http://httpbin.org/post"
    test_url2 = "http://192.168.100.98:1080/api/filetransfer/uploadfile"
    test_file = open("1.txt", "rb")

    cookies = {
    'token': 'Bearer%20eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJxaXdlbi1jbXMiLCJleHAiOjE2ODEzODk0NDgsInN1YiI6IntcInVzZXJJZFwiOjEwfSIsImF1ZCI6InFpd2Vuc2hhcmUiLCJpYXQiOjE2ODA3ODQ2NDh9.7xoNtdJWCu7OiHmrYgWy8CAl2PLsUAQj5aeWImYx6_8',
    'JSESSIONID': 'E716A93AAF983A500536C77A6781B60D',
    }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
                # ,'Cookie': 'token=Bearer%20eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJxaXdlbi1jbXMiLCJleHAiOjE2ODEzODk0NDgsInN1YiI6IntcInVzZXJJZ'
                ,'Referer': 'http://192.168.100.98:1080/?filePath=%2Fzsh%2Flabel_data%2Fimages%2F&fileType=0'
                ,'Origin': 'http://192.168.100.98:1080'
                ,'Content-Type':'multipart/form-data;boundary=-'}

    test_response = requests.post(url=test_url2, headers=headers, cookies=cookies, files = {"file": test_file})
    
    print(test_response.status_code)
    if test_response.ok:
        print("Upload completed successfully!") 
        print(test_response.text)
    else:
        print("Something went wrong!")

    print(test_response.request.headers)


def test2():
    

    import requests

    cookies = {
        'token': 'Bearer%20eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJxaXdlbi1jbXMiLCJleHAiOjE2ODEzODk0NDgsInN1YiI6IntcInVzZXJJZFwiOjEwfSIsImF1ZCI6InFpd2Vuc2hhcmUiLCJpYXQiOjE2ODA3ODQ2NDh9.7xoNtdJWCu7OiHmrYgWy8CAl2PLsUAQj5aeWImYx6_8',
        'JSESSIONID': 'E716A93AAF983A500536C77A6781B60D',
    }

    headers = {
        'Host': '192.168.100.98:1080',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'token': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJxaXdlbi1jbXMiLCJleHAiOjE2ODEzODk0NDgsInN1YiI6IntcInVzZXJJZFwiOjEwfSIsImF1ZCI6InFpd2Vuc2hhcmUiLCJpYXQiOjE2ODA3ODQ2NDh9.7xoNtdJWCu7OiHmrYgWy8CAl2PLsUAQj5aeWImYx6_8',
        'Content-Type': 'multipart/form-data; boundary=---------------------------259233609121957964591672003062',
        'Origin': 'http://192.168.100.98:1080',
        'Referer': 'http://192.168.100.98:1080/?filePath=%2Fzsh%2Flabel_data%2Fimages%2F&fileType=0',
        # 'Cookie': 'token=Bearer%20eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJxaXdlbi1jbXMiLCJleHAiOjE2ODEzODk0NDgsInN1YiI6IntcInVzZXJJZFwiOjEwfSIsImF1ZCI6InFpd2Vuc2hhcmUiLCJpYXQiOjE2ODA3ODQ2NDh9.7xoNtdJWCu7OiHmrYgWy8CAl2PLsUAQj5aeWImYx6_8; JSESSIONID=E716A93AAF983A500536C77A6781B60D',
    }

    test_file = open("1.txt", "rb")
    response = requests.post('http://192.168.100.98:1080/papi/filetransfer/uploadfile', cookies=cookies, headers=headers, files={'file':test_file})
    print(response.text)


if __name__ == '__main__':
    # test_upload_file()
    # test2()

    import os
    import random
    import shutil

    # 源文件夹列表
    path = r'D:\zsh\biaozhu\4.24lanban\img'
    source_folders = os.listdir(path)
    
    # 目标文件夹
    target_folder = r'D:\zsh\biaozhu\4.24lanban\images'

    # 从每个源文件夹中随机选择一张图片复制到目标文件夹
    for folder in source_folders:
        img_path = path +'/'+ folder
        # 获取该文件夹下所有图片文件的路径
        f = os.listdir(img_path)
        image_files = [os.path.join(img_path, f[0])]
        # 如果该文件夹下有图片，则随机选择一张图片复制到目标文件夹
        if image_files:
            # 随机选择一张图片
            selected_image = random.choice(image_files)
            # 复制到目标文件夹
            shutil.copy(selected_image, target_folder)
