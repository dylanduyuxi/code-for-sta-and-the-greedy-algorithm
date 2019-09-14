# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 21:55:01 2019

@author: Du
"""
import pandas as pd
import math
import numpy as np
I1=pd.read_csv('I1.csv')
I2=pd.read_csv('I2.csv')

def get_rou(I1):
    new=list()
    nu=I1.sample(frac=1)
    a=int(math.sqrt(len(I1)))
    for i in range(a):
        new.append(nu.iloc[a*i : a*i + a].values)
    return new

def getseq(I1):
    ini=get_rou(I1)
    rou=[]
    b=int(math.sqrt(len(I1)))
    for p in range(b):
        q=ini[p]
        rou.append(q[:,0])
    return rou
    

def TotalDistance(I1):
    ini=get_rou(I1)
    b=int(math.sqrt(len(I1)))
    d=[]
    ini=get_rou(I1)
    for p in range(b):
        q=ini[p]
        d1=[]
        for i in range(b-1):
            d1.append(((q[i,1]-q[i+1,1])**2+(q[i,2]-q[i+1,2])**2)**0.5)
        d1.append(((q[len(q)-1,1]-0)**2+(q[len(q)-1,2]-0)**2)**0.5)
        d1.append(((q[0,1]-0)**2+(q[0,2]-0)**2)**0.5)
        d.append(sum(d1))
        
    return sum(d)
#need to specify
fol=I2.values
rou=getseq(I2)
def Target(rou):
    b=len(rou)
    d=[]
    #need to specify
    for p in range(b):
        q=rou[p]
        d1=[]
        for i in range(b-1):
            d1.append(((fol[q[i]][1]-fol[q[i+1]][1])**2+(fol[q[i]][2]-fol[q[i]][2])**2)**0.5)
        d1.append(((fol[q[len(q)-1]][1]-0)**2+(fol[q[len(q)-1]][2]-0)**2)**0.5)
        d1.append(((fol[q[0]][1]-0)**2+(fol[q[0]][2]-0)**2)**0.5)
        d.append(sum(d1))    
    return sum(d)
#xold是我们开始随机生成的第一个可行解
xold=getseq(I2)

xnew=xold[:]
#tmax是我们设定的初始最高温度，tmin是我们设定的最低温度，cx为我们的降温系数
tmax=30000
tmin=1e-8
cx=0.98
#count用来计算新解连续没有被采用的次数
count=0
#get_new_jie用来生成随机数交换两个城市之间的位置以生成新解（手动滑稽）
def get_new_jie(xold):
    #need specify
    ti=(len(I2)**0.5)-0.5
    a=np.random.randint(0,ti)
    b=np.random.randint(0,ti)
    c=np.random.randint(0,ti)
    d=np.random.randint(0,ti)

    tempold=xold[:]

    temp=tempold[a][b]
    tempold[a][b]=tempold[c][d]
    tempold[c][d]=temp
    tempnew=tempold
    return tempnew


#主题退火过程
while(tmax>tmin):
    #在tmax温度下找到最优的解xnew
    for i in range(1,500000):
        #如果xnew更优，则直接替换xold，否者以概率d=pow(math.e,-de/tmax)接受该解
        tempnew=get_new_jie(xold)
        de=Target(tempnew)-Target(xold)
        if de<0 :
            count=1
            xold=xnew
            xnew=tempnew

        else:
            count=count+1
            d=pow(math.e,-de/tmax)
            if np.random.random()<d :
                xold = xnew
                xnew = tempnew
            else:
                pass
    #退火
    tmax = tmax * cx
    #如果连续5000次以上新解没有被接受，则说明已有解xold已经足够优，因此可以退出退火
    if count>50000 :
        break
print(count)
print(xnew)
print(Target(xnew))