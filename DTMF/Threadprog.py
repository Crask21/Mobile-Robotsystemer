import pyaudio
import struct
import numpy as np
import time
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import copy
import threading

from scipy.signal import butter, lfilter
from scipy.signal import freqz


class LISTEN():
    def __init__(rec,baud):

#--------------------------------VARIABLES--------------------------------

        rec.FORMAT = pyaudio.paInt16 
        rec.CHANNELS = 1
        rec.RATE = 5000
        rec.INPUT_BLOCK_TIME = 0.1
        rec.INPUT_FRAMES_PER_BLOCK = int(rec.RATE*rec.INPUT_BLOCK_TIME)

        rec.LOWCUT = 200
        rec.HIGHCUT = 3000

        rec.resolution=int(1)
        rec.baudRate=baud
        rec.time_per_read=1/rec.baudRate
        rec.z_pad=rec.RATE/rec.resolution-rec.time_per_read*rec.RATE
        rec.z_pad_arr=np.zeros(int(rec.z_pad))
        rec.variance=60

        #------------------------------------PYAUDIO-----------------------------------
        # pyaudio class instance
        rec.p = pyaudio.PyAudio()

        # stream object to get data from microphone
        rec.stream = rec.p.open(format = rec.FORMAT,                      
                 channels = rec.CHANNELS,                          
                 rate = rec.RATE,                                  
                 input = True, 
                 # is this a good idea? I tried to not give the buffer a fixed size                                
                 #frames_per_buffer = INPUT_FRAMES_PER_BLOCK) 
        )

#found by printing yf.size
        rec.highestLimit=2498

#for dtmf_to_hexa
        rec.dtmf_freq = [[1209,697], # 0
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

        rec.upperRange= 20
        rec.lowerRange=20
        rec.outputList=[]

        #-----------------------------------FREQUENCIES------------------------------------------
        #resolution is defined as fs/(points worked on)
        #To improve resolution zeropadding can be used
        rec.xf = np.linspace(0, rec.RATE, int(rec.time_per_read*rec.RATE+rec.z_pad))
        rec.delList=np.arange(int(-rec.xf.size/2),0)
        rec.xf=np.delete(rec.xf,rec.delList)
        rec.xf_below1000=np.where(rec.xf<1000)
        rec.xf_above1000=np.where(rec.xf>=1000)


        #------------------------------GET THE FORMAT
        #divided by resolution to get the fft in resolution of choice in hz
        rec.data=rec.stream.read(int(rec.RATE*rec.time_per_read))
        rec.count = len(rec.data)/2
        rec.format = "%dh"%(rec.count)
        rec.data_int = np.array(struct.unpack(rec.format, rec.data))
        rec.data_int=np.append(rec.data_int,rec.z_pad_arr)
        #--------------------------------FFT-----------------------
        rec.yf=fft(rec.data_int)
        rec.yf=abs(rec.yf)
        rec.yf=np.delete(rec.yf,rec.delList)

        rec.syncCounter=0
        rec.startReading=False
    #--------------------------------FUNCTIONS--------------------------------
    def butter_bandpass(rec,LOWCUT, HIGHCUT, fs, order=5):
        nyq = 0.5 * fs
        low = LOWCUT / nyq
        high = HIGHCUT / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def butter_bandpass_filter(rec,input, LOWCUT, HIGHCUT, fs, order=5):
        b, a = rec.butter_bandpass(LOWCUT, HIGHCUT, fs, order=order)
        y = lfilter(b, a, input)
        return y

    def find_highest_freqs(rec, freqMagn):
    #find largest frequency
        freqmagnlow=copy.deepcopy(freqMagn)
        freqmagnlow[rec.xf_above1000]=0
        freqmagnhigh=copy.deepcopy(freqMagn)
        freqmagnhigh[rec.xf_below1000]=0
        highestFreqs=[np.argmax(freqmagnlow),np.argmax(freqmagnhigh)]

        return highestFreqs

    def dtmf_to_hexa(rec, inputFreqs):
        output =[]
        inputFreqs.sort()
        for i in range(16):
            if (inputFreqs[0]<rec.dtmf_freq[i][1]+rec.upperRange and inputFreqs[0]>rec.dtmf_freq[i][1]-rec.lowerRange)and(inputFreqs[1]<rec.dtmf_freq[i][0]+rec.upperRange and inputFreqs[1]>rec.dtmf_freq[i][0]-rec.lowerRange):
                output= [i]
        return output
        
    def startListen(rec):
        thr=threading.Thread(target=rec.listenThread, args=())
        thr.start()

    def listenThread(rec):
        while True:
            start=time.time()
            #divided by baudRate too to get the movement of the window
            data = rec.stream.read(int(rec.RATE*rec.time_per_read))
            data_int = np.array(struct.unpack(rec.format, data))
            data_int = np.append(data_int, rec.z_pad_arr)


            #data_int=butter_bandpass_filter(data_int)

            yf=fft(data_int)
            yf=np.delete(yf,rec.delList)
            highestfreqs=rec.find_highest_freqs(abs(yf))
            rec.outputList+=rec.dtmf_to_hexa(highestfreqs)
            print(rec.outputList)
            end=time.time()
            if end-start>rec.time_per_read:
                print("ERROR: The baudrate is too fast")

            if rec.outputList==[0xC,0xC] and rec.syncCounter>5:
                rec.startReading=True
                rec.outputList=[]

            if len(rec.outputList)>0 and not(rec.startReading):
                if rec.outputList[0]!=0xa and rec.outputList[0]!=0xC :
                    rec.outputList=[]

            if rec.outputList==[0xa,0xb]and not(rec.startReading):
                print("Synchronized")
                rec.outputList=[]
                syncCounter+=1
                print("Times synchronized: " +str(rec.syncCounter))


            if rec.outputList!=[0xa,0xb] and len(rec.outputList)==2 and not(rec.startReading):
                print("Sync failed, delaying with 10 percent")
                rec.outputList=[]
                syncCounter=0
                while end-start<rec.time_per_read+rec.time_per_read*0.1:
                    end=time.time()
            while end-start<rec.time_per_read:
                end=time.time()

#roberto = LISTEN()
#roberto.startListen()  
