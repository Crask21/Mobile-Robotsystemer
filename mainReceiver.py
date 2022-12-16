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
    data_prot = protocolClass('0x0',moves=[],robot=robot,filename='output.txt')

    # Listen for package
    #package = data_prot.PhysicalUp()

    package = [0, 1, 1, 7, 0, 8, 6, 10, 2, 0, 1, 0, 1, 2, 13, 10, 8, 0, 8, 4, 4, 0, 1, 0, 1, 3, 13, 10, 14, 7, 3, 14, 10, 0, 1, 0, 1, 4, 10, 13, 12, 3, 4, 6, 14, 0, 1, 0, 1, 5, 5, 3, 0, 2, 12, 9, 14, 0, 1, 0, 1, 6, 7, 6, 14, 4, 13, 14, 11, 0, 1, 0, 1, 7, 8, 0, 14, 4, 3, 0, 10, 0, 1, 0, 1, 8, 8, 0, 13, 12, 13, 14, 1, 0, 1, 0, 1, 9, 4, 4, 6, 5, 6, 5, 7, 10, 2, 0, 6, 14, 8, 15, 5, 0, 1, 0, 1, 10, 7, 5, 7, 4, 7, 3, 1, 11, 5, 0, 1]

    # Convert package to message
    message_in_list = data_prot.decode(package,'0x0')
    


    message = message_in_list[0][0]

    # Write message to txt file
    try:
      with open('received.txt', 'w') as f:
        f.write(message)
    except:
      print('Failed')
    

    



    


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