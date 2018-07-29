# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

from sklearn.metrics import roc_auc_score
#1. Загрузите данные из файла data-logistic.csv. 
#   Это двумерная выборка, целевая переменная на которой принимает 
#   значения -1 или 1.
data = pd.read_csv('data-logistic.csv', encoding='cp1251', sep=',', header=None)

y = data[0]
X = data[[1, 2]]

#2. Убедитесь, что выше выписаны правильные формулы для
#    градиентного спуска. Обратите внимание, что мы используем
#    полноценный градиентный спуск, а не его стохастический вариант!

def get_w(w1, w2, X, y, k, C, flag=1):
    l = len(y)
    summ = 1- 1/(1+ np.exp(-y * (w1*X[1]+w2*X[2])))
    if flag==1:
       w1 = w1 + k * 1/l*summ - k*C*w1
       return w1
    else:
       w2 = w2 + k * 1/l *summ - k*C*w2
       return w2    

#3. Реализуйте градиентный спуск для обычной и L2-регуляризованной
#   (с коэффициентом регуляризации 10) логистической регрессии.
#   Используйте длину шага k=0.1. В качестве начального приближения
#   используйте вектор (0, 0).

def gradient_descent(y, X, C=0.0, w1=0.0, w2=0.0, k=0.1, err=1e-5):
    max_iteration = 10000
    w1_new, w2_new = w1, w2

    for i in range(max_iteration):
        w1_new, w2_new = get_w(w1, w2, X, y, k, C), get_w(w1, w2, X, y, k, C, flag=2)
        e = np.sqrt((w1_new - w1) ** 2 + (w2_new - w2) ** 2)[0]
        print(e)
        print(err)
        if  e <= err:
            break
        else:
            print(w1_new)
            w1, w2 = w1_new, w2_new

    return [w1_new, w2_new]

#4. Запустите градиентный спуск и доведите до сходимости 
#(евклидово расстояние между векторами весов на соседних итерациях должно быть не больше 1e-5). 
#Рекомендуется ограничить сверху число итераций десятью тысячами.

w1, w2 = gradient_descent(y, X)
rw1, rw2 = gradient_descent(y, X, 10.0)


#5. Какое значение принимает AUC-ROC на обучении без регуляризации и при ее использовании? 
#Эти величины будут ответом на задание. В качестве ответа приведите два числа через пробел.
# Обратите внимание, что на вход функции roc_auc_score нужно подавать оценки вероятностей,
# подсчитанные обученным алгоритмом. Для этого воспользуйтесь сигмоидной функцией: 
#a(x) = 1 / (1 + exp(-w1 x1 - w2 x2)).
   #%% 
def a(X, w1, w2):
    return 1 / (1 + np.exp(-w1 * X[1] - w2 * X[2]))

y_score = a(X, w1, w2)
y_rscore = a(X, rw1, rw2)


auc=roc_auc_score(y, y_score)
aucr=roc_auc_score(y, y_rscore)

open('1.txt', 'w').write('{:0.3f} {:0.3f}'.format(auc, aucr))

#6. Попробуйте поменять длину шага. Будет ли сходиться алгоритм, если делать более длинные шаги?
# Как меняется число итераций при уменьшении длины шага?


#7. Попробуйте менять начальное приближение. Влияет ли оно на что-нибудь?