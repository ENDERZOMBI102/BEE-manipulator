import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import *
from config import *
import webbrowser as wb
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
        self.fileMenu = tk.Menu(self.toolBarFrame, tearoff=0, bg="white", fg="black")
        self.fileMenu.add_command(label="Open Portal 2 Directory", command=self.openp2dir)
        self.fileMenu.add_command(label="Open BEEmod Directory", command=self.openBEEdir)
        self.fileMenu.add_command(label="Sync Games", command=self.syncGames)
        self.fileMenu.add_command(label="Quit", command=self.quit)
        
        # options ttb menu
        self.optionMenu = tk.Menu(self.toolBarFrame, tearoff=0, bg="white", fg="black")
        self.optionMenu.add_command(label="Settings", command=self.openSettingsWindow)
        self.optionMenu.add_command(label="Reload Configs", command=self.reloadConfig)
        self.optionMenu.add_command(label="Reload Packages", command=self.reloadPackages)
        self.optionMenu.add_command(label="Manage Games", command=self.openGameManager)
        self.optionMenu.add_command(label="Manage Packages", command=self.openPackageManager)
        
        # help ttb menu
        self.helpMenu = tk.Menu(self.toolBarFrame, tearoff=0, bg="white", fg="black")
        self.helpMenu.add_command(label="About..", command=self.openAboutWindow)
        self.helpMenu.add_command(label="Check Updates", command=self.checkUpdates)
        self.helpMenu.add_command(label="Offline Wiki", command=self.openOfflineWiki)
        self.helpMenu.add_command(label="Online Wiki", command=self.openOnlineWiki)
        self.helpMenu.add_command(label="Github", command=self.openGithub)
        self.helpMenu.add_command(label="Discord", command=self.openDiscord)

        # put all the ttb together
        self.toolBarFrame.add_cascade(label="File", menu=self.fileMenu)
        self.toolBarFrame.add_cascade(label="Options", menu=self.optionMenu)
        self.toolBarFrame.add_cascade(label="Help", menu=self.helpMenu)
        self.configure(menu=self.toolBarFrame)
        # pack the main frame
        self.mainFrame.pack()
		

    # file menu
    def openp2dir(self):
        os.startfile(reconfig.portalDir())

    def openBEEdir(self):
        pass

    def syncGames(self):
        pass

    # options menu
    def openSettingsWindow(self):
        self.viewNew = settingsWindow(self)    
    
    def reloadConfig(self):
        pass

    def reloadPackages(self):
        pass

    def openGameManager(self):
        pass

    def openPackageManager(self):
        pass

    # help menu
    def openAboutWindow(self):
        self.viewNew = aboutWindow(self)

    def checkUpdates(self):
        pass

    def openOfflineWiki(self):
        pass

    def openOnlineWiki(self):
        wb.open("https://github.com/ENDERZOMBI102/BEE-manipulator/wiki")

    def openGithub(self):
        pass

    def openDiscord(self):
        pass



class aboutWindow(tk.Toplevel):
    r"""
        The about window
    """
    def __init__(self, master):

        super().__init__(master)

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

class settingsWindow(tk.Toplevel):
    r"""
        this is the window for the settings
    """
    def __init__(self, master):
        super().__init__(master)
        pass



if __name__=="__main__":
	root=root()
	root.mainloop()
