import pyaudio
from struct import unpack
import numpy as np
from time import time
from scipy.fftpack import fft
from copy import deepcopy

class LISTEN():
    def __init__(rec,baud):

        #--------------------------------VARIABLES--------------------------------
        rec.FORMAT = pyaudio.paInt16 
        rec.CHANNELS = 1
        rec.RATE = 4000
        rec.resolution=int(1)
        rec.baudRate=baud
        rec.time_per_read=1/rec.baudRate
        rec.z_pad=rec.RATE/rec.resolution-rec.time_per_read*rec.RATE
        rec.z_pad_arr=np.zeros(int(rec.z_pad))

        #------------------------------------PYAUDIO-----------------------------------
        # pyaudio class instance
        rec.p = pyaudio.PyAudio()

        # stream object to get data from microphone
        rec.stream = rec.p.open(format = rec.FORMAT,                      
                 channels = rec.CHANNELS,                          
                 rate = rec.RATE,                                  
                 input = True,
                 #input_device_index=3 
                 # is this a good idea? I tried to not give the buffer a fixed size                                
                 #frames_per_buffer = INPUT_FRAMES_PER_BLOCK) 
        )

        #for dtmf_to_hexa
        rec.dtmf_freq = np.array([[1209,697], # 0
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
                    [1633,941]])  # F
        rec.dtmf_single_freqs=np.array([697, 770, 852, 941, 1209, 1336, 1477, 1633])

        rec.upperRange=20
        rec.lowerRange=20
        rec.outputList=np.array([])
        rec.noise_level=2000

        #-----------------------------------FREQUENCIES------------------------------------------
        #resolution is defined as fs/(points worked on)
        #To improve resolution zeropadding can be used
        rec.xf = np.linspace(0, rec.RATE, int(rec.time_per_read*rec.RATE+rec.z_pad))
        rec.delList=np.arange(int(-rec.xf.size/2),0)
        rec.xf=np.delete(rec.xf,rec.delList)
        rec.xf_below1000=np.where(rec.xf<1000)
        rec.xf_above1000=np.where(rec.xf>=1000)
        rec.xf_above1000=np.delete(rec.xf_above1000,-1)
        rec.xf_noise=np.where(rec.xf<650)

        rec.cheatfilter=np.array([],dtype=int)
        for i in rec.dtmf_single_freqs:
            rec.cheatfilter=np.append(rec.cheatfilter,np.arange(i-rec.lowerRange, i+rec.upperRange))
        rec.xf_indices=np.arange(rec.xf.size-1)
        print(rec.cheatfilter)
        rec.cheatfilter=np.delete(rec.xf_indices,rec.cheatfilter)
        #rec.cheatfilter=np.where(rec.xf<rec.dtmf_single_freqs[0] and rec.xf<rec.dtmf_single_freqs[0])

        #------------------------------GET THE FORMAT--------------------------
        #divided by resolution to get the fft in resolution of choice in hz
        rec.data=rec.stream.read(int(rec.RATE*rec.time_per_read),exception_on_overflow=False)
        rec.count = len(rec.data)/2
        rec.format = "%dh"%(rec.count)
        rec.data_int = np.array(unpack(rec.format, rec.data))
        rec.data_int=np.append(rec.data_int,rec.z_pad_arr)

        #--------------------------------FFT-----------------------
        rec.yf=fft(rec.data_int)
        rec.yf=np.absolute(rec.yf)
        rec.yf=np.delete(rec.yf,rec.delList)

        rec.syncCounter=0
        rec.noSignal=0
        rec.startReading=False

    #--------------------------------FUNCTIONS--------------------------------
    def find_highest_freqs(rec, freqMagn):
        #cheat filter
        freqMagn[rec.cheatfilter]=0
        freqmagnlow=deepcopy(freqMagn)
        freqmagnlow[rec.xf_above1000]=0
        freqmagnlow[rec.xf_noise]=0
        freqmagnhigh=deepcopy(freqMagn)
        freqmagnhigh[rec.xf_below1000]=0
        highestFreqs=[np.argmax(freqmagnlow),np.argmax(freqmagnhigh)]
        if any(freqMagn[highestFreqs]<rec.noise_level):
            return np.array([0,0])
        return highestFreqs

    def dtmf_to_hexa(rec, inputFreqs):
        output=0
        inputFreqs.sort()
        for i in np.arange(16):
            if (inputFreqs[0]<rec.dtmf_freq[i][1]+rec.upperRange+1 and inputFreqs[0]>rec.dtmf_freq[i][1]-rec.lowerRange-1)and(inputFreqs[1]<rec.dtmf_freq[i][0]+rec.upperRange+1 and inputFreqs[1]>rec.dtmf_freq[i][0]-rec.lowerRange-1):
                output= i
                break
        if output==0 and rec.startReading:
            print(inputFreqs)
        return np.array([output])

    def startListen(rec):
        print("started listening!")
        while True:
            #-----------------------------Reading-----------------------------
            start=time()
            #divided by baudRate too to get the movement of the window
            data = rec.stream.read(int(rec.RATE*rec.time_per_read), exception_on_overflow=False)
            data_int = np.array(unpack(rec.format, data))
            data_int = np.append(data_int, rec.z_pad_arr)
            
            #-------------------------------FFT-------------------------------
            yf=fft(data_int)
            yf=np.delete(yf,rec.delList)
            highestfreqs=rec.find_highest_freqs(np.absolute(yf))
            rec.outputList+=rec.dtmf_to_hexa(highestfreqs)

            print(rec.outputList)
            
            #-----------------------Check if no signal------------------------
            if rec.dtmf_to_hexa(highestfreqs)==[] and rec.startReading==True:
                rec.noSignal+=1
                if rec.noSignal>5:
                    break
            else:
                rec.noSignal=0

            #-----------------------Check if finished--------------------------
            if rec.outputList==[0xC,0xC] and rec.syncCounter>5:
                rec.startReading=True
                rec.outputList=[]

            #-----------------------Clear if not right first bit---------------
            if len(rec.outputList)>0 and not(rec.startReading):
                if rec.outputList[0]!=0xa and rec.outputList[0]!=0xC :
                    rec.outputList=[]

            #-----------------------Check if succesful-------------------------
            if rec.outputList==[0xa,0xb]and not(rec.startReading):
                print("Synchronized")
                rec.outputList=[]
                rec.syncCounter+=1
                print("Times synchronized: " +str(rec.syncCounter))
            #-----------------------Check if Baudrate is too fast--------------
            end=time()
            if end-start>rec.time_per_read:
                print("ERROR: The baudrate is too fast:"+str(rec.time_per_read)+","+str(end-start-rec.time_per_read))

            #-----------------------Check if failure--------------------------
            if rec.outputList!=[0xa,0xb] and len(rec.outputList)==2 and not(rec.startReading):
                print("Sync failed, delaying with 10 percent")
                rec.outputList=[]
                rec.syncCounter=0
                while end-start<rec.time_per_read+rec.time_per_read*0.1:
                    end=time()
            #-----------------------Delay until proper baudrate----------------
            while end-start<rec.time_per_read:
                end=time()
        
        return rec.outputList

roberto = LISTEN(50)
roberto.startListen()