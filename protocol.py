import numpy as np

print("Hvilken besked vil du sende?")
contents = input()

input1 = [[20,10],[-10,30],[contents]]

def protocol_In(input_List):
    temp_main = []
    temp_main2 = []
    count = 0
    output = []

    for i in range(len(input_List)):
        temp = []
        for j in range(len(input_List[i])):
            if isinstance(input_List[i][j],int) == True:
                temp.append(hex(input_List[i][j]+128))
            elif isinstance(input_List[i][j],str) == True:
                for k in range(len(input_List[i][j])):
                    temp.append(hex(ord(input_List[i][j][k])))
        temp_main.append(temp)

    for i in range(len(temp_main)):
        if len(temp_main[i])>2:
            temp1 = []
            for j in range(len(temp_main[i])):
                temp1.append(hex(int(temp_main[i][j][2],16)))
                temp1.append(hex(int(temp_main[i][j][3],16)))
            temp_main2.append(temp1)
        elif len(temp_main[i])==2:
            temp2 = []
            for j in range(len(temp_main[i])):
                if len(temp_main[i][j])==3:
                    temp2.append(hex(0))
                    temp2.append(hex(int(temp_main[i][j][2],16)))
                elif len(temp_main[i][j])==4:
                    temp2.append(hex(int(temp_main[i][j][2],16)))
                    temp2.append(hex(int(temp_main[i][j][3],16)))
            temp_main2.append(temp2)

    for i in range(len(temp_main2)):
        for j in range(len(temp_main2[i])-1):
            if temp_main2[i][j]=='0x0' and temp_main2[i][j+1]=='0x1':
                temp_main2[i].insert(j,'0xf')
                temp_main2[i].insert(j,'0xf')

    for i in range(len(temp_main2)):
        count=count+1
        temp_main2[i].insert(0,hex(count))
    
    for i in range(len(temp_main2)):
        temp_main2[i].insert(0,'0x1')
        temp_main2[i].insert(0,'0x0')
        temp_main2[i].insert(len(temp_main2[i]),'0x0')
        temp_main2[i].insert(len(temp_main2[i]),'0x1')
    
    for i in range(len(temp_main2)):
        for j in range(len(temp_main2[i])):
            output.append(temp_main2[i][j])

    return output

def protocol_Out(hexaList):
    output = []
    move = []
    output2 = []
    message = []
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
        for l in range(len(tempOut[k])-1):
            if tempOut[k][l]=='0xf':
                if tempOut[k][l+1]=='0xf':
                    continue
                elif tempOut[k][l-1]=='0xf':
                    continue
                else:
                    temp1.append(tempOut[k][l])
            else:
                temp1.append(tempOut[k][l])
        temp1.append(tempOut[k][4])
        output.append(temp1)
    print(output)
    for i in range(len(output)):
        output[i].pop(0)
    
    for i in range(len(output)):
        count = 0
        new_list = []
        if len(output[i])<=4:
            for j in range(len(output[i])-1):
                if count % 2 == 0:
                    new_list.append((16*int(output[i][j],16)+int(output[i][j+1],16))-128)
                    count=count+1
                else:
                    count=count+1
            output2.append(new_list)
        else:
            output2.append(output[i])

    for i in range(len(output2)):
        if len(output2[i])==2:
            move.append(output2[i])
        else:
            message=output2[i]

    return move
#print(protocol_In(input1))
print(protocol_Out(protocol_In(input1)))