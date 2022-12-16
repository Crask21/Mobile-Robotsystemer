from tkinter import *
import sys
sys.path.append('../Mobile-Robotsystems')
from Protocol.DataLink.protocol_class import protocolClass
from Protocol.Physical.DTMF_overclass import DTMF
#from tkinter.ttk import *
#
root = Tk()
root.title("Move GUI")

global window_

dtmfLabel = Label(root,text="Package in hex:")
hexa = Text(root,height=5, borderwidth=0)
dtmfLabel.pack()
hexa.pack()

package = []

baud = 50
fade = 0.003

robot=DTMF(50,20)




global moveList
moveList = []


# Convert list to readable string
def moveDisplay(list):
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

# Display list like it were printed
def listDisplay(list):
    res = ''
    

    for i in range(len(list)):
        temp = ''
        if i == 0:
            temp = '[' + str(list[i])
        elif i == len(list)-1:
            temp =', ' + str(list[i]) + ']'
        else:
            temp =', ' + str(list[i])

        res = res + temp

    return res


def updateBAUD():
    baud = int(baud_enter.get())
    robot.send.setBaud(baud)
   

def updateFADE():

    fade = int(fade_enter.get())
    robot.send.setFade(fade)

def updateLENGTH():
    length = len(package)
    length2.config(text=str(length))





# Set package/moves (not finished)
def manualPackage():
    input = manual_enter.get()

    package = inputToList(input)
    hexa.configure(state=NORMAL)
    hexa.delete("1.0","end")
    hexa.insert(1.0, input)
    hexa.configure(state=DISABLED)

    
    
    

    robot.send.send_package(package)
    length2.config(text=len(package))
    print(package)

# Printable list to python list
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
    
    pack = protocolClass(['0x7','0x0','0x8'],[],robot=robot,filename='output.txt')
    
    # Get moves
    pack.setMoves(moveList,msg_entry.get())
    
    # Convert to package
    pack.DataLinkDown()

    # Send package
    robot.send.send_package(pack.data_list)
    print("Package:")
    print(pack.data_list)
    length2.config(text=len(pack.data_list))

    # Show package
    hexa.configure(state=NORMAL)
    hexa.delete("1.0","end")
    hexa.insert(1.0, listDisplay(pack.data_list))
    hexa.configure(state=DISABLED)
    pack.setMoves(moveList,[])

    
    
    


# Open new window 
def openNewWindow():

    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(root)

    # sets the title of the
    # Toplevel widget
    newWindow.title("Listen")

    # sets the geometry of toplevel
    #newWindow.geometry("200x200")

    # A Label widget to show in toplevel
    Label(newWindow, text ="Listening!").pack()
    return newWindow

window = openNewWindow()

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

    update = moveDisplay(moveList)

    move_txt.configure(state=NORMAL)
    move_txt.delete("1.0","end")
    move_txt.insert(1.0, update)
    move_txt.configure(state=DISABLED)
    printGUI('test')


def printGUI(string_):
    
    Label(window, text=string_).pack()

def decode_pack(list):

    # Get readable list
    res = inputToList(list)

    # Decode
    pack.setPackage(res)
    pack.DataLinkUp()

    # Show decoded package
    translated.config(text = pack.data_list)
    print(pack.data_list)

#decode_pack([0, 1, 10, 11, 12, 1, 8, 0, 9, 4, 12, 8, 2, 0, 1, 0, 1, 10, 11, 12, 2, 13, 10, 8, 15, 0, 5, 15, 0, 1, 0, 1, 10, 11, 12, 3, 4, 4, 6, 5, 6, 5, 7, 10, 2, 0, 6, 14, 2, 8, 9, 0, 1, 0, 1, 10, 11, 12, 4, 7, 5, 7, 4, 7, 3, 12, 10, 10, 0, 1])


def clear_movement():
    # Clear move list
    moveList.clear()

    hexa.configure(state=NORMAL)
    hexa.delete("1.0","end")
    hexa.insert(1.0, '')
    hexa.configure(state=DISABLED)


    move_txt.configure(state=NORMAL)
    move_txt.delete("1.0","end")
    move_txt.configure(state=DISABLED)
    
# Setup frame 1
frame1 = LabelFrame(root,text='Enter moves', padx=20,pady=20)
frame1.pack(padx=10,pady=10)

myLabel = Label(frame1,text="Current movements: ")
move_txt = Text(frame1,height=3, borderwidth=0, width=60)


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
move_txt.grid(row=1,column=1,columnspan=1000)#columnspan=1000
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
frame2 = LabelFrame(root,text='Manual hexa decimal package', padx=20,pady=20)
frame2.pack(padx=10,pady=10)

manual_enter = Entry(frame2, width = 10, borderwidth=5)
submit = Button(frame2, text="Submit",command= manualPackage)


manual_enter.grid(row=0,column=0)
submit.grid(row=1,column=0)

baud_enter = Entry(frame2, width = 10, borderwidth=5)
baud_enter.insert(0,'Baud rate')
baud_submit = Button(frame2, text="Baud submit",command= updateBAUD)
baud_enter.grid(row=0,column=1)
baud_submit.grid(row=1,column=1)


fade_enter = Entry(frame2, width = 10, borderwidth=5)
fade_enter.insert(0,'Fade')
fade_submit = Button(frame2, text="Fade submit",command= updateFADE)
fade_enter.grid(row=2,column=1)
fade_submit.grid(row=3,column=1)

length2 = Label(frame2,text="Length")
length2.grid(row=4,column=1)


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



# Baud
# længde
# fade





#b = Button(frame1, text="dont click")
#b.pack()


#enter.grid(row=0,column=0,columnspan=3,padx=10,pady=10)
#enter.pack()




#myButton = Button(root, text="Click me !",command=click)
#myButton.pack()

root.mainloop()

