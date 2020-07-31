import configparser
import io
import os
from pathlib import Path
from zipfile import ZipFile

import wx
from requests import get

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
	beeVersion = config.load('beeVersion')
	logger.info(f'installed BEE version: {beeVersion}')
	if firstInstall is False:
		# bee isn't installed, can't update
		if beeVersion is None:
			return
	# check updates
	data = utilities.checkUpdate(beeRepoUrl, beeVersion if firstInstall is False else '0')
	logger.info(f'latest BEE version: {data[2]}')
	if not data[0]:
		# no update available, can't update
		logger.info('no update available')
		return
	if not firstInstall:
		# show bee update available dialog
		dialog = wx.RichMessageDialog(
			parent=wx.GetTopLevelWindows()[0],
			message=f'BEE2.4 {data[3]} is available for download, update now?',
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


def beeIsPresent():
	"""
	returns true if bee2.exe is found in the beePath
	:returns: bool
	"""
	path = config.load('beePath')
	if path is None:
		return False
	elif Path(path+'/BEE2.exe').exists():
		return True


def installBee():
	"""
	this will install/update BEE, when called, the function
	will download the latest version based on the os is running on and unzip it
	"""
	# create the progress dialog
	dialog = wx.ProgressDialog(
		parent=wx.GetTopLevelWindows()[0],
		title='Installing BEE2..',
		message='Downloading packages..',
		maximum=100
	)
	if not beeIsPresent():
		logger.info('downloading BEE2...')
		# get the zip binary data
		request = get(config.dynConfig['beeUpdateUrl'], stream=True)  # download BEE
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
		ZipFile(zipdata).extractall(config.load('beePath'))  # extract BEE
		logger.info('BEE2.4 application installed!')
	# install default package pack
	# get the url
	dl_url = get(beePackagesApiUrl).json()['assets'][0]['browser_download_url']
	# get the zip as bytes
	logger.info('downloading default package pack...')
	request = get(dl_url, stream=True)
	# working variables
	zipdata = io.BytesIO()
	dialog.Update(0, message='Downloading default pack..')
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
	# convert to a byte stream, to a zipfile object and then extract
	ZipFile(zipdata).extractall(config.load('beePath'))
	dialog.Close()
	logger.info('finished!')


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
	this definition contains some userful commands to
	manipulate the BEE2.4 config files
	"""

	@staticmethod
	def addGame(path='', name='Portal 2', overwrite=False):
		# the games.cfg file path (its where the games data is stored)
		gamescfgPath = os.getenv('APPDATA').replace('\\', '/') + '/BEEMOD2/config/games.cfg'
		# the cfg is a ini formatted file so import a std lib that can handle them
		data = configparser.ConfigParser()
		# open the cfg for reading
		file = open(gamescfgPath, 'r')
		# read the cfg
		data.read_file(file)
		# close the cfg
		file.close()
		# if the section that we want to write already exist raise an exception apart when overwrite is True
		if data.has_section(name) and overwrite:
			# apply the new game
			data[name] = {'steamid': '620', 'dir': path}
		elif not data.has_section(name):
			# apply the new game
			data[name] = {'steamid': '620', 'dir': path}
		else:
			raise GameAlreadyExistError(f'key name {name} already exist! use another name or overwrite!')
		# reopen the cfg for writing
		file = open(gamescfgPath, 'w')
		# write it
		data.write(file)
		# close it
		file.close()

	@staticmethod
	def createAndAddGame(name='Portal 2', loc='', steamid=620):
		# the games.cfg file path (its where the games data is stored)
		gamescfgPath = os.getenv('APPDATA').replace('\\', '/') + '/BEEMOD2/config/games.cfg'
		if Path(gamescfgPath).exists():
			raise FileExistsError("can' create the file, they already exist!")
		# create the necessary folders
		Path(gamescfgPath + '/../..').resolve().mkdir()
		Path(gamescfgPath + '/..').resolve().mkdir()
		data = configparser.ConfigParser()
		# create and open the file for writing
		file = open(gamescfgPath, 'x')
		# the data
		data[name] = {'steamid': steamid, 'dir': loc}
		# write it
		data.write(file)
		# close it
		file.close()


class downloadError(Exception):
	pass


class GameAlreadyExistError(Exception):
	pass


class BeeNotInstalledException(Exception):
	pass


if __name__ == "__main__":
	configManager.addGame("c:/hellothere", 'test')
