
# import os

# # 删除指定文件夹里的所有文件
# folder_path = r"D:\zsh\biaozhu\3.24toulan\img"
# for filename in os.listdir(folder_path):
#     file_path = os.path.join(folder_path, filename)
#     try:
#         if os.path.isfile(file_path) or os.path.islink(file_path):
#             os.unlink(file_path)
#         elif os.path.isdir(file_path):
#             os.rmdir(file_path)
#     except Exception as e:
#         print('Failed to delete %s. Reason: %s' % (file_path, e))

import requests
def test_upload_file():
    test_url = "http://httpbin.org/post"
    test_url2 = "http://192.168.100.98:1080/papi/filetransfer/uploadfile"
    test_file = open("test.xml", "rb")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
               ,'Content-Type': 'multipart/form-data'}

    test_response = requests.post(test_url2,headers=headers, files = {"form_field_name": test_file})
    
    print(test_response.status_code)
    if test_response.ok:
        print("Upload completed successfully!") 
        print(test_response.text)
    else:
        print("Something went wrong!")

    print(test_response.request.headers)

if __name__ == '__main__':
    test_upload_file()