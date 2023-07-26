import urllib.request
import re
keyname="篮板"#输入商品名称
key=urllib.request.quote(keyname)
headers=("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0")
# 出现连接超时要么是因为爬虫访问过快导致对方服务器连接超时，要么是因为被发现是爬虫程序了，设置爬虫代码设置代理ip
proxies = { 
        'http': '127.0.0.1:1212',
        'https': '127.0.0.1:1212'
    }
opener=urllib.request.build_opener()
opener.addheaders=[headers,proxies]

urllib.request.install_opener(opener)
for i in range(1,100):#爬取10页
    url="https://search.jd.com/Search?keyword="+key+"&wq="+key+"&page="+str(i*2-1)#解析url
    data=urllib.request.urlopen(url).read().decode("utf-8","ignore")
    pat='data-lazy-img="(.*?)"'
    imagelist=re.compile(pat).findall(data)
    for j in range(0,len(imagelist)):
        b1=imagelist[j].replace('/n7', '/n0')
        print("第"+str(i)+"页第"+str(j)+"张爬取成功")
        newurl="http:"+b1
        file="D:/zsh/biaozhu/4.20篮板图片/"+"basketball"+str(i)+"_"+str(j)+".jpg"#file指先在指定文件夹里建立相关的文件夹才能爬取成功
        urllib.request.urlretrieve(newurl, filename=file)