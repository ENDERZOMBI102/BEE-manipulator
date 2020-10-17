import json
from pathlib import Path
from sys import argv
from typing import Dict, Union, Any
from winreg import QueryValueEx, ConnectRegistry, HKEY_CURRENT_USER, OpenKey

from semver import VersionInfo

import utilities
from srctools import Property
from srctools.logger import get_logger

logger = get_logger()
overwriteDict: dict = {}
configPath: Path = Path( './config.cfg' if utilities.frozen() else './../config.cfg' )
assetsPath: str = './assets/' if utilities.frozen() else './../assets/'
"""the path to the assets folder (finishes with /)"""
pluginsPath: str = './plugins' if utilities.frozen() else './../plugins'
version: VersionInfo = VersionInfo(
	major=1,
	minor=0,
	patch=0,
	prerelease='pre3'
)
"""current app version"""

default_config = {
	'config_type': 'BEE2.4 Manipulator Config File',
	'usePrereleases': False if utilities.frozen() else True,
	'steamDir': None,
	'portal2Dir': None,
	'beePath': utilities.__getbee(),
	'beeVersion': None,
	'logWindowVisibility': False,
	'logLevel': 'info',
	'l18nFolderPath': './langs' if utilities.frozen() else './../langs',
	'databasePath': './assets/database.json' if utilities.frozen() else './../assets/database.json',
	'pluginsPath': './plugins' if utilities.frozen() else './../plugins',
	'onlineDatabaseUrl': 'https://hateitapp.ddns.net:8000/api/',
	'lang': 'en_US',
	'showVerifyDialog': False,
	'showUninstallDialog': False,
	'startupUpdateCheck': False,
	"showSplashScreen": False
}


currentConfigData: Dict[str, Any] = {}
_timesSaved: int = 0


def createConfig():
	"""
		a simple function that make the config file
	"""
	with open(configPath, 'w', encoding='utf-8') as file:
		json.dump(default_config, file, indent=3)


def load(section: str, default=None, useDisk=False) -> Union[str, int, bool, None, dict, list]:  # load a config
	"""
	loads a section of the config (json-formatted) and return the data.
	raise an exception if the config or the requested section doesn't exist
	example::

		>>> import config
		>>> print(config.load('version'))
		2.6
	:param default: if no value is found, return this value
	:param section: section of the config to read
	:returns: the readed data
	"""
	if section in overwriteDict.keys():
		logger.debug('using overwrited data!')
		return overwriteDict[section]
	# is that section present?
	if section in currentConfigData.keys() and not useDisk:
		if '--sayconfig' in argv:
			logger.info( f'{section}: {currentConfigData[ section ]}' )
		return currentConfigData[section]
	elif useDisk:
		# the config file exists?
		if configPath.exists():
			# yes, use it to load the configs
			with open( configPath, 'r', encoding='utf-8' ) as file:
				config = json.load(file)  # load the config
				readeData = config[section]  # take the requested field
			if '--sayconfig' in argv:
				logger.info(f'{section}: {readeData}')
			return readeData  # return the readed data
	# if the caller setted a default value, return it
	if default is not None:
		return default
	# if we have the searched section in the default config, return it
	elif section in default_config:
		logger.warning(f"can't load {section} from config file, using default")
		return default_config[section]
	# nothing worked, raise an error
	else:
		logger.error(f"can't load {section} from config file")
		raise ConfigError(f'{section} not found')


def save(data, section):  # save a config
	"""
	save the data on the config (json-formatted), re-create the config if no one is found.
	example::
		>>> import config
		>>> print(config.load('version'))
		'2.6'
		>>> config.save('2.5','version')
		>>> print(config.load('version'))
		'2.5'
	:param data: the data to save
	:param section: the section of the config to save the data to
	"""
	if '--sayconfig' in argv:
		logger.info( f'{section}: {data}' )
	# save
	currentConfigData[section] = data
	logger.debug( f'saved {section}' )
	# save to disk if this is the third save
	global _timesSaved
	if _timesSaved == 0 or _timesSaved == 1:
		_timesSaved += 1
	else:
		_timesSaved = 0
		try:
			# save to disk
			with open( configPath, 'w', encoding='utf-8' ) as file:
				json.dump( currentConfigData, file, indent=4 )
		except:
			logger.error( f'failed to save config to disk!' )
			raise ConfigError( 'error while saving the config' )


def saveAll(cfg: dict = None):

	"""
	A function that saves (and overwrites) the config file
	:param cfg: the config dict
	"""
	if ( cfg is None ) or ( 'config_type' != 'BEE2.4 Manipulator Config File' ):
		raise ValueError("parameter cfg can't be an invalid config!")
	try:
		with open(configPath, 'w', encoding='utf-8') as file:
			json.dump(cfg, file, indent=3)
	except:
		logger.error('An error happened while saving config file, probably is now corrupted')


