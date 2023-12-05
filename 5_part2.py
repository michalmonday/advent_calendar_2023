import re

with open('input_5.txt') as f:
    lines = [line.strip() for line in f.readlines()]

def get_maps(lines):
    # get groups of "seed-to-soil" and all values 
    res = re.findall(r'([a-zA-Z-]+)[^\n]+\n([0-9\n\r\s]+)', '\n'.join(lines[1:]), re.MULTILINE)
    maps = {}
    for r in res:
        maps[r[0]] = [[int(v) for v in s.split()] for s in r[1].split('\n') if s]
    return maps

def get_seeds_ranges(lines):
    values = [int(s) for s in lines[0].split(':')[1].split()]
    ranges = []
    for i, v in enumerate(values):
        if i % 2 == 1:
            ranges.append((values[i-1], values[i-1] + v - 1))
    return ranges

def get_intersection(r, r2):
    if r[0] <= r2[1] and r[1] >= r2[0]:
        return (max(r[0], r2[0]), min(r[1], r2[1]))
    return None

def remove_overlaps(r, ranges):
    ''' removes ranges from range r and returns a list of ranges '''
    ranges_left = list(ranges)
    ranges_created = [r]
    while ranges_left:
        range_to_remove = ranges_left.pop()
        for rc in ranges_created:
            intersection = get_intersection(rc, range_to_remove)
            if intersection is None:
                continue
            # remove intersection from rc
            if rc[0] < intersection[0]:
                ranges_created.append((rc[0], intersection[0] - 1))
            if rc[1] > intersection[1]:
                ranges_created.append((intersection[1] + 1, rc[1]))
            ranges_created.remove(rc)
    return ranges_created

def propagate(seeds_ranges, maps):
    # propagate seed to location
    current_ranges = seeds_ranges
    for map_name, mapped_ranges in maps.items():
        next_ranges = []
        # storing all intersections will allow to recognize regions that are not covered by any range
        # these regions will be added to the next_ranges
        all_intersections = []
        for cur_range in current_ranges:
            for mapped_range in mapped_ranges:
                dst_start, src_start, length = mapped_range
                # get intersection of current in mapped
                intersection = get_intersection(cur_range, (src_start, src_start + length - 1)) 
                if intersection is None:
                    continue
                all_intersections.append(intersection)
                next_ranges.append((dst_start + intersection[0] - src_start, dst_start + intersection[1] - src_start))
        unprocessed_ranges = []
        for cur_range in current_ranges:
            unprocessed_ranges.extend(remove_overlaps(cur_range, all_intersections))
        current_ranges = list(next_ranges) + list(unprocessed_ranges)
    return min(current_ranges, key=lambda x: x[0])[0]
            
seeds_ranges = get_seeds_ranges(lines)
min_location = propagate(seeds_ranges, get_maps(lines))
print(min_location)
