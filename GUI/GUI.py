from tkinter import *
import sys
sys.path.append('../Mobile-Robotsystems')
from Protocol.DataLink.protocol_class import protocolClass
from Protocol.Physical.DTMF_overclass import DTMF

root = Tk()
root.title("Move GUI")


myLabel = Label(root,text="Current package")
myLabel.pack()

robot=DTMF(50,20)

moveList = []


# Convert list to readable string
def stringList(list):
    res = ''
    

    for i in range(len(list)):
        temp = ''
        if i == 0:
            temp = '[' + str(list[i][0]) + ', ' +str(list[i][1]) + ']'
        elif i == len(list)-1:
            temp =', [' + str(list[i][0]) + ', ' +str(list[i][1]) + ']'
        else:
            temp =', [' + str(list[i][0]) + ', ' +str(list[i][1]) + ']'

        res = res + temp

    return res

# Set package/moves (not finished)
def manualPackage():
    input = manual_enter.get()
    myLabel.config(text ="Current package: " +  input) 

    out = []
    for i in input.split(', '):
        out.append(int(i))
    

    robot.send.send_package(out)

# Send current package
def dtmf_send():


    
    
    move = moveList
    pack = protocolClass(move, robot=robot)
    pack.setMoves(move)
    pack.DataLinkDown()


    robot.send.send_package(pack.data_list)

    packLabel.config(text=pack.getPackage())

# Add movement to current package
def addMovement(dir):
    

    if dir == 'up':
        moveList.append([0,int(enter.get())])
    elif dir == 'down':
        moveList.append([0,-int(enter.get())])
    elif dir == 'right':
        moveList.append([-int(enter.get()),0])
    elif dir == 'left':
        moveList.append([int(enter.get()),0])

    update = "Current package: " + stringList(moveList)
    myLabel.config(text = update)

    
    
# Setup frame 1
frame1 = LabelFrame(root,text='Enter moves', padx=20,pady=20)
frame1.pack(padx=10,pady=10)

enter = Entry(frame1, width = 10, borderwidth=5)
up = Button(frame1, text="^",command=lambda: addMovement('up'))
down = Button(frame1, text="v",command=lambda: addMovement('down'))
left = Button(frame1, text="<",command=lambda: addMovement('left'))
right = Button(frame1, text=">",command=lambda: addMovement('right'))

up.grid(row=0,column=1)
enter.grid(row=1,column=1)
down.grid(row=2,column=1)
left.grid(row=1,column=0)
right.grid(row=1,column=3)

# Setup frame 2
frame2 = LabelFrame(root,text='Manual enter', padx=20,pady=20)
frame2.pack(padx=10,pady=10)

manual_enter = Entry(frame2, width = 10, borderwidth=5)
submit = Button(frame2, text="Submit",command= manualPackage)


manual_enter.grid(row=0,column=0)
submit.grid(row=1,column=0)

# Setup frame 3
frame3 = LabelFrame(root,text='Play', padx=20,pady=20)
frame3.pack(padx=10,pady=10)

send_dtmf = Button(frame3, text="Send as DTMF",command= dtmf_send)

send_dtmf.grid(row=0,column=0)

# Setup frame 4 ()
frame4 = LabelFrame(root,text='Translate package', padx=20,pady=20)
frame4.pack(padx=10,pady=10)

packLabel = Label(frame4, text='')
packLabel.grid(row=1,column=0)









#b = Button(frame1, text="dont click")
#b.pack()


#enter.grid(row=0,column=0,columnspan=3,padx=10,pady=10)
#enter.pack()




#myButton = Button(root, text="Click me !",command=click)
#myButton.pack()

root.mainloop()

