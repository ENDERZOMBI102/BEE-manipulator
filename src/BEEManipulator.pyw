import json
import logging
import os
import sys
import traceback
from logging import Logger
from pathlib import Path
from types import TracebackType
from typing import Type

import wx

import cefManager
import config  # must be second import
import downloadManager
import ipc
import localization
import srctools.logger
import timeTest
import utilities
from cli import parsedArguments  # must be first import


class WxLogHandler( wx.Log ):
	"""Handle WX logging, and redirect it to Python's log system."""

	# lookup table to convert WX log levels to stdlib equivalents.
	levelLookupTable = {
		wx.LOG_Debug: logging.DEBUG,
		wx.LOG_Error: logging.ERROR,
		wx.LOG_FatalError: logging.FATAL,
		wx.LOG_Info: logging.INFO,
		wx.LOG_Max: logging.DEBUG,
		wx.LOG_Message: logging.INFO,
		wx.LOG_Progress: logging.DEBUG,
		wx.LOG_Status: logging.INFO,
		wx.LOG_Trace: logging.DEBUG,
		wx.LOG_User: logging.DEBUG,
		wx.LOG_Warning: logging.WARNING,
	}

	def __init__( self ) -> None:
		super().__init__()
		self.logger: logging.Logger = logging.getLogger( 'wxPython' )

	def DoLogRecord( self, level: int, msg: str, info: wx.LogRecordInfo ) -> None:
		"""Pass the WX log system into the Python system."""
		# Filename and function name are bytes, ew.
		self.logger.handle(
			self.logger.makeRecord(
				'wxPython',
				self.levelLookupTable.get( level, logging.INFO ),
				info.filename.decode( 'utf8', 'ignore' ),
				info.line,
				msg,
				(),  # It's already been formatted so no args are needed.
				None,  # Exception info, not compatible.
				info.func.decode( 'utf8', 'ignore' ),
			)
		)


class App( wx.App ):
	instanceChecker = wx.SingleInstanceChecker( 'BM' )
	root: 'root'
	logger: Logger
	ShouldRestart: bool = False
	ShouldExit: bool = False

	def OnPreInit( self ):
		# check if there's another instance running
		if self.instanceChecker.IsAnotherRunning():
			if parsedArguments.bmurl is not None:
				ipc.sendToServer( ('127.0.0.1', 30206), parsedArguments.bmurl )
			else:
				wx.MessageBox(
					message='Another instance of BEE Manipulator is running, aborting.',
					caption='Error!',
					style=wx.OK | wx.CENTRE | wx.STAY_ON_TOP | wx.ICON_ERROR
				)
			self.ShouldExit = True
			return
		# initialize logging
		# overwrite stdout log level if on launched from source
		if not utilities.frozen():
			os.environ[ 'SRCTOOLS_DEBUG' ] = '1'
		# use a window to show the uncaught exception to the user
		self.logger = srctools.logger.init_logging(
			filename='./logs/latest.log',
			main_logger='BEE Manipulator',
			on_error=self.OnError
		)
		# log wx logging to python's logging module
		wx.Log.SetActiveTarget( WxLogHandler() )
		# if we started with --dev parameter, set loglevel to debug
		if parsedArguments.dev:
			config.overwrite( 'logLevel', 'DEBUG' )
			config.overwrite( 'logWindowVisibility', True )
			utilities.devEnv = True
		if parsedArguments.flags is not None:
			# add all flags
			config.dynConfig.parseFlags( parsedArguments.flags )
		# check configs
		self.logger.info( 'Checking config file..' )
		if config.check():
			self.logger.info( 'Valid config file found!' )
		else:
			self.logger.error( 'Invalid or inesistent config file detected!' )
			self.logger.info( 'Creating new config file...' )
			config.createConfig()
			self.logger.info( 'Config file created!' )
		# populate the config dict
		config.currentConfigData = config.default_config
		with open( config.configPath, 'r' ) as file:
			for section, value in json.load( file ).items():
				if section != 'nextLaunch':
					config.currentConfigData[ section ] = value
				else:
					if len( value.keys() ) > 0:
						self.logger.info( 'Seems that we may have crashed last time, lets overwrite things!' )
						config.currentConfigData = {**config.currentConfigData, **value}
					else:
						self.logger.info( 'Nothing to overwrite for this launch!' )
					config.currentConfigData[ 'nextLaunch' ] = {}
		# start localizations
		localization.Localize()
		self.logger.info( f'current lang: {loc( "currentLang" )}' )

	def OnInit( self ):
		if self.ShouldExit:
			return False
		# create all folders
		for folder in ( config.load('cachePath') ):
			Path( folder ).mkdir(exist_ok=True)
		# init locale
		wx.Locale()
		# initialize various things
		utilities.init()
		# initialize modules
		cefManager.manager.init()
		downloadManager.manager.init()
		ipc.manager.init()
		# import after localize() object is created so that loc() is already present
		from uiWX import root
		# set app name
		self.logger.debug( "setting application name.." )
		self.SetAppName( "BEE Manipulator" )
		self.SetAppDisplayName( "BEE Manipulator" )
		self.logger.info( "setted app name" )
		# start ui
		self.logger.info( f'Starting BEE Manipulator v{config.version}!' )
		self.logger.info( 'starting ui!' )
		# start the main loop
		root = root()
		self.SetTopWindow( root )
		root.Show()
		return True

	def OnExit( self ):
		import logging
		# shutdown modules
		ipc.manager.stop()
		downloadManager.manager.stop()
		cefManager.manager.stop()
		with open( config.configPath, 'w' ) as file:
			json.dump( config.currentConfigData, file, indent=4 )
		if config.dynConfig[ 'continueLoggingOnUncaughtException' ]:
			logging.shutdown()
		if self.ShouldRestart:
			os.system( sys.executable )
		return 0

	def OnError( self, etype: Type[ BaseException ], value: BaseException, tb: TracebackType ):
		# in an errored state, wx.MessageBox may not be available, so in case, use wx.SafeShowMessage
		try:
			wx.MessageBox(
				message=''.join( traceback.format_exception( etype, value, tb ) ),
				caption='BM Error!',
				style=wx.OK | wx.CENTRE | wx.STAY_ON_TOP | wx.ICON_ERROR
			)
		except Exception:
			wx.SafeShowMessage( title='BM Error!', text=''.join( traceback.format_exception( etype, value, tb ) ) )
		# try to set logWindowVisibility to True for next time, if it fails, its not a big deal
		try:
			config.overwriteOnNextLaunch( logWindowVisibility=True )
		except Exception:
			pass
		try:
			if self.root is not None:
				self.root.Destroy()
		except AttributeError:
			# the root ui has already been destroyed
			pass


if __name__ == '__main__':
	print( f'BM is running in a {"packed" if utilities.frozen() else "developer"} enviroment.' )
	if sys.platform.startswith( 'win' ):
		import locale
		locale.setlocale( locale.LC_ALL, 'C' )
	timeTest.start()
	app = App()
	if parsedArguments.time:
		timeTest.stop()
	app.MainLoop()
