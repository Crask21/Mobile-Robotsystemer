from main_sender import thread_dtmf
thread_dtmf()



inputList1 = [927,1445];

def dtmf_to_hexa(inputList):

    output = [];

    for i in range(len(inputList)):
        if(inputList[0]>inputList[1]):
            temp = inputList[0];
            inputList[0] = inputList[1];
            inputList[1] = temp;

    input1 = inputList[0];
    input2 = inputList[1];

    if((input1>=650) and (input1<=730)):
        if((input2>=1150) and (input2<=1250)):
            output.append(0);
        elif((input2>=1280) and (input2<=1380)):
            output.append(1);
        elif((input2>=1420) and (input2<=1520)):
            output.append(2);
        elif((input2>=1580) and (input2<=1680)):
            output.append(3);
    elif((input1>=745) and (input1<=810)):
        if((input2>=1150) and (input2<=1250)):
            output.append(4);
        elif((input2>=1280) and (input2<=1380)):
            output.append(5);
        elif((input2>=1420) and (input2<=1520)):
            output.append(6);
        elif((input2>=1580) and (input2<=1680)):
            output.append(7);
    elif((input1>=820) and (input1<=890)):
        if((input2>=1150) and (input2<=1250)):
            output.append(8);
        elif((input2>=1280) and (input2<=1380)):
            output.append(9);
        elif((input2>=1420) and (input2<=1520)):
            output.append('A');
        elif((input2>=1580) and (input2<=1680)):
            output.append('B');
    elif((input1>=900) and (input1<=980)):
        if((input2>=1150) and (input2<=1250)):
            output.append('C');
        elif((input2>=1280) and (input2<=1380)):
            output.append('D');
        elif((input2>=1420) and (input2<=1520)):
            output.append('E');
        elif((input2>=1580) and (input2<=1680)):
            output.append('F');

    return output;
      
            
#dtmf_to_hexa(inputList1)

#print('output')




