import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import *
from config import *
import webbrowser as wb
import os
from browser import browser

class root(tk.Tk):
    def __init__(self):
        # initialize the window
        super().__init__()
        try:
            config.check()
        except:
            config.create_config()
        self.title("BEE Manipulator v"+str(config.load("appVersion")))
        self.geometry("600x500")
        # set window icon
        self.iconphoto(False, tk.PhotoImage(file="./assets/icon.ico"))
        # the main container
        self.checkUpdates(window=False)
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
        # pack the browser
        self.browser = browser(self)
        self.browser.pack()
		

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

    def checkUpdates(self, window = True):
        # if there's an update open a popup, if not open another popup (if window = true)
        if reconfig.checkUpdates():
            self.updatePopup = updatePopup(self)
        elif window:
            self.latestPopup = latestPopup(self)
            

    def openOfflineWiki(self):
        pass

    def openOnlineWiki(self):
        wb.open("https://github.com/ENDERZOMBI102/BEE-manipulator/wiki")

    def openGithub(self):
        wb.open("https://github.com/ENDERZOMBI102/BEE-manipulator/")

    def openDiscord(self):
        wb.open("https://discord.gg/hnGFJrz")



class aboutWindow(tk.Toplevel):
    r"""
        The about window
    """
    def __init__(self, master):
        # configure the window
        super().__init__(master)
        self.focus_force()
        self.grid_columnconfigure(10)
        self.grid_rowconfigure(10)
        # the about text
        self.creditsText = tk.Label(self)
        self.creditsText["text"] = (
            '"BEE Manipulator" : \n{\n"Main Developer" : "ENDERZOMBI102",\n"Icon By" : "N\\A",\n"}')
        self.creditsText.grid(row=5, column=0, sticky="s")
        # ok button
        self.okbtn = tk.Button(self)
        self.okbtn["text"] = "Ok :D"
        self.okbtn["command"] = self.destroy # if the button is pressed, destroy the window
        self.okbtn.grid(row=10, column=0, sticky="s", pady=5, ipadx=10)

class settingsWindow(tk.Toplevel):
    r"""
        this is the window for the settings
    """
    def __init__(self, master):
        super().__init__(master)
        


class updatePopup(tk.Toplevel):
    r"""
        The about window
    """

    def __init__(self, master):

        super().__init__(master)
        self.focus_force()
        self.grid_columnconfigure(10)
        self.grid_rowconfigure(10)

        self.versionLabel = tk.Label(self)
        self.versionLabel["text"] = ("A new version of BEE Manipulator is avaiable!\nCurrent: {0} New: {1}".format(reconfig.version(), reconfig.onlineVersion()))
        self.versionLabel.grid(row=5, rowspan=2)

        self.ATbtn = tk.Button(self)
        self.ATbtn["text"] = "Another Time"
        self.ATbtn["command"] = self.destroy
        self.ATbtn.grid(row=10, column=0, sticky="w", padx=20, pady=5)

        self.YESbtn = tk.Button(self)
        self.YESbtn["text"] = "Update!"
        self.YESbtn["command"] = self.update
        self.YESbtn.grid(row=10, column=0, sticky="e", padx=20, pady=5, ipadx=10)

    def update(self):
        try:
            url = config.load("newVersionUrl")
            wb.open(url)
            self.destroy()
        except:
            self.YESbtn.destroy()
            self.ATbtn.destroy()
            self.versionLabel["text"] = "Can't load download url from config file"
            
            self.YESbtn = tk.Button(self)
            self.YESbtn["text"] = "Ok :C"
            self.YESbtn["command"] = self.destroy
            self.YESbtn.grid(row=10, column=0, sticky="s", pady=5, ipadx=10)

class latestPopup(tk.Toplevel):

    def __init__(self, master):

        super().__init__(master)
        self.focus_force()
        self.grid_columnconfigure(10)
        self.grid_rowconfigure(10)

        self.msgLabel = tk.Label(self)
        self.msgLabel["text"] = "You have the latest version!"
        self.msgLabel.grid(row=5, rowspan=2)
            
        self.okbtn = tk.Button(self)
        self.okbtn["text"] = "Ok :D"
        self.okbtn["command"] = self.destroy
        self.okbtn.grid(row=10, column=0, sticky="s", pady=5, ipadx=10)


if __name__=="__main__":
    root=root()
    root.mainloop()

    


