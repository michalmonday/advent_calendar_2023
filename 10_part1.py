#  | is a vertical pipe connecting north and south.
#  - is a horizontal pipe connecting east and west.
#  L is a 90-degree bend connecting north and east.
#  J is a 90-degree bend connecting north and west.
#  7 is a 90-degree bend connecting south and west.
#  F is a 90-degree bend connecting south and east.
#  . is ground; there is no pipe in this tile.
#  S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

with open('inputs/input_10_small.txt') as f:
    lines = [line.strip() for line in f.readlines()]

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
                    import pdb; pdb.set_trace()
                    whole_path = path + list(reversed(new_paths[0]))
                    return (i + 1 + depths[new_point[1]][new_point[0]]), whole_path
            depths[path[-1][1]][path[-1][0]] = i
            visited_points.update(new_points)
            for new_point in new_points:
                new_paths.append(path + [new_point])
        paths = list(new_paths)
        i += 1
        


start_point = find_start_point(lines)
end_point = start_point

depth, sp = find_shortest_path(start_point)
print(depth)
# print( len(sp) / 2 )
# print(f'path = {sp}')
print(sp)

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