
with open('input_2.txt') as f:
    lines = [line.strip() for line in f.readlines()]

cubes = {
    'red'   : 12, 
    'green' : 13,
    'blue'  : 14
}

def parse_set(s):
    clrs_dict = {'red': 0, 'green': 0, 'blue': 0
    }
    digit_clrs = [dc.strip() for dc in s.strip().split(',')]
    for dc in digit_clrs:
        num, clr = dc.split()
        clrs_dict[clr] = int(num)
    return clrs_dict

def combine_clrs_dicts(cds):
    ''' Given 2 sets, returns a single set with max values from each '''
    combined = {'red': 0, 'green': 0, 'blue': 0}
    for cd in cds:
        for clr, count in cd.items():
            if count > combined[clr]:
                combined[clr] = count
    return combined

def product_of_minimal_required_counts(line):
    sets = [s.strip() for s in line.split(':')[1].split(';')]
    combined = combine_clrs_dicts([parse_set(s) for s in sets])
    prod = 1
    for count in combined.values():
        prod *= count
    return prod
    

total = 0
for line in lines:
    total += product_of_minimal_required_counts(line)

print(total)