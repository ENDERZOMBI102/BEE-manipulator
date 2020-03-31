import utilities
import tkinter as tk
import tkinter.ttk as ttk
import config
import srctools.logger
import logging

# Colours to use for each log level
LVL_COLOURS = {
    logging.CRITICAL: 'white',
    logging.ERROR: 'red',
    logging.WARNING: '#FF7D00',  # 255, 125, 0
    logging.INFO: '#0050FF',
    logging.DEBUG: 'grey'
}

BOX_LEVELS = [
    logging.DEBUG,
    logging.INFO,
    logging.WARNING
]

LVL_TEXT = {
    logging.DEBUG: ('Debug messages'),
    logging.INFO: ('Default'),
    logging.WARNING: ('Warnings Only')
}

visible = False
window = None
textBox = None

class handler(logging.Handler):
    def __init__(self):
        super().__init__(getLevel())
        global textBox
        

        


def init(tkRoot):
    global window, textBox
    window = tk.Toplevel(tkRoot)
    window.wm_withdraw()
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    window.title(f'Logs - {config.version()}')
    window.protocol('WM_DELETE_WINDOW', window.wm_withdraw)
    textBox = tk.Text(
		window,
		name='textBox',
		width=60,
		height=15
	).grid(row=0, column=0, sticky='NSEW')
    utilities.set_window_icon(window)
    logHandler = handler()



def toggleVisibility():
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
