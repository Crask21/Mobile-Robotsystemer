from Send_DTMF.Class_DTMF import DTMF





# DTMF Settings
fs = 44100
amplitude = 5000
media = 'PyGame' # 'SD'
fade_P = 0.02

baud_rate = 10



# Initialization
dtmf = DTMF(fs, amplitude, fade_P, baud_rate, media)


dtmf.synchroniazation(10)
dtmf.send_package([0xB,0xA,0xB,0xA,0xB,0xA,0xB,0xA,0xB,0xA,0xB,0xA,0xB,0xA,0xB,0xA,0xC,0xC])
#dtmf.send_package(dtmf.rand_pack(10))






