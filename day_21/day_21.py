# -*- coding: utf-8 -*-
import time
import numpy as np
from itertools import cycle, permutations

def read_input(path_to_file:str = 'input/raw_input.txt') -> str:
    with open(path_to_file) as f:
        data = [lines.strip('\n') for lines in f.readlines()]
    return data


def part1(data, dice_label_range=100, win_condition = 1000, part_two = False):
    # init everything
    player_one_start = int([x.split(': ') for x in data][0][1])
    player_two_start = int([x.split(': ') for x in data][-1][1])
    player_list = ['Player 1', 'Player 2']
    det_dice = cycle([x for x in range(1,dice_label_range+1)])
    player_scores = {   0: {'name': player_list[0],
                            'curr_pos': player_one_start, 
                            'score': 0,
                            'won': 0},
                        1: {'name': player_list[-1],
                            'curr_pos': player_two_start, 
                            'score': 0,
                            'won': 0}}
    STATE = dict()
    def game(alt = part_two):
        iterator = 0
        curr_player_id = 0
        if alt: # for part 2, splitting into universes
            # 10 possible permutations for each player resulting in 21 positions for each (because end score is 21)
            def calc_universes(score_dict):
                if score_dict[curr_player_id]['score'] >= win_condition: # checks if anyone won
                    score_dict[curr_player_id]['score'] += 1
                    return score_dict
                if STATE.get(score_dict): # checks if this universe already exists
                    return STATE[score_dict]
                for first in range(1,dice_label_range+1):
                    for second in range(1,dice_label_range+1):
                        for third in range(1,dice_label_range+1):
                            # calculate the score like in pt 1
                            score_dict[score_dict]['curr_pos'] += (first+second+third)%10
                            if score_dict[curr_player_id]['curr_pos'] > 10:
                                score_dict[curr_player_id]['curr_pos'] = score_dict[curr_player_id]['curr_pos']%10
                            score_dict[curr_player_id]['score'] += score_dict[curr_player_id]['curr_pos']

                            # recurse down
                            new_player_scores = calc_universes(score_dict)
                            
                # set new calculated state in STATE dictionary
                STATE[score_dict] = new_player_scores
                return new_player_scores

            # start with default values
            print(player_scores)
            return calc_universes(player_scores)

        else: # for part 1
            while (1):
                iterator+=3
                # calculate the dice throws
                moves = []
                for _ in range(0,3):
                    moves.append(next(det_dice))
                # get next position
                player_scores[curr_player_id]['curr_pos'] += sum(moves)%10
                if player_scores[curr_player_id]['curr_pos'] > 10:
                    player_scores[curr_player_id]['curr_pos'] = player_scores[curr_player_id]['curr_pos']%10

                # increase the score
                player_scores[curr_player_id]['score'] += player_scores[curr_player_id]['curr_pos']
                # print('{} rolls {} and moves to space {} for a total score of {}'.format(player_scores[curr_player_id]['name'], '+'.join([str(x) for x in moves]), player_scores[curr_player_id]['curr_pos'], player_scores[curr_player_id]['score']))
                # check for winner
                if (player_scores[curr_player_id]['score'] >= win_condition):
                    other_player_id = 0 if curr_player_id == 1 else 1
                    return player_scores, iterator*player_scores[other_player_id]['score']

                # iterators
                curr_player_id %= 2
                curr_player_id = 0 if curr_player_id == 1 else 1

    return game()


def part2(data):
    player_scores, result = part1(data, dice_label_range=3, win_condition=21, part_two=True)
    return 0


def test():
    data = read_input(path_to_file='input/test_input.txt')
    '''
    start_time = time.perf_counter()
    print('\nResult for part 1 in test: ', part1(data))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    '''
    start_time = time.perf_counter()
    print('\nResult for part 2 in test: ', part2(data))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")    
    

if __name__ == '__main__':
    data  = read_input()
    test()
    
    '''
    start_time = time.perf_counter()
    player_scores, result = part1(data)
    print('\nResult for part 1:', result)
    print('Resulting player scores:', player_scores)
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    
    start_time = time.perf_counter()
    print('\nResult for part 2: ', part2(enh, img))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")
    '''