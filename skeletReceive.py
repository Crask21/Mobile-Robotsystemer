import sys
import moveClass
import protocol
import DTMF_overclass
import time

def main():
    robot=DTMF(20)
    moveObj = moveClass.bot()
    list = robot.listen.startListen()
    list = protocol.organize(list)
    list = protocol.esc_check(list)
    list = protocol.decode_CRC(list)
    list = protocol.remove_seq(list)
    list = protocol.convert_to_decimal(list)
    print(list)
    for i in range(len(list)-1):
        moveObj.move(list[i,0],list[i,1])
    moveObj.stop()

if __name__ == "__main__":
    main()