from Send_DTMF.Class_DTMF import DTMF 
from Send_DTMF.Class_DTMF import CharListToInt
from protocol import protocol_In 
from protocol import protocol_Out
import threading

with open('test.txt') as f:
    PC_message = f.read()


# --------------- INPUT ------------------ #
PC_message = "pi = 3"
robot_control = [[34,-125],[84,-16],[29,36]]
# --------------- INPUT ------------------ #




# Make package
package = CharListToInt(protocol_In([*robot_control,[PC_message]]))



# DTMF Settings
fs = 44100
amplitude = 5000
fade_P = 0.02
baud_rate = 20



# Initialization
dtmf = DTMF(fs, amplitude, fade_P, baud_rate)

# Send Package
sync = dtmf.synchroniazation(10,1)
#dtmf.send_package([*sync,*package])
#dtmf.plot_last_package()

# Print Package
print([sync,package])

def thread_f():
    dtmf.send_package([*sync,*package])



play_package = threading.Thread(target=thread_f, args=())



def thread_dtmf():
    play_package.start()

#from main_sender import thread_dtmf
#thread_dtmf()


