# -*- coding: utf-8 -*-
import time
import numpy as np

def read_input(path_to_file:str = 'input/raw_input.txt') -> str:
    """read_input Read the input

    Reads the input from a file with specified path

    Parameters
    ----------
    path_to_file : str, optional
        Path to the file to be read, by default 'input/raw_input.txt'

    Returns
    -------
    str
        The files content as string.
    """

    with open(path_to_file) as f:
        data = f.readlines()[0].strip('\n')
    return data

HEX_TO_BIN_DICT:dict = {'0' : '0000',
                        '1' : '0001',
                        '2' : '0010',
                        '3' : '0011',
                        '4' : '0100',
                        '5' : '0101',
                        '6' : '0110',
                        '7' : '0111',
                        '8' : '1000',
                        '9' : '1001',
                        'A' : '1010',
                        'B' : '1011',
                        'C' : '1100',
                        'D' : '1101',
                        'E' : '1110',
                        'F' : '1111'}


P2_DICT = { 0: 'sum',
            1: 'product',
            2: 'minimum',
            3: 'maximum',
            4: 'greater',
            5: 'greater than',
            6: 'less than',
            7: 'equal to'
            }

def part1(data:str)->int:
    """part1 Method for solving part 1.

    [extended_summary]

    Parameters
    ----------
    data : str
        The transmission coming in.

    Returns
    -------
    int
        Solution of part 1, sum of all version numbers in transmission.
    """
    print('Hex encoded data:', data)    
    input_data = ''.join([HEX_TO_BIN_DICT[x] for x in data])
    res = []
    res, index, id_list = decode_transmission_block(input_data)
    return sum(res), res, index, id_list

def literal_value(bin:str) -> tuple[int,int]:
    print('Data for literal:', bin)
    number = bin[6:]
    print('Numberpart for literal:', number)
    start_bits = number[::5]
    print('Startbits for subpackets:', start_bits)
    value = ''
    l=5 # minimal length
    for i,s in enumerate(start_bits):
        if i == 0: v = number[:i+5]
        else: v = number[i*5:(i+1)*5]
        v_content = v[1:5]
        print('Value in loop:', v_content)
        value += v_content
        l+=5 # increase length by 5
        if s == '0': break
    print('Value: ', value, 'Length of Value:', l)

    return int(value, 2), l

def decode_transmission_block(data_bin:str, packet_version_list:list = [], list_pt2 = []):
    if len(data_bin)>10:
        print('\nData (bin):', data_bin) 
        # encode header
        version = data_bin[:3]
        version_dec = int(version,2)
        type_id = data_bin[3:6]
        type_id_dec = int(type_id,2)

        packet_version_list.append(version_dec)
        
        print('Packet version list:', packet_version_list)
        print('Current sum of packet version list:', sum(packet_version_list))
        print('Version (bin, dec):', version, version_dec)

        # brackets
        if (type_id_dec == 4):
            # literal value -> one single binary number, is always the last package, returns the packet_version_list
            print('TypeID (bin, dec):', type_id, type_id_dec, 'is a literal')
            value_dec, l = literal_value(data_bin)
            print('Literal decimal value:', value_dec)
            last_index = l+1
            print('Last index of literal:',last_index)

            # For pt 2
            list_pt2.append(value_dec)
            
            print('TypeID list:', packet_version_list)
            print('\nCalculated term:', list_pt2)
            return packet_version_list, last_index, list_pt2
            
        else:
            # operator
            print('TypeID (bin, dec):', type_id, type_id_dec, 'is an operator')
            length_type_id = data_bin[6]
            print('Length type id: ', length_type_id)
            if length_type_id == '1':
                # 11 bit number of how many subpackets are contained
                amount_subpackets = data_bin[7:18]
                amount_subpackets_dec = int(amount_subpackets,2)
                print('Amount of subpackets:', amount_subpackets_dec)
                i = 0
                shift = 0
                subpackets_start = 18
                while (i < amount_subpackets_dec):
                    print('Next package starts at:', subpackets_start)
                    print('Next subpacket number:', i+1)
                    # slice the data and go down each individual package
                    packet_version_list, shift, list_pt2 = decode_transmission_block(data_bin[subpackets_start:], packet_version_list, list_pt2)
                    subpackets_start+=shift
                    i+=1
                    print('Next package starts at:', subpackets_start)
                print('Packet version list:', packet_version_list)
                list_pt2.append(P2_DICT[type_id_dec])
                list_pt2.append(calculator(list_pt2))
                print('\nCalculated term:', list_pt2)
                return packet_version_list, subpackets_start, list_pt2
            
            elif length_type_id == '0':
                # has a 15 bit number following the total length of the subpackets contained
                length_subpacket = data_bin[7:22]
                length_subpacket_dec = int(length_subpacket,2)
                subpackets_start = 22
                subpackets_end = subpackets_start+length_subpacket_dec
                print('Subpackets total length:', length_subpacket_dec)
                print('Subpackets end:', subpackets_end)
                shift = 0
                while (subpackets_start < subpackets_end):
                    packet_version_list, shift, list_pt2 = decode_transmission_block(data_bin[subpackets_start:], packet_version_list, list_pt2)
                    subpackets_start+=shift                  
                    print('Current Index to shift:', shift)
                    print('Next package @:', subpackets_start)
                print('Packet version list:', packet_version_list)
                list_pt2.append(P2_DICT[type_id_dec])
                list_pt2.append(calculator(list_pt2))
                return packet_version_list, subpackets_start, list_pt2
    else:
        list_pt2 = calculator(list_pt2)
        print('\nCalculated term:', list_pt2)
        return packet_version_list, 0, list_pt2

