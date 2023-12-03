
with open('input_2.txt') as f:
    lines = [line.strip() for line in f.readlines()]

cubes = {
    'red'   : 12, 
    'green' : 13,
    'blue'  : 14
}

def parse_set(s):
    clrs_dict = {
        'red'   : 0,
        'green' : 0,
        'blue'  : 0
    }
    digit_clrs = [dc.strip() for dc in s.strip().split(',')]
    for dc in digit_clrs:
        num, clr = dc.split()
        clrs_dict[clr] = int(num)
    return clrs_dict

def is_game_line_possible(line):
    sets = [s.strip() for s in line.split(':')[1].split(';')]
    for s in sets:
        for clr, count in parse_set(s).items():
            if count > cubes[clr]:
                print(f'Not enough {clr} cubes')
                return False
    return True

total_ids = 0
for line in lines:
    if not is_game_line_possible(line):
        continue
    game_id = line.split(':')[0].split()[1]
    print(game_id)
    total_ids += int(game_id)

print(total_ids)