import os
from glob import glob
from functools import wraps, cmp_to_key
from time import time
from itertools import permutations, combinations

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f'{f.__name__} took: {(te-ts):.4f} sec')
        return result
    return wrap

CARD_STRENGHT_DICT = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
}
HAND_STRENGTH_DICT = {
    "High Card": 0,
    "One Pair": 1,
    "Two Pairs": 2,
    "Three of a Kind": 3,
    "Straight": 4,
    "Full House": 5,
    "Four of a Kind": 6,
    "Five of a Kind": 7
}

@timing
def read_input(input_file, end_at=None) -> tuple:
    
    games = []
    with open(input_file, "r") as f:
        input = f.read().splitlines()
        if not end_at:
            end_at = len(input)
        for game in input[:end_at]:
            hand = game.split(" ")[0]
            bid = game.split(" ")[1]
            games.append((hand, bid))
    return games

def score_hand(hand:str, pt2=False) -> tuple:
    # count the number of each card
    card_count = {}
    for card in hand:
        if card[0] not in card_count:
            card_count[card[0]] = 1
        else:
            card_count[card[0]] += 1
            
    if pt2:
        # set jokers value to 1
        CARD_STRENGHT_DICT["J"] = 1
    
    # sort the cards by value
    card_counts = sorted(card_count.items(), key=lambda x: CARD_STRENGHT_DICT[x[0]], reverse=True)
    if pt2:
        # to the highest amount of cards, add the jokers
        highest_card_count = sorted(card_counts, key=lambda x: x[1], reverse=True)[0]
        jokers = card_count.get("J", 0)
        card_count[highest_card_count[0]] += jokers
        card_count["J"] = 0
        card_counts = sorted(card_count.items(), key=lambda x: CARD_STRENGHT_DICT[x[0]], reverse=True)
    
    # check for pairs, three of a kind, four of a kind, five of a kind
    pairs = []
    three_of_a_kind = []
    four_of_a_kind = []
    five_of_a_kind = []
    full_house = []

    for card in card_counts:
        if card[1] == 2:
            pairs.append(card[0])
        elif card[1] == 3:
            three_of_a_kind.append(card[0])
        elif card[1] == 4:
            four_of_a_kind.append(card[0])
        elif card[1] == 5:
            five_of_a_kind.append(card[0])
        
        # check for full house
        if len(three_of_a_kind) == 1 and len(pairs) == 1:
            full_house.append([three_of_a_kind[0], pairs[0]])

    # calculate the hand score
    hand_score = 0
    if len(five_of_a_kind) == 1:
        hand_score = HAND_STRENGTH_DICT["Five of a Kind"]
    elif len(four_of_a_kind) == 1:
        hand_score = HAND_STRENGTH_DICT["Four of a Kind"]
    elif len(full_house) == 1:
        hand_score = HAND_STRENGTH_DICT["Full House"]
    elif len(three_of_a_kind) == 1:
        hand_score = HAND_STRENGTH_DICT["Three of a Kind"]
    elif len(pairs) == 2:
        hand_score = HAND_STRENGTH_DICT["Two Pairs"]
    elif len(pairs) == 1:
        hand_score = HAND_STRENGTH_DICT["One Pair"]
    else:
        hand_score = HAND_STRENGTH_DICT["High Card"]

    
    return hand_score, card_counts

def compare_hands(hand_1:tuple, hand_2:tuple) -> str:
    for card_1, card_2 in zip(hand_1[0], hand_2[0]):
        if CARD_STRENGHT_DICT[card_1[0]] > CARD_STRENGHT_DICT[card_2[0]]:
            return 1
        elif CARD_STRENGHT_DICT[card_1[0]] < CARD_STRENGHT_DICT[card_2[0]]:
            return -1
        else:
            continue
    return 0

def compare_hands_pt2(hand_1:tuple, hand_2:tuple) -> str:
    CARD_STRENGHT_DICT["J"] = 1
    for card_1, card_2 in zip(hand_1[0], hand_2[0]):
        if CARD_STRENGHT_DICT[card_1[0]] > CARD_STRENGHT_DICT[card_2[0]]:
            return 1
        elif CARD_STRENGHT_DICT[card_1[0]] < CARD_STRENGHT_DICT[card_2[0]]:
            return -1
        else:
            continue
    return 0

@timing
def pt(input, pt2=False):
    score_list = {x: [] for x in range(8)}

    for hand, bid in input:
        score, _ = score_hand(hand, pt2=pt2)
        score_list[score].append((hand, bid))

    # score the cards against each other
    sorted_hand_list = []
    for score, hands in score_list.items():
        if len(hands) == 1:
            sorted_hand_list.append(hands[0])
        else:
            if pt2:
                sorted_hands = sorted(hands, key=cmp_to_key(compare_hands_pt2))
            else:
                sorted_hands = sorted(hands, key=cmp_to_key(compare_hands))
            sorted_hand_list.extend(sorted_hands)
           
    rank = 1
    scored_list = []
    for hand, bid in sorted_hand_list:
        scored_list.append((hand, bid, rank, int(bid)*rank))
        rank += 1
    sorted_scored_list = sorted(scored_list, key=lambda x: x[2])
    res_score = sum([x[3] for x in sorted_scored_list])
    if pt2:
        print(f"Result Part 2: {res_score}")
    else:
        print(f"Result Part 1: {res_score}")

def main():
    test_input_file = glob(os.path.join(os.path.dirname(__file__), "input", "test.txt"))[0]
    input_file = glob(os.path.join(os.path.dirname(__file__), "input", "input.txt"))[0]
    # pt 1
    #pt(read_input(test_input_file))
    #pt(read_input(input_file))
    # pt 2
    pt(read_input(test_input_file), pt2=True)
    pt(read_input(input_file), pt2=True)
    

if __name__ == '__main__':
    main()
