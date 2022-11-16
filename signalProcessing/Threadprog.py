import pyaudio
import struct
import numpy as np
import time
from scipy.fftpack import fft
import matplotlib.pyplot as plt

from scipy.signal import butter, lfilter
from scipy.signal import freqz

#--------------------------------VARIABLES--------------------------------


LOWCUT = 200
HIGHCUT = 3000

resolution=int(10)
baudRate=500

FORMAT = pyaudio.paInt16 
CHANNELS = 1
RATE = 15000
INPUT_BLOCK_TIME = 1
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)

#--------------------------------FUNCTIONS--------------------------------
def butter_bandpass(LOWCUT, HIGHCUT, fs, order=5):
    nyq = 0.5 * fs
    low = LOWCUT / nyq
    high = HIGHCUT / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(input, LOWCUT=LOWCUT, HIGHCUT=HIGHCUT, fs=RATE, order=5):
    b, a = butter_bandpass(LOWCUT, HIGHCUT, fs, order=order)
    y = lfilter(b, a, input)
    return y

#------------------------------------PYAUDIO-----------------------------------
# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(format = FORMAT,                      
         channels = CHANNELS,                          
         rate = RATE,                                  
         input = True,                                 
         #frames_per_buffer = INPUT_FRAMES_PER_BLOCK) 
)

#resolution is defined as fs/(points worked on)
xf = np.linspace(0, RATE, int(INPUT_FRAMES_PER_BLOCK/(resolution*INPUT_BLOCK_TIME)))
delList=np.arange(int(-xf.size/2),0)
xf=np.delete(xf,delList)

#divided by resolution to get the fft in resolution of choice in hz
data=stream.read(int(RATE/resolution))
count = len(data)/2
format = "%dh"%(count)

data_int = np.array(struct.unpack(format, data))

yf=fft(data_int)
yf=abs(yf)
yf=np.delete(yf,delList)

#plt.plot(xf,yf)
#plt.show()
data = stream.read(int(RATE/(resolution*baudRate)))
count = len(data)/2
format = "%dh"%(count)

while True:
    #divided by baudRate too to get the movement of the window
    data = stream.read(int(RATE/(resolution*baudRate)))
    data_nex = np.array(struct.unpack(format, data))
    #remove the first points in the array
    data_int=np.delete(data_int,np.arange(int(RATE/(resolution*baudRate))))
    data_int=np.append(data_int,data_nex)
    
    #data_int=butter_bandpass_filter(data_int)

    yf=fft(data_int)
    yf=np.delete(yf,delList)
    
