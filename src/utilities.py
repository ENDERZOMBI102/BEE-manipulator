import os
import sys
from io import BytesIO
from pathlib import Path
from sys import platform
from typing import Union

import wx
from requests import get, RequestException
from semver import VersionInfo

if __name__ == '__main__':
	from localization import loc
import config
from srctools.logger import get_logger

logger = get_logger("utils")
icon: wx.Icon
"""BEE Manipulator icon as wx.Icon object"""


class wxStyles:
	TITLEBAR_ONLY_BUTTON_CLOSE = wx.DEFAULT_FRAME_STYLE ^ wx.MINIMIZE_BOX ^ wx.MAXIMIZE_BOX


class UpdateInfo:

	version: VersionInfo
	url: str
	description: str

	def __init__(self, ver: VersionInfo, url: str, desc: str):
		self.version = ver
		self.url = url
		self.description = desc


def _App__setIcon():
	global icon
	icon = wx.Icon(f'{config.resourcesPath}icons/icon.png' )


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


def checkUpdate(url: str, curVer: VersionInfo) -> UpdateInfo:
	"""
	A function that check for updates, this doesn't include prereleases
	:param url: the api/repo github url
	:param curVer: current version
	:return: an object of class VersionInfo
	"""
	logger.debug(f'checking url..')
	if 'api.github' not in url:
		logger.debug(f'converting url..')
		url = genReleasesApiUrl(url)  # convert normal github repo url to github api url
	logger.debug(f'url valid!')
	logger.debug(f'checking updates on url: {url}')
	data: dict = get( url ).json()  # get the latest release data
	if not isinstance(data, list):
		return UpdateInfo( None, None, None )
	usePrereleases: bool = config.load('usePrereleases')
	for ver in data:
		if ver['draft'] is True:
			continue
		if ( ver['prerelease'] is True ) and ( usePrereleases is False ):
			continue
		data = ver
		break
	if isinstance(data, list):
		return UpdateInfo( None, None, None )
	# variables
	releaseUrl: str = None
	releaseVer: VersionInfo = None
	releaseDesc: str = None
	# special edge-case
	ov = data['tag_name'] if 'BEEmod' not in url else data['tag_name'].replace('2.4', '4', 1)
	# if the most recent release is not a greater one,
	# we just return a UpdateInfo object with every value setted to None
	# else we return a "complete" UpdateInfo object
	if VersionInfo.parse( ov ) > curVer:
		releaseUrl = getReleaseUrl(data)
		releaseVer = VersionInfo.parse( ov )
		releaseDesc = data['body']
	return UpdateInfo( releaseVer, releaseUrl, releaseDesc )


def genReleasesApiUrl(url: str = None) -> str:
	"""
	A function that makes a github api latest release url from a repo url
	aram url: repo url to be transformed
	:return: the github api url
	"""
	splitUrl = url.split('/')  # slit the url in various segments
	return f'https://api.github.com/repos/{splitUrl[3]}/{splitUrl[4]}/releases'  # return the formed url


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


def Downloader(url: str, title: str, message: str, animadots: bool = True) -> BytesIO:
	"""

	:param url: url of the file to download
	:param title: the title of the popup
	:param message: the message of the popup
	:param animadots: if the message has animated dots (defaults to True)
	:return: a buffer with the downloaded bytes
	"""
	dots = 1
	showProgress = config.dynConfig['logDownloadProgress']
	if showProgress is None:
		showProgress = False
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
	bytesdata = BytesIO()  # downloaded bytes
	dl = 0  # how much has been downloaded
	total_length = int(request.headers.get('content-length'))  # total length of the download (bytes)
	# download!
	if showProgress is True:
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
		if showProgress is True:
			logger.info(f'total: {total_length}, bytes done: {dl}, done: {done}%')
		# update with total % done and the message
		dialog.Update(done, newmsg=messageWdots)
	return bytesdata


def frozen() -> bool:
	"""
	if BM is in a frozen state (exe), returns True
	:return: true if it is, otherwise false
	"""
	if getattr(sys, 'frozen', False):
		return True
	else:
		return False


def removeDir(path):
	"""
	remove a folder, including all the files/folders it contains
	:param path: removes a given directory
	"""
	try:
		config.dynConfig['logDeletions']
	except KeyError:
		config.dynConfig['logDeletions'] = True
	# cycle in all subfolders/files
	for file in Path( path ).glob('*'):
		if file.is_dir():
			# RECURSION POWA
			removeDir( file )
		else:
			# remove the file
			os.remove( file )
			if config.dynConfig['logDeletions']:
				logger.debug(f'deleting {file.resolve()}')
	# remove all directories
	for file in Path( path ).glob('*'):
		os.rmdir( file )
		if config.dynConfig['logDeletions']:
			logger.debug(f'deleting {file.resolve()}')
	# and finally, remove the given directory
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
	# gets the BEE path
	if Path(f'{defBeePath}/BEE2/BEE2.exe').exists():
		return f'{defBeePath}/BEE2/'  # the exe file exists, bee has been installed, but the BM config was deleted
	return None


def notimplementedyet():
	"""
	shows a dialog that says that this feature its not implemented
	"""
	wx.GenericMessageDialog(
		parent=wx.GetActiveWindow(),
		message=loc('popup.notimplemented.text'),
		caption=loc('popup.notimplemented.title'),
		style=wx.ICON_INFORMATION | wx.STAY_ON_TOP | wx.OK
	).ShowModal()


def parseValue( param: str ) -> Union[str, int, float, None, bool]:
	if ( param == '' ) or ( param in ['none', 'None'] ):
		return None
	elif param.isdecimal():
		return int( param )
	elif param in 'trueTrueyesYes':
		return True
	elif param in 'falseFalsenoNo':
		return False
	for char in param:
		if char not in '0123456789.':
			return param
	return float( param )


def registerProtocol():
	regCode = r"""
		Windows Registry Editor Version 5.00

		[HKEY_CLASSES_ROOT\bm]
		@="URL:bm"
		"URL Protocol"=""

		[HKEY_CLASSES_ROOT\bm\shell]

		[HKEY_CLASSES_ROOT\bm\shell\open]

		[HKEY_CLASSES_ROOT\bm\shell\open\command]
		@="\"{exe} --bmurl\" \"%1\""
	""".replace( '\t', '' ).replace( '\n', '', 1 ).format( exe=sys.executable.replace( '\\', '\\\\' ) )
	Path( config.load('cachePath') ).mkdir( exist_ok=True )
	regFile = Path( f'{config.load( "cachePath" )}/protocol.reg' )
	regFile.touch( exist_ok=True )
	regFile.write_text( regCode )
	os.system( f'{str( regFile )}' )


defBeePath = str( Path( str( Path( os.getenv('appdata') ).parent ) + '/Local/Programs/').resolve() ).replace(r'\\', '/')
devEnv: bool = False
