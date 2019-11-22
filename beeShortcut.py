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
        self.loading_bar.pack()
        # check the updates
        if(beeManager.checkUpdates()):
            url = config.load("winBeeDownloadUrl")
            # Streaming, so we can iterate over the response.
            r = requests.get(url, stream=True)
            # Total size in bytes.
            total_size = int(r.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            with open('bee2.zip', 'wb') as file:
                for data in r.iter_content(block_size):
                    t.update(len(data))
                    file.write(data)
            t.close()
            if total_size != 0 and t.n != total_size:
                print("ERROR, something went wrong")
        

if __name__ == "__main__":
    ui = bee2UpdaterShortcut()
    ui.mainloop()
