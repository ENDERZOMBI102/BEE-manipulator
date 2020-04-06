import utilities
import config
import srctools.logger
import logging
import wx


# Colours to use for each log level
LVL_COLOURS = {
    logging.CRITICAL: 'white',
    logging.ERROR: 'red',
    logging.WARNING: '#FF7D00',  # 255, 125, 0
    logging.INFO: '#0050FF',
    logging.DEBUG: 'grey'
}

levels = {
    "DEBUG": [logging.DEBUG, "Debug Messages"],
    "DEFAULT": [logging.INFO, "Default"],
    "WARNING": [logging.WARNING, "Warnings Only"]
}

visible = False
window = None # then converted to tk.TopLevel

START = '1.0'  # Row 1, column 0 = first character

class textHandler(logging.Handler):
    global window
    def __init__(self):
        level = getLevel()
        super().__init__(level)
        
    def emit(self, record: str):
        window.text.WriteText(record+"\n")


        

class logWindow(wx.Frame):

    def __init__(self, master):
        super().__init__(master, title="Logs")
        global window
        window = self
        self.SetSize(0, 0, 500, 350)
        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.text.AlwaysShowScrollbars(vflag=True)
        #self.text.Disable()
        


def init(master):
    window = logWindow(master)


def toggleVisibility(placeHolder=None):
    global visible, window
    if not visible:
        window.ShowWithEffect(wx.SHOW_EFFECT_BLEND)
        visible = True
    else:
        window.HideWithEffect(wx.SHOW_EFFECT_BLEND)
        visible = False

def getLevel():
    if "-dev" in utilities.argv:
        return logging.DEBUG
    # check for the level
    level = config.load("logLevel")
    if level == "INFO":
        level = logging.INFO
    elif level == "WARNING":
        level = logging.WARNING
    else:
        level = logging.DEBUG
    return level
