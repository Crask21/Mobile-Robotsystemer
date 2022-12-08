from tkinter import *
import sys
sys.path.append('../Mobile-Robotsystems')

root = Tk()
root.title("Move GUI")


myLabel = Label(root,text="Current package")
myLabel.pack()

moveList = []
li=[[0, 23], [-23, 0], [0, -234], [23, 0], [0, -234], [-234, 0], [634, 0]]

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

def manualMove():
    myLabel.config(text ="Current package: " +  manual_enter.get()) 


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

    
    

frame1 = LabelFrame(root,text='Enter moves', padx=20,pady=20)
frame1.pack(padx=10,pady=10)
frame2 = LabelFrame(root,text='Manual enter', padx=20,pady=20)
frame2.pack(padx=10,pady=10)
frame2 = LabelFrame(root,text='Play', padx=20,pady=20)
frame2.pack(padx=10,pady=10)

enter = Entry(frame1, width = 10, borderwidth=5)
up = Button(frame1, text="^",command=lambda: addMovement('up'))
down = Button(frame1, text="v",command=lambda: addMovement('down'))
left = Button(frame1, text="<",command=lambda: addMovement('left'))
right = Button(frame1, text=">",command=lambda: addMovement('right'))

manual_enter = Entry(frame2, width = 10, borderwidth=5)
submit = Button(frame2, text="Submit",command= manualMove)

up.grid(row=0,column=1)
enter.grid(row=1,column=1)
down.grid(row=2,column=1)
left.grid(row=1,column=0)
right.grid(row=1,column=3)

manual_enter.grid(row=0,column=0)
submit.grid(row=1,column=0)




#b = Button(frame1, text="dont click")
#b.pack()


#enter.grid(row=0,column=0,columnspan=3,padx=10,pady=10)
#enter.pack()




#myButton = Button(root, text="Click me !",command=click)
#myButton.pack()

root.mainloop()

