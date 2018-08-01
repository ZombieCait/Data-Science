# coding=utf-8
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# 1. Загрузите файл classification.csv. В нем записаны истинные классы объектов выборки (колонка true) и ответы
# некоторого классификатора (колонка predicted).

data = pd.read_csv('classification.csv')

# 2. Заполните таблицу ошибок классификации. Для этого подсчитайте величины TP, FP, FN и TN согласно их определениям.
# Например, FP — это количество объектов, имеющих класс 0, но отнесенных алгоритмом к классу 1.
# Ответ в данном вопросе — четыре числа через пробел.

TP, FP, FN, TN = confusion_matrix(data['true'], data['pred']).ravel()
open('1.txt', 'w').write('{} {} {} {}'.format(TP, FP, FN, TN))

# 3. Посчитайте основные метрики качества классификатора:

accuracy = accuracy_score(data['true'], data['pred'])
precision = precision_score(data['true'], data['pred'])
recall = recall_score(data['true'], data['pred'])
f1 = f1_score(data['true'], data['pred'])

open('2.txt', 'w').write('{:0.2f} {:0.2f} {:0.2f} {:0.2f}'.format(accuracy, precision, recall, f1))


# 4. Имеется четыре обученных классификатора. В файле scores.csv записаны истинные классы и значения степени
# принадлежности положительному классу для каждого классификатора на некоторой выборке:
# для логистической регрессии — вероятность положительного класса (колонка score_logreg),
# для SVM — отступ от разделяющей поверхности (колонка score_svm),
# для метрического алгоритма — взвешенная сумма классов соседей (колонка score_knn),
# для решающего дерева — доля положительных объектов в листе (колонка score_tree).
# Загрузите этот файл.

scores=pd.read_csv('scores.csv')

# 5. Посчитайте площадь под ROC-кривой для каждого классификатора. Какой классификатор имеет наибольшее значение
# метрики AUC-ROC (укажите название столбца с ответами этого классификатора)?
# Воспользуйтесь функцией sklearn.metrics.roc_auc_score.
clf_aucs=pd.DataFrame()
for clf in scores.columns[1:]:
    clf_aucs=clf_aucs.append([[clf, roc_auc_score(scores['true'], scores[clf])]])
    

open('3.txt', 'w').write(clf_aucs.sort_values(by=1, ascending=False).head(1)[0][0])



# 6. Какой классификатор достигает наибольшей точности (Precision) при полноте (Recall) не менее 70% ?
# Какое значение точности при этом получается? Чтобы получить ответ на этот вопрос, найдите все точки
# precision-recall-кривой с помощью функции sklearn.metrics.precision_recall_curve. Она возвращает три массива:
# precision, recall, thresholds. В них записаны точность и полнота при определенных порогах,указанных в массиве
# thresholds. Найдите максимальной значение точности среди тех записей, для которых полнота не меньше, чем 0.7.


