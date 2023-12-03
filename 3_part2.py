import re

with open('input_3.txt') as f:
    lines = [line.strip() for line in f.readlines()]

all_num_spans = []
all_asterisk_indices = []
for i, line in enumerate(lines):
    num_spans = [m.span() for m in re.finditer(r'\d+', line)]
    all_num_spans.append(num_spans)
    all_asterisk_indices.append([m.start(0) for m in re.finditer(r'[*]', line)])
    
total = 0
for i, num_spans in enumerate(all_num_spans):
    lines_to_check = lines[(0 if i == 0 else i - 1) : i + 2]
    line_range_to_check = range((0 if i == 0 else i - 1), (i + 1 if i == len(lines) - 1 else i + 2))
    print(f'Checking line: {i} -> {lines[i]}')
    print(f'Checking lines: {line_range_to_check}, lines:')
    print('\n'.join([lines[j] for j in line_range_to_check]))
    for j, asterisk_ind in enumerate(all_asterisk_indices[i]):
        adjacent_numbers = []
        for line_ind in line_range_to_check:
            for begin, end in all_num_spans[line_ind]:
                if asterisk_ind >= begin - 1 and asterisk_ind <= end :
                    adjacent_numbers.append(int(lines[line_ind][begin:end]))
        if len(adjacent_numbers) == 2:
            gear_ratio = adjacent_numbers[0] * adjacent_numbers[1]
            total += gear_ratio
        print(f'Adjacent numbers: {adjacent_numbers}')

print(total)