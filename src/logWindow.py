import logging

import wx

import config
import srctools.logger
import utilities
from pluginSystem import eventHandlerObj

# the visibility of the log window, is initially setted to the value saved in the config file

visible: bool = config.load('logWindowVisibility')
window = None  # then converted to wx.Frame
logger = srctools.logger.get_logger()


class logHandler(logging.Handler):
    """
    this class rappresents the log handler, this will
    recive, format and send the log message to the window
    using the same BEE2.4 log format people are familiar with
    """
    def __init__(self):
        logger.debug('initialised log handler with level NOTSET')
        super().__init__(logging.NOTSET)
        self.setLevel(logging.NOTSET)

    def emit(self, record: logging.LogRecord):
        """
        receive, format, colorize and display a log message
        """
        global window
        if record.levelno == logging.INFO:
            window.text.SetDefaultStyle(wx.TextAttr(wx.Colour(0, 80, 255)))  # blue/cyan
        #
        elif record.levelno == logging.WARNING:
            window.text.SetDefaultStyle(wx.TextAttr(wx.Colour(255, 125, 0)))  # orange
        #
        elif record.levelno == logging.ERROR:
            window.text.SetDefaultStyle(wx.TextAttr(wx.Colour(255, 0, 0)))  # red
        #
        elif record.levelno == logging.DEBUG:
            window.text.SetDefaultStyle(wx.TextAttr(wx.Colour(128, 128, 128)))  # grey
        #
        elif record.levelno == logging.CRITICAL:
            window.text.SetDefaultStyle(wx.TextAttr(wx.Colour(255, 255, 255)))  # white
        # display the log message
        window.text.AppendText(self.format(record))


class logWindow(wx.Frame):
    """
    this class make the log window and the log handler
    """
    def __init__(self):
        super().__init__(
                            wx.GetTopLevelWindows()[0],  # parent
                            title='Logs',  # window title
                            style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER  # to make the window not resizeable
                        )  # init the window
        global window
        window = self
        self.SetIcon( utilities.icon )
        self.SetSize(0, 0, 500, 365)
        sizer = wx.FlexGridSizer(rows=2, cols=1, gap=wx.Size(0, 0))
        try:
            pos = config.load('logWindowPos')
            self.SetPosition( wx.Point(pos) )
        except config.ConfigError as e:
            pass
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
        self.bottomBar = wx.Panel(self, size=wx.Size(500, 25))  # makes the bottom "menu" bar
        BBsizer = wx.GridBagSizer()
        self.clearBtn = wx.Button(  # makes the clear button
            self.bottomBar,
            label='Clear',
            size=wx.Size(50, 20)
        )
        BBsizer.Add(  # add the clear button to the sizer
            self.clearBtn,
            wx.GBPosition(0, 1)
        )
        self.bottomBar.SetSizer(BBsizer)
        sizer.Add(self.text, border=wx.Bottom)
        sizer.Add(self.bottomBar)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_CLOSE, self.OnClose, self)
        self.Bind(wx.EVT_MOVE_END, self.OnMoveEnd, self)
        self.Bind(wx.EVT_BUTTON, self.OnClearButtonPressed, self.clearBtn)
        eventHandlerObj.send('logWindowObject', object=self)
        updateVisibility()

    def OnClearButtonPressed(self, event):
        self.text.Clear()

    @staticmethod
    def OnClose(event):
        logger.debug('hided log window')
        toggleVisibility()

    def OnMoveEnd(self, event):
        # get the window position as wx.Point and convert it to list
        pos = list(self.GetPosition().Get())
        logger.debug(f'saved logwindow position: {pos}')
        config.save(pos, 'logWindowPos')
            

async def init() -> None:

    """
    a function that initiate the log window
    :return:
    """
    logWindow()


def toggleVisibility(placeHolder=None):

    """
    a function that toggles the visibility of the window
    :param placeHolder:
    :return:
    """
    global visible, window
    if not visible:
        visible = True
    else:
        visible = False
    updateVisibility()


def updateVisibility():
    global visible
    # save the visibility
    config.save(visible, 'logWindowVisibility')
    logger.debug('saved window visibility')
    if visible:
        window.ShowWithEffect(wx.SHOW_EFFECT_BLEND)
        window.Raise()
        wx.GetTopLevelWindows()[0].Raise()
    else:
        window.HideWithEffect(wx.SHOW_EFFECT_BLEND)


def changeLevel(level: str) -> None:

    """
    changes and saves the log level that shows on the window
    :param level: level to set the window to
    :return: none
    """
    global window
    level = level.upper()
    if level == 'INFO':
        data = logging.INFO
    elif level == 'WARNING':
        data = logging.WARNING
    elif level == 'ERROR':
        data = logging.ERROR
    else:
        data = logging.DEBUG
    logger.info(f'changed log level to {level}')
    logger.info(f'saved log level {level} to config')
    config.save(level, 'logLevel')
    window.logHandler.setLevel(data)


def getLevel() -> int:

    """
    gets the level form the config file
    :return: log level
    """
    # check for the level
    savedLevel = str( config.load('logLevel') ).upper()
    logger.info(f'loaded log level {savedLevel} from config!')
    if savedLevel == 'INFO':
        level = logging.INFO
    elif savedLevel == 'WARNING':
        level = logging.WARNING
    elif savedLevel == 'ERROR':
        level = logging.ERROR
    else:
        level = logging.DEBUG
    return level
