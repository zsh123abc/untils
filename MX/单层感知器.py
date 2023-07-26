# coding: utf-8
 
# In[ ]:
 
import numpy as np
import matplotlib.pyplot as plt
 
# In[ ]:
 
#输入数据
X = np.array([[1,3,3],
              [1,4,3],
              [1,1,1]])
#标签
Y = np.array([1,1,-1])
#权值初始化，1行3列，取值范围-1到1
W = (np.random.random(3)-0.5)*2
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
    O = np.sign(np.dot(X,W.T))
    #改变的权值公式
    W_C = lr*((Y-O.T).dot(X))/int(X.shape[0])

    W = W + W_C


# In[ ]:

#循环更新权值
for _ in range(10):
    update()#更新权值
    print("当前权值:",W)#打印当前权值
    print(n)#打印迭代次数

    # np.sign：激活函数，负数为-1，0为0，正数为1
    # np.dot()矩阵乘法
    np_dot = np.dot(X,W.T)
    O = np.sign(np_dot)#计算当前输出
    print("当前输出:",O)
    #.all()判断两个矩阵是否全部想等
    #O：实际值，Y.T预期值
    #Y.T对矩阵进行转置,转置:行变为列，列变为行
    if(O == Y.T).all(): #如果实际输出等于期望输出，模型收敛，循环结束
        print('Finished')
        print('epoch:',n)
        break


#画图 

#正样本
x1 = [3,4]
y1 = [3,3]
#负样本
x2 = [1]
y2 = [1]
 
#根据权值计算分界线的斜率以及截距
k = -W[1]/W[2]
d = -W[0]/W[2]
print('k=',k)
print('d=',d)
 
xdata = np.linspace(0,5)
 
plt.figure()
plt.plot(xdata,xdata*k+d,'r')
plt.plot(x1,y1,'bo')
plt.plot(x2,y2,'yo')
plt.show()