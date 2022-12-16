import pyaudio
import numpy as np
from time import time
from scipy.fftpack import fft
from copy import deepcopy
#from Class_DTMF import SEND 
#fs = 44100
#amplitude = 15000
#media = 'PyGame' # 'SD'
#fade_P = 0.003
#baud_rate = 20
#syn = 20
## SYNC
#
#        
#     
#send=SEND(fs, amplitude, fade_P, baud_rate,syn, media,mono=False)

class LISTEN():
    def __init__(rec,baud):
        #--------------------------------VARIABLES--------------------------------
        rec.FORMAT = pyaudio.paInt16 
        rec.CHANNELS = 1
        rec.RATE = 4000
        rec.resolution=int(1)
        rec.baudRate=baud
        rec.read_percentage=1
        rec.time_per_read=1*rec.read_percentage/rec.baudRate
        rec.read_window=1/rec.baudRate
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
                    [1633,941]]) # F
        rec.dtmf_single_freqs=np.array([697, 770, 852, 941, 1209, 1336, 1477, 1633])

        rec.upperRange=20
        rec.lowerRange=20
        rec.outputList=np.array([],dtype=int)
        rec.noise_level=4000

        #-----------------------------------FREQUENCIES------------------------------------------
        #resolution is defined as fs/(points worked on)
        rec.xf = np.linspace(0, rec.RATE, int(rec.time_per_read*rec.RATE+rec.z_pad))
        rec.delList=np.arange(int(-rec.xf.size/2),0)
        rec.xf=np.delete(rec.xf,rec.delList)
        rec.xf_below1000=np.where(rec.xf<1000)
        rec.xf_above1000=np.where(rec.xf>=1000)
        rec.xf_above1000=np.delete(rec.xf_above1000,-1)
        rec.xf_noise=np.where(rec.xf<650)

        #-----------------------------------CHEATFILTER------------------------------------------
        rec.cheatfilter=np.array([],dtype=int)
        for i in rec.dtmf_single_freqs:
            rec.cheatfilter=np.append(rec.cheatfilter,np.arange(i-rec.lowerRange, i+rec.upperRange))
        rec.xf_indices = np.arange(rec.xf.size-1)
        rec.cheatfilter = np.delete(rec.xf_indices,rec.cheatfilter)

        #------------------------------GET THE FORMAT--------------------------
        rec.data=rec.stream.read(int(rec.RATE*rec.time_per_read),exception_on_overflow=False)
        
        
        #------------------------------VARAIBLES--------------------------
        rec.syncCounter=0
        rec.noSignal=0
        rec.startReading=False
        rec.previousRead=0
        rec.currentRead=0
        rec.firstTime=True
        rec.displacement=0
        rec.ABcount=0
        rec.starting=False       

    #--------------------------------FUNCTIONS--------------------------------
    def find_highest_freqs(rec, freqMagn):
        freqMagn[rec.cheatfilter]=0
        #find low frequency of DTMF
        freqmagnlow=deepcopy(freqMagn)
        freqmagnlow[rec.xf_above1000]=0
        freqmagnlow[rec.xf_noise]=0
        #find high frequency of DTMF
        freqmagnhigh=deepcopy(freqMagn)
        freqmagnhigh[rec.xf_below1000]=0
        #make np array of the two frequencies
        highestFreqs=np.array([np.argmax(freqmagnlow),np.argmax(freqmagnhigh)], dtype=int)
        #Remove reading if signal level is below noise threshhold
        if any(freqMagn[highestFreqs]<rec.noise_level):
            return np.array([0,0])
        return highestFreqs

    def dtmf_to_hexa(rec, inputFreqs):
        inputFreqs.sort()
        for i in np.arange(16,dtype=int):
            if (inputFreqs[0]<rec.dtmf_freq[i][1]+rec.upperRange+1 and inputFreqs[0]>rec.dtmf_freq[i][1]-rec.lowerRange-1)and(inputFreqs[1]<rec.dtmf_freq[i][0]+rec.upperRange+1 and inputFreqs[1]>rec.dtmf_freq[i][0]-rec.lowerRange-1):
                output= i
                break
        if not('output' in locals()):    
            hej=0
            #print(inputFreqs)
        else:    
            return output


    def startListen(rec):
        print("started listening!")
        while True:
            #-----------------------------Reading-----------------------------
            #while(not(rec.starting)):
            #    data = rec.stream.read(1, exception_on_overflow=False)
            #    data_int = np.frombuffer(data,dtype='h')
            #    print(int(rec.RATE*rec.time_per_read))
            #    print(np.amax(data_int))
            #    if np.amax(data_int)>1500:
            #        rec.starting=True
            #start=time()
            print(rec.stream.get_read_available())
            data = rec.stream.read(int(rec.RATE*rec.time_per_read), exception_on_overflow=False)
            print(rec.stream.get_read_available())
            #data_int = np.array(unpack(rec.format, data))
            data_int = np.frombuffer(data,dtype='h')
            #zeropad data
            data_int = np.append(data_int, rec.z_pad_arr)
            
            #-------------------------------FFT-------------------------------
            yf=fft(data_int)
            yf=np.delete(yf,rec.delList)
            highestfreqs=rec.find_highest_freqs(np.absolute(yf))
            if rec.startReading:
                rec.outputList=np.append(rec.outputList, rec.dtmf_to_hexa(highestfreqs))
                print(rec.outputList)
            else:
                rec.currentRead=rec.dtmf_to_hexa(highestfreqs)
                #print(rec.currentRead)

            #-----------Count A and Bs
            if rec.currentRead==0xa or rec.currentRead==0xb:
                rec.ABcount+=1
            
            
            #-----------------------Check if no signal------------------------
            if rec.dtmf_to_hexa(highestfreqs)==None and rec.startReading==True:
                rec.noSignal+=1
                if rec.noSignal>5:
                    break
            else:
                rec.noSignal=0

            #-----------------------Check if finished--------------------------
            if rec.currentRead==0xc and rec.ABcount>10:
                rec.startReading=True




            #-----------------------Check if Baudrate is too fast--------------
            #end=time()
            #print(end-start)
           


        rec.outputList=np.delete(rec.outputList,0)
        nones = rec.outputList == None
        rec.outputList = np.delete(rec.outputList,nones)
        rec.outputList=rec.outputList.tolist()

        #-----------------------CLEANING AFTER YOURSELF-----------
        rec.syncCounter=0
        rec.noSignal=0
        rec.startReading=False
        rec.previousRead=0
        rec.currentRead=0
        rec.firstTime=True
        rec.succesful=[]
        rec.failed=[]
        rec.displacement=0
        rec.ABcount=0
        rec.averageSuccess=0
        rec.synchronised=False
        rec.read_since_sync=0
        rec.synctime=time()
        rec.to_be_synchronised=False
        rec.warning=0
        rec.result=rec.outputList
        rec.outputList=np.array([],dtype=int)

        return rec.result

#roberto = LISTEN(160)
#output=roberto.startListen()
#print(output)
#pack=[0, 1, 1, 0, 8, 3, 11, 13, 0, 1, 0, 1, 2, 4, 4, 6, 5, 6, 5, 7, 10, 2, 0, 6, 14, 4, 10, 2, 0, 1, 0, 1, 3, 7, 5, 7, 4, 7, 3, 14, 7, 0, 0, 1]
#send.compare(pack,output)