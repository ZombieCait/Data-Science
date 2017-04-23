import numpy as np
X=np.random.normal(loc=1,scale=10,size=(1000,50))


mean=np.mean(X,axis=0)#axis =0 по столбцам, axis=1 по строкам
std=np.std(X, axis=0)
X_norm=((X-mean)/std)
print(X_norm)

print(np.nonzero(np.sum(X,axis=1)>200))#получение индексов строк, сумма элементов которых превосходит 200

A=np.eye(3)
B=np.eye(3)

AB=np.vstack((A,B))# функция вертикальной стыковки матриц
print(AB)