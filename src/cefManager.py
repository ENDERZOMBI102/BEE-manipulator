import wx
from cefpython3 import cefpython as cef

import config
import utilities
from srctools.logger import get_logger

LOGGER = get_logger()


class CefManager:

	_timer: wx.Timer

	def init( self ):
		LOGGER.info('initializing cefPython!')
		cef.Initialize(
			settings=dict(
				cache_path='',
				product_version=config.version.__str__(),
				user_agent='BEEManipulator',
				persist_user_preferences=False,
				downloads_enabled=True,
				debug=utilities.devEnv,
				log_file='./logs/cef.log' if utilities.frozen() else './../logs/cef.log',
				context_menu={
					'devtools': utilities.devEnv,
					'view_source': utilities.devEnv,
					'navigation': utilities.devEnv,
					'print': False,
					'external_browser': False
				}
			)
		)
		cef.DpiAware.EnableHighDpiSupport()

		self._timer = wx.Timer()
		self._timer.Notify = lambda: cef.MessageLoopWork()
		self._timer.Start( 10 )  # 10ms timer
		LOGGER.info('cefPython initialized!')

	def stop( self ):
		self._timer.Stop()
		cef.Shutdown()


manager: CefManager = CefManager()
