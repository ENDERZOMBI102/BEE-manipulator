import tkinter as tk
from tkinter import messagebox as msg
import tkinter.ttk as ttk
from typing import Union
from config import *
from utilities import *
import webbrowser as wb
import os
from browser import browser

class root(tk.Tk):
    def __init__(self):
        # initialize the window
        super().__init__()
        self.title("BEE Manipulator v"+str(config.load("appVersion")))
        self.geometry("600x500")
        # set window icon
        self.wm_iconbitmap(default="assets/icon.ico")
        self.set_window_icon()
        # check updates
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
        self.optionMenu.add_command(label="Manage Plugins", command=self.openPackageManager)
        
        # help ttb menu
        self.helpMenu = tk.Menu(self.toolBarFrame, tearoff=0, bg="white", fg="black")
        self.helpMenu.add_command(label="About..", command=self.openAboutWindow)
        self.helpMenu.add_command(label="Check Updates", command=self.checkUpdates)
        self.helpMenu.add_command(label="Open Wiki", command=self.openWiki)
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

    def openWiki(self):
        wb.open("https://github.com/ENDERZOMBI102/BEE-manipulator/wiki")

    def openGithub(self):
        wb.open("https://github.com/ENDERZOMBI102/BEE-manipulator/")

    def openDiscord(self):
        wb.open("https://discord.gg/hnGFJrz")

    

    def set_window_icon(window: Union[tk.Toplevel, tk.Tk]):
        """Set the window icon."""
        import ctypes
        # Use Windows APIs to tell the taskbar to group us as our own program,
        # not with python.exe. Then our icon will apply, and also won't group
        # with other scripts.
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                'BEEMANIPULATOR.application',
            )
        except (AttributeError, WindowsError, ValueError):
            pass  # It's not too bad if it fails.

        LISTBOX_BG_SEL_COLOR = '#0078D7'
        LISTBOX_BG_COLOR = 'white'

class aboutWindow(tk.Toplevel):
    r"""
        The about window
    """
    def __init__(self, master):
        # configure the window
        super().__init__(master)
        self.winfo_toplevel().title("About BEE Manipulator")
        self.winfo_toplevel().geometry("240x200")
        self.grid_columnconfigure(10)
        self.grid_rowconfigure(10)
        # the about text
        self.creditsText = tk.Label(self)
        self.creditsText["text"] = (r'''"BEE Manipulator" : {
    "Main Developer" : "ENDERZOMBI102",
    "Icon By" : "N\A"
}''')
        self.creditsText.grid(row=5, column=0, sticky="s")
        # close button
        self.okbtn = tk.Button(self)
        self.okbtn["text"] = "Close"
        self.okbtn["command"] = self.destroy # if the button is pressed, destroy the window
        self.okbtn.grid(row=10, column=0, sticky="s", pady=5, ipadx=10)

class settingsWindow(tk.Toplevel):
    r"""
        this is the window for the settings
    """
    def __init__(self, master):
        super().__init__(master, name='settings')
        


class updatePopup(tk.Toplevel):
    r"""
        The about window
    """

    def __init__(self, master):

        super().__init__(master, name='update Popup')
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
        self.grid_columnconfigure(10)
        self.grid_rowconfigure(10)

        self.msgLabel = tk.Label(self)
        self.msgLabel["text"] = "You have the latest version!"
        self.msgLabel.grid(row=5, rowspan=2)
            
        self.okbtn = tk.Button(self)
        self.okbtn["text"] = "Ok :D"
        self.okbtn["command"] = self.destroy
        self.okbtn.grid(row=10, column=0, sticky="s", pady=5, ipadx=10)


class comingsoonPopup(tk.Toplevel):

    def __init__(self, master):

        super().__init__(master)
        self.grid_columnconfigure(10)
        self.grid_rowconfigure(10)

        self.msgLabel = tk.Label(self)
        self.msgLabel["text"] = "Coming Soon!"
        self.msgLabel.grid(row=5, rowspan=2)

        self.okbtn = tk.Button(self)
        self.okbtn["text"] = "Close"
        self.okbtn["command"] = self.destroy
        self.okbtn.grid(row=10, column=0, sticky="s", pady=5, ipadx=10)


if __name__=="__main__":
    root=root()
    root.mainloop()

    


