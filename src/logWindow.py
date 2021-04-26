import logging

import wx
import wx.py.dispatcher as dispatcher

import config
import srctools.logger
import utilities
from pluginSystem import Events
from utilities import wxStyles

if __name__ == '__main':
	pass

# the visibility of the log window, is initially setted to the value saved in the config file

visible: bool = config.load('logWindowVisibility')
logger = srctools.logger.get_logger()


class LogHandler( logging.Handler ):
	"""
	this class represents the log handler, this will
	receive, format and send the log message to the window
	using the same BEE2.4 log format people are familiar with
	"""
	def __init__(self, wxDest=None):
		logger.debug(f'initialised log handler with level NOTSET')
		super().__init__(logging.NOTSET)
		self.setLevel(logging.NOTSET)

	def emit(self, record: logging.LogRecord):
		"""
		receive, format, colorize and display a log message
		:param record: logging.LogRecord object
		"""

		if record.levelno == logging.INFO:
			LogWindow.instance.text.SetDefaultStyle( wx.TextAttr( wx.Colour( 0, 80, 255 ) ) )  # blue/cyan
		#
		elif record.levelno == logging.WARNING:
			LogWindow.instance.text.SetDefaultStyle( wx.TextAttr( wx.Colour( 255, 125, 0 ) ) )  # orange
		#
		elif record.levelno == logging.ERROR:
			LogWindow.instance.text.SetDefaultStyle( wx.TextAttr( wx.Colour( 255, 0, 0 ) ) )  # red
		#
		elif record.levelno == logging.DEBUG:
			LogWindow.instance.text.SetDefaultStyle( wx.TextAttr( wx.Colour( 128, 128, 128 ) ) )  # grey
		#
		elif record.levelno == logging.CRITICAL:
			LogWindow.instance.text.SetDefaultStyle( wx.TextAttr( wx.Colour( 255, 255, 255 ) ) )  # white
		# display the log message
		LogWindow.instance.text.AppendText( self.format( record ) )


class LogWindow( wx.Frame ):

	instance: 'LogWindow' = None

	def __init__(self):
		super().__init__(
			wx.GetTopLevelWindows()[0],  # parent
			title=f'Logs - {str(config.version)}',  # window title
			# those styles make so that the window can't minimize, maximize, resize and show on the taskbar
			style=wx.FRAME_NO_TASKBAR | wxStyles.TITLEBAR_ONLY_BUTTON_CLOSE ^ wx.RESIZE_BORDER
		)  # init the window
		LogWindow.instance = self
		self.SetIcon( utilities.icon )
		self.SetSize(0, 0, 500, 365)
		sizer = wx.FlexGridSizer( rows=2, cols=1, gap=wx.Size(0, 0) )
		try:
			pos = config.load('logWindowPos')
			if pos is not None:
				self.SetPosition( wx.Point( pos ) )
			else:
				self.SetPosition( wx.Point( 100, 100 ) )
		except config.ConfigError as e:
			logger.warning(e)  # not a problem if it fails
		self.text = wx.TextCtrl(
			self,
			style=wx.TE_MULTILINE | wx.TE_READONLY | wx.VSCROLL | wx.TE_RICH,
			size=wx.Size( self.GetSize()[0], 300 )
		)  # make the textbox
		self.logHandler = LogHandler()
		# set the log message format
		self.logHandler.setFormatter(
			logging.Formatter(
				# One letter for level name
				'[{levelname[0]}] {module}.{funcName}(): {message}\n',
				style='{',
			)
		)
		self.logHandler.setLevel(getLevel())
		logging.getLogger().addHandler(self.logHandler)
		# create bottom bar
		self.bottomBar = wx.Panel( self, size=wx.Size( self.GetSize()[0], 30) )  # makes the bottom "menu" bar
		self.clearBtn = wx.Button(  # makes the clear button
			self.bottomBar,
			label='Clear',
			size=wx.Size(52, 22),
			pos=wx.Point(10, 3)
		)
		self.levelChoice = wx.Choice(
			parent=self.bottomBar,
			size=wx.Size(80, 22),
			pos=wx.Point(self.GetSize()[0]-100, 3),
			choices=['Debug', 'Info', 'Warning', 'Error']
		)
		self.levelChoice.SetSelection( ( getLevel() / 10 ) - 1 )
		self.levelChoice.Refresh()
		sizer.Add(self.text, border=wx.Bottom)
		sizer.Add(self.bottomBar)
		self.SetSizer(sizer)
		self.Bind( wx.EVT_CLOSE, self.OnClose, self )
		self.Bind( wx.EVT_MOVE_END, self.OnMoveEnd, self )
		self.Bind( wx.EVT_BUTTON, self.OnClearButtonPressed, self.clearBtn )
		self.Bind( wx.EVT_CHOICE, self.OnLevelChoice, self.levelChoice )
		dispatcher.send(Events.LogWindowCreated, window=self)
		updateVisibility()
		self.levelChoice.Refresh()

	def OnClearButtonPressed(self, evt: wx.CommandEvent):
		self.text.Clear()

	def OnLevelChoice( self, evt: wx.CommandEvent ):
		if evt.GetSelection() == 0:
			changeLevel('debug')
		elif evt.GetSelection() == 1:
			changeLevel('info')
		elif evt.GetSelection() == 2:
			changeLevel('warning')
		else:
			changeLevel('error')

	@staticmethod
	def OnClose(evt: wx.CloseEvent):
		logger.debug(f'hidden log window')
		toggleVisibility()

	def OnMoveEnd(self, evt: wx.Event):
		# get the window position as wx.Point and convert it to list
		pos = list(self.GetPosition().Get())
		logger.debug(f'saved logwindow position: {pos}')
		config.save(pos, 'logWindowPos')

	def __del__(self):
		logger.removeHandler(self.logHandler)


async def init() -> None:

	"""
	a function that initiate the log window
	"""
	LogWindow()


def toggleVisibility(placeHolder=None):

	"""
	a function that toggles the visibility of the window
	:param placeHolder:
	"""
	global visible
	if not visible:
		visible = True
	else:
		visible = False
	updateVisibility()


def updateVisibility():
	"""
	actually _update and save the log window visibility
	"""
	global visible
	# save the visibility
	config.save(visible, 'logWindowVisibility')
	logger.debug(f'saved window visibility')
	if visible:
		LogWindow.instance.Raise()
		LogWindow.instance.ShowWithEffect( wx.SHOW_EFFECT_BLEND )
		LogWindow.instance.levelChoice.Refresh()
		wx.GetTopLevelWindows()[0].Raise()
	else:
		LogWindow.instance.HideWithEffect( wx.SHOW_EFFECT_BLEND )


def changeLevel(level: str) -> None:
	"""
	changes and saves the log level that shows on the window
	:param level: level to set the window to
	"""
	if level == 'info':
		data = logging.INFO
	elif level == 'warning':
		data = logging.WARNING
	elif level == 'error':
		data = logging.ERROR
	else:
		data = logging.DEBUG
	logger.info(f'changed log level to {level}')
	logger.info(f'saved log level {level} to config')
	config.save(level, 'logLevel')
	LogWindow.instance.logHandler.setLevel( data )


def getLevel() -> int:
	"""
	gets the level form the config file
	:return: log level
	"""
	# check for the level
	savedLevel = str( config.load("logLevel") ).lower()
	logger.info(f'loaded log level {savedLevel} from config!')
	if savedLevel == "info":
		level = logging.INFO
	elif savedLevel == "warning":
		level = logging.WARNING
	elif savedLevel == "error":
		level = logging.ERROR
	else:
		level = logging.DEBUG
	return level
