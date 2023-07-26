# _*_ coding: utf-8 _*_
import requests
import sys
'''
遇到不懂的问题？Python学习交流群：1136201545满足你的需求，资料都已经上传群文件，可以自行下载！
'''
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36" }

##去重方法
def distinct_data():
    ##读取txt中文档的url列表
    datalist_blank=[]
    pathtxt=r'D:\zsh\biaozhu\biaozhu_python\utils\down_dy_video\video_list.txt'
    with open(pathtxt) as f:
        f_data_list=f.readlines()#d得到的是一个list类型
        for a in f_data_list:
            datalist_blank.append(a.strip())#去掉\n strip去掉头尾默认空格或换行符
    # print(datalist)
    data_dict={}
    for data in datalist_blank:
        #print(type(data),data,'\n')
        #print(data.split('/'),'\n',data.split('/').index('m'),'\n')
        #url中以/为切分,在以m为切分   ##把m后面的值放进字典key的位置，利用字典特性去重
        data_sp = data.split('/')
        if int(data_sp.index('m'))==4 :#此处为v6开头的url
            #print(data,44,data.split('/')[5])
            data_key1=data.split("/")[5]
            data_dict[data_key1]=data
        elif int(data.split('/').index('m'))==6: #此处为v1或者v3或者v9开头的url
            #print(data,66,data.split('/')[7],type(data.split('/')[7]))
            data_key2=data.split("/")[7]
            data_dict[data_key2] =data
    #print(len(data_dict),data_dict)
    data_new=[]
    for x,y in data_dict.items():
        data_new.append(y)
    return data_new

def responsedouyin():
    data_url=distinct_data()
    # 使用request获取视频url的内容
    # stream=True作用是推迟下载响应体直到访问Response.content属性
    # 将视频写入文件夹
    num = 1
    for url in data_url:
        res = requests.get(url,stream=True,headers=headers)
        #res = requests.get(url=url, stream=True, headers=headers)
        #定义视频存放的路径
        pathinfo = r'D:\zsh\biaozhu\biaozhu_python\utils\down_dy_video\video\%d.mp4' % num  #%d 用于整数输出   %s用于字符串输出
        # 实现下载进度条显示，这一步需要得到总视频大小
        total_size = int(res.headers['Content-Length'])
        #print('这是视频的总大小：',total_size)
        #设置流的起始值为0
        temp_size = 0
        if res.status_code == 200:
            with open(pathinfo, 'wb') as file:
                #file.write(res.content)
                #print(pathinfo + '下载完成啦啦啦啦啦')
                num += 1
                #当流下载时，下面是优先推荐的获取内容方式，iter_content()函数就是得到文件的内容，指定chunk_size=1024，大小可以自己设置哟，设置的意思就是下载一点流写一点流到磁盘中
                for chunk in res.iter_content(chunk_size=1024):
                    if chunk:
                        temp_size += len(chunk)
                        file.write(chunk)
                        file.flush() #刷新缓存
                #############下载进度条部分start###############
                        done = int(50 * temp_size / total_size)
                        #print('百分比:',done)
                        sys.stdout.write("\r[%s%s] %d % %" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size)+" 下载信息："+pathinfo + "下载完成啦啦啦啦啦")
                        sys.stdout.flush()#刷新缓存
                #############下载进度条部分end###############
                print('\n')#每一条打印在屏幕上换行输出


# if __name__ == '__main__':
    # responsedouyin()
import requests
import urllib.request
def get_url(url):
    headers = {'user-agent': 'mobile'}
    req = requests.get(url, headers=headers, verify=False)
    data = req.json()
    for data in data['aweme_list']:
        name = data['desc'] or data['aweme_id']
        url = data['video']['play_addr']['url_list'][0]
        urllib.request.urlretrieve(url, filename=name + '.mp4')
if __name__ == "__main__":
    get_url('https://api.amemv.com/aweme/v1/aweme/post/?max_cursor=0&user_id=98934041906&count=20&retry_type=no_retry&mcc_mnc=46000&iid=58372527161&device_id=56750203474&ac=wifi&channel=huawei&aid=1128&app_name=aweme&version_code=421&version_name=4.2.1&device_platform=android&ssmix=a&device_type=STF-AL10&device_brand=HONOR&language=zh&os_api=26&os_version=8.0.0&uuid=866089034995361&openudid=008c22ca20dd0de5&manifest_version_code=421&resolution=1080*1920&dpi=480&update_version_code=4212&_rticket=1548080824056&ts=1548080822&js_sdk_version=1.6.4&as=a1b51dc4069b2cc6252833&cp=dab7ca5f68594861e1[wIa&mas=014a70c81a9db218501e1433b04c38963ccccc1c4cac4c6cc6c64c')
