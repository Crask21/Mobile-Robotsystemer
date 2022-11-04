import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import time

#frequencies to delete
delList=np.arange(-1953,0)
delListLow=np.arange(23)

# constants
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second

# create matplotlib figure and axes
fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))

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
xf=np.delete(xf, delList)
xf=np.delete(xf, delListLow)

###find out which indices in xf have frequency higher than 2000
#myList=np.where(xf>500)
#print(myList[0])
#print(xf[24])
#time.sleep(1000)
# create a line object with random data
line, = ax1.plot(x, np.random.rand(CHUNK), '-', lw=2)

# create semilogx line for spectrum
line_fft, = ax2.semilogx(xf, np.random.rand(xf.size), '-', lw=2)

# format waveform axes
ax1.set_title('AUDIO WAVEFORM')
ax1.set_xlabel('samples')
ax1.set_ylabel('volume')
ax1.set_ylim(0, 255)
ax1.set_xlim(0, 2 * CHUNK)
plt.setp(ax1, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])

# format spectrum axes
ax2.set_xlim(20, RATE / 2)

print('stream started')

# for measuring frame rate
frame_count = 0
start_time = time.time()

plt.show(block=False)
hej=2

while True:
    # binary data
    data = stream.read(CHUNK)  
    
    # convert data to integers, make np array, then offset it by 127
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    
    # create np array and offset by 128
    data_np = np.array(data_int, dtype='b')[::2] + 128
    
    line.set_ydata(data_np)
    
    # compute FFT and update line
    yf = fft(data_int)
    yf =np.delete(yf,delList)
    yf =np.delete(yf, delListLow)
    line_fft.set_ydata(np.abs(yf[0:xf.size])  / (128 * CHUNK))
    freqMagn=np.abs(yf[0:xf.size])  / (128 * xf.size)
    #delete frequencies above 2000
    #delList=np.arange(-1953,0)
    #highfreq=np.delete(highfreq,delList)


   
    # update figure canvas
    
    fig.canvas.draw()
    fig.canvas.flush_events()
    

    #print(xf[np.argmax(freqMagn)])
    
    #find frequencies above 0.15 in magnitude
    listFreq=np.where(freqMagn>0.2)
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
    #myProgram=myProgram+xf[highestFreqs]
    #tooBig=len(myProgram)>100
    #if tooBig:
        

    print("------------------------------------")
    


