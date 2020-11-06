import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import morphology
from skimage.measure import label, regionprops
from skimage.filters import threshold_triangle

def circularity(region, label = 1):
    return (region.perimeter ** 2) / region.area

def toGray(image):
    return (0.2989 * image[:,:,0] + 0.587 * image[:,:,1] + 0.114 * image[:,:,2]).astype("uint8")

def binarisation(image, limit_min, limit_max):
    B = image.copy()
    B[B <= limit_min] = 0
    B[B >= limit_max] = 0
    B[B > 0] = 1
    return B

image = plt.imread("img (9).jpg")
gray = toGray(image)

thresh = threshold_triangle(gray)
binary = binarisation(gray, 0, thresh)

binary = morphology.binary_dilation(binary, iterations = 1)

labeled = label(binary)

areas = []

for region in regionprops(labeled):
    areas.append(region.area)
    
#print(np.mean(areas)) # среднее арифметическое значений элементов массива
#print(np.median(areas)) 

for region in regionprops(labeled):
    if region.area < np.mean(areas):
        labeled[labeled == region.label] = 0
    bbox = region.bbox
    if bbox[0] == 0 or bbox[1] == 0:
        labeled[labeled == region.label] = 0

labeled[labeled > 0] = 1
labeled = label(labeled)


i = 0 # счетчик
p = 0 # количество карандашей

for region in regionprops(labeled):
    #print(region.area) # площадь найденной фигуры
    i += 1
    if (( (320000 < region.area < 500000) and (circularity(region, i) > 100))):
        p += 1


print("Количество карандашей на изображении равно ", p)

plt.figure()
plt.subplot(131)
plt.imshow(gray,cmap="gray")
plt.subplot(132)
plt.imshow(binary)
plt.subplot(133)
plt.imshow(labeled)


plt.show()
