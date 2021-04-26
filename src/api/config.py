from typing import Any, Dict, List


def load(section: str, default=None, useDisk=False) -> [str, int, bool, None, dict, list]:
	"""
	loads a section of the config (json-formatted) and return the data.
	raise an exception if the config or the requested section doesn't exist
	example::

		>>> import config
		>>> print( config.load('version') )
		2.6
	:param default: if no value is found, return this value
	:param section: section of the config to read
	:param useDisk: force to read config from disk
	:returns: the readed data
	"""


def save(data, section):
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


def overwrite(section: str, data: any) -> None:
	"""
	overwrite in run time a config
	:param section: the section that has to be overwritten
	:param data: the value the section is overwritten with
	"""


dynConfig: Dict[str, Any]
""" contains fast-access, volatile data """


def steamDir() -> str:
	"""
	a function that retrieves the steam installation folder by reading the win registry
	:return: path to steam folder
	:raises KeyError:
	"""


def portalDir() -> str:
	"""
	a function that retrieves the portal 2 folder by searching in all possible libraries
	:return: path to p2 folder
	:raises FileNotFoundError:
	"""


def libraryFolders() -> List[str]:
	"""
	Retrieves the steam library folders by parsing the libraryfolders.vdf file
	:return: a list with all library paths
	"""


def steamUsername() -> str:
	"""
	Retrieves the steam username
	:return: steam username
	"""


class ConfigError(BaseException):
	""" Base error for config operations """
