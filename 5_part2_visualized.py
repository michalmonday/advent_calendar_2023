# this is a visualization of the solution for part 2 of day 5

import re
import matplotlib.pyplot as plt
import numpy as np
import random
plt.ticklabel_format(style='plain')

with open('inputs/input_5_small.txt') as f:
# with open('input_5.txt') as f:
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

def remove_overlaps_from_multiple_ranges(ranges, ranges_to_remove):
    ''' removes ranges from range r and returns a list of ranges '''
    ranges_left = list(ranges_to_remove)
    ranges_created = list(ranges)
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

def remove_duplicate_ranges(ranges):
    return list(set(ranges))

all_unprocessed_ranges = []
all_translations = []
# global variables are used for later plotting 
def propagate(seeds_ranges, maps):
    # propagate seed to location
    global all_translations
    current_ranges = sorted(seeds_ranges, key=lambda x: x[0])
    for map_name, mapped_ranges in maps.items():
        # print(map_name, mapped_ranges)
        #all_current_ranges.append(remove_duplicate_ranges(current_ranges))
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
                next_range = (dst_start + intersection[0] - src_start, dst_start + intersection[1] - src_start)
                next_ranges.append(next_range)
        # TODO: remove duplicates by merging ranges first and then removing overlaps once
        unprocessed_ranges = remove_overlaps_from_multiple_ranges(current_ranges, all_intersections)

        current_ranges = sorted(list(next_ranges) + list(unprocessed_ranges), key=lambda x: x[0])
        all_translations.append((all_intersections, next_ranges))
        all_unprocessed_ranges.append(unprocessed_ranges)
    return min(current_ranges, key=lambda x: x[0])[0]

def annotate(ax, text, xy, xytext):
    ax.annotate(text, xy=xy, xytext=xytext, color='black', ha='center', va='center')
    circle_item = ax.plot([xy[0]], [xy[1]], 'o', color='orange', markersize=20)
    return circle_item


def plot_mappings(maps):
    global all_translations
    horizontal_axis_names = [k.split('-')[0] for k in maps.keys()] + [list(maps.keys())[-1].split('-')[2]]
    h_pos = 0
    for i, (map_name, mapped_ranges) in enumerate(maps.items()):
        src_name = map_name.split('-')[0]
        dst_name = map_name.split('-')[1]
        for mapped_range in mapped_ranges:
            dst_start, src_start, length = mapped_range
            # fill polygon with following 4 edges: (h_pos, src_start), (h_pos, src_start + length), (h_pos + 1, dst_start + length), (h_pos + 1, dst_start)
            maps_item = plt.fill([h_pos, h_pos, h_pos + 1, h_pos + 1], [src_start, src_start + length, dst_start + length, dst_start], label=src_name, alpha=0.15, color='blue')
            # draw thin black arrow/pointer to indicate the mapping direction using annotate arrowprops
            plt.annotate('', xy=(h_pos + 1, dst_start + length // 2), xytext=(h_pos, src_start + length // 2), arrowprops=dict(arrowstyle='->', color='blue', lw=1.5, alpha=0.8))

        intersections, next_ranges = all_translations[i]
        for intersection, next_range in zip(intersections, next_ranges):
            seeds_paths_item = plt.fill([h_pos, h_pos, h_pos + 1, h_pos + 1], [intersection[0], intersection[1], next_range[1], next_range[0]], alpha=0.4, color='green')
            annotate(plt, str(intersection[0]), xy=(h_pos, intersection[0]), xytext=(h_pos, intersection[0]))
            if i == len(maps) - 1:
                circle_item = annotate(plt, str(next_range[0]), xy=(h_pos+1, next_range[0]), xytext=(h_pos+1, next_range[0]))

        # draw unprocessed ranges as polygon with green color
        for r in all_unprocessed_ranges[i]: # remove_overlaps_from_multiple_ranges(all_unprocessed_ranges[i], all_translations[i]):
            plt.fill([h_pos, h_pos, h_pos + 1, h_pos + 1], [r[0], r[1], r[1], r[0]], alpha=0.4, color='green')
            circle_item = annotate(plt, str(r[0]), xy=(h_pos, r[0]), xytext=(h_pos, r[0]))
            circle_item = annotate(plt, str(r[0]), xy=(h_pos+1, r[0]), xytext=(h_pos+1, r[0]))
        h_pos += 1
    plt.xticks(np.arange(len(horizontal_axis_names)), horizontal_axis_names)
    # set legend with names: "Mappings", "Seeds paths"
    seeds_paths_item[0].set_label('Translated seeds ranges')
    maps_item[0].set_label('Mappings')
    circle_item[0].set_label('Min range value')
    plt.legend(handles=[seeds_paths_item[0], maps_item[0], circle_item[0]], loc='lower right') 
    # plt.legend([maps_items[0], seeds_paths_items[0]], loc='upper left')
    plt.show()
            
seeds_ranges = get_seeds_ranges(lines)
maps = get_maps(lines)
min_location = propagate(seeds_ranges, maps)
print(min_location)

plot_mappings(maps)

