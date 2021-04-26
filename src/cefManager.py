import logging
from typing import Dict

import wx
from cefpython3 import cefpython as cef

import config
import utilities
from api.manager import Manager
from srctools.logger import get_logger

LOGGER = get_logger()


class CefManager(Manager):

	_timer: wx.Timer

	def init( self ):
		LOGGER.info('initializing cefPython!')
		cef.Initialize(
			settings=dict(
				cache_path=utilities.getCorrectPath( './resources/cache' ),
				product_version=config.version.__str__(),
				user_agent='BEEManipulator',
				persist_user_preferences=False,
				uncaught_exception_stack_size=4,
				downloads_enabled=True,
				debug=utilities.devEnv,
				remote_debugging_port=58198,
				log_severity=cef.LOGSEVERITY_VERBOSE if utilities.devEnv else cef.LOGSEVERITY_INFO,
				log_file=utilities.getCorrectPath( './logs/cef.log' ),
				context_menu={
					'devtools': False,
					'view_source': utilities.devEnv,
					'navigation': utilities.devEnv,
					'print': False,
					'external_browser': False
				}
			)
		)
		cef.DpiAware.EnableHighDpiSupport()
		cef.SetGlobalClientHandler( _GlobalHandler() )
		cef.CookieManager.GetGlobalManager().SetStoragePath( utilities.getCorrectPath('./resources/cache') )

		self._timer = wx.Timer()
		self._timer.Notify = lambda: cef.MessageLoopWork()
		self._timer.Start( 10 )  # 10ms timer
		LOGGER.info('cefPython initialized!')

	def stop( self ):
		self._timer.Stop()
		cef.Shutdown()


class _GlobalHandler:

	displayHandler: '_ClientHandler'

	def __init__(self):
		self.displayHandler = _ClientHandler()

	def OnAfterCreated(self, browser: cef.PyBrowser, **kwargs):
		""" Called after a new browser is created. """
		LOGGER.debug(f'A browser widget was created, id: {browser.GetIdentifier()}')
		browser.SetClientHandler( self.displayHandler )


class _ClientHandler:

	levelLookupTable: Dict[ int, int ] = {
		cef.LOGSEVERITY_VERBOSE: logging.DEBUG,
		cef.LOGSEVERITY_INFO: logging.INFO,
		cef.LOGSEVERITY_WARNING: logging.WARNING,
		cef.LOGSEVERITY_ERROR: logging.ERROR,
		cef.LOGSEVERITY_DISABLE: logging.FATAL
	}

	def OnConsoleMessage( self, browser: cef.PyBrowser, level: int, message: str, source: str, line: int ) -> bool:
		""" Called to display a console message. """
		filename = source.split('/')[-1] if len( source ) > 0 else 'devtools'
		function = 'unknown' if len( source ) > 0 else 'console'
		LOGGER.handle(
			LOGGER.makeRecord(
				name='cefPython',
				level=self.levelLookupTable[ level ],
				fn=filename,
				lno=line,
				msg=message,
				args=(),  # It's already been formatted so no args are needed.
				exc_info=None,  # Exception info, not compatible.
				func=function
			)
		)
		return False


manager: CefManager = CefManager()
