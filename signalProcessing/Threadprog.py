import pyaudio
import struct
import numpy as np
import time
from scipy.fftpack import fft
import matplotlib.pyplot as plt

from scipy.signal import butter, lfilter
from scipy.signal import freqz

#--------------------------------VARIABLES--------------------------------

FORMAT = pyaudio.paInt16 
CHANNELS = 1
RATE = 5000
INPUT_BLOCK_TIME = 0.1
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)

LOWCUT = 200
HIGHCUT = 3000

resolution=int(1)
baudRate=60
time_per_read=1/baudRate
z_pad=RATE/resolution-time_per_read*RATE
z_pad_arr=np.zeros(int(z_pad))



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

variance=40

#found by printing yf.size
highestLimit=2498

def find_highest_freqs(freqMagn):
#find largest frequency
    highestFreq=np.argmax(freqMagn)
    #make list of neighbours
    delFreq=np.arange(highestFreq-variance,highestFreq+variance)
    #Indexes higher than 71 is sorted away, since they cause problems
    delFreq=np.delete(delFreq,np.where(delFreq>highestLimit))
    #delete the neighbours
    freqMagn[delFreq]=0
    highestFreqs=[highestFreq, np.argmax(freqMagn)]
    return highestFreqs

#------------------------------------PYAUDIO-----------------------------------
# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(format = FORMAT,                      
         channels = CHANNELS,                          
         rate = RATE,                                  
         input = True, 
         # is this a good idea? I tried to not give the buffer a fixed size                                
         #frames_per_buffer = INPUT_FRAMES_PER_BLOCK) 
)

#-----------------------------------FREQUENCIES------------------------------------------
#resolution is defined as fs/(points worked on)
#To improve resolution zeropadding can be used
xf = np.linspace(0, RATE, int(time_per_read*RATE+z_pad))
delList=np.arange(int(-xf.size/2),0)
xf=np.delete(xf,delList)

#------------------------------GET THE FORMAT
#divided by resolution to get the fft in resolution of choice in hz
data=stream.read(int(RATE*time_per_read))
count = len(data)/2
format = "%dh"%(count)

data_int = np.array(struct.unpack(format, data))
data_int=np.append(data_int,z_pad_arr)

#--------------------------------FFT-----------------------
yf=fft(data_int)
yf=abs(yf)
yf=np.delete(yf,delList)



while True:
    #divided by baudRate too to get the movement of the window
    data = stream.read(int(RATE*time_per_read))
    data_int = np.array(struct.unpack(format, data))
    data_int = np.append(data_int, z_pad_arr)

    
    #data_int=butter_bandpass_filter(data_int)

    yf=fft(data_int)
    yf=np.delete(yf,delList)
    highestfreqs=find_highest_freqs(abs(yf))
    print(highestfreqs)
    
