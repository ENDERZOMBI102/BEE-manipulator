from typing import Callable, Dict

loc: Callable
localizeObj: 'Localize'
Language = str


class LangNotSupportedError(Exception):
	pass


class Localize:
	""" Class that helps with localizing applications """
	lang: Language
	localizations: Dict[Language, Dict[str, str]] = {}

	def loc(self, textId: str, **kwargs) -> str:
		"""
		returns the localized text from a token
		:param textId: the text id/token
		:return: localized text
		"""

	def setLang(self, newLang: str) -> None:
		"""
		Set the current application language
		:param newLang: the language to set to
		"""

	async def loadLocFiles(self) -> None:
		""" Load all .jlang files """

	def downloadLanguage( self, langToDownload: str ) -> None:
		"""
		downloads a language
		:param langToDownload: id of the language
		:return:
		"""