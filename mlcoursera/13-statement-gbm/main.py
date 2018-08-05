import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import log_loss
import matplotlib.pyplot as plt

#1. Загрузите выборку из файла gbm-data.csv с помощью pandas и преобразуйте ее в массив numpy 
#(параметр values у датафрейма). В первой колонке файла с данными записано, была или нет реакция
#. Все остальные колонки (d1 - d1776) содержат различные характеристики молекулы, такие как размер,
# форма и т.д. Разбейте выборку на обучающую и тестовую, используя функцию train_test_split 
#с параметрами test_size = 0.8 и random_state = 241.

data=pd.read_csv('gbm-data.csv').values

X_train, X_test, y_train, y_test = train_test_split(data[:, 1:], data[:, 0], test_size=0.8, random_state=241 )

#2. Обучите GradientBoostingClassifier с параметрами n_estimators=250, verbose=True, random_state=241
# и для каждого значения learning_rate из списка [1, 0.5, 0.3, 0.2, 0.1] проделайте следующее:
#Используйте метод staged_decision_function для предсказания качества на обучающей
# и тестовой выборке на каждой итерации.



def sigmoid(y_pred):
    # Преобразуйте полученное предсказание с помощью сигмоидной функции по формуле 1 / (1 + e^{−y_pred}),
    # где y_pred — предсказаное значение.
    return 1.0 / (1.0 + np.exp(-y_pred))

def  get_log_loss(model, X, y):
    results=[]
    for y_preds in model.staged_decision_function(X):
        results.append(log_loss(y, [sigmoid(y_pred) for y_pred in y_preds]))
    return results

def plot_log_loss(train_loss, test_loss, lr):
    plt.figure()
    plt.plot(test_loss, 'b', linewidth=2)
    plt.plot(train_loss, 'g', linewidth=2)
    plt.legend(['test', 'train'])
    plt.savefig('rate_' + str(lr) + '.png')

    min_loss_value = min(test_loss)
    min_loss_index = test_loss.index(min_loss_value)
    return min_loss_value, min_loss_index
#Вычислите и постройте график значений log-loss (которую можно посчитать с помощью функции
# sklearn.metrics.log_loss) на обучающей и тестовой выборках, а также найдите минимальное значение
# метрики и номер итерации, на которой оно достигается.

def test_model(lr):
    gb=GradientBoostingClassifier(n_estimators=250, verbose=True, random_state=241, learning_rate=lr)
    gb.fit(X_train, y_train)

    train_log_loss=get_log_loss(gb, X_train, y_train)
    test_log_loss=get_log_loss(gb, X_test, y_test)
    return plot_log_loss(train_log_loss, test_log_loss, lr)
    
min_loss_results={}    
for lr in [1, 0.5, 0.3, 0.2, 0.1]:
    min_loss_results[lr]=test_model(lr)    
     
    
#3. Как можно охарактеризовать график качества на тестовой выборке, начиная с некоторой итерации: 
#переобучение (overfitting) или недообучение (underfitting)? В ответе укажите одно из слов overfitting
 #либо underfitting.
open('1.txt', 'w').write('overfitting')
#4. Приведите минимальное значение log-loss на тестовой выборке и номер итерации, на котором оно достигается,
# при learning_rate = 0.2.

#%%
open('2.txt', 'w').write('{:0.2f} {}'.format(min_loss_results[0.2][0], min_loss_results[0.2][1]))

# 5. На этих же данных обучите RandomForestClassifier с количеством деревьев, равным количеству итераций, на котором
# достигается наилучшее качество у градиентного бустинга из предыдущего пункта, c random_state=241 и остальными
# параметрами по умолчанию. Какое значение log-loss на тесте получается у этого случайного леса? (Не забывайте, что
# предсказания нужно получать с помощью функции predict_proba)

rf=RandomForestClassifier(n_estimators=min_loss_results[0.2][1], random_state=241)
rf.fit(X_train, y_train)

rf_loss=log_loss(y_test, rf.predict_proba(X_test)[:, 1])
open('3.txt', 'w').write('{:0.2f}'.format(rf_loss))




