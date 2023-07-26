# 重命名文件
import os

for i in range(1,11):
    path = r'D:\zsh\biaozhu\3.8v\3.15\toulan{}\jieping\images'.format(i)
    cont = 0
    for filename in os.listdir(path):
        cont+=1
        old_name = filename[:-4]
        new_name = 'toulan{}{}'.format(i,cont)
        newfilename = filename.replace(old_name, new_name)
        os.rename(filename, newfilename)