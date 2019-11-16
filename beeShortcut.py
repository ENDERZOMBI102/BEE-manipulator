import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import Progressbar
from PIL import Image
from beeManager import beeManager
from config import *
import subprocess

"""
this script is responsible for the bee2 shortcut, if the online repo has updates,
launching from this will cause the updater to be launched, and install the update.
launching from this cause the ucpUpdater to be launched too, and check if the database
have some updated packages.

this will be a 'standalone' executable
"""
class bee2UpdaterShortcut(tk.Tk):
    def __init__(self):
        super().__init__()
        # create the window
        self.geometry("240x100")
        self.title("BEE2 Updater")
        self.iconbitmap(default="./assets/BEE2.ico")
        # create the "checking updates" label
        self.label=tk.Label(self, text="Checking Updates...")
        self.label.pack()
        # create the loading bar
        self.loading_bar = Progressbar(self)
        self.loading_bar.start(interval=8)
        self.loading_bar.pack()
        # check the updates
        if(beeManager.checkUpdates()):
            beeManager.update()

if __name__ == "__main__":
    ui = bee2UpdaterShortcut()
    ui.mainloop()
