
with open('input_4.txt') as f:
    lines = [line.strip() for line in f.readlines()]

total = 0
for line in lines:
    content = line.split(':')[1].strip()
    winning_numbers = [ int(n.strip()) for n in content.split('|')[0].strip().split() ]
    my_numbers = [ int(n.strip()) for n in content.split('|')[1].strip().split() ]
    matches = 0
    for n in my_numbers:
        if n not in winning_numbers:
            continue
        matches += 1
    if not matches:
        continue
    total += 2 ** (matches - 1)
print(total)
