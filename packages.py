from json import *
import wx
import random
from typing import Union
from utilities import root
from base64 import b64decode as decode

class beePackage:
	r"""
		rappresents a BEE2.4 package, with all its data; icon, author, file name and a description are
		stored here, with the others.
		the icon is stored as base64 string and then returned as image object when icon() is called
	"""
	def __init__(self, ID = None, icon64 = None, version = 0, author = [], description = None, url = "None", filename = None, name =  None):
		self.ID: str = ID
		self.author: str = author
		self.icon64: str = icon64
		self.version = version
		self.description: str = description
		self.url: str = url
		self.filename: str = filename
		self.name: str = name
		self.coAuthors = []
	
	
	def service(self):
		r"""
			this will return the used service, for now only github, dropbox and google drive
		"""
		if "github" in self.url:
			return "github"
		elif "dropbox" in self.url:
			return "dropbox"
		elif "drive.google" in self.url:
			return "gdrive"
	
	
	def repo(self):
		r"""
			this will return the repo link if the package is on github, if the package isn't on github will return None
		"""
		if self.service() == "github":
			splittedUrl = self.url.split("/")
			return f'https://github.com/{plittedUrl[4]}/{splittedUrl[5]}/'
		else:
			return None
	
	
	def icon(self):
		r"""
			return the package icon as image object
		"""
		return decode(self.icon64)
	
	def __getitem__( self, index: str):
		if index in ['ID', 'id'] : return self.ID
		elif index == 'author' : return self.author
		elif index == 'icon64' : return self.icon64
		elif index in ['version', 'ver'] : return self.version
		elif index == 'name' : return self.name
		elif index in ['desc', 'description'] : return self.description
		elif index == 'url' : return self.url
		elif index in ['filename', 'file'] : return self.filename
		elif index in ['coAuhors', 'coauthors'] : return self.coAuthors
		elif index == 'icon' : return self.icon()
		elif index == 'service' : return self.service()
		elif index in ['repo', 'repository'] : return self.repo()


class bmPackage:
	r"""
		rappresents a BeeManipulator package, with all it's data and co.
		the icon is stored as base64 string and then returned as image object when icon() is called
	"""

	def __init__(self, ID=None, author=[], icon64=None, version=0, name = None, desc = None, url = None, content=[], config={}):
		self.ID = ID
		self.author = author
		self.icon64 = icon64
		self.version = version
		self.name = name
		self.desc = desc
		self.url = url
		self.contents = content
		self.config = config
		self.coAuthors = []
	
	
	def icon(self):
		r"""
			return the package icon as image object
		"""
		return decode(self.icon64)

	
	def service(self):
		r"""
			this will return the used service, for now only github, dropbox and google drive
		"""
		if "github" in self.url:
			return "github"
		elif "dropbox" in self.url:
			return "dropbox"
		elif "drive.google" in self.url:
			return "gdrive"

	
	def repo(self):
		r"""
			this will return the repo link if the package is on github, if the package isn't on github will return None
		"""
		if self.service() == "github":
			splittedUrl = self.url.split("/")
			return f'https://github.com/{plittedUrl[4]}/{splittedUrl[5]}/'
		else:
			return None
	
	def cfgOP(self, type = None, data = None, operation = "r"):
		r"""
			for ConFiG OPerations, you can access the config dict directly, but this is the better method, i hope.
			if no operation aurgment is given, use the default operation, r (read).
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
		elif index == 'icon64' : return self.icon64
		elif index in ['version', 'ver'] : return self.version
		elif index == 'name' : return self.name
		elif index in ['desc', 'description'] : return self.desc
		elif index == 'url' : return self.url
		elif index in ['contents', 'content'] : return self.contents
		elif index == 'config' : return self.config
		elif index in ['coAuhors', 'coauthors'] : return self.coAuthors
		elif index == 'icon' : return self.icon()
		elif index == 'service' : return self.service()
		elif index in ['repo', 'repository'] : return self.repo()


class packageFrame(wx.Panel):
	"""
	this is a frame in the package browser
	"""

	def __init__(self, master: wx.Window, package: Union[beePackage, bmPackage]):
		rootSize = wx.App
		#GetTopWindow()
		rootSize = rootSize.GetSize()
		size = wx.Size(rootSize.x-10, rootSize.y/5)
		super().__init__(parent=master, size=size, name=f'BROWSERFRAME_{package.ID}')
		sizer = wx.BoxSizer(wx.VERTICAL)
		titleBar = wx.Panel(self, -1, size=wx.Size(50,100))
		titleText = wx.StaticText(titleBar, -1, label=package.name)
		sizer.Add(titleBar)

		self.Show()


		


	
if __name__ == "__main__":
	x = bmPackage(ID="id.id", url="https://api.github.com/repos/BEEmod/BEE2.4/releases/latest")
	print(x['id'])
	print(x['icon'])
