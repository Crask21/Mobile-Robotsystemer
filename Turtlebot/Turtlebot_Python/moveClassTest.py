
import moveClass

def main():
    moveObj = moveClass.bot()
    while True:
        moveObj.move(0.1,1,3)
        moveObj.move(-0.1,-1,3)

if __name__ == "__main__":
    main()