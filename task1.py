#Part 2 Task 1

import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt


I1=pd.read_csv('I1.csv')
I2=pd.read_csv('I2.csv')
I3=pd.read_csv('I3.csv')

#Task 2

def get_rou(I1):
    new=list()
    nu=I1.sample(frac=1)
    a=int(math.sqrt(len(I1)))
    for i in range(a):
        new.append(nu.iloc[a*i : a*i + a].values)
    return new

#Task 3

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

#Task 4
#need to specify the question I1, I2 or I3
fol=I2.values


def getseq(I1):
    ini=get_rou(I1)
    rou=[]
    b=int(math.sqrt(len(I1)))
    for p in range(b):
        q=ini[p]
        rou.append(q[:,0])
    return rou


def Target(rou):
    b=len(rou)
    d=[]
    
    for p in range(b):
        q=rou[p]
        d1=[]
        for i in range(b-1):
            d1.append(((fol[q[i]][1]-fol[q[i+1]][1])**2+(fol[q[i]][2]-fol[q[i+1]][2])**2)**0.5)
        d1.append(((fol[q[len(q)-1]][1]-0)**2+(fol[q[len(q)-1]][2]-0)**2)**0.5)
        d1.append(((fol[q[0]][1]-0)**2+(fol[q[0]][2]-0)**2)**0.5)
        d.append(sum(d1))    
    return sum(d)


oldrou=[]
for i in range(0,int(len(fol))):
    oldrou.append(i)
e=int(math.sqrt(len(fol)))
oldrou=np.reshape(oldrou,(e,e))

#tmax is the highest temperture
tmax=1000
tmin=0.001
cx=0.99

def swap(oldrou):
    #need specify
    ti=(len(oldrou))
    a=np.random.randint(0,ti)
    b=np.random.randint(0,ti)
    c=np.random.randint(0,ti)
    d=np.random.randint(0,ti)
    tem=oldrou.copy()
    tem[a][b],tem[c][d]=tem[c][d],tem[a][b]
    return tem

#anneal procedure
while(tmax>tmin):

    for i in range(100):
        newrou=swap(oldrou)
        diff=Target(newrou)-Target(oldrou)
        if diff<0 :
            oldrou=newrou
        else:
            d=(math.e)**(-diff/tmax)
            if np.random.random()<d :
                oldrou = newrou
            else:
                pass
    tmax = tmax*cx
    
print(oldrou)
print(Target(oldrou))

#Task 5
with open('sol.csv', 'w') as writeFile:
    writeFile.write(','.join(str(s) for s in oldrou))
    writeFile.write('\n')
    writeFile.write(str(Target(oldrou)))

#Task 6
u=int(len(oldrou))
x=[]
y=[]
for i in range(u):
    x.append(fol[oldrou[i],1])
    y.append(fol[oldrou[i],2])
q=np.zeros(u,int)
x= np.column_stack((q.T,x,q.T))
y= np.column_stack((q.T,y,q.T))

plt.grid()

for i in range(u):
    plt.plot(x[i],y[i],label="Truck %s"%(i+1))
    plt.legend(loc='upper left')