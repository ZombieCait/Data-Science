import pandas as pd
from sklearn.decomposition import PCA
from numpy import corrcoef


'''
1. Загрузите данные close_prices.csv. 
В этом файле приведены цены акций 30 компаний на закрытии торгов за каждый день периода.
'''
data = pd.read_csv('close_prices.csv')
X = data[data.columns[1:]]
'''
2. На загруженных данных обучите преобразование PCA с числом компоненты равным 10.
Скольких компонент хватит, чтобы объяснить 90% дисперсии? 
'''
pca = PCA(10)
pca.fit(X.values)


n_components = [10-i for i in range(10) if round(pca.explained_variance_ratio_[:10-i].sum(), 2 )>0.9][-1]

open('1.txt', 'w').write(str(n_components))
'''
3. Примените построенное преобразование к исходным данным и возьмите значения первой компоненты.
'''
X_comp = pca.transform(X.values)
comp0=X_comp[:, 0]

'''
4. Загрузите информацию об индексе Доу-Джонса из файла djia_index.csv. 
Чему равна корреляция Пирсона между первой компонентой и индексом Доу-Джонса?
'''

djia_index = pd.read_csv('djia_index.csv')
coef = corrcoef(comp0, djia_index['^DJI'])
open('2.txt', 'w').write(str(coef[1, 0]))

'''
5. Какая компания имеет наибольший вес в первой компоненте? Укажите ее название с большой буквы.
'''
main_comp=pd.DataFrame(pca.components_[0],X.columns).sort_values(by=0, ascending=False).index[0]
open('3.txt', 'w').write(main_comp)

