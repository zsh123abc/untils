# coding: utf-8
 
# In[ ]:
 
import numpy as np
import matplotlib.pyplot as plt
 
# In[ ]:

X = np.array([[1,0,0,0,0,0],
              [1,0,1,0,0,1],
              [1,1,0,1,0,0],
              [1,1,1,1,1,1]])

#标签
Y = np.array([-1,1,1,-1])

#权值初始化，取值范围-1到1
W = (np.random.random(X.shape[1])-0.5)*2
print("初始权值：",W)
#学习率设置
lr = 0.21
#计算迭代次数
n = 0
#神经网络输出
O = 0
 
#更新权值
def update():
    #加了global，则可以在函数内部对函数外的对象进行操作了，也可以改变它的值了
    global X,Y,W,lr,n
    n+=1#记录迭代次数
    #矩阵乘，X 三行散列矩阵 W
    O = np.dot(X,W.T)
    #改变的权值公式
    W_C = lr*((Y-O.T).dot(X))/int(X.shape[0])

    W = W + W_C


# In[ ]:

#循环更新权值
for _ in range(1000):
    update()#更新权值

# 收敛条件为迭代次数
O = np.dot(X,W.T)
print("权值：",W)
print("最后逼近值:",O)


#画图 

#正样本
x1 = [0,1]
y1 = [1,0]
#负样本
x2 = [0,1]
y2 = [0,1]

#根据权值计算分界线的斜率以及截距

def calculate(x,root):
    a = W[5]
    b = W[2]+x*W[4]
    c = W[0]+x*W[1]+x*x*W[3]
    if root == 1:#第一个根
        return (-b+np.sqrt(b*b-4*a*c))/(2*a)
    if root == 2:#第二个根
        return (-b-np.sqrt(b*b-4*a*c))/(2*a)

xdata = np.linspace(-1,2)

# plt.figure()
# plt.plot(xdata,calculate(xdata,1),'r')#用红色
# plt.plot(xdata,calculate(xdata,2),'r')#用红色
# plt.plot(x1,y1,'bo')#用蓝色
# plt.plot(x2,y2,'yo')#用黄色
# plt.show()