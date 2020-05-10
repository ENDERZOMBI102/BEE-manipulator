import utilities
import config
import logging
import wx
import webbrowser as wb
import srctools.logger


# the visibility of the log window, is initially setted to the value saved in the config file
visible: bool = config.load("logWindowVisibility")
window = None # then converted to wx.Frame
logger = srctools.logger.get_logger()


class logHandler(logging.Handler):
    """
    this class rappresents the log handler, this will
    recive, format and send the log message to the window
    using the same BEE2.4 log format people are familiar with
    """
    def __init__(self, wxDest=None):
        logger.debug(f'initialised log handler with level NOTSET')
        super().__init__(logging.NOTSET)
        self.setLevel(logging.NOTSET)

    def emit(self, record: logging.LogRecord):
        """
        recive, format, colorize and display a log message
        """
        global window
        if record.levelno == logging.INFO:
            window.text.SetDefaultStyle(wx.TextAttr(wx.Colour(0, 80, 255)))# blue/cyan
        #
        elif record.levelno == logging.WARNING:
            window.text.SetDefaultStyle(wx.TextAttr(wx.Colour(255, 125, 0)))# orange
        #
        elif record.levelno == logging.ERROR:
            window.text.SetDefaultStyle(wx.TextAttr(wx.Colour(255, 0, 0)))# red
        #
        elif record.levelno == logging.DEBUG:
            window.text.SetDefaultStyle(wx.TextAttr(wx.Colour(128, 128, 128)))# grey
        #
        elif record.levelno == logging.CRITICAL:
            window.text.SetDefaultStyle(wx.TextAttr(wx.Colour(255, 255, 255)))# white
        #display the log message
        window.text.AppendText(self.format(record))


class logWindow(wx.Frame):
    """
    this class make the log window and the log handler
    """
    def __init__(self, master):
        super().__init__(
                            master, # parent
                            title="Logs", #window title
                            style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER # to meake the window unresizaeble
                        )  # init the window
        global window
        window = self
        self.SetIcon(wx.Icon('./assets/icon.ico'))
        self.SetSize(0, 0, 500, 365)
        sizer = wx.FlexGridSizer(rows=2, cols=1, gap=wx.Size(0, 0))
        try: self.SetPosition(wx.Point(config.load("logWindowPos")))
        except: pass# not a problem if it fails
        self.text = wx.TextCtrl(
            self,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.VSCROLL | wx.TE_RICH,
            size=wx.Size(self.GetSize()[0], 300)
        )  # make the textbox
        self.logHandler = logHandler()
        # set the log message format
        self.logHandler.setFormatter(logging.Formatter(
            # One letter for level name
            '[{levelname[0]}] {module}.{funcName}(): {message}\n',
            style='{',
        ))
        self.logHandler.setLevel(getLevel())
        logging.getLogger().addHandler(self.logHandler)
        # create bottom bar
        self.bottomBar = wx.Panel(self, size=wx.Size(self.GetSize()[0], 25))# makes the bottom "menu" bar
        BBsizer = wx.GridBagSizer()
        self.clearBtn = wx.Button(# makes the clear button
            self.bottomBar,
            label='Clear',
            size=wx.Size(50, 20)
        )
        BBsizer.Add( # add the clear button to the sizer
            self.clearBtn,
            wx.GBPosition(0, 1)
        )
        self.copyBtn = wx.Button(# makes the copy button
            self.bottomBar,
            label='Copy',
            size=wx.Size(50, 20)
        )
        BBsizer.Add( # add the cpoy button to the sizer
            self.copyBtn,
            wx.GBPosition(0, 3)
        )
        self.levelMenu = wx.Menu( 'Info' )
        info = self.levelMenu.Append(wx.ID_ANY, 'Info')
        warn = self.levelMenu.Append(wx.ID_ANY, 'Warning')
        debug = self.levelMenu.Append(wx.ID_ANY, 'Debug')
        levelMenuButton = wx.Button(self.bottomBar, label= '', size=wx.Size(20, 20))
        BBsizer.Add( # add the cpoy button to the sizer
            levelMenuButton,
            wx.GBPosition(0, 40)
        )
        self.bottomBar.SetSizer(BBsizer)
        sizer.Add(self.text, border=wx.Bottom)
        sizer.Add(self.bottomBar)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_CLOSE, self.OnClose, self)
        self.Bind(wx.EVT_MOVE_END, self.OnMoveEnd, self)
        self.Bind(wx.EVT_MENU, self.changeLevel, self)
        updateVisibility()

    def OnClose(self, event):
        logger.debug(f'hided log window')
        toggleVisibility()

    def OnMoveEnd(self, event):
        # get the window posistion as wx.Point and convert it to list
        pos = list(self.GetPosition().Get())
        logger.debug(f'saved logwindow position: {pos}')
        config.save(pos, 'logWindowPos')

    def changeLevel(self, event: wx.EVT_MENU):
        print(event)
        

async def init(master) -> None:
    """init the logwindow"""
    logWindow(master)    


def toggleVisibility(placeHolder=None):
    global visible, window
    if not visible:
        visible = True
    else:
        visible = False
    updateVisibility()


def updateVisibility():
    global visible
    #save the visibility
    config.save(visible, "logWindowVisibility")
    logger.debug(f'saved window visibility')
    if visible:
        window.ShowWithEffect(wx.SHOW_EFFECT_BLEND)
    else:
        window.HideWithEffect(wx.SHOW_EFFECT_BLEND)

def changeLevel(level: str) -> None:
    """change and saves the log level"""
    global window
    level = level.upper()
    if level == "INFO":
        data = logging.INFO
    elif level == "WARNING":
        data = logging.WARNING
    elif level == "ERROR":
        data  = logging.ERROR
    else:
        data = logging.DEBUG
    logger.info(f'changed log level to {level}')
    logger.info(f'saved log level {level} to config')
    config.save(level, "logLevel")
    window.logHandler.setLevel(data)



def getLevel() -> int:
    if "-logDebug" in utilities.argv:
        return logging.DEBUG
    # check for the level
    savedLevel = str(config.load("logLevel")).upper()
    logger.info(f'loaded log level {savedLevel} from config!')
    if savedLevel == "INFO":
        level = logging.INFO
    elif savedLevel == "WARNING":
        level = logging.WARNING
    elif savedLevel == "ERROR":
        level = logging.ERROR
    else:
        level = logging.DEBUG
    return logging.DEBUG#level
