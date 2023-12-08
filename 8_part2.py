import re
import matplotlib.pyplot as plt
import numpy as np
import math

with open('inputs/input_8.txt') as f:
    lines = [line.strip() for line in f.readlines()]

dirs = lines[0].strip()

locations = {}
for line in lines[2:]:
    src, left, right = re.search(r'(\w+)\s[=]\s\((\w+),\s(\w+)\)', line).groups()
    if src in locations:
        print(f'Warning: {src} already in locations')
    locations[src] = (left, right)

# current_location = list(locations.keys())[0]
# destination = list(locations.keys())[-1]
current_locations = [loc for loc in locations if loc[2] == 'A']
initial_locations = current_locations.copy()
print(f'Current locations = {current_locations}')

first_matches = {loc : 0 for loc in current_locations}
total = 0
while True:
    dir_ = dirs[total % len(dirs)]
    for i in range(len(current_locations)):
        dir_ind = 1 if dir_ == 'R' else 0
        current_locations[i] = locations[current_locations[i]][dir_ind]
    total += 1
    for i, loc in enumerate(current_locations):
        if loc[2] == 'Z' and first_matches[initial_locations[i]] == 0:
            first_matches[initial_locations[i]] = total
    if all(first_matches[loc] > 0 for loc in initial_locations):
        print(f'All locations have matched at least once after {total} iterations')
        break

lcm = math.lcm(*list(first_matches.values()))
print(lcm)