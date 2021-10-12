from abc import ABCMeta

from api.manager import Manager


class TemplateManager(Manager, metaclass=ABCMeta):

	def init( self ) -> None:
		pass

	def stop( self ) -> None:
		pass
