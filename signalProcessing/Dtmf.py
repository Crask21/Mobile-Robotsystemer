
inputList1 = [1336,941]

dtmf_freq = [[1209,697], # 0
                    [1336,697],  # 1
                    [1477,697],  # 2
                    [1633,697],  # 3
                    [1209,770],  # 4
                    [1336,770],  # 5
                    [1477,770],  # 6
                    [1633,770],  # 7
                    [1209,852],  # 8
                    [1336,852],  # 9
                    [1477,852],  # A
                    [1633,852],  # B
                    [1209,941],  # C
                    [1336,941],  # D
                    [1477,941],  # E
                    [1633,941]]  # F

upperRange= 20
lowerRange=10

def dtmf_to_hexa(inputFreqs):

    output =0
    inputFreqs.sort()
    for i in range(16):
        if (inputFreqs[0]<dtmf_freq[i][1]+upperRange and inputFreqs[0]>dtmf_freq[i][1]-lowerRange)and(inputFreqs[1]<dtmf_freq[i][0]+upperRange and inputFreqs[1]>dtmf_freq[i][0]-lowerRange):
            output= hex(i)
    return output
    #print(output)


    #for i in range(len(inputList)):
    #    if(inputList[0]>inputList[1]):
    #        temp = inputList[0]
    #        inputList[0] = inputList[1]
    #        inputList[1] = temp

    

    #if((input1>=650) and (input1<=730)):
    #    if((input2>=1150) and (input2<=1250)):
    #        output=0x0
    #    elif((input2>=1280) and (input2<=1380)):
    #        output=0x1
    #    elif((input2>=1420) and (input2<=1520)):
    #        output=0x2
    #    elif((input2>=1580) and (input2<=1680)):
    #        output=0x3
    #elif((input1>=745) and (input1<=810)):
    #    if((input2>=1150) and (input2<=1250)):
    #        output=0x4
    #    elif((input2>=1280) and (input2<=1380)):
    #        output=0x5
    #    elif((input2>=1420) and (input2<=1520)):
    #        output=0x6
    #    elif((input2>=1580) and (input2<=1680)):
    #        output=0x7
    #elif((input1>=820) and (input1<=890)):
    #    if((input2>=1150) and (input2<=1250)):
    #        output=0x8
    #    elif((input2>=1280) and (input2<=1380)):
    #        output=0x9
    #    elif((input2>=1420) and (input2<=1520)):
    #        output=0xA
    #    elif((input2>=1580) and (input2<=1680)):
    #        output=0xB
    #elif((input1>=900) and (input1<=980)):
    #    if((input2>=1150) and (input2<=1250)):
    #        output=0xC
    #    elif((input2>=1280) and (input2<=1380)):
    #        output=0xD
    #    elif((input2>=1420) and (input2<=1520)):
    #        output=0xE
    #    elif((input2>=1580) and (input2<=1680)):
    #        output=0xF
    #print(hex(output))
    #return output
    #
      
            
dtmf_to_hexa(inputList1)


