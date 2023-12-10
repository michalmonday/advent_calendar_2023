#  | is a vertical pipe connecting north and south.
#  - is a horizontal pipe connecting east and west.
#  L is a 90-degree bend connecting north and east.
#  J is a 90-degree bend connecting north and west.
#  7 is a 90-degree bend connecting south and west.
#  F is a 90-degree bend connecting south and east.
#  . is ground; there is no pipe in this tile.
#  S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

import time
from colorama import Fore, Back, Style

with open('inputs/input_10.txt') as f:
    lines = [line.strip() for line in f.readlines()]

def print_lines(lines, highlight_points=None):
    # reprint all the lines with sp in green and valid_points bold
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if highlight_points and (j, i) in highlight_points:
                print(Fore.CYAN + Style.BRIGHT + char, end='')
            elif (j, i) in sp:
                print(Style.NORMAL + Fore.GREEN + char, end='')
            elif (j, i) in valid_points:
                print(Style.NORMAL + Fore.RED + char, end='')
            else:
                print(Style.NORMAL + Fore.WHITE + char, end='')
        print()


def find_start_point(lines):
    for i, line in enumerate(lines):
        try:
            return (line.index('S'), i)
            
        except ValueError:
            continue
    raise ValueError('No start point found')

def can_advance(point, potential_new_point, prev_point=None):
    ''' Return True if the potential new point is a valid next point. '''
    x, y = point
    new_x, new_y = potential_new_point
    # print(prev_point, point, potential_new_point)

    # can't go back to the previous point
    if potential_new_point == prev_point:
        return False

    # cant go out of bounds
    if new_x < 0 or new_y < 0 or new_x >= len(lines[0]) or new_y >= len(lines):
        return False

    if lines[new_y][new_x] == '.':
        return False

    current_point_allows_upward_movement = lines[y][x] in 'LJ|S'
    current_point_allows_downward_movement = lines[y][x] in 'F7|S'
    current_point_allows_left_movement = lines[y][x] in 'J7-S'
    current_point_allows_right_movement = lines[y][x] in 'LF-S'

    next_point_allows_movement_from_bottom = lines[new_y][new_x] in 'F7|S'
    next_point_allows_movement_from_up = lines[new_y][new_x] in 'LJ|S'
    next_point_allows_movement_from_left = lines[new_y][new_x] in 'J7-S'
    next_point_allows_movement_from_right = lines[new_y][new_x] in 'LF-S'

    # higher x = more to the right
    # higher y = more to the bottom
    is_next_above = new_y < y and new_x == x
    is_next_below = new_y > y and new_x == x
    is_next_to_the_left = new_x < x and new_y == y
    is_next_to_the_right = new_x > x and new_y == y

    
    can_move = any([
        current_point_allows_upward_movement and next_point_allows_movement_from_bottom and is_next_above,
        current_point_allows_downward_movement and next_point_allows_movement_from_up and is_next_below,
        current_point_allows_left_movement and next_point_allows_movement_from_right and is_next_to_the_left,
        current_point_allows_right_movement and next_point_allows_movement_from_left and is_next_to_the_right
    ])
    return can_move

visited_points = set()
depths = [[0] * len(lines[0]) for _ in range(len(lines))]
points_to_visit = set()
found_end_point = False

def get_new_points(point, prev_point=None):
    x, y = point
    potential_points = [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]
    valid_points = [pp for pp in potential_points if can_advance(point, pp, prev_point)]
    return valid_points

def advance(point, prev_point=None, depth=0):
    ''' For a given point, return all possible next points except the previous point. '''
    visited_points.add(point)
    new_points = get_new_points(point, prev_point)
    if end_point in new_points:
        print('Found end point')
        return [point]
    res = [advance(np, point, depth=depth+1) for np in new_points]
    if any(res):
        print('Found path')
        print(f'res = {res}')
        return [point] + [r for r in res[0] if r]
    return False

