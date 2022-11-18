
import pyaudio
import struct
import numpy as np
import time
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import copy

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
baudRate=10
time_per_read=1/baudRate
z_pad=RATE/resolution-time_per_read*RATE
z_pad_arr=np.zeros(int(z_pad))


variance=60

#found by printing yf.size
highestLimit=2498

#for dtmf_to_hexa
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
outputList=[]

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

def find_highest_freqs(freqMagn):
#find largest frequency
    freqmagnlow=copy.deepcopy(freqMagn)
    freqmagnlow[xf_above1000]=0
    freqmagnlow[xf_noise]=0
    freqmagnhigh=copy.deepcopy(freqMagn)
    freqmagnhigh[xf_below1000]=0
    highestFreqs=[np.argmax(freqmagnlow),np.argmax(freqmagnhigh)]

    return highestFreqs



def dtmf_to_hexa(inputFreqs):
    output =[]
    inputFreqs.sort()
    for i in range(16):
        if (inputFreqs[0]<dtmf_freq[i][1]+upperRange and inputFreqs[0]>dtmf_freq[i][1]-lowerRange)and(inputFreqs[1]<dtmf_freq[i][0]+upperRange and inputFreqs[1]>dtmf_freq[i][0]-lowerRange):
            output= [i]
    if output==[]:
        output=inputFreqs[0]

    return output

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
xf_below1000=np.where(xf<1000)
xf_above1000=np.where(xf>=1000)
xf_noise=np.where(xf<650)


#------------------------------GET THE FORMAT
#divided by resolution to get the fft in resolution of choice in hz
for i in range(50):
    data=stream.read(int(RATE*time_per_read))
    count = len(data)/2
    format = "%dh"%(count)
    data_int = np.array(struct.unpack(format, data))
    data_int=np.append(data_int,z_pad_arr)
#--------------------------------FFT-----------------------
yf=fft(data_int)
yf=abs(yf)
yf=np.delete(yf,delList)

#fig=plt.plot(xf,yf)
#plt.show()


syncCounter=0
noSignal=0
startReading=False


while True:
    start=time.time()
    #divided by baudRate too to get the movement of the window
    data = stream.read(int(RATE*time_per_read))
    data_int = np.array(struct.unpack(format, data))
    data_int = np.append(data_int, z_pad_arr)

    
    #data_int=butter_bandpass_filter(data_int)

    yf=fft(data_int)
    yf=np.delete(yf,delList)
    highestfreqs=find_highest_freqs(abs(yf))
    outputList+=dtmf_to_hexa(highestfreqs)
    print(xf[highestfreqs])
    end=time.time()
    if dtmf_to_hexa(highestfreqs)==[] and startReading==True:
        noSignal+=1
        if noSignal>5:
            break
    else:
        noSignal=0

    if end-start>time_per_read:
        print("ERROR: The baudrate is too fast")

    if outputList==[0xC,0xC] and syncCounter>5:
        startReading=True
        outputList=[]

    if len(outputList)>0 and not(startReading):
        if outputList[0]!=0xa and outputList[0]!=0xC :
            outputList=[]

    if outputList==[0xa,0xb]and not(startReading):
        print("Synchronized")
        outputList=[]
        syncCounter+=1
        print("Times synchronized: " +str(syncCounter))
    

    if outputList!=[0xa,0xb] and len(outputList)==2 and not(startReading):
        print("Sync failed, delaying with 10 percent")
        outputList=[]
        syncCounter=0
        while end-start<time_per_read+time_per_read*0.1:
            end=time.time()
    while end-start<time_per_read:
        end=time.time()