import json
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import List

from requests import get

import config
import utilities
from packages import PackageView, BPackage, BMPackage
from srctools.logger import get_logger

logger = get_logger()


class PDatabase:

	db: Path
	path: str

	views: List[PackageView] = []

	def __init__(self):
		self.path = config.load('databasePath')
		self.db = Path( self.path )

	def checkDatabase(self) -> None:
		"""
			check the database, if it doesn't exist or is invalid, re-download it
		"""
		# the db exist?
		if not self.db.exists():
			# no, download it first
			self.downloadDatabase()
		try:
			logger.debug('checking database..')
			with self.db.open('r') as file:
				json.load(file)
			logger.debug('the package database is valid')
		except JSONDecodeError:
			logger.error("the database isn't valid json! it will be downloaded again.")
			if not utilities.isonline():
				logger.warning("can't download database while offline, aborting")
				return False
			self.downloadDatabase()
			# RECURSION
			return self.checkDatabase()
		logger.debug('checking packages assets dir..')
		if not Path( config.assetsPath + '/packages' ).exists():
			logger.warning("the packages folder doesn't exist! creating one..")
			Path( config.assetsPath + '/packages' ).mkdir()
			logger.info('packages folder created!')
		return True

	def downloadDatabase(self) -> None:
		"""
			download the database
		"""
		self.db.touch()
		logger.debug(f'opening "{self.path}" for writing')
		with self.db.open('w') as file:
			logger.debug('downloading database from github..')
			database = get( config.load('onlineDatabaseUrl') ).json()
			json.dump(database, file, indent=4)
			logger.info(f'database saved to {self.path}')
			logger.fatal("FATAL ERROR, can' download database while offline, why the checks didn't worked?")

	async def loadObjects(self, master) -> list:
		"""
			create the correct package object for each one of the packages in the json
		"""
		packageFolderPath = f'{config.assetsPath}packages'

		with self.db.open('r') as file:
			logger.debug(f'loading database from {self.path}..')
			databaseDict = json.load(file)
			logger.info('database loaded!')
		logger.debug('composing package objects from database..')
		for pkg in databaseDict:
			pkg: dict
			logger.info(f'creating package {pkg["identifier"]}, type: {pkg["type"]}')
			# create the package data
			# package folder
			folder = Path(f'{packageFolderPath}/{pkg["identifier"]}')
			if not folder.exists():
				folder.mkdir()
			# icon
			icon = Path(f'{packageFolderPath}/{pkg["identifier"]}/icon.png')
			if not icon.exists():
				if 'icon_url' in pkg.keys():
					if pkg['icon_url'] is not None:
						# is an icon url is specified, use that url
						with icon.open('xb') as file:
							logger.info(f"downloading {pkg['identifier']}'s icon")
							file.write( get( pkg['icon_url'] ).content )
							logger.info('icon downloaded')
					del pkg['icon_url']
				else:
					with icon.open('xb') as file:
						logger.info(f"downloading {pkg['identifier']}'s icon")
						url = makeIconUrl( pkg['repo'] )
						file.write( get( url ).content )
						logger.info('icon downloaded')
			# website
			if 'website' not in pkg.keys():
				pkg['website'] = None
			# package
			# create BEE package
			if pkg['type'].upper() == 'BEE':
				del pkg['type']
				package = BPackage.parse_obj(pkg)
			# or BM package
			elif pkg['type'].upper() == 'BM':
				del pkg['type']
				package = BMPackage.parse_obj(pkg)
			# construct and append the view
			self.views.append( PackageView( master, package ) )


def makeIconUrl(repo: str) -> str:
	splittedUrl = repo.split('/')
	logger.debug(f'icon url: "https://raw.githubusercontent.com/{splittedUrl[4]}/{splittedUrl[5]}/master/icon.png"')
	return f'https://raw.githubusercontent.com/{splittedUrl[4]}/{splittedUrl[5]}/master/icon.png'
