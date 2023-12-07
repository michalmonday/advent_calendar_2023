from math import sqrt, ceil, prod

with open('inputs/input_7.txt') as f:
    lines = [line.strip() for line in f.readlines()]

hands = [line.split()[0].strip() for line in lines]
bets = [int(line.split()[1].strip()) for line in lines]

labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

bits_per_card_score =  ceil( sqrt(len(labels)) )

class REPETITION_SCORES:
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIRS = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

def hand_to_absolute_score(hand):
    '''Return the absolute score of a hand.'''
    score = 0
    repetitions = {}
    for card in hand:
        if card not in repetitions:
            repetitions[card] = 0
        repetitions[card] += 1
    # sort dict by value in descending order
    repetitions = dict(sorted(repetitions.items(), key=lambda item: item[1], reverse=True))
    if len(repetitions) == 1:
        score = REPETITION_SCORES.FIVE_OF_A_KIND
    if len(repetitions) == 2:
        if list(repetitions.values())[0] == 4:
            score = REPETITION_SCORES.FOUR_OF_A_KIND
        else:
            score = REPETITION_SCORES.FULL_HOUSE
    if len(repetitions) == 3:
        if list(repetitions.values())[0] == 3:
            score = REPETITION_SCORES.THREE_OF_A_KIND
        else:
            score = REPETITION_SCORES.TWO_PAIRS
    if len(repetitions) == 4:
        score = REPETITION_SCORES.ONE_PAIR

    for card in hand:
        score = (score << bits_per_card_score) + labels.index(card)
    return score

scores = [hand_to_absolute_score(hand) for hand in hands]
hands_bets_scores = list(zip(hands, bets, scores))
# ascending order
ordered_hands_bets_scores = sorted(hands_bets_scores, key=lambda x: x[2])
total = 0
for i, (hand, bet, score) in enumerate(ordered_hands_bets_scores):
    total += bet * (i + 1)
print(total)
