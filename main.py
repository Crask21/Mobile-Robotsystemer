from Send_DTMF.Class_DTMF import DTMF
from Send_DTMF.Class_DTMF import synchroniazation
from Send_DTMF.Class_DTMF import rand_pack
from protocol import protocol_In
from protocol import protocol_Out





# DTMF Settings
fs = 44100
amplitude = 5000
fade_P = 0.01
baud_rate = 30



# Initialization
dtmf = DTMF(fs, amplitude, fade_P, baud_rate, 'PyGame')








