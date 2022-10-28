import pyaudio
import struct
import numpy as np

from scipy.fftpack import fft


#frequencies to delete
delList=np.arange(-1953,0)
delListLow=np.arange(23)

# constants
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second



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
    input_device_index=3
    
)

# variable for plotting
x = np.arange(0, 2 * CHUNK, 2)       # samples (waveform)
xf = np.linspace(0, RATE, CHUNK)     # frequencies (spectrum)
xf=np.delete(xf, delList)
xf=np.delete(xf, delListLow)





print('stream started')



while True:
    # binary data
    data = stream.read(CHUNK)  
    
    # convert data to integers, make np array, then offset it by 127
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    
    # create np array and offset by 128
    data_np = np.array(data_int, dtype='b')[::2] + 128
    
    
    # compute FFT and update line
    yf = fft(data_int)
    yf =np.delete(yf,delList)
    yf =np.delete(yf, delListLow)
    freqMagn=np.abs(yf[0:xf.size])  / (128 * xf.size)
    #delete frequencies above 2000
    #delList=np.arange(-1953,0)
    #highfreq=np.delete(highfreq,delList)




    #print(xf[np.argmax(freqMagn)])
    
    #find frequencies above 0.15 in magnitude
    listFreq=np.where(freqMagn>0.15)
    #find largest frequency
    highestFreq=np.argmax(freqMagn)
    #make list of neighbours
    delFreq=np.arange(highestFreq-5,highestFreq+5)
    delFreq=np.delete(delFreq,np.where(delFreq>71))
    #delete the neighbours
    freqMagn[delFreq]=0
    highestFreqs=[highestFreq, np.argmax(freqMagn)]
    #closeFreq=np.where(highestFreq)
    print(xf[highestFreqs])
    print("------------------------------------")
    


