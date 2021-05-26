import logging
from typing import Dict

import wx
from cefpython3 import cefpython as cef

import config
import utilities
from api.manager import Manager
from srctools.logger import get_logger

LOGGER = get_logger()


class BrowserPanel(wx.Panel):

	webView: cef.PyBrowser

	def __init__(
			self,
			parent: wx.Window,
			url: str,
			name: str = '',
			pos: wx.Point = wx.DefaultPosition,
			size: wx.Size = wx.DefaultSize,
			style: int = 0
	):
		super( BrowserPanel, self ).__init__(
			parent=parent,
			name=name,
			pos=pos,
			size=size,
			style=wx.WANTS_CHARS | style
		)

		# setup the webview
		window_info = cef.WindowInfo()
		width, height = self.GetClientSize().Get()
		assert self.GetHandle(), 'Window handle not available'
		window_info.SetAsChild( self.GetHandle(), [ 0, 0, width, height ] )

		# setup the browser
		self.webView = cef.CreateBrowserSync(
			window_info,
			url=url
		)
		self.webView.SetClientHandler( self.V8ContextHandler() )

		self.Bind( wx.EVT_SET_FOCUS, self.OnSetFocus, self )
		self.Bind( wx.EVT_SIZE, self.OnSize, self )

	def OnSetFocus( self, evt ):
		if not self.webView:
			return
		cef.WindowUtils.OnSetFocus( self.GetHandle(), 0, 0, 0 )
		self.webView.SetFocus( True )

	def OnSize( self, evt ):
		if not self.webView:
			return
		cef.WindowUtils.OnSize( self.GetHandle(), 0, 0, 0 )
		self.webView.NotifyMoveOrResizeStarted()

	def __del__( self ):
		if not self.webView:
			return
		self.webView.ParentWindowWillClose()
		self.browser = None

	class V8ContextHandler:

		def OnContextCreated( self, browser: cef.PyBrowser, frame: cef.PyFrame ) -> None:
			browser.ExecuteJavascript(
				jsCode="""
				String.prototype.replaceAll = function(oldChar, newChar) {
					return this.replace( new RegExp(oldChar, "g"), newChar )
				}
				"""
			)


class CefManager(Manager):

	_timer: wx.Timer

	def init( self ):
		LOGGER.info('initializing cefPython!')
		if utilities.devEnv and not config.dynConfig['noCefLog']:
			logLevel = cef.LOGSEVERITY_VERBOSE
		else:
			logLevel = cef.LOGSEVERITY_INFO
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
				log_severity=logLevel,
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
