import configparser
import io
import os
from pathlib import Path
from typing import Union
from zipfile import ZipFile

import wx
from requests import get
from semver import VersionInfo

import config
import utilities
from srctools.logger import get_logger

logger = get_logger()
beeRepoUrl: str = 'https://github.com/BEEmod/BEE2.4/'
beeApiUrl: str = 'https://api.github.com/repos/BEEmod/BEE2.4/releases/latest'
beePackagesApiUrl: str = 'https://api.github.com/repos/BEEmod/BEE2-items/releases/latest'


def checkAndInstallUpdate(firstInstall: bool = False) -> None:
	"""
	this function checks if BEE has an update, if so, ask the user if he wants to update it
	:return: None
	"""
	# load current bee version
	beeVersion: str = config.load('beeVersion')
	logger.info(f'installed BEE version: {beeVersion}')
	if firstInstall is False:
		# bee isn't installed, can't update
		if beeVersion is None:
			return
	# check updates
	data = utilities.checkUpdate(beeRepoUrl, VersionInfo.parse( beeVersion if firstInstall is False else '0.0.0') )
	logger.info(f'latest BEE version: {data.version}')
	if data.version is None:
		# no update available, can't update
		logger.info('no update available')
		return
	if not firstInstall:
		# show bee update available dialog
		dialog = wx.RichMessageDialog(
			parent=wx.GetTopLevelWindows()[0],
			message=f'BEE2.4 {data.version} is available for download, update now?\n{data.description}',
			caption='BEE update available!',
			style=wx.YES_NO | wx.YES_DEFAULT | wx.STAY_ON_TOP | wx.ICON_INFORMATION
		)
		choice = dialog.ShowModal()
		# if user says no, don't update
		if choice == wx.ID_NO:
			logger.debug('user cancelled install')
			return
	# user said yes
	logger.debug(f'updating from BEE {beeVersion} to BEE {data[2]}!')
	config.dynConfig['beeUpdateUrl'] = data[1]
	installBee()


def beeIsPresent() -> Union[ bool ]:
	"""
	returns true if bee2.exe is found in the beePath
	:returns: bool, bee path
	"""
	path = config.load('beePath')
	# path is none, bee isn't installed
	if path is None:
		# the exe file exists, bee has been installed, but the BM config was deleted
		if Path(f'{utilities.defBeePath}/BEE2/BEE2.exe').exists():
			return True
		return False
	# bee is installed
	elif Path(path+'/BEE2.exe').exists():
		return True
	else:
		return False


def installBee(ver: VersionInfo = None, folder: str = None):
	"""
	this will install/update BEE, when called, the function
	will download the latest version based on the os is running on and unzip it
	"""
	# create the progress dialog
	dialog = wx.ProgressDialog(
		parent=wx.GetTopLevelWindows()[0],
		title='Installing BEE2..',
		message='Downloading application..',
		maximum=100
	)
	if not beeIsPresent() or ver is not None:
		logger.info('downloading BEE2...')
		# get the zip binary data
		link: str = None
		if ver is None:
			link = config.dynConfig[ 'beeUpdateUrl' ]
		else:
			for tag in get( beeApiUrl.replace('/latest', '') ).json():
				if ver.compare( tag['tag_name'] ) == 0:
					link = tag['assets'][0]['browser_download_url']
		request = get( link, stream=True )  # download BEE
		# working variables
		zipdata = io.BytesIO()
		dialog.Update(0)
		dl = 0
		total_length = int( request.headers.get('content-length') )
		# download!
		for data in request.iter_content(chunk_size=1024):
			dl += len(data)
			zipdata.write(data)
			done = int(100 * dl / total_length)
			print(f'total: {total_length}, dl: {dl}, done: {done}')
			dialog.Update(done)
		logger.info('extracting...')
		dialog.Pulse('Extracting..')
		# read the data as bytes and then create the zipfile object from it
		ZipFile(zipdata).extractall( config.load('beePath') if folder is None else folder )  # extract BEE
		logger.info('BEE2.4 application installed!')
	dialog.Close()
	dialog = wx.ProgressDialog(
		parent=wx.GetTopLevelWindows()[0],
		title='Installing BEE2..',
		message='Downloading default packages..',
		maximum=100
	)
	# install default package pack
	# get the url
	dl_url = get(beePackagesApiUrl).json()['assets'][0]['browser_download_url']
	# get the zip as bytes
	logger.info('downloading default package pack...')
	request = get(dl_url, stream=True)
	# working variables
	zipdata = io.BytesIO()
	dialog.Update(0, newmsg='Downloading default pack..')
	dl = 0
	total_length = int(request.headers.get('content-length'))
	# download!
	for data in request.iter_content(chunk_size=1024):
		dl += len(data)
		zipdata.write(data)
		done = int(100 * dl / total_length)
		print(f'total: {total_length}, dl: {dl}, done: {done}')
		dialog.Update(done)
	logger.info('extracting...')
	dialog.Pulse('Extracting..')
	# convert to a byte stream, then zipfile object and then extract
	ZipFile(zipdata).extractall( config.load('beePath') if folder is None else folder)
	dialog.Close()
	logger.info('finished extracting!')
	logger.info('checking games config file..')
	if Path( os.getenv('APPDATA').replace('\\', '/') + '/BEEMOD2/config/games.cfg' ).exists():
		logger.info("config file exist, checking if has P2..")
		if not configManager.hasGameWithID(620):
			logger.warning("config doesn't have P2!")
			logger.info('adding portal 2 to config!')
			configManager.addGame( path=config.portalDir() )
	else:
		logger.warning("config file doesn't exist!")
		configManager.createAndAddGame( path=config.portalDir() )
	logger.info('finished installing BEE!')


