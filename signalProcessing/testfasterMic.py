import pyaudio
import struct
import numpy as np
import time
from scipy.fftpack import fft
import matplotlib.pyplot as plt


delList=[]
delListLow=[]

baudRate=10
baudTime=1/baudRate

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
#stream = p.open(
#    format=FORMAT,
#    channels=CHANNELS,
#    rate=RATE,
#    input=True,
#    output=True,
#    frames_per_buffer=CHUNK,
#    input_device_index=1
#    
#)

# variable for plotting
#x = np.arange(0, 2 * INPUT_FRAMES_PER_BLOCK, 2)       # samples (waveform)
    # frequencies (spectrum)
#xf=np.delete(xf, delList)
#xf=np.delete(xf, delListLow)

#devinfo = p.get_device_info_by_index(1)  # Or whatever device you care about.
#if p.is_format_supported(96000.0,  # Sample rate
#                         input_device=devinfo['index'],
#                         input_channels=devinfo['maxInputChannels'],
#                         input_format=pyaudio.paInt16):
#  print('Yay!')
#while True:
#    time.time()
print('stream started')

for i in range(2):
    start=time.time()
    data = stream.read(INPUT_FRAMES_PER_BLOCK)
    end=time.time()
    print(end-start)
    #print(data)
    print("------------------")
    count = len(data)/2
    format = "%dh"%(count)
    
    data_int = struct.unpack(format, data)
    x_time_intervals=INPUT_BLOCK_TIME/INPUT_FRAMES_PER_BLOCK
    x_time=np.linspace(0,INPUT_BLOCK_TIME,INPUT_FRAMES_PER_BLOCK)
    xf = np.linspace(0, RATE, INPUT_FRAMES_PER_BLOCK) 
    #print(data_int)
    yf=fft(data_int)
    #print(abs(yf))
    
    print(len(data_int))
    

print(xf[2]-xf[1])
plt.plot(xf,abs(yf))
    #plt.plot(xf,abs(yf))
plt.show()


while False:
    loopStart=time.time()
    # binary data
    data = stream.read(CHUNK)  
    # convert data to integers, make np array, then offset it by 127
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    data=0
    time.sleep(0.01)
    # create np array and offset by 128
    #data_np = np.array(data_int, dtype='b')[::2] + 128
    loopEnd=time.time()
    print(loopEnd-loopStart)
    #print(xf)

