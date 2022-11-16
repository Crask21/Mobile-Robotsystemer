import numpy as np

input = 2

print(input)

def valTo2Hex(value):
    hex_dict = {
    '0' : 0x0,
    '1' : 0x1,
    '2' : 0x2,
    '3' : 0x3,
    '4' : 0x4,
    '5' : 0x5,
    '6' : 0x6,
    '7' : 0x7,
    '8' : 0x8,
    '9' : 0x9,
    'a' : 0xA,
    'b' : 0xB,
    'c' : 0xC,
    'd' : 0xD,
    'e' : 0xE,
    'f' : 0xF
    }
    value = hex(value+128)
    if len(value) == 4: # 2 hexa decimaler 
        return [hex_dict[value[2]], hex_dict[value[3]]]
    else:               # 1 hexa decimal
        return [0x0, hex_dict[value[2]]]


def TwoHexToVal(list):
    return 16*list[0]+list[1]-128


h_input=valTo2Hex(input)

print(h_input)

print(TwoHexToVal(h_input))


