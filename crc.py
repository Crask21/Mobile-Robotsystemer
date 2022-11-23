


def sendercrc(list):
    for j in range(len(list)):
        tempdataword=''
        codeword=[]
        for i in range(len(list[j])):
            tempdata=bin(int(list[j][i],16))
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


        print(remainder,'remainder')
        hexremainder=''

        for i in range(len(remainder)):
            hexremainder=hexremainder+str(remainder[i])
    
        hexremainder=int(hexremainder,2)
   
        hexremainder=hex(hexremainder)
        print(hexremainder, 'hexremainder')
    


def receivercrc(list):
    seqno=[]

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


        print(remainder,'syndrome')
        hexremainder=''

        for i in range(len(remainder)):
            hexremainder=hexremainder+str(remainder[i])
    
        hexremainder=int(hexremainder,2)
        
        if hexremainder!=0x0:
            seqno.append(list[k][0])
   
        hexremainder=hex(hexremainder)
        print(hexremainder, 'hexsyndrome')
    print(seqno)

sendercrc([['0xa','0xa'],['0x1','0x5']])

receivercrc([['0x1','0x5','0xb'],['0xa','0xa','0x9']])