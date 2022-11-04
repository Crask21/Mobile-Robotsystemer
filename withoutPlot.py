import pyaudio
import struct
import numpy as np
import time
from scipy.fftpack import fft

def dtmf_to_hexa(inputList):

    output = []

    for i in range(len(inputList)):
        if(inputList[0]>inputList[1]):
            temp = inputList[0]
            inputList[0] = inputList[1]
            inputList[1] = temp

    input1 = inputList[0]
    input2 = inputList[1]

    if((input1>=650) and (input1<=730)):
        if((input2>=1150) and (input2<=1250)):
            output.append(0)
        elif((input2>=1280) and (input2<=1380)):
            output.append(1)
        elif((input2>=1420) and (input2<=1520)):
            output.append(2)
        elif((input2>=1580) and (input2<=1680)):
            output.append(3)
    elif((input1>=745) and (input1<=810)):
        if((input2>=1150) and (input2<=1250)):
            output.append(4)
        elif((input2>=1280) and (input2<=1380)):
            output.append(5)
        elif((input2>=1420) and (input2<=1520)):
            output.append(6)
        elif((input2>=1580) and (input2<=1680)):
            output.append(7)
    elif((input1>=820) and (input1<=890)):
        if((input2>=1150) and (input2<=1250)):
            output.append(8)
        elif((input2>=1280) and (input2<=1380)):
            output.append(9)
        elif((input2>=1420) and (input2<=1520)):
            output.append('A')
        elif((input2>=1580) and (input2<=1680)):
            output.append('B')
    elif((input1>=900) and (input1<=980)):
        if((input2>=1150) and (input2<=1250)):
            output.append('C')
        elif((input2>=1280) and (input2<=1380)):
            output.append('D')
        elif((input2>=1420) and (input2<=1520)):
            output.append('E')
        elif((input2>=1580) and (input2<=1680)):
            output.append('F')

    return output

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
    frames_per_buffer=CHUNK
    #input_device_index=3
    
)

# variable for plotting
x = np.arange(0, 2 * CHUNK, 2)       # samples (waveform)
xf = np.linspace(0, RATE, CHUNK)     # frequencies (spectrum)
xf=np.delete(xf, delList)
xf=np.delete(xf, delListLow)

#counter to only count specific values
sampleCount=1



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
    
    
    #perhaps use goertzel later for optimization
    yf = fft(data_int)
    yf =np.delete(yf,delList)
    yf =np.delete(yf, delListLow)
    freqMagn=np.abs(yf[0:xf.size])  / (128 * xf.size)
    
    
    #find largest frequency
    highestFreq=np.argmax(freqMagn)
    #make list of neighbours
    delFreq=np.arange(highestFreq-5,highestFreq+5)
    delFreq=np.delete(delFreq,np.where(delFreq>71))
    #delete the neighbours
    freqMagn[delFreq]=0
    highestFreqs=[highestFreq, np.argmax(freqMagn)]
    
    if freqMagn[highestFreqs[1]]>4:
        outputList=outputList+dtmf_to_hexa(xf[highestFreqs])
    print(outputList)
    print("------------------------------------")
    loopEnd=time.time()
    if loopEnd-loopStart>0.1:
        print("ERROR: The baudrate is too fast")
    while loopEnd-loopStart<0.1:
        loopEnd=time.time()
    print(loopEnd-loopStart)
    if outputList==["A","B","C","D","E","F"]:
        print("Synchronization is succesfull")
    if outputList!=["A","B","C","D","E","F"]:
        print("Synchronization commensing, delaying with 0,01 sec")
        while loopEnd-loopStart<0.11:
            loopEnd=time.time()
    elif len(outputList)>8:
        outputList=[]
