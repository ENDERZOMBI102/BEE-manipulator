import wx
from cefpython3 import cefpython as cef


class CefManager:

	_timer: wx.Timer

	def init( self ):
		cef.Initialize()
		cef.DpiAware.EnableHighDpiSupport()

		self._timer = wx.Timer()
		self._timer.Notify = lambda: cef.MessageLoopWork()
		self._timer.Start( 10 )  # 10ms timer

	def stop( self ):
		self._timer.Stop()
		cef.Shutdown()


manager: CefManager = CefManager()
