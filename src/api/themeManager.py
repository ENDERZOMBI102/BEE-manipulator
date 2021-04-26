from abc import ABCMeta, abstractmethod
from typing import Dict

import wx

from .manager import Manager


class Theme:
	background: wx.Colour
	foreground: wx.Colour
	button: wx.Colour


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
