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