import numpy as np
import re

def getDictionary(text):
    dictionary = re.split(r'[.№":?!()%<>;,+#1234567890$&\s]', text)
    dictionary = list(set(dictionary))
    return dictionary

def getSentences(text):
    sentences = text.split('\n')
    for i in range(len(sentences)):
        sentences[i] = deletePunct(sentences[i])
    return sentences

def deletePunct(sentence):
    sentence = re.sub(r'[.№":?!()%<>;,+#1234567890$&\s]', u' ', sentence)
    sentence = re.sub(r'\s+', ' ', sentence)
    return sentence

def getVector(sentence, dictionary):
    words = sentence.split(' ')
    vector =np.zeros(len(dictionary), int)
    for word in words:
        vector[dictionary.index(word)] = vector[dictionary.index(word)] + 1
    return vector

def getSimilarSentences(original, vectors):
    indexes=[]
    for i in range(len(vectors)):
        if np.linalg.norm(original - vectors[i])<=2.5:
            indexes.append(i)
    return indexes

def calcAllDistances(vectors):
    f1 = open('distances.txt', 'a')
    distances=np.zeros((len(vectors),len(vectors)))
    for i in range(len(vectors)):
        for j in range (len(vectors)):
            distances[i][j]=np.linalg.norm(vectors[j] - vectors[i])
            f1.write(str(distances[i][j])+' ')
        f1.write('\n')
    return

f = open('naznach.txt', 'r')
text = f.read()
text = text.lower()
dictionary=getDictionary(text)
sentences=getSentences(text)

#составляем вектор для каждого предложения
vectors=[]
for s in sentences:
    vectors.append(getVector(s, dictionary))

original="По договору аренды т/с № 6,9 от 01.10.2014г. за ноябрь НДС не облагается.".lower()
original=deletePunct(original)
originalVector=getVector(original, dictionary)
indexes=getSimilarSentences(originalVector, vectors)
calcAllDistances(vectors)


for i in indexes:
   print(sentences[i])




