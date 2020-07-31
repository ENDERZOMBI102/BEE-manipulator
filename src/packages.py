import logging
from typing import List

import wx
import wx.lib

from srctools import logger


class PackageFrame(wx.Panel):
	"""	this is a frame in the package browser """

	logger: logging.Logger
	identifier: str
	authors: List[str]
	version: str
	name: str
	description: str
	url: str
	filename: str
	service: str
	repo: str
	# contents: str
	# configs: Dict[str, Any]
	
	def __init__(self, master: wx.Window, identifier: str, authors: List[str], version: str, name: str, description: str, url: str, filename: str, y_pos: int):
		self.logger = logger.get_logger()
		# set obj data
		self.identifier = identifier
		self.authors = authors
		self.version = version
		self.name = name
		self.description = description
		self.url = url
		self.filename = filename
		# self.contents = contents
		# set the service
		if 'github' in self.url:
			self.service = 'github'
		elif 'dropbox' in self.url:
			self.service = 'dropbox'
		elif 'drive.google' in self.url:
			self.service = 'gdrive'
		# set the repo if we use github
		if self.service == 'github':
			splittedUrl = self.url.split("/")
			self.repo = f'https://github.com/{splittedUrl[4]}/{splittedUrl[5]}/'
		else:
			self.repo = None
		super().__init__(
			parent=master,
			size=wx.Size(500, 100),
			pos=[0, y_pos],
			name=f'BROWSERFRAME_{self.identifier}'
		)
		sizer = wx.BoxSizer(wx.VERTICAL)

		infoButton = wx.Button(self, label="More Info")
		modifyButton = wx.Button(self, label="Install")
		self.Bind(wx.EVT_BUTTON, self.OnModifyButtonHandler, modifyButton)
		self.Bind(wx.EVT_BUTTON, self.OnInfoButtonHandler, infoButton)
		self.Bind(wx.EVT_MOUSE_AUX1_DCLICK, self.OnClickHandler, self)
		self.Show()

	def OnClickHandler(self, event: wx.EVT_MOUSE_AUX1_DCLICK):
		pass

	def OnModifyButtonHandler(self, event: wx.EVT_BUTTON):
		pass

	def OnInfoButtonHandler(self, event: wx.EVT_BUTTON):
		pass


class PackageLargeView(wx.Frame):
	pass


if __name__ == "__main__":
	pass
