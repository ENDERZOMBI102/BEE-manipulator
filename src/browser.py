from typing import List

import wx
import wx.html
import wx.html2

from srctools.logger import get_logger

logger = get_logger()


class PackageView(wx.Panel):

	def __init__(self, image: wx.Bitmap, ):
		super(PackageView, self).__init__(
			parent=Browser.instance,
			size=wx.Size( Browser.instance.GetSize().GetWidth(), 100 )
		)


class Browser(wx.ScrolledWindow):
	"""
		the package browser, this will display all the available packages
	"""

	instance: 'Browser'
	childs: List[PackageView] = []

	def __init__(self, master: wx.Window):
		super().__init__(
			parent=master,
			size=master.GetSize()
		)
		Browser.instance = self
		self.loadPackages()

	def OnResize( self, size: wx.Size ):
		self.SetSize( size )

	def loadPackages( self ):
		pass





