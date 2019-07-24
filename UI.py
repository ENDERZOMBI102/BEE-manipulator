from tkinter import *

def ask():
    messagebox.askyesno("sure", "are you sure?")
    
top = Tk()
CheckVar1 = IntVar()
CheckVar2 = IntVar()

CB1 = Checkbutton(top, text = "install radelite package", variable = CheckVar1, onvalue = 1, offvalue = 0, height=5, width = 20)
CB1.place(x = 10, y = 10)
CB2 = Checkbutton(top, text = "install more music package", variable = CheckVar2, onvalue = 1, offvalue = 0, height=5, width = 20)
CB2.place(x = 10, y = 20)
B1 = Button(top, text = "install", command = ask)
B1.place(x = 40, y = -40)



top.geometry("250x250+10+10")
top.mainloop()
