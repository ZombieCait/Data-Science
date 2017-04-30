import numpy as np
import pandas
from sklearn.tree import DecisionTreeClassifier

data = pandas.read_csv('train.csv', index_col='PassengerId')
#оставьте в выборке 4 признака: PClass, Fare, Age,Sex

x_labels=['Pclass', 'Fare','Age', 'Sex']
X=data.loc[:,x_labels]
X['Sex']=X['Sex'].map(lambda sex: 1 if sex=='male' else 0)
Y=data['Survived']
X=X.dropna() #удаляются все строки с nan
Y = Y[X.index.values]

#обучите решающее дерево
clf=DecisionTreeClassifier(random_state=241)
clf.fit(np.array(X.values), np.array(Y.values))
importantFeatures=(pandas.Series(clf.feature_importances_, index=x_labels)).sort_values(ascending=False).head(2).index.values

answer=importantFeatures[0]+','+importantFeatures[1]
print(answer)
f1 = open('1.txt', 'w')
f1.write(str(answer))