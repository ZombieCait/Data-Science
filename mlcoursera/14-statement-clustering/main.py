from skimage.io import imread, imsave
from skimage import img_as_float
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import math
#1. Загрузите картинку parrots.jpg. Преобразуйте изображение, приведя все значения в интервал от 0 до 1.
#Для этого можно воспользоваться функцией img_as_float из модуля skimage. 
#Обратите внимание на этот шаг, так как при работе с исходным изображением вы получите некорректный результат.

image = imread('parrots.jpg')
float_image = img_as_float(image)
w, h, d = float_image.shape
#2. Создайте матрицу объекты-признаки: характеризуйте каждый пиксель тремя координатами -
# значениями интенсивности в пространстве RGB.
features = pd.DataFrame(np.reshape(float_image, (w*h, d)), columns=['R', 'G', 'B'])

#3. Запустите алгоритм K-Means с параметрами init='k-means++' и random_state=241. 
#После выделения кластеров все пиксели, отнесенные в один кластер, попробуйте заполнить
# двумя способами: медианным и средним цветом по кластеру.
def clustering(features, n_clusters=8):
    km = KMeans(init='k-means++', random_state=241, n_clusters=n_clusters)
    features['cluster']=km.fit_predict(features)
    means = features.groupby('cluster').mean().values
    mean_features = [means[c] for c in features['cluster'].values]
    mean_image = np.reshape(mean_features, (w, h, d))
    imsave('images/mean/parrots_' + str(n_clusters) + '.jpg', mean_image)
    
    medians = features.groupby('cluster').median().values
    median_features = [medians[c] for c in features['cluster'].values]
    median_image = np.reshape(median_features, (w, h, d))
    imsave('images/median/parrots_' + str(n_clusters) + '.jpg', median_image)
    return mean_image, median_image
    
mean_image, median_image=clustering(features)
#4. Измерьте качество получившейся сегментации с помощью метрики PSNR. 
#Эту метрику нужно реализовать самостоятельно (см. определение).

def psnr(img1, img2):
    mse=np.mean((img1 - img2) ** 2)
    return 10*math.log10(float(1.0)/mse)

#5. Найдите минимальное количество кластеров, при котором значение PSNR выше 20 
#(можно рассмотреть не более 20 кластеров, но не забудьте рассмотреть оба способа 
#заполнения пикселей одного кластера). Это число и будет ответом в данной задаче.
for n in range(1, 21):
    mean_image, median_image=clustering(features, n)
    psnr_mean, psnr_median=psnr(float_image, mean_image), psnr(float_image, median_image)
    print(psnr_mean, psnr_median)
    if (psnr_mean>20) | (psnr_median>20):
        open('1.txt', 'w').write(str(n))
        break
    
    