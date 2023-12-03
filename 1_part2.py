
import sys

with open('input_1.txt') as f:
    lines = [line.strip() for line in f.readlines()]

words = [
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'
]

def get_extremity_word_indices(words, line):
    lower = sys.maxsize
    upper = -1
    lower_digit = -1
    upper_digit = -1
    for i in range(len(line)):
        for word in words:
            if line[i:].startswith(word):
                if i < lower:
                    lower = i
                    lower_digit = words.index(word) + 1
                if i + len(word) > upper:
                    upper = i 
                    upper_digit = words.index(word) + 1
    return lower, lower_digit, upper, upper_digit

def get_extremity_digit_indices(line):
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
    return lower, lower_digit, upper, upper_digit

total = 0
for line in lines:
    w_lower, w_lower_digit, w_upper, w_upper_digit = get_extremity_word_indices(words, line)
    d_lower, d_lower_digit, d_upper, d_upper_digit = get_extremity_digit_indices(line)
    first_digit = w_lower_digit if w_lower < d_lower else d_lower_digit
    last_digit = w_upper_digit if w_upper > d_upper else d_upper_digit
    to_add = int(f'{first_digit}{last_digit}')
    total += to_add
    # print(f'{line} -> word_lower_digit={w_lower_digit} word_upper_digit={w_upper_digit} digit_lower_digit={d_lower_digit} digit_upper_digit={d_upper_digit} -> to_add={to_add}  |  w_lower_index={w_lower} w_upper_index={w_upper} d_lower_index={d_lower} d_upper_index={d_upper}')

print(total)

    
    