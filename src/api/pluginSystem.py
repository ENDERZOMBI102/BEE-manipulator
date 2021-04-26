from abc import ABCMeta, abstractmethod
from enum import Enum
from multiprocessing.connection import PipeConnection
from typing import Callable

import wx
from semver import VersionInfo

import ipc


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


class RegisterHandler(metaclass=ABCMeta):

	@abstractmethod
	def RegisterMenu( self, menu: wx.Menu, title: str) -> None:
		"""
		Registers a menubar menu
		:param menu: the menu to register
		:param title: title of the menu
		"""

	@abstractmethod
	def RegisterIpcHandler( self, protocol: str, hdlr: Callable[ [ PipeConnection, ipc.Command ], None ] ) -> None:
		"""
		Registers a callable as a IPC protocol handler.
		(mostly used for custom bm://PROC protocols)
		:param protocol: protocol to register, ex: view
		:param hdlr: the callable that will handle this protocol
		"""

	@abstractmethod
	def RegisterBookPage( self, page: wx.Panel, title: str ) -> None:
		"""
		Registers a page for the main notebook widget
		:param page: the page to register
		:param title: title of the page
		"""


class Plugin:
	""" This decorator is used to create a plugin for BEE Manipulator """
	def __init__(self, name: str, version: VersionInfo = None, pluginid: str = None ):
		self.name = name
		self.version = version
		self.pluginid = pluginid

	def __call__( self, cls ):
		pass


class BasePlugin(metaclass=ABCMeta):
	""" Abstract class for plugins, an alternative method to the decorator """

	@abstractmethod
	async def load(self):
		"""	This is called when the plugin should load things and create stuff """

	@abstractmethod
	async def unload(self):
		"""	Called when the plugin is being unloaded, do clean up stuff here """

	@abstractmethod
	def getName( self ) -> str:
		"""
		This method is used to get the plugin's name.
		This is used by BM to know what name to display in the plugin list.
		:return: plugin's name
		"""

	@abstractmethod
	def getVersion( self ) -> VersionInfo:
		"""	Returns a `semver.VersionInfo` object with the plugin version """

	async def reload(self):
		""" Called when the plugin is being reloaded """


def getCacheFolder(plugin: str, relative: bool = True) -> str:
	""" Get the cache folder Path object for this plugin """
