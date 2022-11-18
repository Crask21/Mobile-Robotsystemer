import numpy as np

with open('test.txt') as f:
    contents = f.read()

input_list = [[20,10],[-10,30],[contents]]

def convert_to_hexa(input_List):
    temp_main = []
    for i in range(len(input_List)):
        temp = []
        for j in range(len(input_List[i])):
            if isinstance(input_List[i][j],int) == True:
                temp.append(hex(input_List[i][j]+128))
            elif isinstance(input_List[i][j],str) == True:
                for k in range(len(input_List[i][j])):
                    temp.append(hex(ord(input_List[i][j][k])))
        temp_main.append(temp)
    return temp_main

def hexa_devide(input_List):
    temp_main = []
    for i in range(len(input_List)):
        if len(input_List[i])>2:
            temp = []
            for j in range(len(input_List[i])):
                temp.append(hex(int(input_List[i][j][2],16)))
                temp.append(hex(int(input_List[i][j][3],16)))
            temp_main.append(temp)
        elif len(input_List[i])==2:
            temp1 = []
            for j in range(len(input_List[i])):
                if len(input_List[i][j])==3:
                    temp1.append(hex(0))
                    temp1.append(hex(int(input_List[i][j][2],16)))
                elif len(input_List[i][j])==4:
                    temp1.append(hex(int(input_List[i][j][2],16)))
                    temp1.append(hex(int(input_List[i][j][3],16)))
            temp_main.append(temp1)
    return temp_main

def add_esc(input_List):
    for i in range(len(input_List)):
        for j in range(len(input_List[i])-1):
            if input_List[i][j]=='0x0' and input_List[i][j+1]=='0x1':
                input_List[i].insert(j,'0xf')
                input_List[i].insert(j,'0xf')
    return input_List

def add_seq(input_List):
    count = 0
    for i in range(len(input_List)):
        count=count+1
        input_List[i].insert(0,hex(count))
    return input_List

def add_StartStop(Input_List):
    for i in range(len(Input_List)):
        Input_List[i].insert(0,'0x1')
        Input_List[i].insert(0,'0x0')
        Input_List[i].insert(len(Input_List[i]),'0x0')
        Input_List[i].insert(len(Input_List[i]),'0x1')
    return Input_List

def one_list(input_List):
    output = []
    for i in range(len(input_List)):
        for j in range(len(input_List[i])):
            output.append(input_List[i][j])
    return output

def organize(input_List):
    check = 0
    output = []
    for i in range(len(input_List)-1):
        if input_List[i]=='0x0' and input_List[i+1]=='0x1':
            if input_List[i-1]!='0xF' and input_List[i-2]!='0xf':
                check = check+1
                if check % 2 == 1:
                    temp = []
                    for j in np.arange(i+2,len(input_List)):
                        if input_List[j]=='0x0' and input_List[j+1]=='0x1':
                            if input_List[j-1]=='0xf' and input_List[j-2]=='0xf':
                                temp.append(input_List[j])
                            else:
                                output.append(temp)
                                break
                        else:
                            temp.append(input_List[j])
    return output

def esc_check(inpt_List):
    output = []
    for k in range(len(inpt_List)):
        temp = []
        for l in range(len(inpt_List[k])-1):
            if inpt_List[k][l]=='0xf':
                if inpt_List[k][l+1]=='0xf':
                    continue
                elif inpt_List[k][l-1]=='0xf':
                    continue
                else:
                    temp.append(inpt_List[k][l])
            else:
                temp.append(inpt_List[k][l])
        temp.append(inpt_List[k][len(inpt_List[k])-1])
        output.append(temp)
    return output

def remove_seq(input_List):
    for i in range(len(input_List)):
        input_List[i].pop(0)
    return input_List

def convert_to_decimal(input_List):
    output = []
    for i in range(len(input_List)):
        count = 0
        temp = []
        if len(input_List[i])<=4:
            for j in range(len(input_List[i])-1):
                if count % 2 == 0:
                    temp.append((16*int(input_List[i][j],16)+int(input_List[i][j+1],16))-128)
                    count=count+1
                else:
                    count=count+1
            output.append(temp)
        else:
            output.append(input_List[i])
    return output

def hexa_to_msg(dtmf_signal):
    temp_list = []
    message = ""
    for i in range(len(dtmf_signal)):
        count = 0
        if len(dtmf_signal[i])>2:
            for j in range(len(dtmf_signal[i])-1):
                if count % 2 == 0:
                    temp_list.append(hex(16*int(dtmf_signal[i][j],16)+int(dtmf_signal[i][j+1],16)))
                    count = count+1
                else:
                    count = count+1
    for i in range(len(temp_list)):
        message = message+chr(int(temp_list[i],16))

    return message

def movement(input_List):
    move = []
    for i in range(len(input_List)):
        if len(input_List[i])==2:
            move.append(input_List[i])
    return move

def add_CRC(list):
   

#def add_address(input_List):


#Add protocol
input_list=convert_to_hexa(input_list)
input_list=hexa_devide(input_list)
input_list=add_esc(input_list)
input_list=add_seq(input_list)
input_list=add_CRC(input_list)
#input_list=add_StartStop(input_list)
#input_list=one_list(input_list)
print(input_list)
'''
#Decode protocol
input_list=organize(input_list)
input_list=esc_check(input_list)
input_list=remove_seq(input_list)
input_list=convert_to_decimal(input_list)
print(input_list)
print(hexa_to_msg(input_list))
print(movement(input_list))
'''