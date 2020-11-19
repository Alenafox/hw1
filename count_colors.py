#Прямоугольники: 136
#Оранжевый: 18 Желтый: 22 Зеленый: 40 Синий: 33 Пурпурный: 23
#Круги: 121
#Оранжевый: 21 Желтый: 29 Зеленый: 33 Синий: 25 Пурпурный: 13
#__________________
#Итого: 257


import numpy as np
from skimage.measure import label, regionprops
import matplotlib.pyplot as plt
from skimage import color

def centering(lb, label=1):
    pos = np.where(lb == label)
    cy = np.mean(pos[0])
    cx = np.mean(pos[1])
    if cy == cx:
        return 1
    return 0

def count_colors(colors):
    col_1 = col_2 = col_3 = col_4 = col_5 = 0
    
    for color in colors:
        if color < 0.06:
            col_1 += 1
        if color > 0.06 and color < 0.2:
            col_2 += 1
        if color > 0.2 and color < 0.42:
            col_3 += 1
        if color > 0.42 and color < 0.62:
            col_4 += 1
        if color > 0.62:
            col_5 += 1
            
    print("Оранжевый:", col_1, "Желтый:", col_2, "Зеленый:", col_3, "Синий:", col_4, "Пурпурный:", col_5)

image = plt.imread("balls_and_rects.png")
binary = image.copy()[:, :, 0]
binary[binary > 0] = 1
image = color.rgb2hsv(image)[:, :, 0]

labeled = label(binary)

all_colors = []
rectangles = []
circles = []

for region in regionprops(labeled):
    bb = region.bbox
    cur = np.max(image[bb[0]:bb[2], bb[1]:bb[3]])
    all_colors.append(cur)
    if centering(region.image) == 0:
        rectangles.append(cur)
    else:
        circles.append(cur)

all_colors.sort()
rectangles.sort()
circles.sort()

print("Прямоугольники:", len(circles))
count_colors(circles)
print("Круги:", len(rectangles))
count_colors(rectangles)

print("__________________")
print("Итого:", np.max(labeled))

plt.figure()
plt.imshow(image)
plt.show()
