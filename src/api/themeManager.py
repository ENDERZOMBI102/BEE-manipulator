from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Dict

from .manager import Manager


@dataclass
class Theme:
	background: str
	foreground: str


class ThemeManager( Manager, metaclass=ABCMeta ):

	@abstractmethod
	def getThemes( self ) -> Dict[str, Theme]:
		""" Returns a dict will all available themes """

	@abstractmethod
	def registerTheme( self, theme: Theme ) -> None:
		""" Registers a Theme to be used in BM """

	@abstractmethod
	def getTheme( self ) -> Theme:
		""" Get the current theme object """
