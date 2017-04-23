import pandas
import re

data = pandas.read_csv('train.csv', index_col='PassengerId')

#Какое количество мужчн и женщин ехало на корабле
sexCounts=data['Sex'].value_counts()
f1 = open('1.txt', 'w')
answer=str(sexCounts[0])+' '+str(sexCounts[1])
f1.write(answer)
#какой части пассажиров удалось выжить в процентх округлив до двух знаков
survivedCounts=data['Survived'].value_counts()
survivedPercent=float("{0:.2f}".format(survivedCounts[1]*100/sum(survivedCounts)))
f2 = open('2.txt', 'w')
f2.write(str(survivedPercent))
#Какую долю пассажиры первого класса составляли среди всех остальныъ в процентах
firstClass=data['Pclass'].value_counts()
firstClassPercent=float("{0:.2f}".format(firstClass[1]*100/sum(firstClass)))
f3 = open('3.txt', 'w')
f3.write(str(firstClassPercent))
#Посчитайте среднее и медиану пассажиров
avg=float("{0:.2f}".format(data['Age'].mean()))
mediana=float("{0:.2f}".format(data['Age'].median()))
s=str(avg)+' '+str(mediana)
f4= open('4.txt', 'w')
f4.write(s)
#Коррелируют ли число братьев и сестер с числом родителей/детей
#Посчитать корреляцию Пиросана между SibSP и Parch
#corr=float("{0:.2f}".format(data.pivot_table(['SibSp'],['Parch']).corr()))
corr=data.corr(method='pearson').ix['SibSp', 'Parch']
f5 = open('5.txt', 'w')
f5.write(str(corr))
#самое популярное женское имя на корабле

fn = data[data['Sex'] == 'female']['Name']

def extract_first_name(name):
    m = re.search(".*\\((.*)\\).*", name)
    if m is not None:
        return m.group(1).split(" ")[0]
    # первое слово после Mrs. or Miss. or else
    m1 = re.search(".*\\. ([A-Za-z]*)", name)
    return m1.group(1)

# получаем имя с максимальной частотой
r = fn.map(lambda full_name: extract_first_name(full_name)).value_counts().idxmax()
print(r)
f6 = open('6.txt', 'w')
f6.write(r)