def find_shortest_path(point):
    i = 0
    paths = [[point]]
    visited_points.add(point)
    while True:
        # import pdb; pdb.set_trace()
        new_paths = []
        # print(f'Iteration {i}')
        # print(f'paths = {paths}')
        for path in paths:
            new_points = get_new_points(path[-1], None if len(path) < 2 else path[-2])
            # print(f'new_points = {new_points}')
            for new_point in new_points:
                if new_point in visited_points:
                    # new_points.remove(new_point)
                    # print(f'new_point {new_point} already visited')
                    visited_points.update(new_points)
                    # import pdb; pdb.set_trace()
                    whole_path = path + list(reversed(new_paths[0]))
                    return (i + 1 + depths[new_point[1]][new_point[0]]), whole_path[:-1]
            depths[path[-1][1]][path[-1][0]] = i
            visited_points.update(new_points)
            for new_point in new_points:
                new_paths.append(path + [new_point])
        paths = list(new_paths)
        i += 1
    
class Dirs:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    def from_points(prev_point, point):
        x, y = point
        prev_x, prev_y = prev_point
        if x == prev_x:
            if y < prev_y:
                return Dirs.UP
            else:
                return Dirs.DOWN
        else:
            if x < prev_x:
                return Dirs.LEFT
            else:
                return Dirs.RIGHT
        
def is_path_enclosing_right(path):
    # count how many relative left and right turns the path makes
    # if it makes more right turns then it is enclosing to the right 
    # (and the right side of it will be filled with ones)
    right_turns = 0
    left_turns = 0
    for i in range(len(path) - 1):
        prev_point = path[i]
        point = path[i+1]
        prev_dir = Dirs.from_points(prev_point, point)
        point_dir = Dirs.from_points(point, prev_point)
        if prev_dir == Dirs.UP:
            if point_dir == Dirs.RIGHT:
                right_turns += 1
            elif point_dir == Dirs.LEFT:
                left_turns += 1
        elif prev_dir == Dirs.RIGHT:
            if point_dir == Dirs.DOWN:
                right_turns += 1
            elif point_dir == Dirs.UP:
                left_turns += 1
        elif prev_dir == Dirs.DOWN:
            if point_dir == Dirs.LEFT:
                right_turns += 1
            elif point_dir == Dirs.RIGHT:
                left_turns += 1
        elif prev_dir == Dirs.LEFT:
            if point_dir == Dirs.UP:
                right_turns += 1
            elif point_dir == Dirs.DOWN:
                left_turns += 1
    return right_turns > left_turns

start_point = find_start_point(lines)
end_point = start_point

depth, sp = find_shortest_path(start_point)

# for each horizontal location, create a list of points that are at that location
hor_locations = { x: [] for x in range(len(lines[0]))  }
vert_locations = { y: [] for y in range(len(lines))  }

# print(sp)


for point in sp:
    x, y = point
    assert point not in hor_locations[x], f'point {point} already in hor_locations[{x}]'
    hor_locations[x].append(point)
    assert point not in vert_locations[y], f'point {point} already in vert_locations[{y}]'
    vert_locations[y].append(point)

# sort points in hor_locations by y (lowest to highest)
# sort points in vert_locations by x (lowest to highest)
for x, points in hor_locations.items():
    points.sort(key=lambda p: p[1], reverse=False)
for y, points in vert_locations.items():
    points.sort(key=lambda p: p[0], reverse=False)


# total_y_diff = 0
# for x, points in hor_locations.items():
#     # for every vertical value of odd point get its difference from the next point if such exists
#     points.sort(key=lambda p: p[1], reverse=False)
#     # print(x, points)
#     for i, point in enumerate(points):
#         if i % 2 == 1:
#             continue
#         if i == len(points) - 1:
#             break
#         y_diff = abs(points[i+1][1] - point[1]) - 1
#         # print(f'    y_diff = {y_diff} i = {i}')
#         total_y_diff += y_diff
# print(total_y_diff)

print(f'is_path_enclosing_right(sp) = {is_path_enclosing_right(sp)}')

def get_closest_point_horizontally(point, points, on_the_right_only):
    # if on_the_right_only is True, return the closest point to the right of the given point
    # if it is false then return the closest point to the left of the given point
    x, y = point
    if on_the_right_only:
        for p in points:
            if p[0] > x:
                return p
    else:
        for p in reversed(points):
            if p[0] < x:
                return p
    return point

def get_closest_point_vertically(point, points, above_only):
    # if above_only is True, return the closest point above the given point
    # if it is false then return the closest point below the given point
    x, y = point
    if above_only:
        for p in points:
            if p[1] > y:
                return p
    else:
        for p in reversed(points):
            if p[1] < y:
                return p
    return point

