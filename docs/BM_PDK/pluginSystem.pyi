from abc import ABCMeta, abstractmethod
from logging import Logger

class Plugin:

	def __init__(self, pluginid: str, name: str, version: str = None):
		"""
		this decorator is used to decorate a class that contains a plugin for BEE Manipulator
		"""
		pass

	def __call__(self, cls):
		pass


def getLogger() -> Logger:
	pass


class BasePlugin(metaclass=ABCMeta):

	@abstractmethod
	async def load(self):
		pass

	@abstractmethod
	async def unload(self):
		pass

	async def reload(self):
		pass