import logging

import wx

visible: bool
logger: logging.Logger
LogLevel = int


class LogHandler(logging.Handler):
	"""
	this class represents the log handler, this will
	receive, format and send the log message to the window
	using the same BEE2.4 log format people are familiar with
	"""

	def emit(self, record: logging.LogRecord) -> None:
		"""
		receive, format, colorize and display a log message
		:param record: logging.LogRecord object
		"""


class LogWindow(wx.Frame):

	instance: 'LogWindow'
	text: wx.TextCtrl
	logHandler: LogHandler

	bottomBar: wx.Panel
	levelChoice: wx.Choice

	def OnClearButtonPressed(self, evt: wx.CommandEvent):
		""" Called when the clear button is pressed """

	def OnLevelChoice( self, evt: wx.CommandEvent ):
		""" Called when the level is changed using the dropdown menu """


def toggleVisibility() -> None:
	""" A function that toggles the visibility of the window """


def updateVisibility() -> None:
	"""	Actually _update and save the log window visibility """


def changeLevel(level: str) -> None:
	"""
	changes and saves the log level that shows on the window
	:param level: level to set the window to
	"""


def getLevel() -> LogLevel:
	"""
	gets the level form the config file
	:return: log level
	"""
