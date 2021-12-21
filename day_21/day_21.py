# -*- coding: utf-8 -*-
import time
import numpy as np
from itertools import cycle, repeat

def read_input(path_to_file:str = 'input/raw_input.txt') -> str:
    with open(path_to_file) as f:
        data = [lines.strip('\n') for lines in f.readlines()]
    return data


def part1(data, dice_label_range=100, win_condition = 1000):
    # init everything
    player_one_start = int([x.split(': ') for x in data][0][1])
    player_two_start = int([x.split(': ') for x in data][-1][1])
    player_list = ['Player 1', 'Player 2']
    det_dice = cycle([x for x in range(1,dice_label_range+1)])
    player_scores = {   0: {'name': player_list[0],
                            'curr_pos': player_one_start, 
                            'score': 0},
                        1: {'name': player_list[-1],
                            'curr_pos': player_two_start, 
                            'score': 0}}
    def game():
        iterator = 0
        curr_player_id = 0
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
    player_scores, result = part1(data, dice_label_range=3)
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