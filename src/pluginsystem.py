import asyncio
import importlib.util
from pathlib import Path
from typing import Dict, Coroutine, List, Callable

import config
from srctools.logger import get_logger

logger = get_logger()
_eventHandlers: Dict[str, List[Coroutine]] = {}


class Plugin:
	"""
	this decorator is used to create a plugin for BEE Manipulator
	"""
	def __init__(self, pluginid: str, name: str, version: str, getLogger=False):
		self.getLogger = getLogger
		self.pluginid = pluginid
		self.name = name
		self.version = version

	def __call__(self, cls):
		# make a subclass to check for methods
		class wrap(cls):
			__state__ = 'unloaded'
			if self.getLogger:
				logger = get_logger()

			def getPath(self):
				self.__class__.__base__.__module__
		# checks if the plugin has the NEEDED methods
		if not asyncio.iscoroutinefunction(getattr(wrap, 'load', Callable)):
			raise PluginNotValid('missing required coroutine "load"!')
		if not asyncio.iscoroutinefunction(getattr(wrap, 'unload', Callable)):
			raise PluginNotValid('missing required coroutine "unload"!')
		# checks the optional methods
		if getattr(wrap, 'getEventHandler', placeholder) == placeholder:  # has getEventHandler?
			pass  # no
		elif asyncio.iscoroutinefunction( wrap.getEventHandler ):  # is it a coroutine?
			raise PluginNotValid('the "getEventHandler" coroutine should be a method')  # yes
		else:
			self.checkGetEventHandler( wrap.getEventhandler )  # has the correct number of parameters?
		if not asyncio.iscoroutinefunction(getattr(wrap, 'reload', placeholder)):
			raise PluginNotValid('the "reload" method should be a coroutine')
		if self.pluginid in systemObj.plugins.keys():
			if not systemObj.isReloading:
				logger.error(f'Duplicate plugin found! id: {self.pluginid}, duplicate name: {self.name}, it will replace the other plugin')
		systemObj.plugins[self.pluginid] = wrap()
		getattr(systemObj.plugins[self.pluginid], 'getEventHandler', placeholder2)(eventHandlerObj)
		return wrap


def _checkGetEventHandler(func: Callable):
	# is a method?
	if 'self' in func.__code__.co_varnames:
		# yes
		# does it have 1 parameter beside self?
		if func.__code__.co_argcount - 1 != 1:
			raise PluginNotValid('"getEventHandler" should have only 1 parameter (not counting self)')  # no
	else:
		# no
		# does it have 1 parameter?
		if func.__code__.co_argcount != 1:
			raise PluginNotValid('"getEventHandler" should have only 1 parameter')  # no


class PluginNotValid(Exception): pass


class eventHandler:
	"""
	a class that provides events handling
	- on(event, callback) subscribe CALLBACK to EVENT
	- send(event, kwargs) triggers EVENT with KWARGS as data
	"""

	def __init__(self):
		logger.info('plugin event handler started!')

	@staticmethod
	def on(evt: str, callback: Coroutine):
		"""
		listen for an event
		:param evt: event to listen for
		:param callback: the coroutine that will be executed when this event is triggered
		:return: nothing
		"""
		if evt in _eventHandlers.keys():
			_eventHandlers[evt].append(callback)
		else:
			_eventHandlers[evt] = []
			_eventHandlers[evt].append(callback)

	@staticmethod
	def send(evt: str, **kwargs):
		"""
		trigger an event
		:param evt: event to trigger
		:param kwargs: event data
		:return:
		"""
		if evt in _eventHandlers.keys():
			if len(kwargs) == 0:
				for callback in _eventHandlers[evt]:
					asyncio.run(callback())
			else:
				for callback in _eventHandlers[evt]:
					asyncio.run(callback(kwargs))

	'''
	# idk if use the wx one is better or not...
	@staticmethod
	def on(evt: str, callback: Coroutine):
		"""
		a version of on that uses the wx dispatcher
		:param evt: event to listen for
		:param callback: the callback that will be executed with event data
		:return: nothing
		"""
		dispatcher.connect(callback, evt)

	@staticmethod
	def send(evt: str, **kwargs):
		"""
		a version of send that uses the wx dispatcher
		:param evt: event to trigger
		:param kwargs: data of the event
		:return: nothing
		"""
		dispatcher.send(evt, kwargs)
	'''


