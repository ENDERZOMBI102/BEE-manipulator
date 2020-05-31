from srctools.logger import get_logger
from typing import Union, Tuple
from requests import get
from sys import platform
import config
import wx

LOGGER = get_logger("utils")


def boolcmp(value: Union[bool, int, str] ) -> bool:
	r"""
	a small function to compare bool values
	"""
	LOGGER.debug(f'converting "{value}" to boolean!')
	if value in [True, 'true', 'yes', 1]:
		return True
	elif value in [False, 'false', 'no', 0]:
		return False
	else:
		raise ValueError('invalid input!')


def isonline():
	try:
		LOGGER.debug('checking connection..')
		get('https://www.google.com/')
		get('https://github.com/')
		return True
	except:
		return False


def keyExist(data: dict, key: str):
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


def checkUpdate(url: str = None, curVer: str = None) -> Tuple[bool, str, int]:
	"""
	A function that check for updates, this doesn't include prereleases
	:param url: the api/repo github url
	:param curVer: current version
	:return: true or false
	"""
	LOGGER.debug(f'checking params..')
	if ( url is None ) or ( curVer is None ):  # check if any of the parameters are None
		raise ValueError('missing one or all of the parameters')
	LOGGER.debug(f'params ok!')
	LOGGER.debug(f'checking url..')
	if 'api.github' not in url:
		LOGGER.debug(f'converting url..')
		url = genApiUrl(url)  # convert normal github repo url to github api url
	LOGGER.debug(f'url valid!')
	LOGGER.debug(f'checking updates on url: {url}')
	data = get(url).json()  # get the latest release data
	available: bool = True
	url: str = None
	# first we convert the tag name to an int
	# then we compare it with the given current version
	if toNumbers( data['tag_name'] ) > curVer:
		if not boolcmp(data["draft"]):  # check if the release is not a draft
			available = True
			url = getReleaseUrl(data)
	return available, url, toNumbers(data['tag_name'])


def genApiUrl(url: str = None) -> str:
	"""
	A function that makes a github api latest release url from a repo url
	:param url: repo url to be transformed
	:return: the github api url
	"""
	splitUrl = url.split('/')  # slit the url in varius segments
	return f'https://api.github.com/repos/{splitUrl[4]}/{splitUrl[5]}/releases/latest/'  # return the formed url


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

def versioncmp( ver0: str = None, ver1: str = None, operation: str = None ):



argv = []
root: wx.Frame = None
