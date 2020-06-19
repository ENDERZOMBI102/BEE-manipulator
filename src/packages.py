import logging
import pathlib
from typing import Union

import requests
import wx
import wx.lib

import beeManager
from srctools import logger


class beePackage:
	"""
	represents a BEE2.4 package, with all its data; icon, author, file name and a description are
	stored here, with the others.
	"""
	def __init__(self, ID = None, icon = None, version = 0, author = [], description = None, url = "None", filename = None, name =  None):
		self.ID: str = ID
		self.author: str = author
		self.icon: str = icon
		self.version = version
		self.description: str = description
		self.url: str = url
		self.filename: str = filename
		self.name: str = name
		self.coAuthors = []

	def service(self):
		"""
			this will return the used service, for now only github, dropbox and google drive
		"""
		if "github" in self.url:
			return "github"
		elif "dropbox" in self.url:
			return "dropbox"
		elif "drive.google" in self.url:
			return "gdrive"

	def repo(self):
		"""
			this will return the repo link if the package is on github, if the package isn't on github will return None
		"""
		if self.service() == "github":
			splittedUrl = self.url.split("/")
			return f'https://github.com/{splittedUrl[4]}/{splittedUrl[5]}/'
		else:
			return None

	def icons(self):
		"""
			return the package icon as image object
		"""
		return

	def __getitem__( self, index: str):
		if index in ['ID', 'id'] : return self.ID
		elif index == 'author' : return self.author
		elif index in ['version', 'ver'] : return self.version
		elif index == 'name' : return self.name
		elif index in ['desc', 'description'] : return self.description
		elif index == 'url' : return self.url
		elif index in ['filename', 'file'] : return self.filename
		elif index in ['coAuhors', 'coauthors'] : return self.coAuthors
		elif index == 'icon' : return self.icon
		elif index == 'service' : return self.service()
		elif index in ['repo', 'repository'] : return self.repo()


class bmPackage:
	"""
		represents a BeeManipulator package, with all it's data and co.
	"""

	def __init__(self, ID=None, author=[], icon=None, version=0, name = None, desc = None, url = None, content=[], config={}):
		self.ID = ID
		self.author = author
		self.icon = icon
		self.version = version
		self.name = name
		self.desc = desc
		self.url = url
		self.contents = content
		self.config = config
		self.coAuthors = []

	def service(self):
		"""
			this will return the used service, for now only github, dropbox and google drive
		"""
		if "github" in self.url:
			return "github"
		elif "dropbox" in self.url:
			return "dropbox"
		elif "drive.google" in self.url:
			return "gdrive"

	def repo(self):
		"""
			this will return the repo link if the package is on github, if the package isn't on github will return None
		"""
		if self.service() == "github":
			splittedUrl = self.url.split("/")
			return f'https://github.com/{splittedUrl[4]}/{splittedUrl[5]}/'
		else:
			return None

	def cfgOP(self, type = None, data = None, operation = "r"):
		"""
			for ConFiG OPerations, you can access the config dict directly, but this is the better method, i hope.
			if no operation augment is given, use the default operation, r (read).
			on read, if the requested "type" doesn't exist, a None is returned.
		"""
		if operation == "w":
			self.config[type] == data
		else:
			if self.config[type]:
				return self.config[type]
			else:
				return None

	def __getitem__( self, index: str):
		if index in ['ID', 'id'] : return self.ID
		elif index == 'author' : return self.author
		elif index in ['version', 'ver'] : return self.version
		elif index == 'name' : return self.name
		elif index in ['desc', 'description'] : return self.desc
		elif index == 'url' : return self.url
		elif index in ['contents', 'content'] : return self.contents
		elif index == 'config' : return self.config
		elif index in ['coAuhors', 'coauthors'] : return self.coAuthors
		elif index == 'icon' : return self.icon
		elif index == 'service' : return self.service()
		elif index in ['repo', 'repository'] : return self.repo()


class packageFrame(wx.Panel):
	"""	this is a frame in the package browser """

	package: Union[beePackage, bmPackage]
	logger: logging.Logger

	def __init__(self, master: wx.Window, package: Union[beePackage, bmPackage], y):
		self.package = package
		self.logger = logger.get_logger()
		super().__init__(
			parent=master,
			size=wx.Size(500, 100),
			pos = [0, y],
			name=f'BROWSERFRAME_{package.ID}'
		)
		sizer = wx.BoxSizer(wx.VERTICAL)
		titleBar = wx.Panel(self, -1, size=wx.Size(500,20))
		titleText = wx.StaticText(titleBar, -1, label=package.name)
		sizer.Add(titleBar)
		if ( not package.icon in [None, ''] ) and pathlib.Path(package.icon).exists():
			bmp = wx.Bitmap()
			bmp.LoadFile(package.icon)
			image = wx.StaticBitmap(
				self,
				bitmap=bmp
			)
		else:
			pass
		infoButton = wx.Button(self, label="More Info")
		modifyButton = wx.Button(self, label="Install")
		self.Bind(wx.EVT_BUTTON, self.OnModifyButtonHandler, modifyButton)
		self.Bind(wx.EVT_BUTTON, self.OnInfoButtonHandler, infoButton)
		self.Bind(wx.EVT_MOUSE_AUX1_DCLICK, self.OnClickHandler, self)
		self.Show()

	def OnClickHandler(self, event: wx.EVT_MOUSE_AUX1_DCLICK):
		self.install()

	def install(self, update: bool = False):
		packagesPath: str = beeManager.packageFolder()
		service: str = self.package.service()  # package host service
		filebytes: bytes  # the file content in bytes
		fileurl: str  # the file download url
		filename: str  # the file name
		filepath: str  # file path in the disk
		self.logger.info(f'installing package {self.package.ID}')
		self.logger.debug('getting file url and name')
		if service == 'github':
			data = requests.get(self.package.url).json()  # get the release data
			fileurl = data['assets'][0]['browser_download_url']  # take the file url
			filename = data['assets'][0]['name']  # take the file name
		elif service == 'gdrive':
			fileurl = self.package.url  # take the file url
			filename = self.package.filename  # take the file name
		else:
			self.logger.warning(f'unexpected service found, expected "gdrive" or "github" got "{service}", aborting')
			return  # unsupported service
		self.logger.debug(f'file name: {filename}, file url: {fileurl}')
		# the filepath is generated by combining the packages folder path + filename
		filepath = packagesPath.join(filename)
		self.logger.debug('downloading file...')
		try:
			# get the file
			filebytes = requests.get(fileurl).content
		except Exception as e:
			self.logger.error(f'FAILED TO DOWNLOAD FILE! error: {e}')
			return
		self.logger.debug('success!')
		self.logger.debug('writing file to disk..')
		mode = 'x+b' if update is False else 'wb'
		try:
			# write file to disk
			with open(filepath, mode) as file:
				file.write(filebytes)
		except Exception as e:
			self.logger.error(f'FAILED TO SAVE FILE! error: {e}')
			return
		self.logger.info('successufully installed package!')
		# done

	def OnModifyButtonHandler(self, event: wx.EVT_BUTTON):
		pass

	def OnInfoButtonHandler(self, event: wx.EVT_BUTTON):
		pass


if __name__ == "__main__":
	x = bmPackage(ID="id.id", url="https://api.github.com/repos/BEEmod/BEE2.4/releases/latest")
	print(x['id'])
	print(x['icon'])
