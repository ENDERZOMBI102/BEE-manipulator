import builtins
import json
from pathlib import Path
from typing import Dict, Callable

import requests

import config
from cli import parsedArguments
from srctools.logger import get_logger

logger = get_logger()
loc: Callable
localizeObj: 'Localize' = None


class LangNotSupportedError(Exception):
	pass


class Localize:
	""" Class that helps with localizing applications """
	lang: str
	localizations: Dict[str, Dict[str, str]] = {}

	def __init__(self):
		# get globals
		global loc, localizeObj
		# check language overwrite
		if parsedArguments.lang is not None:
			config.overwrite( 'lang', parsedArguments.lang )
		# inject loc function to builtins
		self.install()
		# set globals
		loc = self.loc
		localizeObj = self
		# Initialize localizations by loading all .jlang files and the current language
		self.lang = config.load('lang')
		self.loadLocFiles()

	def install(self):
		"""	Makes the loc() function available to everyone """
		builtins.loc = self.loc

	def loc(self, textId: str, **kwargs) -> str:
		"""
		Returns the localized text from a token
		\t
		:param textId: the text id/token
		:return: localized text
		"""
		if textId in self.localizations[ self.lang ].keys():
			txt = self.localizations[ self.lang ][ textId ]
			for key, value in kwargs.items():
				txt = txt.replace( '{' + key + '}', value )
		else:
			if 'missingtranslation' in self.localizations[ self.lang ].keys():
				txt = self.localizations[ self.lang ][ 'missingtranslation' ]
			else:
				txt = 'OHNO'
		return txt

	def setLang(self, newLang: str):
		"""
		Set the current application language
		\t
		:param newLang: the language to set to
		"""
		logger.debug(f'checking if language {newLang} is supported..')
		if newLang in self.localizations.keys():
			self.lang = newLang
			config.save(newLang, 'lang')
			logger.info(f'changed lang to {newLang}')
		else:
			logger.error( LangNotSupportedError(f'unsupported language {newLang}!') )

	def loadLocFiles(self):
		""" Load all .jlang files """
		logger.debug('loading lang folder path..')
		# create Path obj with the lang file path
		folder = Path( config.load('l18nFolderPath') )
		# if it doesn't exist, download the default lang file: en_US.jlang
		if not folder.exists():
			logger.error(f'NO LANG FOLDER FOUND!')
			folder.mkdir()
			logger.info('downloading english translation from github!')
			self.downloadLanguage( 'en_US' )
		logger.info(f'langs folder path is "{folder.absolute()}"')
		langFile: Path
		# iterate in all jlang files in the lang folder
		for langFile in folder.glob('*.jlang'):
			logger.debug(f'loading lang file "{langFile.name}"')
			# open the file
			with langFile.open('r') as file:
				# save the file into the dictionary (l18ns[langcode][textid])
				self.localizations[langFile.name.replace('.jlang', '')] = json.load(file)
			logger.info(f'loaded lang file {langFile.name}!')
		# repeat for all files

	@staticmethod
	def downloadLanguage( langToDownload: str ):
		"""
		Downloads a language
		\t
		:param langToDownload: id of the language
		:return:
		"""
		try:
			# get lang file from github
			data = requests.get(
				f'https://github.com/ENDERZOMBI102/BEE-manipulator/raw/master/langs/{langToDownload}.jlang'
			).json()
			# create a Path object with the lang file path
			langFile = Path(f'{config.load("l18nFolderPath")}/{langToDownload}.jlang')
			# mode to open the file with
			mode = 'x'
			# if the lang file exist, use mode Write, else continue with creation (x)
			if langFile.exists:
				mode = 'w'
			# open the lang file with adeguate mode
			with langFile.open(mode=mode) as file:
				# write the Json LANG file
				json.dump(data, file, indent=4)
		except Exception as e:
			# en_US is the base/essential lang file, without it, we can't continue
			if langToDownload == 'en_US':
				logger.fatal( f' Failed to download lang file!', exc_info=e )
				exit(1)
			else:
				logger.error(f'failed to download lang file {langToDownload}')
