import wx
from cefpython3 import cefpython as cef

import utilities


class CefManager:

	_timer: wx.Timer

	def init( self ):
		cef.Initialize(
			dict(
				cache_path='',
				user_agent='BEEManipulator',
				persist_user_preferences=False,
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

	def stop( self ):
		self._timer.Stop()
		cef.Shutdown()


manager: CefManager = CefManager()
