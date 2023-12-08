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
current_locations = [loc for loc in locations if loc[2] == 'A']
total = 0
all_locs_end_with_z = False
while not all_locs_end_with_z:
    dir = dirs[total % len(dirs)]
    for i in range(len(current_locations)):
        dir_ind = 1 if dir == 'R' else 0
        current_locations[i] = locations[current_locations[i]][dir_ind]
    all_locs_end_with_z = all([loc[2] == 'Z' for loc in current_locations])
    total += 1
    if total % 1000000 == 0:
        print(total)
print(total)