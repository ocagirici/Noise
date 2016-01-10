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

def mergeSort(alist):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]
        mergeSort(lefthalf)
        mergeSort(righthalf)
        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1

def sort_mse_vertically(original):
    size = len(original)
    vertical = {}
    for i in range(size):
        count = 0
        for j in range(size):
            count += original[i][j]
        vertical[i] = count
    return mergeSort(vertical)

def sort_mse_horizontally(original):
    size = len(original)
    horizontal = {}
    for i in range(size):
        count = 0
        for j in range(size):
            count += original[j][i]
        horizontal[i] = count
    return mergeSort(horizontal)

def mse_of_sqrts(original, noisy):
    numsqrt = math.floor(math.sqrt(len(original)))
    sqrtmatrix = [[0 for i in range(numsqrt)] for j in range(numsqrt)]
    currstartx = 0
    currendx = numsqrt - 1
    for i in range(numsqrt):
        currstarty = 0
        currendy = numsqrt - 1
        for j in range(numsqrt):
            orr = {}
            no = {}
            orr = original[i*currstartx : (i*currendx + 1), i*currstarty : (i*currendy + 1)]
            no = noisy[i*currstartx : (i*currendx + 1), i*currstarty : (i*currendy + 1)]
            sqrtmatrix[i][j] = mse_matrix(orr, no)
            currstarty += numsqrt
            currendy += numsqrt
        currstartx += numsqrt
        currendx += numsqrt
    ver = {}
    hor = {}
    ver = sort_mse_vertically(sqrtmatrix)
    hor = sort_mse_horizontally(sqrtmatrix)
    mul = 0
    for i in range(numsqrt):
        mul += ver[i] * hor[i]
    mul /= numsqrt
    res = math.sqrt(mul)
    return res

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
    return stdev(m)  #   lol


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
