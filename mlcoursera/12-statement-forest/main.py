import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.cross_validation import KFold
from sklearn.metrics import r2_score
import numpy as np
import matplotlib.pyplot as plt
#1. Загрузите данные из файла abalone.csv. Это датасет, в котором требуется предсказать
#возраст ракушки (число колец) по физическим измерениям.

data=pd.read_csv('abalone.csv')

#2. Преобразуйте признак Sex в числовой: значение F должно перейти в -1, I — в 0, M — в 1.
#Если вы используете Pandas, то подойдет следующий код: data['Sex'] = data['Sex'].map(lambda x: 1 if x == 'M' else (-1 if x == 'F' else 0))
sex={'F': -1,
     'I': 0,
     'M': 1 }

data['Sex']=data['Sex'].map(lambda x: sex[x])

#3. Разделите содержимое файлов на признаки и целевую переменную. В последнем столбце записана целевая
#переменная, в остальных — признаки.

X=data.drop(data.columns[-1], axis=1)
y=data[data.columns[-1]]

#4. Обучите случайный лес (sklearn.ensemble.RandomForestRegressor) с различным числом деревьев:
#от 1 до 50 (не забудьте выставить "random_state=1" в конструкторе). 
#Для каждого из вариантов оцените качество работы полученного леса на кросс-валидации по 5 блокам. 
#Используйте параметры "random_state=1" и "shuffle=True" при создании генератора кросс-валидации 
#sklearn.cross_validation.KFold. В качестве меры качества воспользуйтесь коэффициентом детерминации 
#(sklearn.metrics.r2_score).
#5. Определите, при каком минимальном количестве деревьев случайный лес показывает качество 
#на кросс-валидации выше 0.52. Это количество и будет ответом на задание.

scores=[]
flag=0
cv=KFold(y.size, shuffle=True, n_folds=5, random_state=1)
for i in range(1,50):
    score=np.mean(cross_val_score(RandomForestRegressor(n_estimators=i, random_state=1), X=X, y=y, cv=cv, scoring='r2'))
    scores.append(score)
    if (score>=0.52) & (flag==0):
        print(i, score)
        open('1.txt', 'w').write(str(i))
        flag=1
    

#6. Обратите внимание на изменение качества по мере роста числа деревьев. Ухудшается ли оно?
        
plt.plot(scores)
plt.xlabel('n_estimators')
plt.ylabel('score')
plt.savefig('estimators_score.png')