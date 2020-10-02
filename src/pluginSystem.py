import asyncio
import importlib.util
import traceback
from abc import ABCMeta, abstractmethod
from pathlib import Path
from types import ModuleType
from typing import Dict, Coroutine, List, Callable

import config
from srctools.logger import get_logger

logger = get_logger()
_eventHandlers: Dict[str, List[Coroutine]] = {}


class Plugin:
	"""
	this decorator is used to create a plugin for BEE Manipulator
	"""
	def __init__(self, pluginid: str, name: str, version: str = None ):
		self.pluginid = pluginid
		self.name = name
		self.version = version

	def __call__(self, cls):
		# make a subclass to check for methods
		class wrap(cls):
			__state__ = 'unloaded'

			def getPath(self):
				return self.__class__.__base__.__module__
		# checks if the plugin has the NEEDED methods
		# load
		if not asyncio.iscoroutinefunction(getattr(wrap, 'load', Callable)):
			raise PluginNotValid('missing required coroutine "load"!')
		# unload
		if not asyncio.iscoroutinefunction(getattr(wrap, 'unload', Callable)):
			raise PluginNotValid('missing required coroutine "unload"!')
		# checks the optional methods
		# reload
		if not asyncio.iscoroutinefunction(getattr(wrap, 'reload', placeholder)):
			raise PluginNotValid('the "reload" method should be a coroutine')
		if self.pluginid in systemObj.plugins.keys():
			if not systemObj.isReloading:
				logger.error(f'Duplicate plugin found! id: {self.pluginid}, duplicate name: {self.name}, it will replace the other plugin')
		systemObj.plugins[self.pluginid] = wrap()
		return wrap


class PluginNotValid(Exception):
	pass


async def placeholder(ph0=None):
	pass


def placeholder2(ph0=None, ph1=0):
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

	async def reload(self):
		"""
		called when the plugin is being reloaded
		"""
		pass


class system:

	isReloading: bool = False
	plugins: Dict[str, object] = {}
	modules: List[ModuleType] = []

	def __init__(self):
		pass

	def startSync(self):
		"""
		starts the plugin system
		instantiate and loads the plugins
		:return: nothing
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
		:return: nothing
		"""
		fdr = Path(f'{config.pluginsPath}/')
		for plg in fdr.glob('*.py'):
			name = plg.name.replace('.py', '')
			spec = importlib.util.spec_from_file_location(name, plg)
			module = importlib.util.module_from_spec(spec)
			self.modules.append(module)
			try:
				spec.loader.exec_module(module)
			except PluginNotValid as e:
				logger.error(f"can't load a plugin! error:\n{e}")
			except Exception as e:
				error = ''.join( traceback.format_exception( type(e), e, e.__traceback__ ) )
				logger.error(f"can't load plugin! error: {error}")

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

	async def hardReload(self, ph=None):
		"""
		hard reloads a specified plugin
		- if the identifier is all reloads all plugins
		- delete a plugin module and reload it from disk
		:param pluginid: plugin to reload
		:return: nothing
		"""
		# cicle in the plugins
		print( f'plugins found: {len( self.plugins)}' )
		for i in range( len( self.plugins) ):
			# we're reloading, set isReloading to True
			self.isReloading = True
			# get data
			f = 0
			for key in self.plugins.keys():
				if f == i:
					pluginid = key
				f += 1
			module = self.modules[i]
			print('stop!')
			# wait for the plugin to unload
			await self.plugins[pluginid].unload()
			# get the plugin's module spec
			spec = importlib.util.spec_from_file_location( name=module.__name__, location=module.__file__ )
			# get the plugin's module
			module = importlib.util.module_from_spec(spec)
			# execute the plugin's module
			spec.loader.exec_module(module)
			# wait for the plugin to load
			await self.plugins[pluginid].load()
			# change the plugin's state to loaded
			self.plugins[pluginid].__state__ = 'loaded'
			# no mo reloading
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


systemObj: system = system()
