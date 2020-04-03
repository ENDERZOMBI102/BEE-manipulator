import utilities
import tkinter as tk
import tkinter.ttk as ttk
import config
import srctools.logger
import logging
from tkinter.constants import RIGHT, LEFT, Y, BOTH

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
    def __init__(self):
        level = getLevel()
        super().__init__(level)
        global window
        self.textBox: tk.Text
        self.textBox = tk.Text(
		    window,
		    name='textBox',
		    width=60,
		    height=15
	    ).grid(row=0, column=0, sticky='NSEW')
        self.vbar = tk.Scrollbar(window)
        self.vbar.grid(row=0, column=0)
        self.vbar['command'] = self.textBox.yview
        
        
        
def init(tkRoot):
    global window
    window = tk.Toplevel(tkRoot)
    window.transient(tkRoot)
    window.wm_withdraw()
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    window.title('Logs')
    window.protocol('WM_DELETE_WINDOW', toggleVisibility)
    utilities.set_window_icon(window)
    logHandler = textHandler()
    window.bind("<Control-l>", toggleVisibility)
    window.bind("<Control-c>", textHandler.clear)



def toggleVisibility(placeHolder=None):
    global visible, window
    if not visible:
        window.wm_deiconify()
        visible = True
    else:
        window.wm_withdraw()
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