async def placeholder(placeholder2):
	pass


def placeholder2(ph0=None, ph1=0):
	pass


class system:

	isReloading: bool= False
	plugins: Dict[str, object] = {}

	def __init__(self):
		pass

	async def start(self):
		"""
		starts the plugin system
		instantiate and loads the plugins
		:return: nothing
		"""
		logger.info('started loading plugins!')
		await self.instantiate()
		await self.load()
		logger.info('finished loading plugins!')

	async def instantiate(self):
		"""
		instantiate all plugins in the plugins folder
		:return: nothing
		"""
		fdr = Path(f'{config.pluginsPath}/')
		for plg in fdr.glob('*.py'):
			name = plg.name.replace('.py', '')
			spec = importlib.util.spec_from_file_location(name, plg)
			module = importlib.util.module_from_spec(spec)
			try:
				spec.loader.exec_module(module)
			except PluginNotValid as e:
				logger.error(f"can't load a plugin! error:\n{e}")
			except Exception as e:
				logger.error(f"can't load plugin! error: {e.__class__} {e}")

	async def load(self, identifier: str = None):
		"""
		trigger the load event/method on every plugin/a specified plugin
		:param identifier: plugin to trigger load for
		:return: nothing
		"""
		if identifier is not None:
			if self.plugins[identifier].__state__ == 'loaded':
				raise Exception('trying to load an already loaded plugin!')
			await self.plugins[identifier].load()
			self.plugins[identifier].__state__ = 'loaded'
			return
		for plg in self.plugins.values():
			await plg.load()
			plg.__state__ = 'loaded'

	async def unload(self, identifier: str = None):
		"""
		trigger the unload event/method on every plugin/a specified plugin
		:param identifier: plugin to trigger unload for
		:return: nothing
		"""
		if identifier is not None:
			if self.plugins[identifier].__state__ == 'unloaded':
				raise Exception('trying to unload an already unloaded plugin!')
			await self.plugins[identifier].unload()
			self.plugins[identifier].__state__ = 'unloaded'
			return
		for plg in self.plugins.values():
			await plg.unload()
			plg.__state__ = 'unloaded'

	async def reload(self, identifier: str):
		"""
		reload a specified plugin
		:param identifier: plugin to reload
		:return: nothing
		"""
		getattr(self.plugins[identifier], 'reload', str)()
		await self.unload(identifier)
		await self.load(identifier)

	async def hardReload(self, pluginid: str):
		"""
		hard reloads a specified plugin
		- if the identifier is all reloads all plugins
		- delete a plugin module and reload it from disk
		:param pluginid: plugin to reload
		:return: nothing
		"""
		if pluginid == 'all':
			# reload every plugin
			for name in self.plugins.keys():
				await self.hardReload(name)
		else:
			# we're reloading, set isReloading to True
			self.isReloading = True
			# wait for the plugin to unload
			await self.plugins[pluginid].unload()
			# get the plugin's module spec
			spec = importlib.util.find_spec(self.plugins[pluginid].__class__.__base__.__module__)
			# get the plugin's module
			module = importlib.util.module_from_spec(spec)
			# execute the plugin's module
			spec.loader.exec_module(module)
			# wait for the plugin to load
			await self.plugins[pluginid].load()
			# change the plugin's state to loaded
			self.plugins[pluginid].__state__ = 'loaded'
			self.isReloading = False

	async def unloadAndStop(self):
		"""
		unload all plugins and delete them, used to stop the system
		:return: nothing
		"""
		await self.unload()
		x = []
		for identifier in self.plugins.keys():
			x.append(identifier)
		for i in x:
			del self.plugins[i]


eventHandlerObj: eventHandler = eventHandler()
systemObj: system = system()
