# coding=utf-8
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.feature_extraction import DictVectorizer
from scipy.sparse import hstack
import re
#from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, precision_recall_curve


'''
1. Загрузите данные об описаниях вакансий и соответствующих годовых 
зарплатах из файла salary-train.csv (либо его заархивированную версию salary-train.zip).
'''
train=pd.read_csv('salary-train.csv')

'''
2. Проведите предобработку:
Приведите тексты к нижнему регистру (text.lower()).
Замените все, кроме букв и цифр, на пробелы — это облегчит дальнейшее 
разделение текста на слова. Для такой замены в строке text подходит 
следующий вызов: re.sub('[^a-zA-Z0-9]', ' ', text). 
'''
def preprocessing(text):
    return text.map(lambda t: t.lower()).replace('[^a-zA-Z0-9]', ' ', regex=True)

train['FullDescription']=preprocessing(train['FullDescription'])

'''
Примените TfidfVectorizer для преобразования текстов в векторы признаков. 
Оставьте только те слова, которые встречаются хотя бы в 5 объектах (параметр min_df у TfidfVectorizer).
'''
vectorizer=TfidfVectorizer(min_df=5)
train_vect_text=vectorizer.fit_transform(train['FullDescription'])


'''
Замените пропуски в столбцах LocationNormalized и ContractTime на специальную строку 'nan'. 
Примените DictVectorizer для получения one-hot-кодирования признаков LocationNormalized и ContractTime.
'''
train['LocationNormalized']=train['LocationNormalized'].fillna('nan')
train['ContractTime']=train['ContractTime'].fillna('nan')

encoder = DictVectorizer()

train_enc=encoder.fit_transform(train[['LocationNormalized', 'ContractTime']].to_dict('records'))

'''
Объедините все полученные признаки в одну матрицу "объекты-признаки". 
Обратите внимание, что матрицы для текстов и категориальных признаков являются разреженными.
Для объединения их столбцов нужно воспользоваться функцией scipy.sparse.hstack.
'''
X_train = hstack([train_vect_text, train_enc])
y_train=train['SalaryNormalized']

'''
3. Обучите гребневую регрессию с параметрами alpha=1 и random_state=241. 
Целевая переменная записана в столбце SalaryNormalized.
'''

ridge=Ridge(alpha=1, random_state=241)
ridge.fit(X_train, y_train)

'''
4. Постройте прогнозы для двух примеров из файла salary-test-mini.csv.
Значения полученных прогнозов являются ответом на задание. Укажите их через пробел.
'''

test=pd.read_csv('salary-test-mini.csv')
test_vect_text=vectorizer.transform(preprocessing(test['FullDescription']))
test['LocationNormalized']=test['LocationNormalized'].fillna('nan')
test['ContractTime']=test['ContractTime'].fillna('nan')
test_enc=encoder.transform(test[['LocationNormalized', 'ContractTime']].to_dict('records'))
X_test = hstack([test_vect_text, test_enc])

y_pred=ridge.predict(X_test)
open('1.txt', 'w').write('{:0.2f} {:0.2f}'.format(y_pred[0], y_pred[1]))