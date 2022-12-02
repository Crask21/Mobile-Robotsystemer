import numpy as np

def sendercrc(list):
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
        


        #print(hexremainder)
        #print(tempremainder)
        #hexremainder=int(hexremainder,2)
   
        #hexremainder=hex(hexremainder)
        #print(hexremainder)
        #list[k].append(hexremainder)
    print(list)
    


def receivercrc(list):
    seqno=[]
    count=0

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


        print(remainder,'syndrome')
        hexremainder=''

        for i in range(len(remainder)):
            hexremainder=hexremainder+str(remainder[i])
    
        hexremainder=int(hexremainder,2)
        
        if hexremainder!=0x0:
            seqno.append(count)
        count+=1
   
        #hexremainder=hex(hexremainder)
        #print(hexremainder, 'hexsyndrome')
    print(seqno)


sendercrc([['0x1','0x5','0xb'],['0xa','0xa','0x9']])


receivercrc([['0x1', '0x5', '0xb', '0xf', '0x9', '0x9'], ['0xa', '0xa', '0x9', '0x1', '0xd', '0x0']])



