import webbrowser as wb

import wx
import wx.html
import wx.richtext
from markdown2 import markdown

import config
import utilities
from srctools.logger import get_logger


def init(master):
	aboutWindow(master)


class aboutWindow(wx.Frame):

	logger = get_logger()

	def __init__(self, master):
		super().__init__(master, title='About BEE Manipulator', style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
		# self.SetSize( wx.Size(300, 260) )
		self.SetIcon( utilities.icon )
		self.box = wx.html.HtmlWindow( self )
		try:
			self.logger.debug('trying to open about.html..')
			with open(f'{config.assetsPath}/about.html', 'r') as file:
				self.logger.debug('opened about.html!')
				data = file.read().replace( r'{0}', config.version.__str__() )
		except FileNotFoundError:
			self.logger.warning('failed to load about.html! falling back to about.md')
			self.logger.debug('opening about.md..')
			# set the page to the converted markdown text
			with open(f'{config.assetsPath}/about.md', 'r') as file:
				self.logger.debug('converting markdown to html..')
				data = markdown(file.read())
			with open(f'{config.assetsPath}/about.html', 'w') as file:
				file.write(data)
			data = data.replace(r'{0}', config.version())
		self.logger.debug('loaded html data! displaying..')
		self.box.SetPage(data)
		self.CenterOnParent()
		self.Raise()
		self.Show()
		self.box.OnLinkClicked = self.linkHandler

	@staticmethod
	def linkHandler(link):
		wb.open(link.GetHref())
