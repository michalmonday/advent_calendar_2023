import re

with open('input_3.txt') as f:
    lines = [line.strip() for line in f.readlines()]

all_num_spans = []
for i, line in enumerate(lines):
    num_spans = [m.span() for m in re.finditer(r'\d+', line)]
    all_num_spans.append(num_spans)
    
total = 0
for i, num_spans in enumerate(all_num_spans):
    lines_to_check = lines[(0 if i == 0 else i - 1) : i + 2]
    for j, (begin, end) in enumerate(num_spans):
        is_adjacent = False
        for line in lines_to_check:
            if re.search(r'[^.A-Za-z0-9 ]', line[begin - 1: end + 1]):
                is_adjacent = True
                break
        if not is_adjacent:
            continue
        print(lines[i][begin:end])
        total += int(lines[i][begin:end])

print(total)