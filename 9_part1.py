
with open('inputs/input_9.txt') as f:
    lines = [line.strip() for line in f.readlines()]

def get_diffs(vals):
    diffs = []
    for i in range(len(vals) - 1):
        diffs.append(vals[i+1] - vals[i])
    return diffs

def get_all_diffs(vals):
    all_diffs = []
    diffs = get_diffs(vals)
    all_diffs.append(diffs)
    while not all(d==0 for d in diffs):
        diffs = get_diffs(diffs)
        all_diffs.append(diffs)
    return all_diffs

def extrapolate_diffs(all_diffs):
    value = 0
    for i in reversed(range(len(all_diffs))):
        value += all_diffs[i-1][-1]
    return value

total = 0
for line in lines:
    vals = [int(val.strip()) for val in line.split()]
    all_diffs = get_all_diffs(vals) 
    print(vals)
    print(all_diffs)
    val = extrapolate_diffs(all_diffs) + vals[-1]
    print('Extrapolated value:', val)
    total += val
    print()

print('Total:', total)