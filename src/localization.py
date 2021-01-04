import asyncio
import builtins
import json
from pathlib import Path
from sys import argv
from typing import Dict, Callable

import requests

import config
from srctools.logger import get_logger

logger = get_logger()
loc: Callable
localizeObj: 'Localize' = None

# check if a language is forced
if '--lang' in argv:
	try:
		lang = argv[argv.index('--lang') + 1]
	except IndexError:
		logger.error('missing value for command line parameter --lang! it will be ignored!')
	else:
		config.overwrite('lang', lang)


class LangNotSupportedError(Exception):
	pass


class Localize:
	"""
	class that helps with localizing applications
	"""
	lang: str
	localizations: Dict[str, Dict[str, str]] = {}

	def __init__(self):
		# get globals
		global loc, localizeObj
		# inject loc function to builtins
		self.install()
		# set globals
		loc = self.loc
		localizeObj = self
		# run initialization
		asyncio.run(self.init())

	async def init(self):
		"""
		initialize localizations
		this will load all .jlang files and the current language
		:return:
		"""
		self.lang = config.load('lang')
		await self.loadLocFiles()

	def install(self):
		"""
		makes the loc() function available to everyone
		"""
		builtins.loc = self.loc

	def loc(self, textId) -> str:
		"""
		returns the localized text from a token
		:param textId: the text id/token
		:return: localized text
		"""
		try:
			return self.localizations[ self.lang ][ textId ]
		except KeyError:
			logger.error(f'missing translation! key: {textId}')
			if 'missingtranslation' in self.localizations[self.lang].keys():
				return self.localizations[ self.lang ][ 'missingtranslation' ]
			return 'OHNO'

	def setLang(self, newLang: str):
		"""
		set the current application language
		:param newLang: the language to set to
		"""
		logger.debug(f'checking if language {newLang} is supported..')
		if newLang in self.localizations.keys():
			self.lang = newLang
			config.save(newLang, 'lang')
			logger.info(f'changed lang to {newLang}')
		else:
			logger.error( LangNotSupportedError(f'unsupported language {newLang}!') )

	async def loadLocFiles(self):
		"""
		load all .jlang files
		"""
		logger.debug('loading lang folder path..')
		# create Path obj with the lang file path
		folder = Path( config.load('l18nFolderPath') )
		# if it doesn't exist, download the default lang file: en_US.jlang
		if not folder.exists():
			logger.error(f'NO LANG FOLDER FOUND!')
			folder.mkdir()
			logger.info('downloading english translation from github!')
			self.dl('en_US')
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

	def dl(self, langToDownload: str):
		"""
		downloads a language
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
