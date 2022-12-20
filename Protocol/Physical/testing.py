from Class_DTMF import SEND
import sys
import numpy as np 
sys.path.append('../Mobile-Robotsystems')
#from Turtlebot.moveClass import moveClass
#from Protocol.DataLink.protocol_class import protocolClass
from Protocol.Physical.DTMF_overclass import DTMF
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import time
import csv

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
fs = 4000
amplitude = 15000
fade_P = 0.000
baud_rate = 10
sync = 20
send = SEND(fs, amplitude, fade_P, baud_rate,sync)
pack = [0, 1, 1, 0, 8, 3, 11, 13, 0, 1, 0, 1, 2, 4, 4, 6, 5, 6, 5, 7, 10, 2, 0, 6, 14, 4, 10, 2, 0, 1, 0, 1, 3, 7, 5, 7, 4, 7, 3, 14, 7, 0, 0, 1]






robot=DTMF(baud_rate,30, mono_robot = True)
#pack = protocolClass('0x0',[],robot)



def fft():
    twoDTMF = [*send.makeDTMF(697,1477), *send.makeDTMF(697,1209)]

    newDTMF = twoDTMF[int(4/8*len(twoDTMF)):]

    print(len(twoDTMF))
    print(len(newDTMF))

    xf = np.linspace(0,fs,len(newDTMF))
    yf=fft(newDTMF)
    yf=abs(yf)

    fig2 = plt.plot(xf,yf)
    plt.show()


pack=send.rand_pack(185)
print(pack)
# fe

send.setBaud(50)
send.setFade(0.005)
title1 = '1'
points1 = [*send.makeDTMF(1209,697),*send.makeDTMF(1336,697),*send.makeDTMF(1209,697)]
#print(points1)
send.send_package([0,15,0],plot=True)
send.plot_last_package(curve='r--')
#send.plot_last_package(curve='r--',title="20 baud rate with 40% fade")

send.setBaud(50)
send.setFade(0.005)
title2 = '2'
points2 = [*send.makeDTMF(1209,697),*send.makeDTMF(1633,697),*send.makeDTMF(1209,697)]
points3 = [*send.makeDTMF(1209,697),*send.makeDTMF(1477,770),*send.makeDTMF(1209,697)]
send.send_package([0],plot=True)
#send.plot_last_package(curve='r--',title="60 baud rate with 40% fade")







# field names 
fields1 = ['1'] 
fields2 = ['2'] 
    
# data rows of csv file 
rows = [ ['0x010'], 
         points1, 
         ['0x030'], 
         points2,
         ['0x060'], 
         points3]
  
with open('GFG.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)

    write.writerows(rows)
#send.send_package([0,15],False)


print(pack)


send.makeDTMF(1,1)

import time

import numpy as np
import pyaudio

p = pyaudio.PyAudio()

volume = 0.5  # range [0.0, 1.0]
fs = 44100  # sampling rate, Hz, must be integer
duration = 1  # in seconds, may be float
f = 440.0  # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
samples = (np.sin(2 * np.pi * np.arange(fs * duration) * 1209 / fs)+np.sin(2 * np.pi * np.arange(fs * duration) * 697 / fs)).astype(np.float32)

# per @yahweh comment explicitly convert to bytes sequence
output_bytes = (volume * samples).tobytes()

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# play. May repeat with different volume values (if done interactively)
start_time = time.time()
stream.write(output_bytes)
print("Played sound for {:.2f} seconds".format(time.time() - start_time))

stream.stop_stream()
stream.close()

p.terminate()



