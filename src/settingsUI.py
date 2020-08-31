import wx

import config
from localization import localizeObj

if __name__ == '__main__':
	from localization import loc
from srctools.logger import get_logger

logger = get_logger()
"""
	see
	- https://github.com/domdfcoding/GunShotMatch/blob/master/GuiV2/GSMatch2_Core/GUI/settings_panel.py
	- https://github.com/domdfcoding/GunShotMatch/blob/master/GuiV2/GSMatch2_Core/Old/Preferences.py
	- https://docs.wxpython.org/wx.PreferencesEditor.html?highlight=addpage#wx.PreferencesEditor.AddPage
"""


class window(wx.PreferencesEditor):
	r"""
		this is the window for the settings
	"""

	def __init__(self):
		logger.debug('initializing settings window..')
		super().__init__(title=loc('settings.window.text'))
		self.AddPage(GeneralPage())
		self.AddPage(PathsPage())
		self.AddPage(AdvPage())
		logger.debug('settings window initialized!')

	def show(self):
		self.Show(wx.GetTopLevelWindows()[0])


class GeneralPage(wx.PreferencesPage):
	name: str = loc('settings.tab.general.name')
	BUWC: wx.CheckBox
	VGCC: wx.CheckBox
	SUCC: wx.CheckBox
	LDDL: wx.Choice

	def GetName(self):
		return self.name

	def CreateWindow(self, parent):
		panel = wx.Panel(parent)
		panel.SetMinSize((600, 300))

		rightsizer = wx.BoxSizer(wx.VERTICAL)
		leftsizer = wx.BoxSizer(wx.VERTICAL)
		# BEE Uninstall Warning | checkbox
		self.BUWC = wx.CheckBox(parent=panel, id=wx.ID_ANY, label="BEE Uninstall Warning")
		self.BUWC.SetToolTip(wx.ToolTip('If checked, shows a warning when uninstalling BEE'))
		if not config.load('noUninstallDialog'):
			self.BUWC.SetValue(True)
		leftsizer.Add(
			self.BUWC,
			wx.SizerFlags(1).Left()
		)
		# Verify Game Cache warning | checkbox
		self.VGCC = wx.CheckBox(parent=panel, id=wx.ID_ANY, label="Verify Game Files Warning")
		self.VGCC.SetToolTip(wx.ToolTip('If checked, shows a warning when verifying game files'))
		if not config.load('noVerifyDialog'):
			self.VGCC.SetValue(True)
		leftsizer.Add(
			self.VGCC,
			wx.SizerFlags(1).Left()
		)
		# Startup Update Check | checkbox
		self.SUCC = wx.CheckBox(parent=panel, label="Startup Update Check")
		self.SUCC.SetToolTip(wx.ToolTip('If checked, checks if updates are available on startup'))
		if not config.load('noStartupUpdateCheck'):
			self.SUCC.SetValue(True)
		leftsizer.Add(
			self.SUCC,
			wx.SizerFlags(1).Left()
		)
		# language | dropdown list
		self.LDDL = wx.Choice(
			parent=panel,
			choices=list( localizeObj.localizations.keys() )
		)
		self.LDDL.SetSelection( self.LDDL.FindString(localizeObj.lang) )
		self.LDDL.SetToolTip(wx.ToolTip('The language of BM, requires restart'))

		# add the sizers
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(
			leftsizer,
			wx.SizerFlags(1).Left()
		),
		sizer.Add(
			rightsizer,
			wx.SizerFlags(1).Top()
		)
		panel.SetSizer(sizer)
		return panel


class PathsPage(wx.PreferencesPage):
	name: str = loc('settings.tab.paths.name')

	def GetName(self):
		return self.name

	def CreateWindow(self, parent):
		panel = wx.Panel(parent)
		panel.SetMinSize((600, 300))

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(
			wx.StaticText(panel, -1, "General Settings"),
			wx.SizerFlags(1).Center()
		)

		panel.SetSizer(sizer)
		return panel


class AdvPage(wx.PreferencesPage):
	name: str = loc('settings.tab.advanced.name')

	def GetName(self):
		return self.name

	def CreateWindow(self, parent):
		panel = wx.Panel(parent)
		panel.SetMinSize((600, 300))

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(
			wx.StaticText(panel, -1, "Advanced Settings"),
			wx.SizerFlags(1).Center()
		)
		panel.SetSizer(sizer)
		return panel
