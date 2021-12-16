# -*- coding: utf-8 -*-
import time

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
        data = f.readlines()[0]
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
    data_bin = ''.join([HEX_TO_BIN_DICT[x] for x in data])
    res, _ = decode_transmission_block(data_bin)
    return  sum(res)

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

def decode_transmission_block(data_bin:str, packet_version_list:list = []):
    print('\nData (bin):', data_bin)
    # TODO recurse the packed packages    
    # encode header
    version = data_bin[:3]
    version_dec = int(version,2)
    type_id = data_bin[3:6]
    type_id_dec = int(type_id,2)

    packet_version_list.append(version_dec)        
    print('Packet version list:', packet_version_list)

    print('Version (bin, dec):', version, version_dec)
    if (type_id_dec == 4):
        # literal value -> one single binary number, is always the last package, returns the packet_version_list
        print('TypeID (bin, dec):', type_id, type_id_dec, 'is a literal')
        value_dec, l = literal_value(data_bin)
        print('Literal decimal value:', value_dec)
        last_index = l+1
        print('Last index of literal:',last_index)
        return packet_version_list, last_index
        
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
            for i in range(amount_subpackets_dec):
                subpackets_start = 18
                print('Next package starts at:', subpackets_start)
                print('Next subpacket number:', i+1)
                # slice the data and go down each individual package
                subpackets_start+=shift
                packet_version_list, shift = decode_transmission_block(data_bin[subpackets_start:], packet_version_list)
                print('Next package starts at:', subpackets_start)
            print('Packet version list:', packet_version_list)
            return packet_version_list, subpackets_start
        
        elif length_type_id == '0':
            # has a 15 bit number following the total length of the subpackets contained
            length_subpacket = data_bin[7:22]
            length_subpacket_dec = int(length_subpacket,2)
            subpackets_start = 22
            subpackets_end = subpackets_start+length_subpacket_dec
            print('Subpackets total length:', length_subpacket_dec)
            print('Subpackets end:', subpackets_end)
            shift = 0
            while (subpackets_start+shift < subpackets_end and len(data_bin[subpackets_start:subpackets_end])>10):
                packet_version_list, shift = decode_transmission_block(data_bin[subpackets_start:], packet_version_list)
                subpackets_start+=shift
                print('Current Index to shift:', shift)
                print('Next package @:', subpackets_start)
            print('Packet version list:', packet_version_list)
            
            return packet_version_list, subpackets_start
    


def part2(data):
    return 0
     
def test():
    out = read_input(path_to_file='input/test_input.txt')
    
    start_time = time.perf_counter()
    print('\nResult for part 1 in test: ', part1(out))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    '''
    start_time = time.perf_counter()
    print('\nResult for part 2 in test: ', part2(out))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")    
    '''
    
if __name__ == '__main__':
    input_matrix = read_input()
    test()
    '''
    start_time = time.perf_counter()
    print('\nResult for part 1: ', part1(input_matrix))
    finish_time = time.perf_counter()
    print(f"Calculated part 1 in {(finish_time - start_time):0.4f}s")
    
    start_time = time.perf_counter()
    print('\nResult for part 2: ', part2(input_matrix))
    finish_time = time.perf_counter()
    print(f"Calculated part 2 in {(finish_time - start_time):0.4f}s")
    '''