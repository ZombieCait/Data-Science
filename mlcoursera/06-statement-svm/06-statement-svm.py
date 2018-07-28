import pandas as pd
from sklearn.svm import SVC

data=pd.read_csv('svm-data.csv', delimiter=',', header=None)

Y=data[0]
X=data.loc[:, 1:] #not include 1 column

#training model
model=SVC(kernel='linear', C=100000, random_state=241)
model.fit(X, Y)

#numbers of supported vectors sorted in increasing
vectors=model.support_
vectors.sort()

f1 = open('1.txt', 'w')
f1.write(' '.join([str(vector+1) for vector in vectors]))