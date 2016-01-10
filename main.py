from PIL import Image
import numpy as np
import operator
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from os import listdir
from os.path import isfile, join, splitext
from statistics import stdev

def mse_matrix(original, noisy):
    if len(original) is not len(noisy):
        return False
    size = len(original)
    diff = 0
    for i in range(size):
        for j in range(size):
            diff += (int(original[i][j]) - int(noisy[i][j])) ** 2
    return diff / (len(original) ** 2)


def adj_cells(i, j, size):
    adj = []
    if j is not 0:
        adj.append([i, j - 1])  # U
    if j is not size:
        adj.append([i, j + 1])  # D
    if i is not size:
        adj.append([i + 1, j])  # R
    if i is not 0:
        adj.append([i - 1, j])  # L
    if i is not size and j is not 0:
        adj.append([i + 1, j - 1])  # UR
    if i is not 0 and j is not 0:
        adj.append([i - 1, j - 1])  # UL
    if i is not size and j is not size:
        adj.append([i + 1, j + 1])  # DR
    if i is not 0 and j is not size:
        adj.append([i - 1, j + 1])  # DL

    return adj

def compare_without_sort(original, noisy):
    size = len(original)
    diff_matrix = np.zeros(shape=(size, size))
    for i in range(size):
        for j in range(size):
            diff_matrix[i][j] = (int(original[i][j]) - int(noisy[i][j]))
    sum = 0
    m = []
    map = dict()
    for v in sorted(map.items(), key=operator.itemgetter(1)):
        i, j = v[0]
        adj = []
        for k in adj_cells(i, j, size-1):
            adj.append(diff_matrix[k[0], k[1]])
        diff_matrix[i][j] = stdev(adj)
        sum += diff_matrix[i, j]
        m.append(diff_matrix[i, j])
    return stdev(m)


def compare(original, noisy):
    size = len(original)
    diff_matrix = np.zeros(shape=(size, size))
    for i in range(size):
        for j in range(size):
            diff_matrix[i][j] = (int(original[i][j]) - int(noisy[i][j]))
    sum = 0
    m = []
    map = dict()
    for i in range(size):
        for j in range(size):
            map[(i, j)] = abs(diff_matrix[i, j])
    for v in sorted(map.items(), key=operator.itemgetter(1)):
        i, j = v[0]
        adj = []
        for k in adj_cells(i, j, size-1):
            adj.append(diff_matrix[k[0], k[1]])
        diff_matrix[i][j] = stdev(adj)
        sum += diff_matrix[i, j]
        m.append(diff_matrix[i, j])
    return stdev(m)

dir = './pic/'
files = [f for f in listdir(dir) if isfile(join(dir, f))]

img = dict()
for f in files:
    img[splitext(f)[0]] = np.asarray(Image.open(dir + f).convert('L'))


for i in img.keys():
    if i != 'einstein':
        print(i, compare(img['einstein'], img[i]))


# keys = list(img.keys())
# for i in range(len(keys)-1):
#     for j in range(i+1, len(keys)):
#         print("dist({},{}): {:.2f}".format(keys[i], keys[j],
#                                        diff(img[keys[i]], img[keys[j]])))
