import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import *
from config import *

class root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BEE Manipulator v"+str(config.load("appVersion")))
        self.geometry("600x500")
        #the main container
        self.mainFrame = tk.Frame(self)
        #
        #
        #
        #
        self.mainFrame.pack()
		
if __name__=="__main__":
	root=root()
	root.mainloop()
