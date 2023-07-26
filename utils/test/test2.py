# 创建多个目录
import os

path = 'D:/zsh/biaozhu/3.8v/3.15'
for i in range(2,11):
    os.mkdir(path+'/toulan{}'.format(i))

    os.chdir(path+'/toulan{}'.format(i))
    os.mkdir('images')

    os.mkdir('jieping')