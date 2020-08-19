import io
import os
import sys
from pathlib import Path
from sys import platform
from typing import Union, Tuple

import wx
from requests import get, RequestException

import config
from srctools.logger import get_logger

logger = get_logger("utils")


def boolcmp(value: Union[bool, int, str]) -> bool:
	"""
	function to evaluate string or numbers to bool values
	:param value: the value to compare
	:return: if the value may represents a false return False, else true
	"""
	logger.debug(f'converting "{value}" to boolean!')
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
		logger.debug('checking connection..')
		get('https://www.google.com/')
		get('https://github.com/')
		return True
	except RequestException:
		return False


def keyExist(data: dict, key: str):
	"""
	check if a dictionary has a key
	:param data: dictionary to check
	:param key: the key to check
	:return:
	"""
	logger.debug(f'checking key "{key}"')
	try:
		data[key]
		return True
	except KeyError:
		return False


def toNumbers(arg=None):
	nums = []
	for i in arg:
		if i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.']:
			nums.append(i)
	return int(''.join(nums))


def checkUpdate(url: str, curVer: str) -> Union[Tuple[bool, str, int], Tuple[bool, None, None]]:
	"""
	A function that check for updates, this doesn't include prereleases
	:param url: the api/repo github url
	:param curVer: current version
	:return: true or false
	"""
	logger.debug(f'checking url..')
	if 'api.github' not in url:
		logger.debug(f'converting url..')
		url = genApiUrl(url)  # convert normal github repo url to github api url
	logger.debug(f'url valid!')
	logger.debug(f'checking updates on url: {url}')
	data = get(url).json()  # get the latest release data
	if 'documentation_url' in data.keys():
		return False, None, None
	# variables
	available: bool = True
	releaseUrl: str = None
	# first we convert the tag name to an int
	# then we compare it with the given current version
	if versioncmp(data['tag_name'], curVer):
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


def versioncmp(ver0: str, ver1: str):
	"""
	do a ver0 > ver1 comparison, three . separated values
	:param ver0: version base
	:param ver1: version to compare
	:return: ver0 > ver1
	"""
	ver0 = ver0.replace('.', '')
	ver1 = ver1.replace('.', '')
	if (int(ver0[0]) > int(ver1[0])) or (int(ver0[1]) > int(ver1[1])) or (int(ver0[2]) > int(ver1[2])):
		return True
	return False


def isnegative(value: Union[None, bool]) -> bool:
	"""
	a function that checks if a value is negative (None, False, 0)
	:param value:
	:return:
	"""
	if value is None:
		return True
	else:
		return not value


def Downloader(url: str, title: str, message: str, animadots: bool = True) -> bytes:
	"""

	:param url: url of the file to download
	:param title: the title of the popup
	:param message: the message of the popup
	:param animadots: if the message has animated dots (defaults to True)
	:return:
	"""
	dots = 1
	showProgress = config.dynConfig['logDownloadProgress']
	# create progress dialog
	dialog = wx.ProgressDialog(
		parent=wx.GetTopLevelWindows()[0],
		title=title,
		message=message,
		maximum=100
	)
	dialog.Update(0)  # update to 0 so it doesn't glitch
	# working variables
	messageWdots = message  # defaulting to the message
	request = get(url, stream=True)  # the request
	bytesdata = io.BytesIO()  # downloaded bytes
	dl = 0  # how much has been downloaded
	total_length = int(request.headers.get('content-length'))  # total length of the download (bytes)
	# download!
	if (showProgress is True) and (showProgress is not None):
		logger.info(f'downloading {url}!')
	for data in request.iter_content(chunk_size=1024):
		dl += len(data)
		bytesdata.write(data)
		done = int(100 * dl / total_length)
		if animadots:
			# set the message with dots for the animation
			if dots == 1:
				dots = 2
				messageWdots = message + '.'
			elif dots == 2:
				dots = 3
				messageWdots = message + '..'
			elif dots == 3:
				dots = 1
				messageWdots = message + '...'
		# if showProgress is true, show the progress on the log
		if (showProgress is True) and (showProgress is not None):
			logger.info(f'total: {total_length}, bytes done: {dl}, done: {done}%')
		# update with total % done and the message
		dialog.Update(done, newmsg=messageWdots)
	return bytesdata.read()


def frozen() -> bool:
	"""
	if BM is in a frozen state (exe), returns True
	:return: bool
	"""
	if getattr(sys, 'frozen', False):
		return True
	else:
		return False


def removeDir(path):
	"""
	remove a folder, including all the files/folders it contains
	:param path:
	:return:
	"""
	try:
		config.dynConfig['logDeletions']
	except:
		config.dynConfig['logDeletions'] = True
	for file in Path( path ).glob('*'):
		if file.is_dir():
			removeDir( file )
		else:
			os.remove( file )
			if config.dynConfig['logDeletions']:
				logger.debug(f'deleting {file.resolve()}')
	for file in Path( path ).glob('*'):
		os.rmdir( file )
		if config.dynConfig['logDeletions']:
			logger.debug(f'deleting {file.resolve()}')
	os.rmdir( path )


def tempDirPath() -> str:
	if frozen():
		path = './../temp/'  # frozen
	else:
		path = './temp/'  # not frozen
	fdr = Path(path)
	if not fdr.exists():
		fdr.mkdir()
	return path


def __getbee() -> Union[None, str]:
	if Path(f'{defBeePath}/BEE2/BEE2.exe').exists():
		return f'{defBeePath}/BEE2/BEE2.exe'  # the exe file exists, bee has been installed, but the BM config was deleted
	return None


def notimplementedyet():
	"""
	not implemented error
	:return:
	"""
	wx.GenericMessageDialog(
		parent=wx.GetActiveWindow(),
		message='This feature is not yet implemented, return later!',
		caption='Not implemented',
		style=wx.ICON_INFORMATION | wx.STAY_ON_TOP | wx.OK
	).ShowModal()


defBeePath = str( Path( str( Path( os.getenv('appdata') ).parent ) + '/Local/Programs/').resolve() ).replace(r'\\', '/')
env = 'dist'
root: wx.Frame = None


if __name__ == '__main__':
	pass



