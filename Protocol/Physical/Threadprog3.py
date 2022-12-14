import pyaudio
import numpy as np
from time import time
from scipy.fftpack import fft
from copy import deepcopy
import math
#from Class_DTMF import SEND 
#fs = 44100
#amplitude = 15000
#media = 'PyGame' # 'SD'
#fade_P = 0.15
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
                    [1633,941]])  # F
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
        #rec.xf_above1000=np.delete(rec.xf_above1000,-1)
        rec.xf_noise=np.where(rec.xf<650)

        #-----------------------------------CHEATFILTER------------------------------------------
        rec.cheatfilter=np.array([],dtype=int)
        for i in rec.dtmf_single_freqs:
            rec.cheatfilter=np.append(rec.cheatfilter,np.arange(i-rec.lowerRange, i+rec.upperRange))
        rec.xf_indices = np.arange(rec.xf.size-1)
        rec.cheatfilter = np.delete(rec.xf_indices,rec.cheatfilter)

        #------------------------------GET THE FORMAT--------------------------
        rec.data=rec.stream.read(int(rec.RATE*rec.time_per_read),exception_on_overflow=False)
        
        
        #------------------------------GET THE FORMAT--------------------------
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

    def getVectors(rec, angles):
        vectors=[]
        for i in angles:
            vector=[math.cos(i*2*math.pi),math.sin(i*2*math.pi)]
            vectors.append(vector)
        #print(vectors)
        return vectors
    def sumvectors(rec, vectors):
        vectorSum=[0,0]
        for i in vectors:
            vectorSum[0]+=i[0]
            vectorSum[1]+=i[1]
        #print(vectorSum)
        return np.array(vectorSum)
    def getAngle(rec, cartesianCoord):
        #print(cartesianCoord)
        angle=math.atan2(cartesianCoord[1],cartesianCoord[0])
        angleinList=angle/(math.pi*2)
        return angleinList
    def getAverage(rec, angles):
        vectors=rec.getVectors(angles)
        vectorSum=rec.sumvectors(vectors)
        average=rec.getAngle(vectorSum)
        return average%1

    def startListen(rec):
        print("started listening!")
        while True:
            #-----------------------------Reading-----------------------------
            start=time()
            #print(rec.stream.get_read_available())
            data = rec.stream.read(int(rec.RATE*rec.time_per_read), exception_on_overflow=False)
            #print(rec.stream.get_read_available())
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
            if rec.currentRead==0xc and rec.synchronised:
                rec.startReading=True



            #-----------------------Check if Baudrate is too fast--------------
            end=time()
            if end-start>rec.read_window:
                print("ERROR: The baudrate is too fast:"+str(rec.read_window)+","+str(end-start-rec.read_window))
           
            #-----------------------Check if fits -----------------------------
            if rec.currentRead != rec.previousRead and not(rec.synchronised) and rec.ABcount>3:
                print("fits")
                rec.succesful.append(rec.displacement)
                rec.displacement+=0.05
                while end-start<rec.read_window+rec.read_window*0.05:
                    end=time()
                
            
            #-----------------------Check if does not fit----------------------
            if rec.currentRead == rec.previousRead and not(rec.synchronised) and rec.ABcount>3:
                print("does not fit")
                rec.failed.append(rec.displacement)
                rec.displacement+=0.05
                #print("Hej")
                while end-start<rec.read_window+rec.read_window*0.05:
                    end=time()
            if not(rec.synchronised):
                print(rec.displacement)
            if rec.displacement>0.97 and not(rec.synchronised):
                print("synchronising:")
                rec.to_be_synchronised=True
                print("succesful:")
                print(rec.succesful)
                print("Failed:")
                print(rec.failed)
                print("recommended displacement:")
                print(rec.getAverage(rec.succesful))
                while end-start<rec.read_window+rec.read_window*rec.getAverage(rec.succesful):
                    end=time()
                np.mean(rec.succesful)
            
            rec.previousRead=rec.currentRead
            #-----------------------Delay until proper baudrate----------------
            #-----------------synced-----------------
            if rec.synchronised:
               while end-rec.synctime<rec.read_window*rec.read_since_sync:
                    end=time() 
            #---------------not synced---------------
            if not(rec.synchronised):
                while end-start<rec.read_window:
                    end=time()
            print(end-start)
            if (end-start>0.7 or end-start<0.3) and rec.startReading:
                rec.warning+=1
            #set timer if just syncronised
            if rec.to_be_synchronised:
                rec.synchronised=True
                rec.synctime=time()
                rec.to_be_synchronised=False
            if rec.synchronised:
                rec.read_since_sync+=1

        rec.outputList=np.delete(rec.outputList,0)
        rec.outputList=rec.outputList.tolist()
        print("Warning: times beyond recommended time")
        print(rec.warning)
        return rec.outputList

#roberto = LISTEN(50)
#output=roberto.startListen()
#pack=[0, 1, 10, 11, 12, 1, 8, 0, 9, 4, 12, 8, 2, 0, 1, 0, 1, 10, 11, 12, 2, 13, 10, 8, 15, 0, 5, 15, 0, 1, 0, 1, 10, 11, 12, 3, 4, 4, 6, 5, 6, 5, 7, 10, 2, 0, 6, 14, 2, 8, 9, 0, 1, 0, 1, 10, 11, 12, 4, 7, 5, 7, 4, 7, 3, 12, 10, 10, 0, 1]
#send.compare(pack,output)