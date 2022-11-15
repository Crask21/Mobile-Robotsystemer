import numpy as np

with open('test.txt') as f:
    contents = f.read()

input1 = [[20,10],[10,-30],[contents]]

def protocol_In(input_List):
    temp_main = []
    count = 0
    output = []
    for i in range(len(input1)):
        temp = []
        for j in range(len(input1[i])):
            if isinstance(input1[i][j],int) == True:
                temp.append(hex(input1[i][j]))
            elif isinstance(input1[i][j],str) == True:
                for k in range(len(input1[i][j])):
                    temp.append(hex(ord(input1[i][j][k])))
        temp_main.append(temp)
    for i in range(len(temp_main)):
        for j in range(len(temp_main[i])):
            if temp_main[i][j]=='0x0' and temp_main[i][j+1]=='0x1':
                temp_main[i].insert(j,'0xf')
                temp_main[i].insert(j,'0xf')
    for i in range(len(temp_main)):
        count=count+1
        temp_main[i].insert(0,hex(count))
    
    for i in range(len(temp_main)):
        temp_main[i].insert(0,'0x1')
        temp_main[i].insert(0,'0x0')
        temp_main[i].insert(len(temp_main[i]),'0x0')
        temp_main[i].insert(len(temp_main[i]),'0x1')
    '''
    for i in range(len(temp_main)):
        for j in range(len(temp_main[i])):
            output.append(temp_main[j])
    '''

    return temp_main

def protocol_Out(hexaList):
    output = []
    tempOut=[]
    check = 0
    for i in range(len(hexaList)-1):
        if hexaList[i]=='0x0' and hexaList[i+1]=='0x1':
            if hexaList[i-1]!='0xF' and hexaList[i-2]!='0xf':
                check = check+1
                if check % 2 == 1:
                    temp = []
                    for j in np.arange(i+2,len(hexaList)):
                        if hexaList[j]=='0x0' and hexaList[j+1]=='0x1':
                            if hexaList[j-1]=='0xf' and hexaList[j-2]=='0xf':
                                temp.append(hexaList[j])
                            else:
                                tempOut.append(temp)
                                break
                        else:
                            temp.append(hexaList[j])
    for k in range(len(tempOut)):
        temp1 = []
        for l in range(len(tempOut[k])):
            if tempOut[k][l]=='0xf':
                if tempOut[k][l+1]=='0xf':
                    continue
                elif tempOut[k][l-1]=='0xf':
                    continue
                else:
                    temp1.append(tempOut[k][l])
            else:
                temp1.append(tempOut[k][l])
        output.append(temp1)
    return output

print(protocol_In(input1))
#print(protocol_Out(protocol_In(input1)))