def calculator(term:list):
    print('(Sub-)Term to calculate:', term)
    new_term = []
    if len(term) == 3 and isinstance(term[-1], str):
        # go through the list from left to right, after two values comes a operand, use operand on those two values in order, create new list with result
        # unpack if needed
        for item in term:
            print(item, type(item))
            if isinstance(item, list):
                term[term.index(item)] = item[0]

        print('Begin calculation with:', term)
        a = term.pop(0)
        b = term.pop(0)
        o = term.pop(0)        
        # switch case on o
        if o == 'sum': new_term.append(a+b)
        elif o == 'product': new_term.append(a*b)
        elif o == 'minimum': new_term.append(np.min(a,b))
        elif o == 'maximum': new_term.append(np.max(a,b))
        elif o == 'greater than': new_term.append(int(a>b))
        elif o == 'less than': new_term.append(int(a<b))
        elif o == 'equal to': new_term.append(int(a==b))
        return new_term[0]
    elif len(term) >= 3 and isinstance(term[-1], str):        
        # get all numbers in front of operand
        number_list = []
        o = term.pop(-1)
        print('Operator:', o)
        while term:
            if isinstance(term[-1],int):
                number_list.append(term.pop(-1))
                print('Number list:', number_list)
                print('Remaining Term:', term)
        # switch case on o
        if o == 'sum': new_term.append(np.sum(number_list))
        elif o == 'product': new_term.append(np.prod(number_list))
        elif o == 'minimum': new_term.append(np.min(number_list))
        elif o == 'maximum': new_term.append(np.max(number_list))
        elif o == 'greater than': new_term.append(int(number_list[0] > number_list[1]))
        elif o == 'less than': new_term.append(int(number_list[0] < number_list[1]))
        elif o == 'equal to': new_term.append(int(number_list[0] == number_list[1]))
        print('New term:', new_term)
        return new_term[0]
    else: return term[0]

def part2(data:str):
    p1_sum, p1_list, _ , calculation = part1(data)
    print('\nPart 2 starting')
    print('Resulting list of part 1:', p1_list)
    print('Resulting calculation:', calculation)    


def test():
    out = read_input(path_to_file='input/test_input.txt')
    '''
    start_time = time.perf_counter()
    print('\nResult for part 1 in test: ', part1(out))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    '''
    start_time = time.perf_counter()
    print('\nResult for part 2 in test: ', part2(out))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")    

    
if __name__ == '__main__':
    data = read_input()
    test()

    '''
    start_time = time.perf_counter()
    print('\nResult for part 1: ', part1(data))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    
    start_time = time.perf_counter()
    print('\nResult for part 2: ', part2(data))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")
    '''