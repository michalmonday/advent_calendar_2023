import re

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
current_location = 'AAA'
destination = 'ZZZ'
total = 0
while current_location != destination:
    print(f'{current_location} -> {locations[current_location]}')
    dir = dirs[total % len(dirs)]
    if dir == 'L':
        current_location = locations[current_location][0]
    elif dir == 'R':
        current_location = locations[current_location][1]
    else:
        raise ValueError('Invalid direction')
    total += 1
print(total)