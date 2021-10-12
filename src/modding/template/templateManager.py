from api.templateManager import TemplateManager as AbstractTemplateManager


class TemplateManager(AbstractTemplateManager):

	def init( self ) -> None:
		pass

	def stop( self ) -> None:
		pass


manager: TemplateManager = TemplateManager()
