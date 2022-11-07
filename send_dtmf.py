import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import sounddevice as sd
#import pygame

import pygame



fs = 44100 # Hz   sample frequency
baud = 1
duration = 1/baud
percentage_fade = 0.1




def makeDTMF(amplitude,dur,freq1,freq2,k,f_sample):


    time = np.arange(k*dur, k*dur + dur, 1/f_sample)
    xi = amplitude * np.sin(2*np.pi*freq2*time) + amplitude * np.sin(2*np.pi*freq1*time)   # 0.5 is arbitrary to avoid clipping sound card DAC
    #x = (x*32768).astype(np.int16)                                     # scale to int16 for sound card


    number_of_faded_points = int(dur*percentage_fade * f_sample)
    fade = np.linspace(0,1,num=number_of_faded_points)
    fade_end = np.linspace(1,0,num=number_of_faded_points)

    for j in np.arange(number_of_faded_points):
        xi[j] = xi[j] * fade[j]

    for j in np.arange(-1*number_of_faded_points,-1):    
        xi[j] = xi[j] * fade_end[j]
        
    
    #return [time,xi]
    return xi



dtmf_f = [[1209,697],[1336,697],[1477,697],[1633,697],[1209,770],[1336,770],[1477,770],[1633,770],[1209,852],[1336,852],[1477,852],[1633,852],[1209,941],[1336,941],[1477,941],[1633,941]]

print(dtmf_f[0xF])

w0 = makeDTMF(10000,duration,dtmf_f[0x0][0],dtmf_f[0x0][1],0,fs)
w1 = makeDTMF(10000,duration,dtmf_f[0x1][0],dtmf_f[0x1][1],0,fs)
w2 = makeDTMF(10000,duration,dtmf_f[0x2][0],dtmf_f[0x2][1],0,fs)
w3 = makeDTMF(10000,duration,dtmf_f[0x3][0],dtmf_f[0x3][1],0,fs)
w4 = makeDTMF(10000,duration,dtmf_f[0x4][0],dtmf_f[0x4][1],0,fs)
w5 = makeDTMF(10000,duration,dtmf_f[0x5][0],dtmf_f[0x5][1],0,fs)
w6 = makeDTMF(10000,duration,dtmf_f[0x6][0],dtmf_f[0x6][1],0,fs)
w7 = makeDTMF(10000,duration,dtmf_f[0x7][0],dtmf_f[0x7][1],0,fs)
w8 = makeDTMF(10000,duration,dtmf_f[0x8][0],dtmf_f[0x8][1],0,fs)
w9 = makeDTMF(10000,duration,dtmf_f[0x9][0],dtmf_f[0x9][1],0,fs)
wA = makeDTMF(10000,duration,dtmf_f[0xA][0],dtmf_f[0xA][1],0,fs)
wB = makeDTMF(10000,duration,dtmf_f[0xB][0],dtmf_f[0xB][1],0,fs)
wC = makeDTMF(10000,duration,dtmf_f[0xC][0],dtmf_f[0xC][1],0,fs)
wD = makeDTMF(10000,duration,dtmf_f[0xD][0],dtmf_f[0xD][1],0,fs)
wE = makeDTMF(10000,duration,dtmf_f[0xE][0],dtmf_f[0xE][1],0,fs)
wF = makeDTMF(10000,duration,dtmf_f[0xF][0],dtmf_f[0xF][1],0,fs)


seq = [*wA,*wB,*wC]
seq_numb = 3



wav_wave = np.array(seq, dtype=np.int16)



time = np.arange(0, duration*seq_numb, 1/fs)
#time = np.delete(time,0)
plt.plot(time,seq,'r--')
plt.ylabel('some numbers')
plt.show()

#while True:
    #sd.play(wav_wave, blocking=True)





###    t = np.arange(i * duration, duration + i * duration, 1/fs)
##    xi = 0.5 * np.sin(2*np.pi*sekv[i][0]*t) + 0.5 * np.sin(2*np.pi*sekv[i][1]*t)   # 0.5 is arbitrary to avoid clipping sound card DAC
##    #x  = (x*32768).astype(np.int16)                                     # scale to int16 for sound card
##
##
##    number_of_faded_points = int(duration*percentage_fade * fs)
##    fade = np.linspace(0,1,num=number_of_faded_points)
##
##    for j in np.arange(number_of_faded_points):
##        xi[j] = xi[j] * fade[j]
##        xi[duration - j - 1] = xi[duration - j - 1] * fade[j]
##        #print(x[i])
##    
##    X = X + xi
##    T = T + t