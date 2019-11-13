import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
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
class beeUpdaterShortcut(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("240x100")
        self.title("BEE2 Updater")
        # create the loading bar
        self.loading_bar = pbar(self)
        self.loading_bar.start(interval=8)
        self.loading_bar.pack()
