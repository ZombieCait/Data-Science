import pandas as pd
import numpy as np
from sklearn import datasets, grid_search
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import KFold

newsgroups = datasets.fetch_20newsgroups(
                    subset='all',
                    categories=['alt.atheism', 'sci.space']
             )
X=newsgroups.data
Y=newsgroups.target

vectorizer=TfidfVectorizer()
vectorizer.fit_transform(X)

tfidfMatrix=vectorizer.transform(X)
grid = {'C': np.power(10.0, np.arange(-5, 6))}
cv = KFold(Y.size, n_folds=5, shuffle=True, random_state=241)
model = SVC(kernel='linear', random_state=241)
gs = grid_search.GridSearchCV(model, grid, scoring='accuracy', cv=cv)
gs.fit(tfidfMatrix, Y)

score=0
C=0
for s in gs.grid_scores_:
   if s.mean_validation_score >score:
       score = s.mean_validation_score
       C=s.parameters['C']

model = SVC(kernel='linear', random_state=241, C=C)
model.fit(vectorizer.transform(X), Y)
#%%
feature_mapping = vectorizer.get_feature_names()
coef=pd.DataFrame(model.coef_.data, model.coef_.indices)
top_words=coef[0].map(lambda w: abs(w)).sort_values(ascending=False).head(10).index.map(lambda i: feature_mapping[i]).tolist()
top_words.sort()


open('1.txt', 'w').write(','.join(top_words))