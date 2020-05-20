from config import *
import wx

class settingsWindow(wx.Frame):
    r"""
        this is the window for the settings
    """

    def __init__(self, master=None):
        super().__init__(master, name='Settings', title='Settings')
        

#

if __name__ == '__main__':
    app = wx.App()
    settings = settingsWindow()
    settings.Show()
    app.MainLoop()