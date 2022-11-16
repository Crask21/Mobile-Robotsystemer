from Class_DTMF import DTMF
from Class_DTMF import rand_pack
from Class_DTMF import synchroniazation



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
media = 'PyGame' # 'SD'
fade_P = 0.02
baud_rate = 10



# Initialization
dtmf = DTMF(fs, amplitude, fade_P, baud_rate, media)



dtmf.send_package(synchroniazation(10))
dtmf.send_package(rand_pack(10))







# Plot FFT
    #data_P.send_package([0xC])
    #data_P.plot_fft()

# Send custom freq
    #sound = data_P.makeDTMF(amplitude,1/baud_rate,dtmf_freq[0xC][1],dtmf_freq[0xC][0],fs,fade_P)
    #data_P.play_PyGame(sound)




#def thread_f():
#    data_P.send_package(sync)
#    data_P.send_package(random_data)


#play_package = threading.Thread(target=thread_f, args=())

#play_package.start()


