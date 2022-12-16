import numpy as np
x = y = z = np.arange(0.0,5.0,1.0)
#np.savetxt('test.out', x, delimiter=',')   # X is an array
test=69
np.savetxt('test.txt', (x,y,z), delimiter=",",fmt='%1.4d',footer="#This is test ello: "+str(test))   # x,y,z equal sized 1D arrays
#np.savetxt('test.out', x, fmt='%1.4e')   # use exponential notation
x=np.arange(16,dtype=int)
print(x)
print(int(x[0]))