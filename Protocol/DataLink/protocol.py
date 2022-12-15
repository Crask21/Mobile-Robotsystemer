import numpy as np

# 0xa betyder afsender computer
# 0xb er robotten
# oxc er modtager computer



# Hej Prip, Ditzel har ringet
"""
[0, 1, 1, 4, 0, 8, 6, 10, 0, 0, 0, 0, 2, 0, 8, 0, 9, 4, 0, 2, 0, 0, 0, 0, 1, 1, 13, 8, 8, 13, 8, 0, 0, 0, 1, 0, 1, 4, 4, 4, 5, 6, 5, 5, 6, 10, 0, 4, 6, 13, 6, 10, 12, 0, 1, 0, 1, 5, 5, 5, 4, 4, 3, 2, 14, 3, 8, 0, 1, 0, 1]


Traceback (most recent call last):
  File "mainTurtlebot.py", line 43, in <module>
    main()
  File "mainTurtlebot.py", line 19, in main
    pack.DataLinkUp()
  File "/home/ubuntu/code/Mobile-Robotsystems/Protocol/DataLink/protocol_class.py", line 58, in DataLinkUp
    self.data_list=protocol.esc_check(self.data_list)
  File "/home/ubuntu/code/Mobile-Robotsystems/Protocol/DataLink/protocol.py", line 133, in esc_check
    temp.append(inpt_List[k][-1])
IndexError: list index out of range
"""



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

def data_seg(input_List, n):
    temp = []
    for i in range(len(input_List)):
        if len(input_List[i]) > 2:
            for j in range(0, len(input_List[i]), n):
                temp.append(input_List[i][j:j+n])
        else:
            temp.append(input_List[i])
    return temp          

def hexa_devide(input_List):
    temp_main = []
    for i in range(len(input_List)):
        if len(input_List[i])>2:
            temp = []
            for j in range(len(input_List[i])):
                temp.append(hex(int(input_List[i][j][2],16)))
                temp.append(hex(int(input_List[i][j][3],16)))
            temp_main.append(temp)
            
        elif len(input_List[i])<2:
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
    output2 = []
    for i in range(len(input_List)):
        for j in range(len(input_List[i])):
            output.append(input_List[i][j])
    for i in range(len(output)):
        output2.append(int(output[i],16))
    return output2
    

def organize(input_List):
    check = 0
    output = []
    tempA = []
    for i in range(len(input_List)):
        tempA.append(hex(input_List[i]))
    #print(tempA)
    
    for i in range(len(tempA)-1):
        if tempA[i]=='0x0' and tempA[i+1]=='0x1':
            if tempA[i-1]!='0xf' or tempA[i-2]!='0xf':
                check = check+1
                if check % 2 == 1:
                    temp = []
                    for j in np.arange(i+2,len(tempA)-1):
                        if tempA[j]=='0x0' and tempA[j+1]=='0x1':
                            if tempA[j-1]=='0xf' and tempA[j-2]=='0xf':
                                temp.append(tempA[j])
                            else:
                                output.append(temp)
                                break
                        else:
                            temp.append(tempA[j])
            
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
        temp.append(inpt_List[k][-1])
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
        if len(input_List[i])==4:
            for j in range(len(input_List[i])-1):
                if count % 2 == 0:
                    temp.append((16*int(input_List[i][j],16)+int(input_List[i][j+1],16))-128)
                    count=count+1
                else:
                    count=count+1
            output.append(temp)
        else:
            string = ""
            for j in range(len(input_List[i])-1):
                if count % 2 == 0:
                    string += chr(16*int(input_List[i][j],16)+int(input_List[i][j+1],16))
                    count = count+1
                else:
                    count=count+1
            stringL = [string]
            output.append(stringL)
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
        tempdataword=tempdataword+'0000000000000'
        for j in range(len(tempdataword)):
          codeword.append(int(tempdataword[j]))
        #print(codeword)

        result=[]
        divisor=[1,1,1,1,0,0,1,1,1,1,0,1,1]

    

        tempres=codeword

        for j in range(len(codeword)-13):
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
        
        tempremainder=''
        temptempremainder=''
            
        for i in range(len(remainder)):
            hexremainder=hexremainder+str(remainder[i])
        
        for x in range(0,3):
            for y in range(4):
                tempremainder += hexremainder[y+4*(x)]
                
            #print(tempremainder[x*4:])
            temptempremainder=tempremainder[x*4:]

            tttr=int(temptempremainder,2)
            tttr=hex(tttr)
            #print(tttr)
            #tempremainder=''
            list[k].append(tttr)
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
        divisor=[1,1,1,1,0,0,1,1,1,1,0,1,1]

    

        tempres=codeword

        for j in range(len(codeword)-13):
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
            list[k].pop(len(list[k])-1)
            list[k].pop(len(list[k])-1)
        else:
            list[k]= [list[k][0],"error"]
            print("Error in data")
    return list

def add_address(input_List, address):
    #address = ['0xa','0x0','0xd']
    input_List = [address] + input_List
    return input_List

def decode_address(input_List, address):
    if input_List[0][2] == address : print('second true')
    if len(input_List[0])>2 and input_List[0][2] == address:
        return input_List
    else:
        print("Addressing sucks")
        return False

    

def data_comb(input_List):
    output = []
    temp = []
    print(input_list)
    for i in range(len(input_List)):
        if len(input_List[i])!=4:
            for j in range(len(input_List[i])):
                temp.append(input_List[i][j])
        elif i!=0 and len(input_List[i-1])!=4:
            print("data_comb")
            print(input_List[i])
            print("data comb")
            for j in range(len(input_List[i])):
                temp.append(input_List[i][j])
        else:
            output.append(input_List[i])
    output.append(temp)
    return output



"""
list1 = []
for i in range(1000):
    list1.append(i+1)
for i in range(0, len(list1), 100):
    chunk = list1[i:i+100]
    print(chunk)
"""