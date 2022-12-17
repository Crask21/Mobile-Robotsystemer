from Protocol.Physical.Class_DTMF import SEND

from Protocol.Physical.Threadprog5 import LISTEN

class DTMF:
    def __init__(self, baud, sync=10, mono_robot=False):
        # DTMF Settings
        fs = 44100
        amplitude = 15000
        media = 'PyGame' # 'SD'
        fade_P = 0.005
        baud_rate = baud
        syn = sync
        # SYNC

        

        
        self.send = SEND(fs, amplitude, fade_P, baud_rate,syn, media,mono=mono_robot)
        self.listen=LISTEN(baud_rate, syn, fade_P, amplitude, fs, pack=[0, 1, 1, 0, 8, 3, 11, 13, 0, 1, 0, 1, 2, 5, 3, 7, 5, 6, 3, 6, 3, 6, 5, 7, 3, 8, 6, 15, 0, 1, 0, 1, 3, 6, 6, 7, 5, 6, 12, 2, 0, 7, 2, 6, 15, 14, 10, 7, 0, 1, 0, 1, 4, 7, 5, 7, 4, 6, 5, 6, 11, 7, 0, 1])


#robot=DTMF(10)
#robot.listen.startListen()
#robot.send.send_package([0xc,0xa,0xa,0xa,0xa,0xb])
# helo

def compare(data, original, recieved, compare = True):


        dif = len(recieved) - len(original)

        if len(recieved) > len(original):
                recieved2 = recieved.copy()
                recieved = recieved[:len(recieved) - dif]


        if original == recieved:
            print('100% match')
            print("Original: ",original)
            
            print("Recieved: ",recieved2)
            return 100
        


        elif compare:
            count = 0

            length = len(original) if dif >= 0 else len(recieved)

            for i in range(length):
                if recieved[i] == original[i]:
                    count += 1
            accuracy = count/len(original)*100
            
            print(accuracy,'% match.', len(original) - count, 'errors')
            print('Original:',original)
            print('Recieved:',recieved)
            return accuracy


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
            return count/16*100



