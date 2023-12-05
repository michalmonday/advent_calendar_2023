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

def propagate(seed, maps):
    # propagate seed to location
    val = seed
    for k, v in maps.items():
        for range_ in v:
            dst_start, src_start, length = range_
            if val >= src_start and val < src_start + length:
                val = dst_start + val - src_start
                break
    return val

seeds = [int(s) for s in lines[0].split(':')[1].split()]
maps = get_maps(lines)
# for k, v in maps.items():
#     print(k, v)

min_location = min(propagate(seed, maps) for seed in seeds)
print(min_location)
