import wx

from database import PDatabase
from srctools.logger import get_logger

logger = get_logger()


class Browser(wx.ScrolledWindow):
	"""
		the package browser, this will display all the available packages
	"""
	sizer: wx.GridBagSizer

	def __init__(self, master: wx.Window):
		super().__init__(
			parent=master,
			size=master.GetSize()
		)
		# wx.CallAfter( PDatabase.load() )



	def reload(self):
		self.database = PDatabase()
