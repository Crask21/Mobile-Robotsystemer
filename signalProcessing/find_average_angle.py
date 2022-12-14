import numpy as np
import math

myAngles=[0, 0.05, 0.1, 0.15, 0.2, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]

def getVectors(angles):
    vectors=[]
    for i in angles:
        vector=[math.cos(i*2*math.pi),math.sin(i*2*math.pi)]
        vectors.append(vector)
    #print(vectors)
    return vectors
def sumvectors(vectors):
    vectorSum=[0,0]
    for i in vectors:
        vectorSum[0]+=i[0]
        vectorSum[1]+=i[1]
    #print(vectorSum)
    return np.array(vectorSum)
def getAngle(cartesianCoord):
    #print(cartesianCoord)
    angle=math.atan2(cartesianCoord[1],cartesianCoord[0])
    angleinList=angle/(math.pi*2)
    return angleinList
def getAverage(angles):
    vectors=getVectors(angles)
    vectorSum=sumvectors(vectors)
    average=getAngle(vectorSum)
    return average%1

print(myAngles)
average=getAverage(myAngles)
print(average)





