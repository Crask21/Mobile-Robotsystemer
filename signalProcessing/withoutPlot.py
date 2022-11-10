import pyaudio
import struct
import numpy as np
import time
import Class_DTMF
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

thread_f()

x.start()

baudRate=8
baudTime=1/baudRate

#variables for use later
syncCounter=0
outputList=[]
startReading=False

# constants
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second

def find_highest_freqs(freqMagn):
#find largest frequency
    highestFreq=np.argmax(freqMagn)
    #make list of neighbours
    delFreq=np.arange(highestFreq-5,highestFreq+5)
    #Indexes higher than 71 is sorted away, since they cause problems
    delFreq=np.delete(delFreq,np.where(delFreq>71))
    #delete the neighbours
    freqMagn[delFreq]=0
    highestFreqs=[highestFreq, np.argmax(freqMagn)]
    return highestFreqs
    
def dtmf_to_hexa(inputFreqs):
    output =[]
    inputFreqs.sort()
    for i in range(16):
        if (inputFreqs[0]<dtmf_freq[i][1]+upperRange and inputFreqs[0]>dtmf_freq[i][1]-lowerRange)and(inputFreqs[1]<dtmf_freq[i][0]+upperRange and inputFreqs[1]>dtmf_freq[i][0]-lowerRange):
            output= [i]
    return output





#frequencies to delete
delListHigh=np.arange(-1953,0)
delListLow=np.arange(23)
delList=np.concatenate((delListHigh,delListLow))

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



while True:
    loopStart=time.time()
    # binary data
    data = stream.read(CHUNK)  
    # convert data to integers, make np array, then offset it by 127
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    # create np array and offset by 128
    data_np = np.array(data_int, dtype='b')[::2] + 128

    
    #perhaps use goertzel later for optimization
    yf = fft(data_int)
    yf =np.delete(yf,delList)
    freqMagn=np.abs(yf[0:xf.size])  / (128 * xf.size)
    
    highestFreqs=find_highest_freqs(freqMagn)

    if freqMagn[highestFreqs[1]]>1:
        outputList=outputList+dtmf_to_hexa(xf[highestFreqs])
    print(outputList)
    print("------------------------------------")
    loopEnd=time.time()

    if loopEnd-loopStart>baudTime:
        print("ERROR: The baudrate is too fast")
    while loopEnd-loopStart<baudTime:
        loopEnd=time.time()
    
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
        while loopEnd-loopStart<baudTime+baudTime*0.1:
            loopEnd=time.time()














