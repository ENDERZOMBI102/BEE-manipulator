import asyncio

import wx

from database import PDatabase
from packages import PlaceHolderView
from srctools.logger import get_logger

logger = get_logger()


class Browser(wx.ScrolledWindow):
	"""
		the package browser, this will display all the available packages
	"""
	database: PDatabase
	sizer: wx.GridBagSizer

	def __init__(self, master: wx.Window):
		super().__init__(parent=master)
		# return
		self.database = PDatabase()
		if self.database.checkDatabase():
			asyncio.run(  self.database.loadObjects(self) )
		else:
			self.views = [ PlaceHolderView(self) ]

	def reload(self):
		self.database = PDatabase()
