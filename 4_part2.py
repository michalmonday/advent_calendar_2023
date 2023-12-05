
with open('input_4.txt') as f:
    lines = [line.strip() for line in f.readlines()]

counts = [1] * len(lines)

total = 0
for i, line in enumerate(lines):
    # total += 1
    # counts[i] -= 1
    content = line.split(':')[1].strip()
    winning_numbers = [ int(n.strip()) for n in content.split('|')[0].strip().split() ]
    my_numbers = [ int(n.strip()) for n in content.split('|')[1].strip().split() ]
    matches = sum([1 for n in my_numbers if n in winning_numbers])
    for j in range(matches):
        index = i + j + 1
        if index >= len(lines):
            continue
        counts[index] += counts[i]

total = sum(counts)
print(total)
