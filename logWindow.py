import utilities
import config
import logging
import wx
import srctools.logger
import asyncio


# the visibility of the log window, is initially setted to the value saved in the config file
visible: bool = config.load("logWindowVisibility")
window = None # then converted to wx.Frame


class logHandler(logging.Handler):
    """
    this class rappresents the log handler, this will
    recive, format and send the log message to the window
    using the same BEE2.4 log format people are familiar with
    """
    def __init__(self, wxDest=None):
        super().__init__(logging.NOTSET)
        self.setLevel(logging.NOTSET)

    def emit(self, record: logging.LogRecord) -> None:
        """
        recive, format, colorize and display a log message
        """
        global window
        if record.levelno == logging.INFO:
            window.text.SetDefaultStyle(wx.TextAttr(wx.Colour(0, 80, 255)))# blue/cyan

        elif record.levelno == logging.WARNING:
            window.text.SetDefaultStyle(wx.TextAttr(wx.Colour(255, 125, 0)))# orange

        elif record.levelno == logging.ERROR:
            window.text.SetDefaultStyle(wx.TextAttr(wx.Colour(255, 0, 0)))# red

        elif record.levelno == logging.DEBUG:
            window.text.SetDefaultStyle(wx.TextAttr(wx.Colour(128, 128, 128)))# grey

        elif record.levelno == logging.CRITICAL:
            window.text.SetDefaultStyle(wx.TextAttr(wx.Colour(255, 255, 255)))# white
        #display the log message
        window.text.AppendText(self.format(record))


class logWindow(wx.Frame):
    """
    this class make the log window and the log handler
    """
    def __init__(self, master):
        super().__init__(master, title="Logs")# init the window
        global window
        window = self
        self.SetSize(0, 0, 500, 350)
        self.text = wx.TextCtrl(
            self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.TE_RICH)# make the textbox
        self.logHandler = logHandler()
        # set the log message format
        self.logHandler.setFormatter(logging.Formatter(
            # One letter for level name
            '[{levelname[0]}] {module}.{funcName}(): {message}\n',
            style='{',
        ))
        logging.getLogger().addHandler(self.logHandler)


def init(master) -> None:
    """init the logwindow"""
    
    asyncio.run(logWindow(master))
    updateVisibility()


def toggleVisibility(placeHolder=None) -> None:
    global visible, window
    if not visible:
        visible = True
    else:
        visible = False
    updateVisibility()


def updateVisibility() -> None:
    global visible
    #save the visibility
    config.save(visible, "logWindowVisibility")
    if visible:
        window.ShowWithEffect(wx.SHOW_EFFECT_BLEND)
    else:
        window.HideWithEffect(wx.SHOW_EFFECT_BLEND)

def changeLevel(level: str) -> None:
    """change and saves the log level"""
    global window
    if level == "INFO":
        data = logging.INFO
    elif level == "WARNING":
        data = logging.WARNING
    elif level == "ERROR":
        data  = logging.ERROR
    else:
        data = logging.DEBUG
    config.save(level, "logLevel")
    window.logHandler.setLevel(data)



def getLevel() -> int:
    if "-dev" in utilities.argv:
        return logging.DEBUG
    # check for the level
    savedLevel = str(config.load("logLevel")).upper()
    if savedLevel == "INFO":
        level = logging.INFO
    elif savedLevel == "WARNING":
        level = logging.WARNING
    elif savedLevel == "ERROR":
        level = logging.ERROR
    else:
        level = logging.DEBUG
    return level
