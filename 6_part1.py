from math import prod

with open('inputs/input_6.txt') as f:
    lines = [line.strip() for line in f.readlines()]

times = [ int(num.strip()) for num in lines[0].split(':')[1].strip().split() ]
distances = [ int(num.strip()) for num in lines[1].split(':')[1].strip().split() ]

total_ways = {f'{t}_{i}' : 0 for i, t in enumerate(times)}
for i, (time, dist) in enumerate(zip(times, distances)):
    for j in range(1, time):
        winning = j * (time - j) > dist 
        print(f'time: {time}, j: {j}, dist: {dist} -> {j * (time - j)} {"winning" if winning else ""}')
        if winning:
            total_ways[f'{time}_{i}'] += 1

print(total_ways)

print(prod(total_ways.values()))