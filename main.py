#!/usr/bin/python3

import numpy as np

train_name = "mnist_train_100.csv"
test_name = "mnist_test_10.csv"


class NeuNet(object):
    
    def __init__(self,innodes,hidenodes,outnodes,lnrate):
        self.inodes = innodes
        self.hnodes = hidenodes
        self.onodes = outnodes
        self.lr = lnrate
        self.wih = np.random.normal(0, pow(self.hnodes,-0.5), (self.hnodes,self.inodes))
        self.who = np.random.normal(0, pow(self.onodes,-0.5), (self.onodes,self.hnodes))
        pass
    
    def query(self,ipt):
        ipt = np.dot(self.wih, ipt)
        ipt = act(ipt)
        ipt = np.dot(self.who, ipt)
        ipt = act(ipt)
        return int(np.where(ipt == np.max(ipt))[0])
    
    def train(self,input,answer):
        oi = np.dot(self.wih, input)
        oi = act(oi)
        oh = np.dot(self.who, oi)
        oh = act(oh)
        eo = answer - oh
        eh = np.dot(self.who.T, eo)
        self.who += self.lr * np.dot(eo * oh * (1 - oh), oi.T)
        self.wih += self.lr * np.dot(eh * oi * (1 - oi), input.T)
        return np.sum(eo * eo)
    
    def save(self):
        np.save("vars.npy", np.array([self.inodes, self.hnodes, self.onodes, self.lr]))
        np.save("wih.npy", self.wih)
        np.save("who.npy", self.who)
        pass
    
    def load(self):
        self.innodes, self.hnodes, self.onodes, self.lr = np.load("vars.npy")
        self.innodes, self.hnodes, self.onodes = int(self.innodes), int(self.hnodes), int(self.onodes)
        self.wih = np.load("wih.npy")
        self.who = np.load("who.npy")
        pass


def train(times):
    for i in range(times):
        for j in datas:
            ans = np.array([np.zeros(work.onodes)]).T + 0.01
            data = np.asfarray([j.split(',')]).T
            ans[int(data[0,0]),0] = 0.99
            data = data[1:] / 255 * 0.99 + 0.01
            print("No.%d: cost = %f" % (i,work.train(data,ans)))
            pass
        pass
    pass

def test():
    ret=int()
    for i in exam:
        data = np.asfarray([i.split(',')]).T
        ans = int(data[0,0])
        data = data[1:] / 255 * 0.99 + 0.01
        pdt = work.query(data)
        ret +=  pdt == ans
        print(pdt, "->", ans)
    return "%.2f%%" % (ret / len(exam) * 100)

def act(mat):
    return 1/(1+np.exp(-mat))


work = NeuNet(784, 200, 10, 0.01)
file = open(train_name, 'r')
datas = file.readlines()
file.close()
file = open(test_name, 'r')
exam = file.readlines()
file.close()


if __name__ == '__main__':
    
    cmd = input("/>")
    while True:
        if cmd == 'save':
            work.save()
            pass
        elif cmd == 'load':
            work.load()
            pass
        elif cmd == 'train':
            times = int(input("  for: "))
            train(times)
            pass
        elif cmd == 'test':
            print(test())
            pass
        elif cmd == 'exit':
            exit()
            pass
        elif cmd == 'set':
            var_name = input("  name: ")
            var_val = eval(input("  val: "))
            if var_name == 'lr':
                work.lr = var_val
            else:
                print("  '%s' is not defined" % (var_name))
        else:
            print("  Unknown command")
            pass
        cmd = input("/>")
        pass