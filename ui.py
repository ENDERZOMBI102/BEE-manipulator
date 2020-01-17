import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import *
from config import *
from richPresence import *
from time import sleep

class root(tk.Tk):
    def __init__(self):
        # initialize the window
        super().__init__()
        x = richPresence()
        self.title("BEE Manipulator v"+str(config.load("appVersion")))
        self.geometry("600x500")
        # the main container
        self.mainFrame = tk.Frame(self)
        # set window icon
        self.iconphoto(False, tk.PhotoImage(file="./assets/icon.ico"))
        #  
        #
        #
        #
        self.mainFrame.pack()
        sleep(200)
        x.update("idle")
		
if __name__=="__main__":
	root=root()
	root.mainloop()
