import json
import os
import urllib
from pathlib import Path

import wx
from requests import get

import config
import utilities
from packages import PackageFrame
from srctools.logger import get_logger

database: list = None
databasePath: str = config.load('databasePath')
logger = get_logger()


class browser(wx.ScrolledWindow):
	"""
		the package browser, this will display all the available packages
	"""
	sizer: wx.GridBagSizer

	def __init__(self, master: wx.Notebook):
		global database, databasePath
		super().__init__(master)
		logger.debug('loading database path..')
		logger.debug('loaded database path from config!')
		logger.info(f'Loading database! (path: {databasePath})')
		checkDatabase()
		self.loadDatabase()

	def reload(self):
		global databasePath
		downloadDatabase()
		databasePath = config.load('databasePath')
		self.loadDatabase()
	
	def loadDatabase(self):
		return
		if not os.path.exists(databasePath):
			database = loadPlaceHolder()
		else:
			database = loadObj()
		self.sizer = wx.GridBagSizer(vgap=2, hgap=0)
		null = wx.LogNull()
		yy = 0
		for pkg in database:
			package = PackageFrame(master=self, package=pkg, y=yy)
			yy += 100
		del null

	def loadPlaceHolder(self):
		return


"""
	check, download, upload, and load the database
"""


def checkDatabase() -> None:
	"""
		check the database, if it doesn't exist or is invalid, redownload it
	"""
	global logger
	try:
		logger.debug('checking database..')
		with open(databasePath, "r") as file:
			json.load(file)
		logger.debug('the package database is valid')
	except:
		logger.error("ERROR! the database isn't valid json! the database will be downloaded again.")
		if not utilities.isonline():
			logger.warning("can't download database while offline, aborting")
			exit(2)
		downloadDatabase()
		checkDatabase()
	logger.debug('checking packages assets dir..')
	if not Path( config.assetsPath + '/packages' ).exists():
		logger.warning("the packages folder doesn't exist! creating one..")
		Path( config.assetsPath + '/packages' ).mkdir()
		logger.info('packages folder created!')


def downloadDatabase() -> None:
	"""
		download the database
	"""
	global logger
	if not utilities.isonline():
		logger.warning("can't download database while offline, aborting")
		return
	try:
		logger.debug(f'creating/opening file "{databasePath}" for writing')
		with open(databasePath, "w") as file:
			logger.debug('downloading database from github..')
			database = get('https://raw.githubusercontent.com/ENDERZOMBI102/ucpDatabase/master/Database.json').json()
			json.dump(database, file, indent=3)
			logger.info(f'database saved to {databasePath}')
	except:
		logger.fatal("FATAL ERROR, can' download database while offline, why the checks didn't worked?")
		raise Exception("how did you get here?")


def loadObj() -> list:
	r"""
		create the correct package object for each one of the packages in the json
	"""
	packageFolderPath = config.assetsPath + 'packages'
	logger.debug('opening database..')
	with open(databasePath, 'r') as file:
		logger.debug('loading database..')
		databaseDict = json.load(file)
		logger.info('database loaded!')
	database = []
	logger.debug('composing package objects from database..')
	for pkg in databaseDict:
		logger.info(f'creating package {pkg["ID"]}, type: {pkg["type"]}')
		# if is a BEE package load those info
		if pkg["type"] == "BEE" or pkg["type"] == "bee":
			package = beePackage()
			package.ID = pkg["ID"]
			package.author = pkg["author"]
			package.name = pkg["name"]
			package.description = pkg["desc"]
			package.coAuthors = pkg["co_author"]
			package.version = pkg["version"]
			package.url = pkg["api_latest_url"]
			# or those if is a BM package
		elif pkg["type"] == "BM" or pkg["type"] == "bm":
			package = bmPackage()
			package.ID = pkg["ID"]
			package.author = pkg["author"]
			package.name = pkg["name"]
			package.coAuthors = pkg["co_author"]
			package.desc = pkg["desc"]
			package.version = pkg["version"]
			package.url = pkg["api_latest_url"]
			package.contents = pkg["contents"]
			package.config = pkg["config"]
		# now that we have our package object, we have to verify and load some thing from the internet
		# take the file name from the api latest OR from the database if the package isn't on github
		logger.debug('finding package filename..')
		if package.service() == "github" and package.filename and utilities.isonline() and not pkg["filename"]:
			logger.debug('package uses github as host, GETting filename')
			tmp = get(package.url).json()
			package.filename == tmp["assets"][0]["name"]
		elif package.filename:
			logger.debug(f'package uses {package.service()}, loading filename from package info')
			package.filename == pkg["filename"]
		else:
			pass
		# obtain the icon url
		logger.debug('GETting package icon..')
		if package.service() == "github" and not utilities.keyExist(pkg, 'icon_url'):
			iconurl = package.repo() + 'raw/master/icon.png'
		elif utilities.keyExist(pkg, 'icon_url'):
			iconurl = pkg['icon_url']
		else: iconurl = None
		# save the icon
		iconPath = f'{packageFolderPath}/{package.ID}/icon.png'
		if not Path(f'{packageFolderPath}/{package.ID}').exists():
			Path(f'{packageFolderPath}/{package.ID}').mkdir()
		if ( not Path(iconPath).exists() ) and ( not iconurl is None):
			open( iconPath, 'x').close()
			urllib.request.urlretrieve(
				iconurl,
				iconPath
			)
		if iconurl is None:
			package.icon = None
		package.icon = iconPath
		# check the validity of coAuthors
		if package.coAuthors in [None, ""]:
			package.coAuthors = []
		# and finally append the package to the database list
		database.append(package)
		logger.debug(f'package {package.name} added to database')
		iconPath = None
		iconurl = None
	logger.info('finished loading database from database.json!')
	# return the list we made
	return database


def loadPlaceHolder():
	return []