def uninstall():
	"""
	uninstall BEE2.4
	:return: None
	"""
	path = config.load('beePath')
	logger.info('removing BEE2.4!')
	logger.info('deleting app files..')
	utilities.removeDir( path )
	config.save(None, 'beePath')
	logger.info('app files deleted!')


def verifyGameCache():
	# try to delete the bee2 folder ine p2 root dir
	pass


@property
def packageFolder():
	beePath = config.load('beePath')
	if beePath is None:
		raise BeeNotInstalledException("can't access beePath!")
	else:
		return f'{beePath}/packages/'


class configManager:
	"""
	BEE2.4 config manager
	this definition contains some useful commands to
	manipulate the BEE2.4 config files
	"""

	gamescfgPath = os.getenv('APPDATA').replace('\\', '/') + '/BEEMOD2/config/games.cfg'

	@staticmethod
	def addGame(path='', name='Portal 2', steamid=620, overwrite=False):
		"""
		adds a game to the games.cfg BEE config file
		:param path: path to the game (absolute)
		:param name: name of the game that will shows inside BEE game selection menu
		:param steamid: the game steam id
		:param overwrite: overwrite if there's a game with the same NAME
		:return: None
		"""
		# the games.cfg file path (its where the games data is stored)

		# the cfg is a ini formatted file so import a std lib that can handle them
		data = configparser.ConfigParser()
		# open the cfg for reading
		file = open(configManager.gamescfgPath, 'r')
		# read the cfg
		data.read_file(file)
		# close the cfg
		file.close()
		# if the section that we want to write already exist raise an exception apart when overwrite is True
		if data.has_section(name) and overwrite:
			# apply the new game
			data[name] = {'steamid': steamid, 'dir': path}
		elif not data.has_section(name):
			# apply the new game
			data[name] = {'steamid': steamid, 'dir': path}
		else:
			raise GameAlreadyExistError(f'key name {name} already exist! use another name or overwrite!')
		# reopen the cfg for writing
		file = open(configManager.gamescfgPath, 'w')
		# write it
		data.write(file)
		# close it
		file.close()

	@staticmethod
	def createAndAddGame(name='Portal 2', path='', steamid=620):
		"""
		create the games.cfg config file and add a game
		:param name: name of the game that will shows inside BEE game selection menu
		:param path: path to the game (absolute)
		:param steamid: the game steam id
		:return:
		"""
		if Path(configManager.gamescfgPath).exists():
			raise FileExistsError("can't create the config file, it already exist!")
		# create the necessary folders
		Path(configManager.gamescfgPath + '/../..').resolve().mkdir()
		Path(configManager.gamescfgPath + '/..').resolve().mkdir()
		data = configparser.ConfigParser()
		# create and open the file for writing
		file = open(configManager.gamescfgPath, 'x')
		# the data
		data[name] = {'steamid': steamid, 'dir': path}
		# write it
		data.write(file)
		# close it
		file.close()

	@staticmethod
	def hasGameWithID(steamid):
		logger.debug(f'checking config for game with steamid {steamid}')
		games = configparser.ConfigParser()
		games.read(configManager.gamescfgPath)
		for game in games.sections():
			if games[game]['steamid'] == steamid:
				return True
		return False

	@staticmethod
	def hasGameWithName(name):
		logger.debug(f'checking config for game with name {name}')
		games = configparser.ConfigParser()
		games.read(configManager.gamescfgPath)
		if name in games:
			return True
		else:
			return False


class downloadError(Exception):
	pass


class GameAlreadyExistError(Exception):
	pass


class BeeNotInstalledException(Exception):
	pass


if __name__ == "__main__":
	configManager.addGame("c:/hello", 'test')
