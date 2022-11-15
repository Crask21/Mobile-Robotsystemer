import pyaudio
import struct
import numpy as np
import time
from scipy.fftpack import fft
import matplotlib.pyplot as plt

#------------------------FUNCTIONS--------------------------------
def listen():
    while True:
        data = stream.read(INPUT_FRAMES_PER_BLOCK)

baudRate=30
    
resolution=10

FORMAT = pyaudio.paInt16 
#SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 1
#RATE = 44100
RATE = 48000
INPUT_BLOCK_TIME = 1
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(format = FORMAT,                      
         channels = CHANNELS,                          
         rate = RATE,                                  
         input = True,                                 
         frames_per_buffer = INPUT_FRAMES_PER_BLOCK) 

data=stream.read(int(RATE/resolution))
count = len(data)/2
format = "%dh"%(count)

data_int = list(struct.unpack(format, data))

while True:
    start=time.time()
    data = stream.read(int(RATE/(resolution*50)))
    end=time.time()
    print(end-start)
    count = len(data)/2
    format = "%dh"%(count)
    data_nex = list(struct.unpack(format, data))
    
    del data_int[0:int(RATE/(resolution*50))]
    data_int.append(data_nex)
    

#threading.Thread(target=listen)
