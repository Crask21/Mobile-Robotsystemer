from Class_DTMF import SEND


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




# DTMF Settings
fs = 44100
amplitude = 5000
fade_P = 0.4
baud_rate = 50
sync = 30

send = SEND(fs, amplitude, fade_P, baud_rate,sync)
pack = [14, 14, 1, 12, 0, 0, 12, 9, 9, 15, 11, 10, 7, 12, 9, 13, 14, 14, 12, 0, 15, 12, 11, 1, 7, 6, 6, 7, 0, 1, 12, 8, 6, 13, 8, 3, 1, 1, 0, 6]

pack = [*pack,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


send.send_package([0x0],False)
send.send_package(pack)

print(pack)









list_send =     [11, 8, 5, 1, 15, 2, 5, 6, 14, 14, 11, 2, 2, 6, 15, 12]
list_recieved = [11, 8, 5, 1, 15, 2, 4, 6, 14, 13, 11, 2, 2, 6, 15,1,1]



def compare(original, recieved, compare = True):

    dif = len(recieved) - len(original)

    if len(recieved) > len(original):
            recieved = recieved[:len(recieved) - dif]

    if original == recieved:
        print('100% match')
    


    elif compare:
        count = 0

        length = len(original) if dif >= 0 else len(recieved)

        for i in range(length):
            if recieved[i] == original[i]:
                count += 1
        
        print(count/len(original)*100,'% match.', len(original) - count, 'errors')
        print('Original:',original)
        print('Recieved:',recieved)


    else:
        send_count =[]
        for i in range(16):
            send_count.append(original.count(i))

        recieved_count = []
        for i in range(16):
            recieved_count.append(recieved.count(i))

        count = 0
        for i in range(16):
            
            if recieved_count[i] == send_count[i]:
                count += 1



        print(count/16*100,'% count match. ', count, 'errors')
        print(original)
        print(recieved)

compare(list_send,list_recieved)

