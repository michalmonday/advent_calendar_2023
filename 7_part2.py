from math import sqrt, ceil, prod
import re
from collections import Counter


with open('inputs/input_7.txt') as f:
    lines = [line.strip() for line in f.readlines()]

class REPETITION_SCORES:
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIRS = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

def hand_to_repetition_score(hand):
    hand = re.sub(r'[J]', '', hand)
    jokers = 5 - len(hand)
    if jokers == 5:
        return REPETITION_SCORES.FIVE_OF_A_KIND
    repetitions = { card: count for card, count in Counter(hand).items() if count }
    # sort dict by value in descending order
    repetitions = dict(sorted(repetitions.items(), key=lambda item: item[1], reverse=True))
    counts = list(repetitions.values())
    counts[0] += jokers
    match counts[0]:
        case 5: score = REPETITION_SCORES.FIVE_OF_A_KIND
        case 4: score = REPETITION_SCORES.FOUR_OF_A_KIND
        case 3: score = REPETITION_SCORES.FULL_HOUSE if len(counts) > 1 and counts[1] == 2 else REPETITION_SCORES.THREE_OF_A_KIND
        case 2: score = REPETITION_SCORES.TWO_PAIRS if len(counts) > 1 and counts[1] == 2 else REPETITION_SCORES.ONE_PAIR
        case 1: score = REPETITION_SCORES.HIGH_CARD
    return score

def hand_to_absolute_score(hand):
    '''Return the absolute score of a hand.'''
    score = hand_to_repetition_score(hand)
    for card in hand:
        score = (score << bits_per_card_score) + labels.index(card)
    return score

labels = ['0', 'J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

hands = [line.split()[0].strip() for line in lines]
bets = [int(line.split()[1].strip()) for line in lines]
bits_per_card_score =  ceil( sqrt(len(labels)) )
scores = [hand_to_absolute_score(hand) for hand in hands]
hands_bets_scores = list(zip(hands, bets, scores))
# ascending order
ordered_hands_bets_scores = sorted(hands_bets_scores, key=lambda x: x[2])
total = 0
for i, (hand, bet, score) in enumerate(ordered_hands_bets_scores):
    total += bet * (i + 1)
print(total)
