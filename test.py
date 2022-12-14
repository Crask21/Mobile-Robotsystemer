from Protocol.DataLink.protocol_class import protocolClass
from Protocol.Physical.DTMF_overclass import DTMF

obj1 = protocolClass(['0xa','0x0','0x3'],[[10,20],[20,30]],DTMF(50,10,mono_robot=True))
obj1.DataLinkDown()
obj1.DataLinkUp()
print(obj1)

