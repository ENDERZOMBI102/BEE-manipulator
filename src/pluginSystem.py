import asyncio
import importlib.util
import traceback
from abc import ABCMeta, abstractmethod
from enum import Enum
from multiprocessing.connection import PipeConnection
from pathlib import Path
from types import ModuleType
from typing import Dict, Callable

import wx
from semver import VersionInfo
from wx.py import dispatcher

import config
import ipc
from srctools.logger import get_logger

logger = get_logger()


class Events(Enum):

	RegisterEvent = 'RegisterMenusEvent'
	LogWindowCreated = 'LogWindowEvent'
	UnregisterMenu = 'UnregisterMenuEvent'
	DownloadCompleted = 'DownloadCompletedEvent'
	DownloadStarted = 'DownloadStartedEvent'
	UnregisterIpcHandler = 'UnregisterIpcHandlerEvent'
	UnregisterBookPage = 'UnregisterBookPage'
	ReloadModuleEvent = 'ReloadModuleEvent'


class Errors:

	class PageNotFoundException(Exception):
		pass

	class MenuNotFoundException(Exception):
		pass

	class DupeMenuFoundException(RuntimeError):
		pass


class RegisterHandler:

	_mainWindow = None
	_ipcManager: ipc.ipcManager = None
	"""PRIVATE ATTRIBUTE"""

	def __init__(self):
		import uiWX
		self._mainWindow: 'uiWX.root'
		self._mainWindow = uiWX.root.instance
		self._ipcManager = ipc.manager

	def RegisterMenu( self, menu: wx.Menu, title: str):
		index = self._mainWindow.menuBar.FindMenu(title)
		if index == wx.NOT_FOUND:
			self._mainWindow.menuBar.Append( menu, title )
		else:
			raise Errors.DupeMenuFoundException(f'duplicate menu "{menu.GetTitle()}"')

	def RegisterIpcHandler( self, protocol: str, hdlr: Callable[ [ PipeConnection, ipc.Command ], None ] ):
		self._ipcManager.addHandler(protocol, hdlr)

	def RegisterBookPage( self, page: wx.Panel, title: str ):
		if page.GetParent() != self._mainWindow.book:
			logger.error(f'page parent isnt the main book')
		else:
			self._mainWindow.book.AddPage(page, title)


class Plugin:
	"""
	this decorator is used to create a plugin for BEE Manipulator
	"""
	def __init__(self, name: str, version: VersionInfo = None, pluginid: str = None ):
		self.name = name
		self.version = version
		self.pluginid = pluginid

	def __call__( self, cls ):
		# make a subclass to check for methods
		class WrappedPlugin(cls):
			__state__ = 'unloaded'
			version: VersionInfo = self.version
			name: str = self.name

			def getPath(self) -> Path:
				return Path( systemObj.modules[ self.__class__.__base__.__module__ ].__file__ ).resolve()

			def getName( self ) -> str:
				return self.name

			def getVersion( self ) -> VersionInfo:
				return self.version

		# a plugin's ID is the name of the class
		if self.pluginid is None:
			self.pluginid = WrappedPlugin.__base__.__name__

		logger.debug(f'instantiated plugin "{self.pluginid}" from {WrappedPlugin.__base__.__module__}.py')
		# checks if the plugin has the NEEDED methods
		# load
		if not asyncio.iscoroutinefunction( getattr( WrappedPlugin, 'load', Callable ) ):
			raise PluginNotValid('missing required coroutine "load"!')
		# unload
		if not asyncio.iscoroutinefunction( getattr( WrappedPlugin, 'unload', Callable ) ):
			raise PluginNotValid('missing required coroutine "unload"!')

		# reload
		# check reload only if its present
		if getattr(WrappedPlugin, 'reload', None) is not None:
			# reload check
			if not asyncio.iscoroutinefunction( WrappedPlugin.reload ):
				# its not a coroutine, raise an error
				err = PluginNotValid('the "reload" method should be a coroutine')
				# set the plugin id in the exception
				err.pluginid = self.pluginid
				raise err
		# check if another plugin already registered itself with this plugin's ID
		if self.pluginid in systemObj.plugins.keys():
			if not systemObj.isReloading:
				logger.error(f'Duplicate plugin found! id: {self.pluginid}, duplicate name: {self.name}')
				# only load the most recent one
				if WrappedPlugin.version <= systemObj.plugins[self.pluginid].getVersion():
					logger.warning(
						f'{self.name} from {WrappedPlugin.__class__.__module__} will not be loaded!'
					)
					return WrappedPlugin

		# load the new one
		systemObj.plugins[self.pluginid] = WrappedPlugin()
		return WrappedPlugin


