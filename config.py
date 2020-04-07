import json# for manipulating json files
from os import path# for open files
from sys import platform# for knowing where the file is executed on
from requests import get# for the the connection
from srctools.property_parser import Property# for parse vdfs files
from srctools.logger import get_logger
from utilities import *
from winreg import *

logger = get_logger("config")
cfg = {
	"config_type": "BEE2.4 Manipulator Config File",
	"appVersion": "0.0.1",
	"lastVersion": False,
	"beePrereleases":False,
	"beeUpdateUrl": None,
	"steamDir":None,
	"portal2Dir":None,
	"beePath": None,
	"logWindowVisibility": False,
	"logLevel": "info"
}

def createConfig():
	r"""
		a simple function that make the config file
	"""
	global cfg
	with open('config.cfg', 'w', encoding="utf-8") as file:
		json.dump(cfg, file, indent=3)

def load(section):# load a config
	r"""
	loads a section of the config (json-formatted) and return the data.
	raise an exception if the config or the requested section doesn't exist
	example::

		>>> import config
		>>> print(config.load("version"))
		2.6
	"""
	try:
		with open('config.cfg', 'r', encoding="utf-8") as file:
			cfg = json.load(file)# load the config
			readeData = cfg[section]# take the requested field
		return readeData # return the readed data
	except:
		raise configError("can't load " + section)

def save(data, section):# save a config
	r"""
	save the data on the config (json-formatted), re-create the config if no one is found.
	example::
		>>> import config
		>>> print(config.load("version"))
		'2.6'
		>>> config.save("2.5","version")
		>>> print(config.load("version"))
		'2.5'
	"""
	if not check(): createConfig()
	try:
		with open('config.cfg', 'r', encoding="utf-8") as file:
			cfg = json.load(file)# load the config file
			cfg[section]=data
		with open('config.cfg', 'w', encoding="utf-8") as file:
			json.dump(cfg, file, indent=3)
	except:
		raise configError("error while saving the config")


def loadAll() -> dict:
	try:
		logger.debug("loading config file")
		with open('config.cfg', 'r', encoding="utf-8") as file:
			cfg = json.load(file)  # load the config file
			logger.debug("config file loaded, returning it as dict")
		return cfg
	except:
		logger.error("no config file found! creating & loading new one")
		createConfig()# create new config file and call the function again
		return loadAll()


def saveAll(cfg: dict):
	"""
	this saves the config file object returned from loadAll()
	"""
	try:
		with open('config.cfg', 'w', encoding="utf-8") as file:
			json.dump(cfg, file, indent=3)
	except:
		logger.error("An error happened while saving config file, please open the console and")


def check(arg = None) -> bool:
	r"""
	if no aurgment is present check if the config file exist and if is a BM config file, else will
	check if the given section exists.
	"""
	try:
		with open('config.cfg', 'r') as file:
			cfgj = json.load(file)
			return True
	except:
		return False
	if arg is None:# check the aurgment is present
		global cfg
		# check if EVERY config exists
		for i in cfg.keys():
			if cfgj[i]: continue
			return False
		# final check
		if cfgj['config_type'] == "BEE2.4 Manipulator Config File":
			# the check is made successfully
			return True
		else:
			# the config file is not a BM config file
			return False
	try:
		with open("config.cfg", 'r') as file:  # try to open the config file
			cfgj = json.load(file) # load the config file
			if cfgj[arg]:
				return True
			else:
				return False
	except:
		createConfig()


 # dynamic/static configs
def osType() -> str:
	return platform

def steamDir( cmde = False) -> str:
	r"""
		this function return the steam installation folder
	"""
	if not check("steamDir"):
		save(None, "steamDir")# create the condif value in case it doesn't exist

	if not load("steamDir") is None:
		return load("steamDir")# return the folder
	elif platform == "win32":
		# get the steam directory from the windows registry
		# HKEY_CURRENT_USER\Software\Valve\Steam
		try:
			logger.debug("Opening windows registry...")
			with ConnectRegistry(None, HKEY_CURRENT_USER) as reg:
				aKey = OpenKey(reg, "Software\\Valve\\Steam")# open the steam folder in the windows registry
		except Exception as e:
			logger.critical("Can't open windows registry! this is *VERY* bad!", exc_info=1)
			raise Exception(e)
		try:
			keyValue = QueryValueEx(aKey, "SteamPath")# find the steam path
			save(keyValue[0], "steamDir")# save the path, so we don't have to redo all this
			return keyValue[0]
		except:
			raise KeyError("Can't open/find the steam registry keys")

def portalDir() -> str:
	if not load("portal2Dir") is None:
		return load("portal2Dir")# check if we already saved the path, in case, return it
	else:
		# check every library if has p2 installed in it
		library = libraryFolders()
		for path in library:
			try:
				LOGGER.info(f'searching in {path}..')
				with open(path + "appmanifest_620.acf", "r") as file:
					pass
				# if yes save it
				path += "common/Portal 2/"
				LOGGER.info(f'portal 2 found! path: {path}')
				save(path, "portal2Dir")
				return path
			except:
				# if no, just continue
				continue
	

discordToken = "655075172767760384"
			
def libraryFolders() -> list:
	paths = []# create a list for library paths
	paths.append(steamDir() + "/steamapps/")# add the default
	try:
		# open the file that contains the library paths
		with open(steamDir() + "/steamapps/libraryfolders.vdf", "r") as file:
			library = Property.parse(file, "libraryfolders.vdf").as_dict()
			# remove useless stuff
			library.pop("TimeNextStatsReport")
			library.pop("ContentStatsID")
	except:
		raise Exception("Error while reading steam library file")

	# check for other library paths, if the dict is empty, there's no one
	if not len(library) is 0:
		for i in len(library):
			paths.append(library[str(i)] + "/steamapps/")# append the path
	
	# return the "compiled" list of libraries
	return paths

def steamUsername():
	try:
		with ConnectRegistry(None, HKEY_CURRENT_USER) as reg:
			aKey = OpenKey(reg, "Software\\Valve\\Steam")
	except Exception as e:
		raise Exception(e)
	try:
		keyValue = QueryValueEx(aKey, "LastGameNameUsed")
		return keyValue[0]
	except:
		return None
		
def checkUpdates() -> bool:
	if not isonline():
		return False
	ov=get('https://api.github.com/repos/ENDERZOMBI102/BEE-manipulator/releases/latest').json()
	url = ov["assets"][0]["browser_download_url"]
	ov = ov['tag_name']
	# loads and format the online version
	onlineVersion = toNumbers(ov)
	# loads and format the app version config
	appVersion = toNumbers(load('appVersion'))
	# here's the actual check
	if  appVersion < onlineVersion:
		save("true", "lastVersion")
		return True
	else:
		save("false", "lastVersion")
		save(onlineVersion, "onlineAppVersion")
		save(url, "newVersionUrl")
		return False

def version():
	return load("appVersion")

def onlineVersion():
	return load("onlineAppVersion")


class configError(BaseException):
	r"""
	base error for config operations
	"""

if __name__ == "__main__":
	print(portalDir())
			
			
