import tkinter as tk
import tkinter.ttk as ttk
from config import *

class settingsWindow(tk.Toplevel):
    r"""
        this is the window for the settings
    """

    def __init__(self, master):
        super().__init__(master, name='settings')
