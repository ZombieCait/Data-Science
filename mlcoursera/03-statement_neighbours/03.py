import pandas
import sklearn
from sklearn.cross_validation import KFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier


#загрузка данных
data=pandas.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data", header=None)
#извлечение признаков и данных, классы - первая колонка, признаки остальные
Y=data[0]
X=data.loc[:, 1:]#добавляю в конец столбцы из data

#Оценку качества необходимо провести методом кросс-валидации по 5 блокам (5-fold).
#  Создайте генератор разбиений, который перемешивает выборку перед формированием блоков (shuffle=True).
#  Для воспроизводимости результата, создавайте генератор KFold с фиксированным параметром random_state=42.
#  В качестве меры качества используйте долю верных ответов (accuracy).


kfold= KFold(n=len(X), n_folds=5, shuffle=True,random_state=42)

# 4. Найдите точность классификации на кросс-валидации для метода k ближайших соседей
# (sklearn.neighbors.KNeighborsClassifier), при k от 1 до 50. При каком k получилось оптимальное качество?
# Чему оно равно (число в интервале от 0 до 1)? Данные результаты и будут ответами на вопросы 1 и 2.

def test_accuracy(kfold, X, Y):
    scores=list()
    k_range=range(1,51)
    for k in k_range:
        cls=KNeighborsClassifier(n_neighbors=k)
        scores.append(cross_val_score( cls, X, Y, cv=kfold, scoring='accuracy' ))

    return pandas.DataFrame(scores, k_range).mean(axis=1).sort_values(ascending=False)


accuracy=test_accuracy(kfold, X,Y)
top_accuracy=accuracy.head(1)
f1 = open('1.txt', 'w')
f1.write(str(top_accuracy.index[0]))
f2 = open('2.txt', 'w')
f2.write(str(float("{0:.2f}".format(top_accuracy.values[0]))))


#масштабирование признаков
X=sklearn.preprocessing.scale(X)
accuracy=test_accuracy(kfold, X, Y)

#ответ 3,4

top_accuracy=accuracy.head(1)
f3 = open('3.txt', 'w')
f3.write(str(top_accuracy.index[0]))

f4 = open('4.txt', 'w')
f4.write(str(float("{0:.2f}".format(top_accuracy.values[0]))))

