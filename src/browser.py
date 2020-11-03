import wx

from srctools.logger import get_logger

logger = get_logger()


class Browser(wx.ScrolledWindow):
	"""
		the package browser, this will display all the available packages
	"""

	def __init__(self, master: wx.Window):
		super().__init__(
			parent=master,
			size=master.GetSize()
		)

