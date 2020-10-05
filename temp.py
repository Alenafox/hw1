#работает для всех файлов, стоит только поменять название файла

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict
 
 
FILE_NAME = 'figure1.txt'

def result(real_length, max_length):
    if max_length == 0:
        return "Изображение пустое, фигуры не найдено"
    else:
        return real_length/max_length
 
def find_ones(arr):
   max = 0
   for num in arr:
      if np.sum(num) > max: #если сумма элементов больше максимума
        max = np.sum(num) #записываем эту сумму в максимум
   return max
    
def read_data() -> Dict:
    return_array = []
    with open(FILE_NAME, 'r') as f:
        data = f.read()
    splited_data = data.split('\n')
    resolution = float(splited_data[0])
    for row in splited_data[2:-1]:
        splited_row = row.split(' ')
        return_array.append(list(map(int, splited_row[:-1])))
    return {"resolution": resolution, "array": return_array}
 
max_length = find_ones(read_data()['array'])
res = result(read_data()['resolution'], max_length)
print("Result = " ,res)
 
plt.imshow(read_data()['array'])
plt.show()