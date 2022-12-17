import numpy as np
import pandas as pd
numberNFreqs=[]
baudrates=[]
for i in range(6000):
    fs=i
    allData=[[]]
    data=[]
    noiceBaudrates=[]
    for baud in range(2,201):
        data=[]
        #print("\nbaud:")
        #print(baud)
        data.append(baud)
        #print("samplesize:")
        samplesize=fs*(1/baud)
        data.append(samplesize)
        #print(samplesize)

        decimalVal=fs*(1/baud)%1
        #print(decimalVal)
        #print("reads until tone is skipped:")
        try:
            reads=str(samplesize/decimalVal)
        except:
            reads="NaN"
            noiceBaudrates.append(baud)
            baudrates.append(baud)
        data.append(reads)
        allData.append(data)

    #df=pd.DataFrame(allData,columns=["Baudrate", "samplesize","reads until skipped"])
    #df=df.drop(index=0)
    #print(df)
    #df.to_excel("DisplacementOfReads"+str(fs)+".xlsx")
    #print("sample frequency:"+str(fs))
    #print(noiceBaudrates)
    numberNFreqs.append(len(noiceBaudrates))
print(numberNFreqs)
numberNFreqs=np.array(numberNFreqs)

print(np.argmax(numberNFreqs)+2)

