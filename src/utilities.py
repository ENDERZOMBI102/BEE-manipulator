from sys import platform
from typing import Union, Tuple

import wx
from requests import get

from srctools.logger import get_logger

LOGGER = get_logger("utils")


def boolcmp(value: Union[bool, int, str] ) -> bool:

	"""
	function to evaluate string or numbers to bool values
	:param value: the value to compare
	:return: if the value may rappresents a false return False, else true
	"""
	LOGGER.debug(f'converting "{value}" to boolean!')
	if value in [True, 'true', 'yes', 1]:
		return True
	elif value in [False, 'false', 'no', 0]:
		return False
	elif isinstance(value, int):
		if value > 0:
			return True
		else:
			return False
	else:
		raise ValueError('invalid input!')


def isonline():

	"""
	simple function that checks if the pc is online or not
	:return: True if it is else False
	"""
	try:
		LOGGER.debug('checking connection..')
		get('https://www.google.com/')
		get('https://github.com/')
		return True
	except:
		return False


def keyExist(data: dict, key: str):

	"""
	check if a dictionary has a key
	:param data: dictionary to check
	:param key: the key to check
	:return:
	"""
	LOGGER.debug(f'checking key "{key}"')
	try:
		x = data[key]
		return True
	except KeyError:
		return False


def toNumbers(arg=None):
	nums = []
	for i in arg:
		if i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.']:
			nums.append(i)
	return int(''.join(nums))


def checkUpdate(url: str, curVer: str) -> Tuple[bool, str, int]:

	"""
	A function that check for updates, this doesn't include prereleases
	:param url: the api/repo github url
	:param curVer: current version
	:return: true or false
	"""
	LOGGER.debug(f'checking url..')
	if 'api.github' not in url:
		LOGGER.debug(f'converting url..')
		url = genApiUrl(url)  # convert normal github repo url to github api url
	LOGGER.debug(f'url valid!')
	LOGGER.debug(f'checking updates on url: {url}')
	data = get(url).json()  # get the latest release data
	if 'documentation_url' in data.keys():
		return False, None, None
	# variables
	available: bool = True
	releaseUrl: str = None
	# first we convert the tag name to an int
	# then we compare it with the given current version
	if versioncmp( data['tag_name'], curVer ):
		if not boolcmp(data["draft"]):  # check if the release is not a draft
			# not a draft
			available = True
			releaseUrl = getReleaseUrl(data)
	return available, releaseUrl, data['tag_name']


def genApiUrl(url: str = None) -> str:
	"""
	A function that makes a github api latest release url from a repo url
	:param url: repo url to be transformed
	:return: the github api url
	"""
	splitUrl = url.split('/')  # slit the url in various segments
	return f'https://api.github.com/repos/{splitUrl[3]}/{splitUrl[4]}/releases/latest'  # return the formed url


def getReleaseUrl(data) -> str:
	"""
	a function that return the correct release for the platform
	:param data: the latest release data
	:return: the asset url
	"""
	# if there's a single asset, we can't fail
	if len(data['assets']) == 1:
		return data['assets'][0]['browser_download_url']
	# cycle in the assets
	for asset in data['assets']:
		# get the correct url for the OS we're on
		if 'mac' in asset['name'] and 'darwin' in platform:
			return asset['browser_download_url']
		elif 'win' in asset['name'] and 'win' in platform:
			return asset['browser_download_url']
	raise Exception("how this happened?, you're on linux?")


def versioncmp( ver0: str, ver1: str):
	"""
	do a ver0 > ver1 comparation, three . separated values
	:param ver0: version base
	:param ver1: version to compare
	:return: ver0 > ver1
	"""
	ver0 = ver0.replace('.', '')
	ver1 = ver1.replace('.', '')
	if ( int(ver0[0]) > int(ver1[0]) ) or ( int(ver0[1]) > int(ver1[1]) ) or ( int(ver0[2]) > int(ver1[2]) ):
		return True
	return False


def GetMainWindow() -> wx.Frame:
	return wx.GetTopLevelWindows()[0]


env = 'dist'
root: wx.Frame = None
