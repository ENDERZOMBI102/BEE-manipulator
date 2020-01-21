import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import *
from config import *
import os

class root(tk.Tk):
    def __init__(self):
        # initialize the window
        super().__init__()
        self.title("BEE Manipulator v"+str(config.load("appVersion")))
        self.geometry("600x500")
        # set window icon
        self.iconphoto(False, tk.PhotoImage(file="./assets/icon.ico"))
        # the main container
        self.mainFrame = tk.Frame(self)
        r"""
            there are the functions to make the main window, every # comment indicates
            what part is build there, to make it more clear and readable
            ttb = top tool bar
            TODO: make every menu a class/function
        """
        # top tool bar
        self.toolBarFrame = tk.Menu(self, bg="lightgrey", fg="black")
        # file ttb menu
        self.fileMenu = tk.Menu(self.toolBarFrame, tearoff=0, bg="lightgrey", fg="black")
        self.fileMenu.add_command(label="Open Portal 2 Directory", command=self.openp2dir)
        self.fileMenu.add_command(label="Open BEEmod Directory", command=self.openBEEdir)
        # options ttb menu
        self.optionMenu = tk.Menu(self.toolBarFrame, tearoff=0, bg="lightgrey", fg="black")

        # help ttb menu
        self.helpMenu = tk.Menu(self.toolBarFrame, tearoff=0, bg="lightgrey", fg="black")
        self.helpMenu.add_command(label="About..", command=self.openAboutWindow)
        # put all the ttb together
        self.toolBarFrame.add_cascade(label="File", menu=self.fileMenu)
        self.toolBarFrame.add_cascade(label="Options", menu=self.optionMenu)
        self.toolBarFrame.add_cascade(label="Help", menu=self.helpMenu)
        self.configure(menu=self.toolBarFrame)
        # pack the main frame
        self.mainFrame.pack()
		


    def openp2dir(self):
        os.startfile(reconfig.portalDir())

    def openAboutWindow(self):
        self.viewNew = aboutWindow()


    def openBEEdir(self):
        pass



class aboutWindow(tk.Toplevel):
    r"""
        The about window
    """
    def __init__(self):

        tk.Toplevel.__init__(self)

        self.outputLabel2 = tk.Label(self)
        self.outputLabel2["text"] = ("Enter Value")
        self.outputLabel2.grid(row=5, rowspan=2)

        self.entrySpace2 = tk.Entry(self)
        self.entrySpace2.grid(row=8, column=0, rowspan=2)

        self.Button2 = tk.Button(self)
        self.Button2["text"] = "Try Me"
        #self means "MySecondGUI" not "MainControl" here
        self.Button2["command"] = self.buttonPressed2
        self.Button2.grid(row=14, column=0, rowspan=2)

    def buttonPressed2(self):
        pass

        




if __name__=="__main__":
	root=root()
	root.mainloop()
