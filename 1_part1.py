
import sys

with open('input_1.txt') as f:
    lines = [line.strip() for line in f.readlines()]

def get_extremity_digits(line):
    '''Given a line like: "abcd1ab5cd9" returns: [1,9]'''
    lower = sys.maxsize
    upper = -1
    lower_digit = -1
    upper_digit = -1
    for i in range(len(line)):
        if line[i] >= '0' and line[i] <= '9':
            if i < lower:
                lower = i
                lower_digit = int(line[i])
            if i > upper:
                upper = i
                upper_digit = int(line[i])
    return lower_digit, upper_digit

total = 0
for line in lines:
    first_digit, last_digit = get_extremity_digits(line)
    total += int(f'{first_digit}{last_digit}')

print(total)

    
    