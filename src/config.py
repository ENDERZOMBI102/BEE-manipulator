import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from semver import VersionInfo

import utilities
from srctools import Property
from srctools.logger import get_logger
from srctools.tokenizer import TokenSyntaxError

logger = get_logger()
overwriteDict: dict = {}
configPath: Path = Path( './config.cfg' )
resourcesPath: str = './resources'
""" The path to the assets folder """
version: VersionInfo = VersionInfo(
	major=1,
	minor=0,
	patch=0,
	prerelease='pre3',
	build='build0'
)
""" current app version """

default_config = {
	'config_type': 'BEE2.4 Manipulator Config File',
	'usePrereleases': False if utilities.frozen() else True,
	'steamDir': None,
	'portal2Dir': None,
	'beePath': utilities.__getbee(),
	'beeVersion': None,
	'logWindowVisibility': False,
	'logLevel': 'info',
	'l18nFolderPath': './langs',
	'databasePath': f'{resourcesPath}/database.json',
	'pluginsPath': './plugins',
	'cachePath': f'{resourcesPath}/cache',
	'rpcReconnectTime': 30,
	'onlineDatabaseUrl': '',
	'lang': 'en_US',
	'showVerifyDialog': True,
	'showUninstallDialog': True,
	'startupUpdateCheck': True,
	'showSplashScreen': False,
	'nextLaunch': {}
}


currentConfigData: Dict[str, Any] = {}
_timesSaved: int = 0


def createConfig():
	"""
		a simple function that make the config file
	"""
	with open(configPath, 'w', encoding='utf-8') as file:
		json.dump(default_config, file, indent=3)