def get_opposite_point(point, current_direction, is_path_enclosing_right):
    # use hor_locations and vert_locations to find the opposite point depending on current_direction
    x, y = point
    if current_direction == Dirs.UP:
        opposite_point = get_closest_point_horizontally(point, vert_locations[y], on_the_right_only=is_path_enclosing_right)
    elif current_direction == Dirs.RIGHT:
        opposite_point = get_closest_point_vertically(point, hor_locations[x], above_only=is_path_enclosing_right)
    elif current_direction == Dirs.DOWN:
        opposite_point = get_closest_point_horizontally(point, vert_locations[y], on_the_right_only=not is_path_enclosing_right)
    elif current_direction == Dirs.LEFT:
        opposite_point = get_closest_point_vertically(point, hor_locations[x], above_only=not is_path_enclosing_right)
    return opposite_point

valid_points = set()

print(f'path length = {len(sp)}')

last_direction = None
for i, point in enumerate(sp):
    if i == 0:
        continue
    prev_point = sp[i-1]
    point = sp[i]
    # print_lines(lines, highlight_points=[point, prev_point])
    # time.sleep(0.05)
    direction = Dirs.from_points(prev_point, point)
    opposite_point = get_opposite_point(point, direction, not is_path_enclosing_right(sp))
    try:
        distance = abs(point[0] - opposite_point[0]) + abs(point[1] - opposite_point[1]) - 1
    except Exception as e:
        print(f'point = {point} opposite_point = {opposite_point}')
        # import pdb; pdb.set_trace()
        # opposite_point = get_opposite_point(point, direction, is_path_enclosing_right(sp))

    if distance > 0:
        # import pdb; pdb.set_trace()
        # all points between point and opposite_point are valid
        if direction == Dirs.UP or direction == Dirs.DOWN:
            for x in range(min(point[0], opposite_point[0]) + 1, max(point[0], opposite_point[0])):
                valid_points.add((x, point[1]))
        elif direction == Dirs.LEFT or direction == Dirs.RIGHT:
            for y in range(min(point[1], opposite_point[1]) + 1, max(point[1], opposite_point[1])): 
                valid_points.add((point[0], y))
        
    if i > 0 and direction != last_direction:
        opposite_point = get_opposite_point(prev_point, direction, not is_path_enclosing_right(sp))
        try:
            distance = abs(prev_point[0] - opposite_point[0]) + abs(prev_point[1] - opposite_point[1]) - 1
        except Exception as e:
            print(f'prev_point = {prev_point} opposite_point = {opposite_point}')
            # import pdb; pdb.set_trace()
            # opposite_point = get_opposite_point(prev_point, direction, is_path_enclosing_right(sp))

        if distance > 0:
            # import pdb; pdb.set_trace()
            # all points between prev_point and opposite_point are valid
            if direction == Dirs.UP or direction == Dirs.DOWN:
                for x in range(min(prev_point[0], opposite_point[0]) + 1, max(prev_point[0], opposite_point[0])):
                    valid_points.add((x, prev_point[1]))
            elif direction == Dirs.LEFT or direction == Dirs.RIGHT:
                for y in range(min(prev_point[1], opposite_point[1]) + 1, max(prev_point[1], opposite_point[1])): 
                    valid_points.add((prev_point[0], y))

    last_direction = direction
        
    if i % 1000 == 0:
        print(f'i = {i}')


    # print(f'point = {point} direction = {direction} distance = {distance} opposite_point = {opposite_point}')


print(len(valid_points))

print_lines(lines)

# for vp in valid_points:
#     x, y = vp
#     print(lines[y][x], (x, y))


# prev_point = None
# for point in sp:
#     print(lines[point[1]][point[0]], end=' ')
#     x, y = point
#     # print "up" "right" "down" "left"
#     if prev_point:
#         prev_x, prev_y = prev_point
#         if x == prev_x:
#             if y < prev_y:
#                 print('up')
#             else:
#                 print('down')
#         else:
#             if x < prev_x:
#                 print('left')
#             else:
#                 print('right')
#     else:
#         print('start')
#     prev_point = point

# print( len(advance(start_point) ) // 2)


# print(start_point)