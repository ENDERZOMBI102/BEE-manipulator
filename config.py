import json# for manipulating json files
from os import path# for open files
from sys import platform# for knowing where the file is executed on
from requests import get# for the the connection
from srctools.property_parser import Property# for parse vdfs files
from srctools.logger import get_logger
from utilities import *
from winreg import *

logger = get_logger("config")

def createConfig():
	r"""
		a "simple" function that make the config file
	"""
	cfg={
			"config_type": "BEE2.4 Manipulator Config File",
			"appVersion": "0.0.1",
			"lastVersion": False,
			"beePrereleases":False,
			"beeUpdateUrl": None,
			"steamDir":None,
			"portal2Dir":None,
			"beePath": None,
			"logLevel": "info"
		}
	with open('config.cfg', 'w', encoding="utf-8") as file:
		json.dump(cfg, file, indent=3)

def load(section):# load a config
	r"""
	loads a section of the config (json-formatted) and return the data.
	raise an exception if the config or the requested section doesn't exist
	example::

		>>> import config
		>>> print(config.load("version"))
		'2.6'
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
	check()
	try:
		with open('config.cfg', 'r', encoding="utf-8") as file:
			cfg = json.load(file)# load the config file
			cfg[section]=data
		with open('config.cfg', 'w', encoding="utf-8") as file:
			json.dump(cfg, file, indent=3)
	except:
		raise configError("error while saving the config")

def check(arg = None):
	r"""
	if no aurgment is present check if the config file exist and if is a BM config file, else will
	check if the given section exists.
	"""
	try:
		with open('config.cfg', 'r') as file:
			cfg = json.load(file)
			return True
	except:
		return False
	if arg is None:# check the aurgment is present
		try:
			# check if EVERY config exists
			x = cfg["beePrereleases"]
			x = cfg["appVersion"]
			x = cfg["lastVersion"]
			x = cfg["beePrereleases"]
			x = cfg["beeUpdateUrl"]
			x = cfg["steamDir"]
			x = cfg["portal2Dir"]
			x = cfg['config_type']
		except:
			# the config file is not a BM config file
			return False
		# final check
		if cfg['config_type'] == "BEE2.4 Manipulator Config File":
			# the check is made successfully
			return True
		else:
			# the config file is not a BM config file
			return False
	try:
		with open("config.cfg", 'r') as file:  # try to open the config file
			cfg = json.load(file) # load the config file
			if cfg[arg]:
				return True
			else:
				return False
	except:
		createConfig()


 # dynamic/static configs
def osType():
	return platform

def steamDir( cmde = False):
	r"""
		this function return the steam installation folder
	"""
	if check("steamDir"):
		pass

	if not load("steamDir") is None:
		return load("steamDir")
	elif platform == "win32":
		# get the steam directory from the windows registry
		# HKEY_CURRENT_USER\Software\Valve\Steam
		try:
			with ConnectRegistry(None, HKEY_CURRENT_USER) as reg:
				aKey = OpenKey(reg, r"Software\Valve\Steam")
		except Exception as e:
			raise Exception(e)
		try:
			keyValue = QueryValueEx(aKey, "SteamPath")
			save(keyValue[0], "steamDir")
			return keyValue[0]
		except:
			return "Error while reading registry"

def portalDir():
	if not load("portal2Dir") is None:
		return load("portal2Dir")
	else:
		# check every library if has p2 installed in it
		library = libraryFolders()
		for path in library:
			try:
				with open(path + "appmanifest_620.acf", "r") as file:
					print(path)
					pass
				# if yes save it
				save(path + "common/Portal 2/", "portal2Dir")
				return path + "common/Portal 2/"
			except:
				# if no, just continue
				continue
	

discordToken = "655075172767760384"
			
def libraryFolders():
	paths = []# create a list for library paths
	paths.append(steamDir() + "/steamapps/")# add the default
	try:
		with open(steamDir() + "/steamapps/libraryfolders.vdf", "r") as file:
			library = Property.parse(file, "libraryfolders.vdf").as_dict()
			try:
				# check for other libraries
				for i in range(10):
					paths.append(library[str(i)] + "/steamapps/")
			except:
				pass
	except:
		raise Exception("Error while reading steam library file")
	# return the "compiled" list of libraries
	return paths

def steamUsername():
	try:
		with ConnectRegistry(None, HKEY_CURRENT_USER) as reg:
			aKey = OpenKey(reg, r"Software\\Valve\\Steam")
	except Exception as e:
		raise Exception(e)
	try:
		keyValue = QueryValueEx(aKey, "LastGameNameUsed")
		return keyValue[0]
	except:
		return None
		
def checkUpdates():
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
			
			
