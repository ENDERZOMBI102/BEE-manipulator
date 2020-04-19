import wx
import config
import json
from requests import get
from base64 import b64encode as encode
from packages import *
from srctools.logger import get_logger

database: list = None
databasePath: str = None
logger = get_logger()

class browser(wx.Window):
	r"""
		the package browser, this will display all the avaiable packages
	"""
	def __init__(self, master):
		global database, databasePath
		super().__init__(master)
		databasePath = config.load('databasePath')
		checkDatabase()
		
		



r"""
	check, download, upload, and load the database
"""
def checkDatabase():
	r"""
		check the database
	"""
	global logger
	try:
		logger.debug('checking database..')
		with open(databasePath, "r") as file:
			json.load(file)
		logger.debug('the package database is valid')
	except:
		logger.error('ERROR! the database isn\' valid json! the database will be downloaded again.')
		downloadDatabase()
		checkDatabase()

def downloadDatabase():
	r"""
		download the database
	"""
	global logger
	if not config.isonline():
		logger.warning('can\'t download database while offline, aborting')
	try:
		with open(databasePath, "w") as file:
			database = get("https://raw.githubusercontent.com/ENDERZOMBI102/ucpDatabase/master/Database.json").json()
			json.loads(database)
			json.dump(database, file, indent=4)
	except:
		raise Exception("how did you get here?")

def loadObj():
	r"""
		create the correct package object for each one of the packages in the json
	"""
	with open(databasePath, 'r') as file:
		databaseDict = json.load(file)
	database = []
	for pkg in databaseDict:
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
		if package.service() == "github" and package.filename and config.isonline() and not pkg["filename"]:
			tmp = get(package.url)
			package.filename == tmp["assets"][0]["name"]
		elif package.filename:
			package.filename == pkg["filename"]
		else
		# obtain the icon url
		if package.service() == "github":
			iconurl = package.repo() + "raw\\master\\icon.png"
		elif pkg["icon_url"] and config.isonline():
			iconurl = pkg["icon_url"]
		# obtain the icon
		icon = get(iconurl)
		# convert it to base64
		package.icon64 = encode(icon)
		# check the validity of coAuthors
		if package.coAuthors in [None, ""]:
			package.coAuthors = []
		# and finally append the package to the database list
		database.append(package)
	
	# return the list we made
	return database