def check(cfg: dict = None) -> bool:

	"""
	check if the config file exist and if is a BM config file
	:param cfg: optional string to use instead of reopening from the file system
	:return: True if is a valid config
	"""
	if cfg is None:
		try:
			with open(configPath, 'r') as file:
				cfg = json.load(file)  # load the file
		except FileNotFoundError:
			return False
	# check if EVERY config exists
	for i in default_config.keys():
		if i in cfg.keys():
			continue
		return False
	# final check
	if cfg['config_type'] == 'BEE2.4 Manipulator Config File':
		# the check is made successfully
		return True
	else:
		# the config file is not a BM config file
		return False


def overwrite(section: str, data: any) -> None:

	"""
	overwrite in run time a config
	:param section: the section that has to be overwritten
	:param data: the value the section is overwritten with
	:return: None
	"""
	overwriteDict[section] = data
	logger.debug(f'Overwritten config {section}!')


class __dynConfig:
	"""
	a class that contains run-time configs, that requires fast access.
	THIS IS NEVER SAVED TO DISK
	"""

	__configs: Dict[str, any] = {}

	def __init__(self):
		pass

	def __getitem__(self, item):
		if self.__configs[item]:
			return self.__configs[item]
		else:
			return None

	def __setitem__(self, key, value):
		self.__configs[key] = value


dynConfig: __dynConfig = __dynConfig()
"""contains fast-access, volatile data"""

# dynamic/static configs


def steamDir() -> str:

	"""
	a function that retrieves the steam installation folder by reading the win registry
	:return: path to steam folder
	"""
	if 'steamDir' not in currentConfigData.keys():
		save(None, 'steamDir')  # create the config without value in case it doesn't exist

	if not load('steamDir') is None:
		return load('steamDir')  # return the folder
	elif utilities.platform == 'win32':
		# get the steam directory from the windows registry
		# HKEY_CURRENT_USER\Software\Valve\Steam
		try:
			logger.debug('Opening windows registry...')
			with ConnectRegistry(None, HKEY_CURRENT_USER) as reg:
				aKey = OpenKey(reg, r'Software\Valve\Steam')  # open the steam folder in the windows registry
		except Exception as e:
			logger.critical("Can't open windows registry! this is *VERY* bad!", exc_info=True)
			raise Exception(e)
		try:
			keyValue = QueryValueEx(aKey, 'SteamPath')  # find the steam path
			save(keyValue[0], 'steamDir')  # save the path, so we don't have to redo all this
			return keyValue[0]
		except:
			raise KeyError("Can't open/find the steam registry keys")


def portalDir() -> str:

	"""
	a function that retrives the portal 2 folder by searching in all possible libraries
	:return: path to p2 folder
	"""
	if not load('portal2Dir') is None:
		return load('portal2Dir')  # check if we already saved the path, in case, return it
	else:
		# check every library if has p2 installed in it
		library = libraryFolders()
		for path in library:
			try:
				logger.info(f'searching in {path}..')
				with open(path + 'appmanifest_620.acf', 'r') as file:
					pass
				# if yes save it
				path += 'common/Portal 2/'
				logger.info(f'portal 2 found! path: {path}')
				save(path, 'portal2Dir')
				return path
			except FileNotFoundError:
				# if no, just continue
				continue


discordToken: str = '655075172767760384'


def libraryFolders() -> list:

	"""
	retrives the steam library folders by parsing the libraryfolders.vdf file
	:return: a list with all library paths
	"""
	paths = [steamDir() + '/steamapps/']  # create a list for library paths
	try:
		# open the file that contains the library paths
		with open(steamDir() + '/steamapps/libraryfolders.vdf', 'r') as file:
			library = Property.parse(file, 'libraryfolders.vdf').as_dict()
			# remove useless stuff
			library['libraryfolders'].pop('timenextstatsreport')
			library['libraryfolders'].pop('contentstatsid')
	except Exception as e:
		raise Exception(f'Error while reading steam library file: {e}')

	# check for other library paths, if the dict is empty, there's no one
	if len(library['libraryfolders']) != 0:
		for i in len(library['libraryfolders']):
			paths.append(library['libraryfolders'][str(i)] + '/steamapps/')  # append the path

	# return the "compiled" list of libraries
	return paths


def steamUsername():

	"""
	retrives the steam username
	:return: steam username
	"""
	try:
		with ConnectRegistry(None, HKEY_CURRENT_USER) as reg:
			aKey = OpenKey(reg, r'Software\Valve\Steam')
	except Exception as e:
		raise Exception(e)
	try:
		keyValue = QueryValueEx(aKey, 'LastGameNameUsed')
		return keyValue[0]
	except:
		return None


def devMode() -> bool:
	return utilities.boolcmp( load('devMode') )


class ConfigError(BaseException):
	r"""
	base error for config operations
	"""


if __name__ == '__main__':
	print(steamUsername())
	print(portalDir())
