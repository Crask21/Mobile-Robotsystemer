from tkinter import *
import sys
sys.path.append('../Mobile-Robotsystems')
from Protocol.DataLink.protocol_class import protocolClass
from Protocol.Physical.DTMF_overclass import DTMF

root = Tk()
root.title("Move GUI")



dtmfLabel = Label(root,text="Package in hex:")
hexa = Text(root,height=1, borderwidth=0)
dtmfLabel.pack()
hexa.pack()



robot=DTMF(50,20)


pack = protocolClass([], robot=robot)

global moveList
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

    hexa.configure(state=NORMAL)
    hexa.delete("1.0","end")
    hexa.insert(1.0, input)
    hexa.configure(state=DISABLED)

    out = []
    for i in input.split(', '):
        out.append(int(i))
    

    robot.send.send_package(out)
    print(out)

def inputToList(list):
    res = []
    
    if list[0] == '[':
        list = list[1:]
        list = list[:-1]
        for i in list.split(', '):
            res.append(int(i))
    elif ',' in list:
        for i in list.split(', '):
            res.append(int(i))
    else:
        for i in list.split(' '):
            res.append(int(i))

    return res


# Send current package
def dtmf_send():
    
    
    
    pack.setMoves(moveList,msg_entry.get())
    

    pack.DataLinkDown()

    robot.send.send_package(pack.data_list)
    print("Package:")
    print(pack.data_list)

    #hexa.config(text=pack.getPackage())
    hexa.configure(state=NORMAL)
    hexa.delete("1.0","end")
    hexa.insert(1.0, pack.getPackage())
    hexa.configure(state=DISABLED)


# Add movement to current package
def addMovement(dir):
    
 

    if dir == 'up':
        value = int(enter_ud.get())
        moveList.append([0,value])
    elif dir == 'down':
        value = int(enter_ud.get())
        moveList.append([0,-value])
    elif dir == 'right':
        value = int(enter_lr.get())
        moveList.append([-value,0])
    elif dir == 'left':
        value = int(enter_lr.get())
        moveList.append([value,0])

    update = stringList(moveList)

    move_txt.configure(state=NORMAL)
    move_txt.delete("1.0","end")
    move_txt.insert(1.0, update)
    move_txt.configure(state=DISABLED)

def decode_pack(list):

    res = inputToList(list)

    pack.setPackage(res)
    pack.DataLinkUp()

    translated.config(text = pack.data_list)
    print(pack.data_list)

#decode_pack([0, 1, 10, 11, 12, 1, 8, 0, 9, 4, 12, 8, 2, 0, 1, 0, 1, 10, 11, 12, 2, 13, 10, 8, 15, 0, 5, 15, 0, 1, 0, 1, 10, 11, 12, 3, 4, 4, 6, 5, 6, 5, 7, 10, 2, 0, 6, 14, 2, 8, 9, 0, 1, 0, 1, 10, 11, 12, 4, 7, 5, 7, 4, 7, 3, 12, 10, 10, 0, 1])


def clear_movement():
    moveList.clear()

    move_txt.configure(state=NORMAL)
    move_txt.delete("1.0","end")
    move_txt.configure(state=DISABLED)
    
# Setup frame 1
frame1 = LabelFrame(root,text='Enter moves', padx=20,pady=20)
frame1.pack(padx=10,pady=10)

myLabel = Label(frame1,text="Current movements: ")
move_txt = Text(frame1,height=1, borderwidth=0)


label_ud = Label(frame1,text="Up or Down:")
enter_ud = Entry(frame1, width = 5, borderwidth=5)
enter_ud.insert(0, "10")
up = Button(frame1, text="^",command=lambda: addMovement('up'))
down = Button(frame1, text="v",command=lambda: addMovement('down'))

label_lr = Label(frame1,text="Left or Right:")
enter_lr = Entry(frame1, width = 5, borderwidth=5)
enter_lr.insert(0, "90")
left = Button(frame1, text="<",command=lambda: addMovement('left'))
right = Button(frame1, text=">",command=lambda: addMovement('right'))
msg_entry = Entry(frame1, width = 10, borderwidth=5)
msg_entry.insert(0,'Message')
clear = Button(frame1, text="Clear package",command=clear_movement)
send_dtmf = Button(frame1, text="Send as DTMF",command= dtmf_send)

myLabel.grid(row=0,column=1)
move_txt.grid(row=1,column=1,columnspan=1000)
label_ud.grid(row=2,column=1)
up.grid(row=3,column=1)
enter_ud.grid(row=4,column=1)
down.grid(row=5,column=1)

label_lr.grid(row=6,column=1)
left.grid(row=7,column=0)
enter_lr.grid(row=7,column=1)
right.grid(row=7,column=2)
msg_entry.grid(row=8,column=1,pady=10)
clear.grid(row=9,column=1)

send_dtmf.grid(row=10,column=1,pady=20)

# Setup frame 2
frame2 = LabelFrame(root,text='Manual hexa deciaml package', padx=20,pady=20)
frame2.pack(padx=10,pady=10)

manual_enter = Entry(frame2, width = 10, borderwidth=5)
submit = Button(frame2, text="Submit",command= manualPackage)


manual_enter.grid(row=0,column=0)
submit.grid(row=1,column=0)

    # Setup frame 3
#frame3 = LabelFrame(root,text='Play', padx=20,pady=20)
#frame3.pack(padx=10,pady=10)
#
#send_dtmf = Button(frame3, text="Send as DTMF",command= dtmf_send)
#
#send_dtmf.grid(row=0,column=0)


# Setup frame 4 ()
frame4 = LabelFrame(root,text='Translate package', padx=20,pady=20)
frame4.pack(padx=10,pady=10)

decode_enter = Entry(frame4, width = 10, borderwidth=5)
decode = Button(frame4, text='Decode package', command=lambda: decode_pack(decode_enter.get()))
translated = Label(frame4, text='')

decode_enter.grid(row=1,column=0)
decode.grid(row=2,column=0)
translated.grid(row=3,column=0)



dtmf_send()




#b = Button(frame1, text="dont click")
#b.pack()


#enter.grid(row=0,column=0,columnspan=3,padx=10,pady=10)
#enter.pack()




#myButton = Button(root, text="Click me !",command=click)
#myButton.pack()

root.mainloop()

