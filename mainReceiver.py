import time
#from Turtlebot.moveClass import moveClass
from Protocol.DataLink.protocol_class import protocolClass
from Protocol.Physical.DTMF_overclass import DTMF
import Protocol.DataLink.protocol as protocol

to_hex = {
  '0x0':0,
  '0x1':1,
  '0x2':2,
  '0x3':3,
  '0x4':4,
  '0x5':5,
  '0x6':6,
  '0x7':7,
  '0x8':8,
  '0x9':9,
  '0x10':10,
  '0x11':11,
  '0x12':12,
  '0x13':13,
  '0x14':14,
  '0x15':15
  }



def main():
    
    # Initialize DTMF receive/ send
    robot=DTMF(50,10)

    # Initialize protocol class
    data_prot = protocolClass('0x8',moves=[],robot=robot,filename='output.txt')

    # Listen for package
    #package = data_prot.PhysicalUp()

    package =  [0, 1, 1, 0, 8, 3, 11, 13, 0, 1, 0, 1, 2, 4, 4, 6, 5, 6, 5, 7, 10, 2, 0, 6, 14, 4, 10, 2, 0, 1, 0, 1, 3, 7, 5, 7, 4, 7, 3, 14, 7, 0, 0, 1]

    


    # Convert package to message
    data_prot.setPackage(package)
    message = data_prot.DataLinkUp()
    


    # Write message to txt file
    with open('received.txt', 'w') as f:
        f.write(message)

    



    


if __name__ == "__main__":
    main()


"""
Traceback (most recent call last):
  File "mainReceiver.py", line 31, in <module>
    main()
  File "mainReceiver.py", line 19, in main
    message = protocol.hexa_to_msg(package)
  File "/home/ubuntu/code/Mobile-Robotsystems/Protocol/DataLink/protocol.py", line 174, in hexa_to_msg
    if len(dtmf_signal[i])>2:
TypeError: object of type 'int' has no len()
"""