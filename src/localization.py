import asyncio
import builtins
import json
from pathlib import Path
from sys import argv
from typing import Dict

import requests

import config
from srctools.logger import get_logger

logger = get_logger()
loc: callable

# check of forced language
if '--lang' in argv:
	try:
		lang = argv[argv.index('--lang') + 1]
	except:
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
		global loc
		# inject loc function to builtins
		self.install()
		# set globals
		loc = self.loc
		# run initialization
		asyncio.run(self.init())

	async def init(self):
		self.lang = config.load('lang')
		await self.loadLocFiles()

	def install(self):
		builtins.loc = self.loc

	def loc(self, textId) -> str:
		return self.localizations[self.lang][textId]

	def setLang(self, newLang: str):
		logger.debug(f'checking if language {newLang} is supported..')
		if newLang in self.localizations.keys():
			self.lang = newLang
			config.save(newLang, 'lang')
			logger.info(f'changed lang to {newLang}')
		else:
			logger.error(LangNotSupportedError(f'unsupported language {newLang}!'))

	async def loadLocFiles(self):
		logger.debug('loading lang folder path..')
		# create Path obj with the lang file path
		folder = Path( config.load('l18nFolderPath') )
		# if it doesn't exist, download the default lang file: EN_us.jlang
		if not folder.exists():
			logger.error(f'NO LANG FOLDER FOUND!')
			folder.mkdir()
			logger.info('downloading english lang from github!')
			await self.dl('en_US')
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
		try:
			# get lang file from github
			data = requests.get(
				f'https://github.com/ENDERZOMBI102/BEE-manipulator/raw/master/langs/{langToDownload}.jlang'
			).json
			# TODO: substitute with chained version
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
		except:
			# en_US is the base/essential lang file, without it, we can't continue
			if langToDownload == 'en_US':
				logger.fatal(f' Failed to download lang file!', exc_info=True)
				exit(1)
			else:
				logger.error(f'failed to download lang file {langToDownload}')