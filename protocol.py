import numpy as np

# 0xa betyder afsender computer
# 0xb er robotten
# oxc er modtager computer

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
    for k in range(len(list)):
        tempdataword=''
        codeword=[]
        for i in range(len(list[k])):
            tempdata=bin(int(list[k][i],16))
            tempdata=tempdata[2:]
            #print(tempdata)

            while(len(tempdata)<4):
               tempdata='0'+ tempdata
         #print(tempdata)
            tempdataword=tempdataword+tempdata

        #print(tempdataword)
        tempdataword=tempdataword+'00000'
        for j in range(len(tempdataword)):
          codeword.append(int(tempdataword[j]))
        #print(codeword)

        result=[]
        divisor=[1,0,0,1,1]

    

        tempres=codeword

        for j in range(len(codeword)-5):
            if(tempres[0]==1):
               for i in range(len(divisor)):
                  result.append(tempres[i]^divisor[i])
               result.pop(0)
               result.append(codeword[len(divisor)+j])
               tempres=result
               #print(tempres)
               result = []
            else:
                for i in range(len(divisor)):
                    result.append(tempres[i]^0)
                result.pop(0)
                result.append(codeword[len(divisor)+j])
                tempres=result
                #print(tempres)
                result = []

        remainder=[]

        for i in range(len(tempres)-1):
            remainder.append(tempres[i])


        #print(remainder,'remainder')
        hexremainder=''

        for i in range(len(remainder)):
            hexremainder=hexremainder+str(remainder[i])
    
        hexremainder=int(hexremainder,2)
   
        hexremainder=hex(hexremainder)
        list[k].append(hexremainder)
    return list

def decode_CRC(list):
    for k in range(len(list)):
        tempdataword=''
        codeword=[]
        for i in range(len(list[k])):
            tempdata=bin(int(list[k][i],16))
            tempdata=tempdata[2:]
            #print(tempdata)

            while(len(tempdata)<4):
                tempdata='0'+ tempdata
            #print(tempdata)
            tempdataword=tempdataword+tempdata

        #print(tempdataword)
    
        tempdataword=tempdataword + '0'
        for j in range(len(tempdataword)):
            codeword.append(int(tempdataword[j]))
        #print(codeword)

        result=[]
        divisor=[1,0,0,1,1]

    

        tempres=codeword

        for j in range(len(codeword)-5):
            if(tempres[0]==1):
                for i in range(len(divisor)):
                    result.append(tempres[i]^divisor[i])
                result.pop(0)
                result.append(codeword[len(divisor)+j])
                tempres=result
                #print(tempres)
                result = []
            else:
                for i in range(len(divisor)):
                    result.append(tempres[i]^0)
                result.pop(0)
                result.append(codeword[len(divisor)+j])
                tempres=result
                #print(tempres)
                result = []

        remainder=[]

        for i in range(len(tempres)-1):
            remainder.append(tempres[i])


        #print(remainder,'syndrome')
        hexremainder=''

        for i in range(len(remainder)):
            hexremainder=hexremainder+str(remainder[i])
    
        hexremainder=int(hexremainder,2)
   
        hexremainder=hex(hexremainder)

        if hexremainder == '0x0':
            list[k].pop(len(list[k])-1)
        else:
            print("Error in data")
    return list

def add_address(input_List):
    sender = '0xa'
    medium = '0xb'
    receiver = '0xc'
    for i in range(len(input_List)):
        input_List[i].insert(0,receiver)
        input_List[i].insert(0,medium)
        input_List[i].insert(0,sender)
    
    return input_List

def decode_address(input_List):
    for i in range(len(input_List)):
        if input_List[i][0]=='0xa' and input_List[i][1]=='0xb' and input_List[i][2]=='0xc':
            for j in range(3):
                input_List[i].pop(0)
        else:
            print('This message is not for me')

    return input_List