class PluginNotValid(Exception):
	pluginid: str


def placeholder(*args, **kwargs):
	pass


class BasePlugin(metaclass=ABCMeta):

	@abstractmethod
	async def load(self):
		"""
		this is called when the plugin should load things and create stuff
		"""
		pass

	@abstractmethod
	async def unload(self):
		"""
		called when the plugin is being unloaded, do clean up stuff here
		"""
		pass

	@abstractmethod
	def getName( self ) -> str:
		"""
		This method is used to get the plugin's name.
		This is used by BM to know what name to display in the plugin list.
		:return: plugin's name
		"""
		pass

	@abstractmethod
	def getVersion( self ) -> VersionInfo:
		"""
		returns a `semver.VersionInfo` object with the plugin version
		"""
		pass

	async def reload(self):
		"""
		called when the plugin is being reloaded
		"""
		pass

	def getPath(self) -> Path:
		return Path( systemObj.modules[self.__class__.__base__.__module__].__file__ ).resolve()

	def __init_subclass__(cls, **kwargs):
		systemObj.plugins[cls.__class__.__name__] = cls()
		logger.debug( f'instantiated plugin "{cls.__name__}" from {cls.__module__}.py' )

	__state__: str = 'unloaded'


class system:

	isReloading: bool = False
	plugins: Dict[str, BasePlugin] = {}
	modules: Dict[str, ModuleType] = {}

	def __init__(self):
		pass

	def startSync(self):
		"""
		starts the plugin system
		instantiate and loads the plugins
		"""
		logger.info('started loading plugins!')
		asyncio.run( self.start() )
		logger.info('finished loading plugins!')

	async def start(self):
		await self.instantiate()
		await self.load()

	async def instantiate(self):
		"""
		instantiate all plugins in the plugins folder
		"""
		fdr = Path(f'{config.pluginsPath}/')
		for plg in fdr.glob('*.py'):
			name = plg.name.replace('.py', '')
			spec = importlib.util.spec_from_file_location(name, plg)
			module = importlib.util.module_from_spec(spec)
			self.modules[module.__name__] = module
			try:
				spec.loader.exec_module(module)
			except PluginNotValid as e:
				logger.error(f"can't load {e.pluginid}! error:\n{e}")
			except Exception as e:
				error = ''.join( traceback.format_exception( type(e), e, e.__traceback__ ) )
				logger.error(f"can't load plugin! error: {error}")

	async def load(self, identifier: str = None):
		"""
		trigger the load event/method on every plugin/a specified plugin
		:param identifier: plugin to trigger load for
		"""
		if identifier is not None:
			if self.plugins[identifier].__state__ == 'loaded':
				raise Exception('trying to load an already loaded plugin!')
			try:
				await self.plugins[identifier].load()
				self.plugins[ identifier ].__state__ = 'loaded'
			except Exception as e:
				logger.error(f'caught exception while loading plugin "{identifier}"')
				logger.error( ''.join( traceback.format_exception( type(e), e, e.__traceback__ ) ) )
			return
		for plg in self.plugins.keys():
			await self.load(plg)

	async def unload(self, identifier: str = None):
		"""
		trigger the unload event/method on every plugin/a specified plugin
		:param identifier: plugin to trigger unload for
		"""
		if identifier is not None:
			if self.plugins[identifier].__state__ == 'unloaded':
				raise Exception('trying to unload an already unloaded plugin!')
			try:
				await self.plugins[identifier].unload()
			except Exception as e:
				logger.error(f'caught exception while unloading plugin "{identifier}"')
				logger.error( ''.join( traceback.format_exception( type(e), e, e.__traceback__ ) ) )
			self.plugins[identifier].__state__ = 'unloaded'
			return
		for plg in self.plugins.keys():
			await self.unload(plg)
		# redraw the menu bar in case a plugin added something
		wx.GetTopLevelWindows()[0].menuBar.Refresh()

	async def reload( self ):
		"""
		hard reloads a specified plugin
		- if the identifier is all reloads all plugins
		- delete a plugin module and reload it from disk
		"""
		# cycle in the plugins
		logger.info( f'plugins found: {self.plugins.__len__()}' )
		for i in range( self.plugins.__len__() ):
			# we're reloading, set isReloading to True
			self.isReloading = True
			# get data
			f = 0
			pluginid = None
			for key in self.plugins.keys():
				if f == i:
					pluginid = key
					break
				f += 1
			# this shouldn't happen but this is there to prevent exceptions
			if pluginid is None:
				continue
			# get the right module for a type of plugin
			if isinstance(self.plugins[pluginid], BasePlugin):
				module = self.modules[ self.plugins[pluginid].__module__ ]
			else:
				module = self.modules[ self.plugins[pluginid].__class__.__base__.__module__ ]
			# wait for the plugin to unload
			try:
				await self.plugins[pluginid].unload()
			except Exception as e:
				logger.error(f'caught exception while unloading plugin "{pluginid}"')
				logger.error( ''.join( traceback.format_exception( type(e), e, e.__traceback__ ) ) )
			# get the plugin's module spec
			spec = importlib.util.spec_from_file_location( name=module.__name__, location=module.__file__ )
			# get the plugin's module
			module = importlib.util.module_from_spec(spec)
			# try to execute the plugin's module
			try:
				spec.loader.exec_module(module)
			except PluginNotValid as e:
				logger.error(f"can't load a plugin! error:\n{e}")
				continue
			except Exception as e:
				error = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
				logger.error(f"can't load plugin! error: {error}")
				continue
			# reassign the module in the dict
			self.modules[module.__name__] = module
			# wait for the plugin to load
			try:
				await self.plugins[pluginid].load()
			except Exception as e:
				logger.error(f'caught exception while loading plugin "{pluginid}"')
				logger.error( ''.join( traceback.format_exception( type(e), e, e.__traceback__ ) ) )
				self.plugins[ pluginid ].__state__ = 'errored'
			else:
				# change the plugin's state to loaded
				self.plugins[pluginid].__state__ = 'loaded'
			# no mo reloading
			self.isReloading = False
		# dispatch events
		try:
			dispatcher.send( Events.RegisterEvent, handler=RegisterHandler() )
			from logWindow import logWindow
			dispatcher.send(Events.LogWindowCreated, window=logWindow.instance)
		except Errors.DupeMenuFoundException as e:
			logger.error( 'Found duplicate menus while registering! reload can\'t countinue!' )
			logger.error( ''.join( traceback.format_exception( type( e ), e, e.__traceback__ ) ) )
		except Exception as e:
			logger.error( 'caught exception while processing reload events "RegisterEvent", reload can\'t countinue!' )
			logger.error( ''.join( traceback.format_exception( type( e ), e, e.__traceback__ ) ) )

	async def unloadAndStop(self):
		"""
		unload all plugins and delete them, used to stop the system
		"""
		await self.unload()
		x = []
		for identifier in self.plugins.keys():
			x.append(identifier)
		for i in x:
			del self.plugins[i]


systemObj: system = system()
