import sklearn.datasets
from numpy import linspace
import pandas
from sklearn.cross_validation import KFold, cross_val_score
from sklearn.neighbors import KNeighborsRegressor

#загрузка данных
data=sklearn.datasets.load_boston()
X=data.data
Y=data.target

#преведение признаков к одному масштабу
X=sklearn.preprocessing.scale(X)

# 3. Переберите разные варианты параметра метрики p по сетке от 1 до 10 с таким шагом, чтобы всего было протестировано
# 200 вариантов (используйте функцию numpy.linspace). Используйте KNeighborsRegressor с n_neighbors=5 и
# weights='distance' — данный параметр добавляет в алгоритм веса, зависящие от расстояния до ближайших соседей.
# В качестве метрики качества используйте среднеквадратичную ошибку (параметр scoring='mean_squared_error' у
# cross_val_score). Качество оценивайте, как и в предыдущем задании, с помощью кросс-валидации по 5 блокам с
# random_state = 42, не забудьте включить перемешивание выборки (shuffle=True).
def test_mean_squared_error(kfold, X, y):
    scores = list()
    p_range = linspace(1, 10, 200)#по сетке от 1 до 10 с таким шагом, чтобы всего было протестировано 200 вариантов
    for p in p_range:
        model = KNeighborsRegressor(p=p, n_neighbors=5, weights='distance')
        scores.append(cross_val_score(model, X, y, cv=kfold, scoring='neg_mean_squared_error'))

    return pandas.DataFrame(scores, p_range).max(axis=1).sort_values(ascending=False)


kfold= KFold(n=len(X), n_folds=5, shuffle=True,random_state=42)
mean_squared_error=test_mean_squared_error(kfold, X,Y)

#Определите, при каком p качество на кросс-валидации оказалось оптимальным.
top=mean_squared_error.head(1)
f1 = open('1.txt', 'w')
f1.write(str(float("{0:.2f}".format(top.index[0]))))
