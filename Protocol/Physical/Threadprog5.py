import pyaudio
import numpy as np
from time import time
from scipy.fftpack import fft
from copy import deepcopy
import pandas as pd

class LISTEN():
    def __init__(rec, baud, sync=0, fade=0, amplitude=0, senderFs=0, pack=[]):
        #--------------------------------VARIABLE FOR LOG-------------------------
        rec.sync=sync
        rec.fade=fade
        rec.amplitude=amplitude
        rec.senderFs=senderFs
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

        #------------------------------VARAIBLES--------------------------
        rec.expectedPack=pack
        rec.accuracy=0
        rec.averageMagn1=0
        rec.averageMagn2=0


        rec.noSignal=0
        rec.startReading=False
        rec.currentRead=0
        rec.ABcount=0
        rec.starting=False   
        
        #for log
        rec.tones=np.array([[99,99,99,99,99]])    
        rec.getLog=True
        rec.multipleTests=True
        rec.testNumber=0

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
        if not("output" in locals()):    
            hej=0
            #print(inputFreqs)
        else:    
            return int(output)

    def compare(rec, original, recieved, compare = True):

        dif = len(recieved) - len(original)

        if len(recieved) > len(original):
                recieved2 = recieved.copy()
                recieved = recieved[:len(recieved) - dif]


        if original == recieved:
            print("100% match")
            print("Original: ",original)
            
            print("Recieved: ",recieved2)
        


        elif compare:
            count = 0

            length = len(original) if dif >= 0 else len(recieved)

            for i in range(length):
                if recieved[i] == original[i]:
                    count += 1
            
            print(count/len(original)*100,"% match.", len(original) - count, "errors")
            print("Original:",original)
            print("Recieved:",recieved)


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



            print(count/16*100,"% count match. ", count, "errors")
            print(original)
            print(recieved)

    def writeLogTXT(rec):
        with open("log"+str(rec.testNumber)+".txt", "w") as f:
            f.write("\Settings:\nBaudrate:"+str(rec.baudRate)+"\nsync:" +str(rec.sync)+"\nfade:"+str(rec.fade)+"\namplitude:"+str(rec.amplitude)+"\nsenderFs:"+str(rec.senderFs))
            f.write("\n\nMeasurements\nAverageMagn1:"+str(rec.averageMagn1)+"\nAverageMagn2:"+str(rec.averageMagn2))

    def writeLogXL(rec):
        pdAccuracy=pd.Series([rec.accuracy])
        log=pd.DataFrame(rec.tones,columns=["Rec Freq1","Rec Freq2","Freq1 magn","Freq2 magn","Rec Pkg"])
        log["Freq1 magn"]=log["Freq1 magn"].div(log["Freq1 magn"].max())
        log["Freq2 magn"]=log["Freq2 magn"].div(log["Freq2 magn"].max())
        log=log.drop(0)
        #print(log)
        pdPack=pd.Series(rec.expectedPack)
        log["Exp pkg"]=pdPack
        #find expected frequencies based on expected package
        expfreq1=[]
        expfreq2=[]
        for i in pdPack:
            expfreq1.append(rec.dtmf_freq[i][1])
            expfreq2.append(rec.dtmf_freq[i][0])
        pdExpfreq1=pd.Series(expfreq1)
        pdExpfreq2=pd.Series(expfreq2)
        log["Exp Freq1"]=pdExpfreq1
        log["Exp Freq2"]=pdExpfreq2
        log["diff Freq1"]=log["Rec Freq1"]-log["Exp Freq1"]
        log["diff Freq2"]=log["Rec Freq2"]-log["Exp Freq2"]
        log["Accuracy"]=pdAccuracy

        #add mean magn and diff
        means={"diff Freq1":log["diff Freq1"].mean(),"diff Freq2":log["diff Freq1"].mean(), "Freq1 magn":log["Freq1 magn"].mean(), "Freq2 magn":log["Freq2 magn"].mean()}
        pdMeans=pd.DataFrame(means, index=[0])
        log=pd.concat([log,pdMeans],ignore_index=True)
        #rearrange order
        log=log[["Exp pkg","Rec Pkg","Exp Freq1", "Exp Freq2","Rec Freq1", "Rec Freq2","diff Freq1","diff Freq2", "Freq1 magn", "Freq2 magn", "Accuracy"]]
        log.to_excel("log"+str(rec.testNumber)+".xlsx")

    def startListen(rec):
        print("started listening!")
        while True:
            #-----------------------------Reading-----------------------------
            #while(not(rec.starting)):
            #    data = rec.stream.read(1, exception_on_overflow=False)
            #    data_int = np.frombuffer(data,dtype="h")
            #    print(int(rec.RATE*rec.time_per_read))
            #    print(np.amax(data_int))
            #    if np.amax(data_int)>1500:
            #        rec.starting=True
            #start=time()
            data = rec.stream.read(int(rec.RATE*rec.time_per_read), exception_on_overflow=False)

            data_int = np.frombuffer(data,dtype="h")
            #zeropad data
            data_int = np.append(data_int, rec.z_pad_arr)
            #-------------------------------FFT-------------------------------
            yf=fft(data_int)
            yf=np.delete(yf,rec.delList)
            freqmagn=np.absolute(yf)
            highestfreqs=rec.find_highest_freqs(freqmagn)
            if rec.startReading:
                rec.outputList=np.append(rec.outputList, rec.dtmf_to_hexa(highestfreqs))
                print(rec.outputList)
                #stuff for log
                if rec.getLog:
                    forText=np.append(highestfreqs,freqmagn[highestfreqs])
                    try:
                        forText=np.append(forText, int(rec.dtmf_to_hexa(highestfreqs)))
                    except:
                        forText=np.append(forText, 99)
                    forText=np.array([forText])
                    rec.tones=np.append(rec.tones,forText,axis=0)
            else:
                rec.currentRead=rec.dtmf_to_hexa(highestfreqs)
            #-----------Count A and Bs-----------
            if rec.currentRead==0xa or rec.currentRead==0xb:
                rec.ABcount+=1
            #-----------------------Check if no signal------------------------
            if rec.dtmf_to_hexa(highestfreqs)==None and rec.startReading==True:
                rec.noSignal+=1
                if rec.noSignal>5:
                    break
            else:
                rec.noSignal=0
            #-----------------------Check if ready to start--------------------------
            if rec.currentRead==0xc and rec.ABcount>10:
                rec.startReading=True
        #remove second 12 from sync
        rec.outputList=np.delete(rec.outputList,0)
        rec.accuracy=rec.compare(rec.expectedPack,list(rec.outputList))
        print(rec.accuracy)
        if rec.getLog:
            rec.writeLogXL()
            rec.writeLogTXT()
            rec.testNumber+=1


        
        nones = rec.outputList == None
        rec.outputList = np.delete(rec.outputList,nones)
        rec.outputList=rec.outputList.tolist()

        #-----------------------CLEANING AFTER YOURSELF-----------
        rec.tones=np.array([[99,99,99,99,99]]) 
        rec.syncCounter=0
        rec.noSignal=0
        rec.startReading=False
        rec.currentRead=0
        rec.ABcount=0
        rec.synchronised=False
        rec.to_be_synchronised=False
        rec.result=rec.outputList
        rec.outputList=np.array([],dtype=int)


        return rec.result

#roberto = LISTEN(50)
#
#output=roberto.startListen()
#
#
#if roberto.multipleTests:
#    while True:
#        output=roberto.startListen()