def load(section: str, default=None, useDisk=False) -> [str, int, bool, None, dict, list]:  # load a config
	"""
	loads a section of the config (json-formatted) and return the data.
	raise an exception if the config or the requested section doesn't exist
	example::

		>>> import config
		>>> print( config.load('version') )
		2.6
	\t
	:param default: if no value is found, return this value
	:param section: section of the config to read
	:param useDisk: force to read config from disk
	:returns: the readed data
	"""
	if section in overwriteDict.keys():
		logger.debug('using overwrited data!')
		return overwriteDict[section]
	# is that section present?
	if section in currentConfigData.keys() and not useDisk:
		if dynConfig['logConfigActions']:
			logger.info( f'loading {section}: {currentConfigData[ section ]}' )
		return currentConfigData[section]
	elif useDisk:
		# the config file exists?
		if configPath.exists():
			# yes, use it to load the configs
			with open( configPath, 'r', encoding='utf-8' ) as file:
				config = json.load(file)  # load the config
				readeData = config[section]  # take the requested field
			if dynConfig['logConfigActions']:
				logger.info(f'loading {section}: {readeData}')
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
	\t
	:param data: the data to save
	:param section: the section of the config to save the data to
	"""
	global _timesSaved
	if dynConfig['logConfigActions']:
		logger.info( f'saving {section}: {data}' )
	# save
	if section != 'placeholderForSaving':
		currentConfigData[section] = data
		logger.debug( f'saved {section}' )
	else:
		_timesSaved = 2
	# save to disk if this is the third save
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


def check() -> bool:
	"""
	Check if the config file exist and if is a BM config file
	\t
	:return: True if is a valid config
	"""
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
	return cfg['config_type'] == default_config['config_type']


def overwrite(section: str, data: any) -> None:
	"""
	Overwrite in run time a config
	\t
	:param section: the section that has to be overwritten
	:param data: the value the section is overwritten with
	"""
	overwriteDict[section] = data
	logger.debug(f'Overwritten config {section}!')


class __dynConfig:
	"""
	a class that contains run-time configs, that requires fast access.
	THIS IS NEVER SAVED TO DISK
	"""

	__flags: Dict[ str, Any ]

	def __init__(self) -> None:
		self.__flags = {}

	def parseFlags( self, rawFlags: str ):
		flags: List[ List[str] ] = [ flag.split('=') for flag in rawFlags.split( ';' ) ]
		self.__flags = {flag[0 ]: utilities.parseValue( flag[1 ] ) for flag in flags}

	def __getitem__(self, item):
		return self.__flags.get( item, None )

	def __setitem__(self, key, value):
		self.__flags[key] = value


dynConfig: __dynConfig = __dynConfig()
""" contains fast-access, volatile data """


def overwriteOnNextLaunch(**kwargs) -> None:
	overwrites = load('nextLaunch')
	overwrites = { **overwrites, **kwargs }
	save('nextLaunch', overwrites)


# dynamic/static configs


def steamDir() -> str:
	"""
	a function that retrieves the steam installation folder by reading the win registry
	\t
	:return: path to steam folder
	:raises KeyError:
	"""
	steamFolder: str = ''
	if load('steamDir') is not None:
		return load('steamDir')  # return the folder
	elif utilities.platform == 'win32':
		from winreg import QueryValueEx, ConnectRegistry, HKEY_CURRENT_USER, OpenKey
		# get the steam directory from the windows registry
		# HKEY_CURRENT_USER\Software\Valve\Steam
		try:
			logger.debug('Opening windows registry...')
			with ConnectRegistry(None, HKEY_CURRENT_USER) as reg:
				aKey = OpenKey(reg, r'Software\Valve\Steam')  # open the steam folder in the windows registry
		except Exception as e:
			logger.critical("Can't open windows registry! this is *VERY* bad!", exc_info=e)
			raise
		try:
			keyValue = QueryValueEx(aKey, 'SteamPath')  # find the steam path
			steamFolder = keyValue[0]
		except:
			raise KeyError("Can't open/find the steam registry keys")
	elif utilities.platform == 'linux':
		# the steam folder is 99.9% of the times located a t this path
		# expand ~ to user folder path (/home/USERNAME/...)
		steamFolder = str( Path( '~/.steam/steam' ).expanduser() )

	if steamFolder:
		save( steamFolder, 'steamDir' )  # save the path, so we don't have to redo all this
		return steamFolder
	else:
		raise RuntimeError("Can't find the steam folder!")


def portalDir() -> str:
	"""
	A function that retrieves the portal 2 folder by searching in all possible libraries
	\t
	:return: path to p2 folder
	:raises FileNotFoundError:
	"""
	# check if we already saved the path, in case, return it
	if load('portal2Dir') is None:
		save( getSteamAppDir( 620 ), 'portal2Dir' )
	return load('portal2Dir')


def getSteamAppDir(appid: int) -> str:
	"""
	a function that retrieves the folder of an app by searching in all possible libraries
	\t
	:param appid: The app's id to search for
	:return: path to app's folder
	:raises RuntimeError: raised when the app is not found
	"""
	for path in libraryFolders():
		try:
			logger.info(f'searching for {appid} in {path}..')
			with open(f'{path}appmanifest_{appid}.acf', 'r') as file:
				# found the app!
				# get the app's name
				instDir = Property.parse( file, f'appmanifest_{appid}.acf' ).as_dict()[ 'appstate' ][ 'installdir' ]
				path += f'common/{instDir}/'
				logger.info(f'{appid} found! path: {path}')
				return path
		except FileNotFoundError:
			# if no, just continue
			continue
	raise RuntimeError(f'No path found for app {appid}!')


discordToken: str = '655075172767760384'


def libraryFolders() -> List[str]:
	"""
	Retrieves the steam library folders by parsing the libraryfolders.vdf file
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
		logger.error('Unexpected error while reading "libraryfolders.vdf", only default library will be available.', e)
		return paths

	# check for other library paths, if the dict is empty, there's no one
	if len( library['libraryfolders'] ) != 0:
		for i in range( len( library['libraryfolders'] ) ):
			paths.append( library['libraryfolders'][ i ] + '/steamapps/' )  # append the path

	# return the "compiled" list of libraries
	return paths


def steamUsername() -> Optional[str]:
	"""
	Retrieves the steam username
	\t
	:return: steam username
	"""
	try:
		with open( f'{steamDir()}/config/loginusers.vdf' ) as file:
			users = Property.parse( file, 'loginusers.vdf' ).as_dict()[ 'users' ]
		# find the first user in the users dict and take is username
		return users[ [ usr for usr in users.keys() ][ 0 ] ][ 'personaname' ]
	except ( FileNotFoundError, TokenSyntaxError ):
		return None


class ConfigError(BaseException):
	""" Base error for config operations """


if __name__ == '__main__':
	print(steamUsername())
	print(portalDir())
