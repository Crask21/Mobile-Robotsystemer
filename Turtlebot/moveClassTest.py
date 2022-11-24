#   Following code tests demonstrates the implemenation
#   of moveClass.py
#
#   import moveClass
#   moveObj = moveClass.bot()
#   moveObj.move(ang,dist)
#
#   It is important to moveObj.stop() at the end


import sys
import Turtlebot.Source.moveClass as moveClass

def main():
    ang = sys.argv[1]
    dist = sys.argv[2]
    
    moveObj = moveClass.bot()
    moveObj.move(ang, dist)
    moveObj.stop()

if __name__ == "__main__":
    main()