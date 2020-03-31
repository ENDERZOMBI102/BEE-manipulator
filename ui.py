import tkinter as tk
from tkinter import messagebox as msg
import tkinter.ttk as ttk
import config
from utilities import *
import beeManager
import webbrowser as wb
import os
import logWindow
from browser import browser
from utilities import set_window_icon
from settingsUI import settingsWindow

class root(tk.Tk):
    def __init__(self):
        # initialize the window
        super().__init__()
        self.title("BEE Manipulator v"+str(config.load("appVersion")))
        self.geometry("600x500")
        self.lift()
        # set window icon
        self.wm_iconbitmap(default="assets/icon.ico")
        set_window_icon(self)
        # check updates
        logWindow.init(self)
        logWindow.toggleVisibility()
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
		

    # file menu
    def openp2dir(self):
        os.startfile(config.portalDir())

    def openBEEdir(self):
        if(config.beePath() is None):
            popup = popup(self, "Error", "BEE isn't installed", canBeClosed=False)
        else:
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
        if config.checkUpdates():
            self.updatePopup = updatePopup(self)
        elif window:
            self.popup = popup(self, "Update Checker", "you have the latest version!", 2, False)

    def openWiki(self):
        wb.open("https://github.com/ENDERZOMBI102/BEE-manipulator/wiki")

    def openGithub(self):
        wb.open("https://github.com/ENDERZOMBI102/BEE-manipulator/")

    def openDiscord(self):
        wb.open("https://discord.gg/hnGFJrz")

    def verifyGameCache(self):
        beeManager.verifyGameCache()

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

class popup(tk.Toplevel):
    r"""
        a basic popup, text is the text it display
        closeButtonStyle can be multiple values:
        0 : Close
        1 : Ok
        2 : Ok :D
    """
    def __init__(self, master, title, text, closeButtonStyle = 0, canBeClosed = True):
        if closeButtonStyle == 0:
            closeButtonText = "Close"
        elif closeButtonStyle == 1:
            closeButtonText = "Ok"
        elif closeButtonStyle == 2:
            closeButtonText = "Ok :D"
        else:
            closeButtonText = "Close"
        super().__init__(master)
        self.wm_withdraw()
        if not canBeClosed:
            self.protocol('WM_DELETE_WINDOW', None)
        self.title = title
        self.grid_columnconfigure(10)
        self.grid_rowconfigure(10)

        self.msgLabel = tk.Label(self)
        self.msgLabel["text"] = text
        self.msgLabel.grid(row=5, rowspan=2)

        self.okbtn = tk.Button(self)
        self.okbtn["text"] = closeButtonText
        self.okbtn["command"] = self.destroy
        self.okbtn.grid(row=10, column=0, sticky="s", pady=5, ipadx=10)
        self.wm_deiconify()


if __name__=="__main__":
    root=root()
    root.mainloop()

    


