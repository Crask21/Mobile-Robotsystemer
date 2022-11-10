import pyaudio
import struct
import numpy as np
import time
from scipy.fftpack import fft

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
upperRange= 20
lowerRange=20
def dtmf_to_hexa(inputFreqs):
    output =[]
    inputFreqs.sort()
    for i in range(16):
        if (inputFreqs[0]<dtmf_freq[i][1]+upperRange and inputFreqs[0]>dtmf_freq[i][1]-lowerRange)and(inputFreqs[1]<dtmf_freq[i][0]+upperRange and inputFreqs[1]>dtmf_freq[i][0]-lowerRange):
            output= [i]
    return output

#frequencies to delete
#delList=np.arange(-1953,0)
#delListLow=np.arange(23)
delList=[]
delListLow=[]

baudRate=10
baudTime=1/baudRate

# constants
CHUNK = 1024 * 3             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 100000                 # samples per second


# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK,
    input_device_index=1
    
)

# variable for plotting
x = np.arange(0, 2 * CHUNK, 2)       # samples (waveform)
xf = np.linspace(0, RATE, CHUNK)     # frequencies (spectrum)
#xf=np.delete(xf, delList)
#xf=np.delete(xf, delListLow)


print('stream started')

outputList=[]

while True:
    loopStart=time.time()
    # binary data
    data = stream.read(CHUNK)  
    # convert data to integers, make np array, then offset it by 127
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    
    # create np array and offset by 128
    data_np = np.array(data_int, dtype='b')[::2] + 128
    loopEnd=time.time()
    print(loopEnd-loopStart)
    #print(xf)

