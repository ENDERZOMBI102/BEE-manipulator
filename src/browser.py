import wx
import config
import json
import utilities
from requests import get
from base64 import b64encode as encode
from packages import *
from srctools.logger import get_logger
import os

database: list = None
databasePath: str = None
logger = get_logger()

class browser(wx.ScrolledWindow):
	r"""
		the package browser, this will display all the avaiable packages
	"""
	def __init__(self, master: wx.Notebook):
		global database, databasePath
		super().__init__(master)
		logger.debug('loading database path..')
		databasePath = config.load('databasePath')
		logger.debug('loaded database path from config!')
		logger.info(f'Loading database! (path: {databasePath})')
		checkDatabase()
		self.loadDatabase()
	
	
	def reload(self):
		downloadDatabase()
		databasePath = config.load('databasePath')
		self.loadDatabase()
	
	def loadDatabase(self):
		if not os.path.exists('./assets/database.json'):
			database = loadPlaceHolder()
		else:
			database = loadObj()
		databaseFrames = []
		for pkg in database:
			databaseFrames.append(packageFrame(master=self, package=pkg))


	def loadPlaceHolder(self):
		return


r"""
	check, download, upload, and load the database
"""
def checkDatabase() -> None:
	r"""
		check the database, if it doesn't exist or is invalid, redownload it
	"""
	global logger
	try:
		logger.debug('checking database..')
		with open(databasePath, "r") as file:
			json.load(file)
		logger.debug('the package database is valid')
	except:
		logger.error('ERROR! the database isn\' valid json! the database will be downloaded again.')
		if utilities.isonline() == False:
			logger.warning('can\'t download database while offline, aborting')
			return
		downloadDatabase()
		checkDatabase()

def downloadDatabase() -> None:
	r"""
		download the database
	"""
	global logger
	if utilities.isonline() == False:
		logger.warning('can\'t download database while offline, aborting')
		return
	try:
		logger.debug('creating/opening file "./assets/database.json" for writing')
		with open(databasePath, "w") as file:
			logger.debug('downloading database from github..')
			database = get("https://raw.githubusercontent.com/ENDERZOMBI102/ucpDatabase/master/Database.json").json()
			json.dump(database, file, indent=3)
			logger.info(f'database saved to {databasePath}')
	except:
		logger.fatal('FATAL ERROR, can\' download database while offline, why the checks didn\'t worked?')
		raise Exception("how did you get here?")

def loadObj() -> list:
	r"""
		create the correct package object for each one of the packages in the json
	"""
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
			iconurl = package.repo() + "raw\\master\\icon.png"
		elif utilities.keyExist(pkg, "icon_url"):
			iconurl = pkg["icon_url"]
		# obtain the icon
		icon = get(iconurl)
		# convert it to base64
		package.icon64 = encode(icon.content)
		# check the validity of coAuthors
		if package.coAuthors in [None, ""]:
			package.coAuthors = []
		# and finally append the package to the database list
		database.append(package)
		logger.debug(f'package {package.name} added to database')
	logger.info('finished loading database from database.json!')
	# return the list we made
	return database

def loadPlaceHolder():
	return []
