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

pencils = 0

for i in range(1, 13):
    
    image = plt.imread("img ("+str(i)+").jpg")
  
    gray = toGray(image)
  
    thresh = threshold_triangle(gray)
  
    binary = binarisation(gray, 0, thresh)
    binary = morphology.binary_dilation(binary, iterations = 1)
  
    labeled = label(binary)
    areas = []
    for region in regionprops(labeled):
        areas.append(region.area)
    
    for region in regionprops(labeled):
        if region.area < np.mean(areas):
            labeled[labeled == region.label] = 0
        bbox = region.bbox
        if bbox[0] == 0 or bbox[1] == 0:
            labeled[labeled == region.label] = 0
        
    labeled[labeled > 0] = 1
    labeled = label(labeled)
  
    j = 0 # счетчик
    p = 0 # количество карандашей
    for region in regionprops(labeled):
        j += 1
        if (( (320000 < region.area < 500000) and (circularity(region, j) > 100))):
            p += 1
    print("Количество карандашей на изображении img ("+str(i)+").jpg равно ", p)
    pencils = pencils + p

print("Общее число карандашей на изображениях равно ", pencils)
