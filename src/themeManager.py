from typing import Dict

from api.themeManager import ThemeManager as AbstractThemeManager, Theme


class ThemeManager(AbstractThemeManager):

	def init( self ) -> None:
		pass

	def stop( self ) -> None:
		pass

	def registerTheme( self, theme: Theme ) -> None:
		pass

	def getThemes( self ) -> Dict[ str, Theme ]:
		pass

	def getTheme( self ) -> Theme:
		pass


manager: ThemeManager = ThemeManager()
