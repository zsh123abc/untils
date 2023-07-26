import numpy as np
import matplotlib.pyplot as plt

class LinearNeuralNetwork(object):
    def __init__(self, data, label,learing_rate,epoch):
        self.data = data
        self.label = label
        self.learning_rate = learing_rate
        self.W = (np.random.random(data.shape[1]) - 0.5) * 2
        self.output = 0
        self.epoch=epoch
        
        
    #更新权值
    def update(self, data, label):
        self.output = np.dot(data, self.W.T)
        # 取平均后，收敛得更快了
        delta_W = self.learning_rate * ((label - (self.output).T).dot(data))
        self.W += delta_W
        #self.output = np.sign(np.dot(self.W, data))
    #训练
    def fit(self, data, label):
        n = 0
        while n<self.epoch:
            self.update(data, label)
            o=np.sign(np.dot(data, self.W.T))#公式写错，应该是data*W，不是W*data结果不同
            n += 1
        print("epochs:", n)
        print(self.W)
        print("output：")
        print(o)
        return
    #获取权值
    def getW(self):
        return self.W
    #预测
    def predict(self, testData):
        return np.sign(np.dot(self.W, testData))
if __name__ == '__main__':
    #输入数据
    X = np.array([[1,0,0,0,0,0],[1,0,1,0,0,1],[1,1,0,1,0,0],[1,1,1,1,1,1]])
    #标签
    Y = np.array([-1,1,1,-1])
    LNN=LinearNeuralNetwork(X,Y,0.11,10000)
    LNN.fit(X,Y)
    #求解表达式
    def calculate(x,root):
        a = W[5]
        b = W[2]+x*W[4]
        c = W[0]+x*W[1]+x*x*W[3]
        if root==1:
            return (-b+np.sqrt(b*b-4*a*c))/(2*a)
        if root==2:
            return (-b-np.sqrt(b*b-4*a*c))/(2*a)
    x1 = [0,1]
    y1 = [1,0]
    #负样本
    x2 = [0,1]
    y2 = [0,1]
    W=LNN.getW()    

    xdata = np.linspace(-1,2)

    plt.figure()

    plt.plot(xdata,calculate(xdata,1),'r')
    plt.plot(xdata,calculate(xdata,2),'r')

    plt.plot(x1,y1,'bo')
    plt.plot(x2,y2,'yo')
    plt.show()

    print(W)
