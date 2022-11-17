from Send_DTMF.Class_DTMF import DTMF
from protocol import protocol_In
from protocol import protocol_Out

with open('test.txt') as f:
    PC_message = f.read()

print(PC_message)
# --------------- INPUT ------------------ #
PC_message = "pi = 3"
robot_control = [[34,-125],[84,-16],[29,36]]
# --------------- INPUT ------------------ #






package = protocol_In([*robot_control,[PC_message]])



# DTMF Settings
fs = 44100
amplitude = 5000
fade_P = 0.01
baud_rate = 200



# Initialization
dtmf = DTMF(fs, amplitude, fade_P, baud_rate, 'PyGame')

sync = dtmf.synchroniazation(10)
dtmf.send_package(package)

print([dtmf.synchroniazation(10),package])


