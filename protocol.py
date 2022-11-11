import numpy as np

input = [0x0,0x1,0x3,0xf,0xf,0x0,0x1,0x5,0x7,0x0,0x1,0x0,0x1,0x1,0x2,0x0,0x1,0x3,0x4,0x0,0x1,0xf,0xf,0x0,0x1,0x4,0x5,0x0,0x1,0x7]

def protocol(hexaList):
    output = []
    tempOut=[]
    check = 0
    for i in range(len(hexaList)-1):
        if hexaList[i]==0x0 and hexaList[i+1]==0x1:
            if hexaList[i-1]!=0xF and hexaList[i-2]!=0xF:
                check = check+1
                if check % 2 == 1:
                    temp = []
                    for j in np.arange(i+2,len(hexaList)):
                        if hexaList[j]==0x0 and hexaList[j+1]==0x1:
                            if hexaList[j-1]==0xf and hexaList[j-2]==0xf:
                                temp.append(hexaList[j])
                            else:
                                tempOut.append(temp)
                                break
                        else:
                            temp.append(hexaList[j])
    for k in range(len(tempOut)):
        temp1 = []
        for l in range(len(tempOut[k])):
            if tempOut[k][l]==0xf:
                if tempOut[k][l+1]==0xf:
                    continue
                elif tempOut[k][l-1]==0xf:
                    continue
                else:
                    temp1.append(tempOut[k][l])
            else:
                temp1.append(tempOut[k][l])
        output.append(temp1)
    return output

print(protocol(input))
