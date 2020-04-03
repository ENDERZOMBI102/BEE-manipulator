import tkinter as tk
from tkinter import messagebox as msg
import tkinter.ttk as ttk
import config
from typing import Union
from utilities import *
import beeManager
import webbrowser as wb
import os
import logWindow
from browser import browser
from utilities import set_window_icon
from settingsUI import settingsWindow
from srctools.logger import get_logger

class root(tk.Tk):
    def __init__(self):
        # initialize the window
        super().__init__()
        self.wm_title(f'BEE Manipulator v{config.version()}')
        self.geometry("600x500")
        self.lift()
        # set window icon
        self.wm_iconbitmap(default="assets/icon.ico")
        set_window_icon(self)
        # check updates
        logWindow.init(self)
        self.LOGGER = get_logger("mainLoop")
        try:
            if (config.load("logWinodowVisible")):
                logWindow.toggleVisibility()
        except:
            logWindow.toggleVisibility()
        self.LOGGER.debug("starting background update check for BEE Manipulator")
        self.checkUpdates(window=False)
        r"""
            there are the functions to make the main window, every # comment indicates
            what part is build there, to make it more clear and readable
            ttb = top tool bar
            TODO: make every dropdown menu a class
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
        self.optionMenu.add_command(label="Toggle Log Window", command=logWindow.toggleVisibility)
        self.optionMenu.add_command(label="Reload Configs", command=self.reloadConfig)
        self.optionMenu.add_command(label="Reload Packages", command=self.reloadPackages)
        self.optionMenu.add_command(label="Manage Games", command=self.openGameManager)
        self.optionMenu.add_command(label="Manage Packages", command=self.openPackageManager)
        self.optionMenu.add_command(label="Manage Plugins", command=self.openPackageManager)

        # options ttb menu
        self.portal2 = tk.Menu(self.toolBarFrame, tearoff=0, bg="white", fg="black")
        self.portal2.add_command(label="Verify Game Cache", command=self.verifyGameCache)
        self.portal2.add_command(label="Uninstall BEE2.4", command=self.uninstallBee)
        self.portal2.add_command(label="Install BEE2.4", command=self.installBee)
        
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
        self.toolBarFrame.add_cascade(label="Portal 2", menu=self.portal2)
        self.toolBarFrame.add_cascade(label="Help", menu=self.helpMenu)
        self.configure(menu=self.toolBarFrame)
        # pack the browser
        self.browser = browser(self)
        self.browser.pack()
		
        self.bind("<Control-l>", logWindow.toggleVisibility)

    # file menu
    def openp2dir(self):
        os.startfile(config.portalDir())

    def openBEEdir(self):
        if(config.load("beePath") is None):
            self.viewNew = simplePopup(self, "Error", "BEE isn't installed", canBeClosed=False)
        else:
            pass



    def syncGames(self):
        pass

    # options menu
    def openSettingsWindow(self):
        self.LOGGER.debug("opening settings window!")
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
        self.LOGGER.debug("opening about window")
        self.viewNew = aboutWindow(self)

    def checkUpdates(self, window = True):
        # if there's an update open a popup, if not open another popup (if window = true)
        if config.checkUpdates():
            self.LOGGER.debug("opening update popup")
            self.viewNew = updatePopup(self)
        elif window:
            self.LOGGER.info("latest version already instelled")
            self.LOGGER.debug("opening \"latest version\" popup")
            self.viewNew = simplePopup(self, 'Update Checker', "you have the latest version!", 2, False)

    def openWiki(self):
        self.LOGGER.debug(
            "starting browser instance with url: https://github.com/ENDERZOMBI102/BEE-manipulator/wiki")
        wb.open("https://github.com/ENDERZOMBI102/BEE-manipulator/wiki")

    def openGithub(self):
        self.LOGGER.debug("starting browser instance with url: https://github.com/ENDERZOMBI102/BEE-manipulator/")
        wb.open("https://github.com/ENDERZOMBI102/BEE-manipulator/")

    def openDiscord(self):
        self.LOGGER.debug("starting browser instance with url: https://discord.gg/hnGFJrz")
        wb.open("https://discord.gg/hnGFJrz")

    def verifyGameCache(self):
        self.LOGGER.debug("displaying message box \"usure\"")
        self.viewNew = simplePopup(self, )

    def uninstallBee(self):
        pass

    def installBee(self):
        pass

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
        self.creditsText.grid(row=5, column=0, sticky="snew")
        # close button
        self.okbtn = tk.Button(self)
        self.okbtn["text"] = "Close"
        self.okbtn["command"] = self.destroy # if the button is pressed, destroy the window
        self.okbtn.grid(row=10, column=0, sticky="s", pady=5, ipadx=10)
        


class updatePopup(tk.Toplevel):
    r"""
        The update window
    """

    def __init__(self, master):

        super().__init__(master, name='update Popup')
        self.grid_columnconfigure(10)
        self.grid_rowconfigure(10)

        self.versionLabel = tk.Label(self)
        self.versionLabel["text"] = ("A new version of BEE Manipulator is avaiable!\nCurrent: {0} New: {1}".format(version(), onlineVersion()))
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

class simplePopup(tk.Toplevel):
    r"""
        a basic popup, text is the text it display
        closeButtonStyle can be multiple values:
        0 : Close
        1 : Ok
        2 : Ok :D
        3 : use the closeButton parameter
        callBack will make the close button start a callback
    """
    def __init__(self, master: Union[tk.Toplevel, tk.Tk], title: str, text: str, closeButtonStyle = 0, canBeClosed = True, closeButton = "", callBack = None):
        #set button callback
        self.callBack = callBack
        # set the button text
        if closeButtonStyle == 0: closeButtonText = "Close"
        elif closeButtonStyle == 1: closeButtonText = "Ok"
        elif closeButtonStyle == 2: closeButtonText = "Ok :D"
        elif closeButtonStyle == 3: closeButtonText = closeButton
        else: raise ValueError(f'{closeButtonStyle} isn\'t a valid selection! valid selections: 0, 1, 2 and 3')
        super().__init__(master, name=title.lower())
        self.transient(master)
        self.wm_withdraw()
        self.columnconfigure(10)
        self.rowconfigure(10)
        self.title = title
        set_window_icon(self)
        if not canBeClosed: 
            self.protocol('WM_DELETE_WINDOW', self.wm_deiconify)
        #self.wm_title = title
        #self.setvar("title", title)        
        self.wm_resizable(False, False)

        self.msgLabel = tk.Label(self)
        self.msgLabel["text"] = text
        self.msgLabel.grid(row=5, rowspan=2)

        self.okbtn = tk.Button(self)
        self.okbtn["text"] = closeButtonText
        self.okbtn["command"] = self.runCallBack
        self.okbtn.grid(row=10, column=0, sticky="s", pady=5, ipadx=10)
        self.wm_deiconify()
        
    def runCallBack(self):
        if self.callBack is not None: self.callBack()
        self.destroy()


if __name__=="__main__":
    root=root()
    root.mainloop()
