import operator
map = {(0, 1) : 5, (0, 2): 3, (1, 0): 1, (2, 0): 6}
print(map)
for v in sorted(map.items(), key=operator.itemgetter(1), reverse=True):
    print(v[0])


