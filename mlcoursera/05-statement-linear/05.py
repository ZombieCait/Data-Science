import numpy as np
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import pandas


data_train=pandas.read_csv('perceptron-train.csv', header=None)
Y_train=data_train[0]
X_train=data_train.loc[:, 1:]

data_test=pandas.read_csv('perceptron-test.csv', header=None)
Y_test=data_test[0]
X_test=data_test.loc[:, 1:]

#обучение персептрона
clf = Perceptron(random_state=241)
clf.fit(X_train, Y_train)

#accuracy before
accuracy_before=accuracy_score(Y_test, clf.predict(X_test))

#Нормализуйте обучающую и тестовую выборку с помощью класса StandardScaler.
scaler=StandardScaler()
X_train_scaled=scaler.fit_transform(X_train)
X_test_scaled=scaler.transform(X_test)

#Обучите персептрон на новой выборке. Найдите долю правильных ответов на тестовой выборке.
clf = Perceptron(random_state=241)
clf.fit(X_train_scaled, Y_train)

accuracy_after=accuracy_score(Y_test, clf.predict(X_test_scaled))

#ответ
f1 = open('1.txt', 'w')
f1.write(str(float("{0:.3f}".format(accuracy_after-accuracy_before))))
