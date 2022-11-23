import pyaudio
import struct
import numpy as np
import time
from scipy.fftpack import fft
import copy
import threading

from scipy.signal import butter, lfilter

import sys



class LISTEN():
    def __init__(rec,baud):

#--------------------------------VARIABLES--------------------------------

        rec.FORMAT = pyaudio.paInt16 
        rec.CHANNELS = 1
        rec.RATE = 4000
        rec.INPUT_BLOCK_TIME = 0.1
        rec.INPUT_FRAMES_PER_BLOCK = int(rec.RATE*rec.INPUT_BLOCK_TIME)

        rec.LOWCUT = 200
        rec.HIGHCUT = 3000

        rec.resolution=int(1)
        rec.baudRate=baud
        rec.time_per_read=1/rec.baudRate
        rec.z_pad=rec.RATE/rec.resolution-rec.time_per_read*rec.RATE
        rec.z_pad_arr=np.zeros(int(rec.z_pad))
        #rec.variance=60

        #------------------------------------PYAUDIO-----------------------------------
        # pyaudio class instance
        rec.p = pyaudio.PyAudio()

        # stream object to get data from microphone
        rec.stream = rec.p.open(format = rec.FORMAT,                      
                 channels = rec.CHANNELS,                          
                 rate = rec.RATE,                                  
                 input = True,
                 input_device_index=1 
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
        rec.dtmf_single_freqs=[697,
                                770,
                                852,
                                941,
                                1209,
                                1336,
                                1477,
                                1633]

        rec.upperRange=20
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
        rec.xf_above1000=np.delete(rec.xf_above1000,-1)
        rec.xf_noise=np.where(rec.xf<650)

        rec.cheatfilter=[]
        for i in rec.dtmf_single_freqs:
            rec.cheatfilter+=range(i-rec.lowerRange, i+rec.upperRange)
        rec.xf_indices=np.arange(rec.xf.size-1)
        rec.cheatfilter=np.delete(rec.xf_indices,rec.cheatfilter)
        #rec.cheatfilter=np.where(rec.xf<rec.dtmf_single_freqs[0] and rec.xf<rec.dtmf_single_freqs[0])


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
        rec.noSignal=0
        rec.startReading=False
    #--------------------------------FUNCTIONS--------------------------------

    def find_highest_freqs(rec, freqMagn):
    #find largest frequency
        #cheat filter
        freqMagn[rec.cheatfilter]=0

        freqmagnlow=copy.deepcopy(freqMagn)
        freqmagnlow[rec.xf_above1000]=0
        freqmagnlow[rec.xf_noise]=0
        freqmagnhigh=copy.deepcopy(freqMagn)
        freqmagnhigh[rec.xf_below1000]=0
        highestFreqs=[np.argmax(freqmagnlow),np.argmax(freqmagnhigh)]
        if any(freqMagn[highestFreqs]<1000):
            return [0,0]
        return highestFreqs

    def dtmf_to_hexa(rec, inputFreqs):
        output =[]
        inputFreqs.sort()
        for i in range(16):
            if (inputFreqs[0]<rec.dtmf_freq[i][1]+rec.upperRange+1 and inputFreqs[0]>rec.dtmf_freq[i][1]-rec.lowerRange-1)and(inputFreqs[1]<rec.dtmf_freq[i][0]+rec.upperRange+1 and inputFreqs[1]>rec.dtmf_freq[i][0]-rec.lowerRange-1):
                output= [i]
        if output==[] and rec.startReading:
            print(inputFreqs)
        return output
        
    def startListen(rec):
        thr=threading.Thread(target=rec.listenThread, args=())
        thr.start()

    
    def compare(data,original, recieved, compare=True):
        if len(recieved) > len(original):
            dif = len(recieved) - len(original)
            recieved = recieved[:len(recieved) - dif]

        if original == recieved:
            print('100% match')
        else:
            send_count =[]
            for i in range(16):
                send_count.append(original.count(i))




            recieved_count = []
            for i in range(16):
                recieved_count.append(recieved.count(i))

            count = 0
            for i in range(16):
                
                if recieved_count[i] == send_count[i]:
                    count += 1



            print(count/16*100,'% count match')
            print(original)
            print(recieved)

    def listenThread(rec):
        #print(*rec.cheatfilter, sep = ", ")
        rec.pack=input("Enter sent package")
        while True:
            start=time.time()
            #divided by baudRate too to get the movement of the window
            data = rec.stream.read(int(rec.RATE*rec.time_per_read))
            data_int = np.array(struct.unpack(rec.format, data))
            data_int = np.append(data_int, rec.z_pad_arr)
            #end1 = time.time()
            #print("read")
            #print(end1-start)
            #data_int=butter_bandpass_filter(data_int)
            
            yf=fft(data_int)
            #print("fft")
            #end2=time.time()
            #print(end2-end1)
            yf=np.delete(yf,rec.delList)
            highestfreqs=rec.find_highest_freqs(abs(yf))
            rec.outputList+=rec.dtmf_to_hexa(highestfreqs)

            print(rec.outputList)
            

            if rec.dtmf_to_hexa(highestfreqs)==[] and rec.startReading==True:
                rec.noSignal+=1
                if rec.noSignal>5:
                    rec.compare(rec.pack,rec.outputList)
                    break
            else:
                rec.noSignal=0


            if rec.outputList==[0xC,0xC] and rec.syncCounter>5:
                rec.startReading=True
                rec.outputList=[]

            if len(rec.outputList)>0 and not(rec.startReading):
                if rec.outputList[0]!=0xa and rec.outputList[0]!=0xC :
                    rec.outputList=[]

            if rec.outputList==[0xa,0xb]and not(rec.startReading):
                print("Synchronized")
                rec.outputList=[]
                rec.syncCounter+=1
                print("Times synchronized: " +str(rec.syncCounter))

            #end3=time.time()
            #print("conditionals")
            #print(end3-end2)
            end=time.time()
            if end-start>rec.time_per_read:
                print("ERROR: The baudrate is too fast")

            if rec.outputList!=[0xa,0xb] and len(rec.outputList)==2 and not(rec.startReading):
                print("Sync failed, delaying with 10 percent")
                rec.outputList=[]
                rec.syncCounter=0
                while end-start<rec.time_per_read+rec.time_per_read*0.1:
                    end=time.time()
            while end-start<rec.time_per_read:
                end=time.time()



#
roberto = LISTEN(10)
#
roberto.listenThread()  
