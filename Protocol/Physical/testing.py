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
amplitude = 1000
fade_P = 0.1
baud_rate = 80
sync = 20
send = SEND(fs, amplitude, fade_P, baud_rate,sync)
pack = [0, 1, 10, 11, 12, 1, 8, 10, 9, 4, 7, 0, 1, 0, 1, 10, 11, 12, 2, 7, 6, 9, 14, 5, 0, 1, 0, 1, 10, 11, 12, 3, 4, 4, 6, 5, 6, 5, 7, 10, 2, 0, 6, 14, 7, 5, 7, 4, 7, 3, 0, 0, 1]



pack = [*pack,0,0]

send.send_package([0x0,0xF,0x0],False)
send.plot_last_package()
#send.send_package(pack)

print(pack)








