from config import *
import wx

class settingsWindow(wx.Frame):
    r"""
        this is the window for the settings
    """

    def __init__(self, master):
        super().__init__(master, name='settings')
