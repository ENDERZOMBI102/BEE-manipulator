import json
import os
import sys
import traceback
from logging import Logger
from pathlib import Path
from sys import argv
from types import TracebackType
from typing import Type

import wx

import config
import localization
import srctools.logger
import timeTest
import utilities


class App(wx.App):

	instanceChecker = wx.SingleInstanceChecker('BM')
	root: 'root'
	logger: Logger
	ShouldRestart: bool = False
	ShouldExit: bool = False

	def OnPreInit(self):
		# check if there's another instance running
		if self.instanceChecker.IsAnotherRunning():
			wx.MessageBox(
				message='another instance of BM is running, aborting.',
				caption='Error!',
				style=wx.OK | wx.CENTRE | wx.STAY_ON_TOP | wx.ICON_ERROR
			)
			self.ShouldExit = True
			return False
		# initialize logging
		# use a window to show the uncaught exception to the user
		srctools.logger.init_logging( './logs/latest.log' if utilities.frozen() else './../logs/latest.log', on_error=self.OnError )
		self.logger = srctools.logger.get_logger('BEE Manipulator')
		# if we started with --dev parameter, set loglevel to debug
		if '--dev' in argv:
			config.overwrite('logLevel', 'DEBUG')
		config.overwrite('logWindowVisibility', True)
		config.overwrite('l18nFolderPath', './../langs')
		utilities.env = 'dev'
		# check configs
		self.logger.info('Checking config file..')
		if config.check():
			self.logger.info('Valid config file found!')
		else:
			self.logger.error('Invalid or inesistent config file detected!')
			self.logger.info('Creating new config file...')
			config.createConfig()
			self.logger.info('Config file created!')
		# populate the config dict
		config.currentConfigData = config.default_config
		with open( config.configPath, 'r' ) as file:
			for section, value in json.load( file ).items():
				config.currentConfigData[ section ] = value
		# start localizations
		localization.Localize()
		self.logger.info(f'current lang: {loc("currentLang")}')

	def OnInit(self):
		if self.ShouldExit:
			return False
		# create icon object
		utilities.__setIcon()
		# import after localize() object is created so that loc() is already present
		from uiWX import root
		# set app name
		self.logger.debug("setting application name..")
		self.SetAppName("BEE Manipulator")
		self.SetAppDisplayName("BEE Manipulator")
		self.logger.debug("setted app name")
		# start ui
		self.logger.info(f'Starting BEE Manipulator v{config.version}!')
		self.logger.info('starting ui!')
		# start the main loop
		root = root()
		root.Show()
		self.SetTopWindow(root)
		return True

	def OnExit(self):
		with open(config.configPath, 'w') as file:
			json.dump(config.currentConfigData, file, indent=4)
		if self.ShouldRestart:
			os.system(sys.executable)
		return 0

	def OnError( self, etype: Type[BaseException], value: BaseException, tb: TracebackType ):
		try:
			wx.MessageBox(
				message=''.join( traceback.format_exception(etype, value, tb) ),
				caption='BM Error!',
				style=wx.OK | wx.CENTRE | wx.STAY_ON_TOP | wx.ICON_ERROR
			)
		except Exception:
			wx.SafeShowMessage( title='BM Error!', text=''.join( traceback.format_exception(etype, value, tb) ) )
		if self.root is not None:
			self.root.Destroy()


if __name__ == '__main__':
	# use file dir as working dir
	path = Path(__file__).resolve()
	if utilities.frozen():
		print(f"BM exe path: {path.parent.resolve()}")
	else:
		print(f"BM source path: {path.parent}")
	os.chdir(path.parent)
	timeStartup = '--time' in argv
	if timeStartup:
		timeTest.start()
	app = App()
	if timeStartup:
		timeTest.stop()
	app.MainLoop()
