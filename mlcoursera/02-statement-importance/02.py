import numpy as np
import pandas
from sklearn.tree import DecisionTreeClassifier

#import sys
#sys.path.append("..")
#from shad_util import print_answer

data = pandas.read_csv('train.csv', index_col='PassengerId')

# 2. Оставьте в выборке четыре признака: класс пассажира (Pclass), цену билета (Fare),
# возраст пассажира (Age) и его пол (Sex).

x_labels = ['Pclass', 'Fare', 'Age', 'Sex']
X = data.loc[:, x_labels]

# 3. Обратите внимание, что признак Sex имеет строковые значения.

X['Sex'] = X['Sex'].map(lambda sex: 1 if sex == 'male' else 0)

# 4. Выделите целевую переменную — она записана в столбце Survived.

y = data['Survived']

# 5. В данных есть пропущенные значения — например, для некоторых пассажиров неизвестен их возраст.
# Такие записи при чтении их в pandas принимают значение nan. Найдите все объекты, у которых есть пропущенные признаки,
# и удалите их из выборки.

X = X.dropna()
y = y[X.index.values]

# 6. Обучите решающее дерево с параметром random_state=241 и остальными параметрами по умолчанию.

clf = DecisionTreeClassifier(random_state=241)
clf.fit(np.array(X.values), np.array(y.values))

# 7. Вычислите важности признаков и найдите два признака с наибольшей важностью.
# Их названия будут ответами для данной задачи (в качестве ответа укажите названия признаков через запятую или пробел,
# порядок не важен).

importances = pandas.Series(clf.feature_importances_, index=x_labels)
importantFeatures=importances.sort_values(ascending=False).head(2).index.values
answer=importantFeatures[0]+','+importantFeatures[1]
print(answer)
f1 = open('1.txt', 'w')
f1.write(str(answer))
