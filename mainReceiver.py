import time
#from Turtlebot.moveClass import moveClass
from Protocol.DataLink.protocol_class import protocolClass
from Protocol.Physical.DTMF_overclass import DTMF
import Protocol.DataLink.protocol as protocol


def main():
    
    # Initialize DTMF receive/ send
    robot=DTMF(20,10, mono_robot = True)

    # Initialize protocol class
    data_prot = protocolClass(moves=[],robot=robot)

    # Listen for package
    package = data_prot.PhysicalUp()
    # Convert package to message
    message = protocol.hexa_to_msg(package)
    
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