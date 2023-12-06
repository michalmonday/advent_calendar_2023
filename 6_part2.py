from math import prod, sqrt, ceil, floor
import matplotlib.pyplot as plt
plt.ticklabel_format(style='plain')
import numpy as np

with open('inputs/input_6.txt') as f:
    lines = [line.strip() for line in f.readlines()]

time = int(''.join(lines[0].split(':')[1].strip().split()))
dist = int(''.join(lines[1].split(':')[1].strip().split()))
# time = 10
# dist = 17

def quadratic(a, b, c):
    return (-b + sqrt(b**2 - 4*a*-c)) / (2*a)

x = quadratic(-1, time, dist)
print( time - floor(x) - ceil(x) )

all_dists = []
total_ways = 0
for j in range(1, time):
    # if j % 10000000 == 0:
    #     print(j)
    y = j * (time - j)
    all_dists.append(y)
    winning = y > dist 
    # print(f'time: {time}, j: {j}, dist: {dist} -> {j * (time - j)} {"winning" if winning else ""}')
    if winning:
        total_ways += 1

print(f'total_ways: {total_ways}')

plt.plot(range(1, time), all_dists)
# plot horizontal dist line
plt.plot([0, time], [dist, dist])
plt.show()

