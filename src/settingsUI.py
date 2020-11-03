import asyncio
from pathlib import Path

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
		self.AddPage(DevelopmentPage())
		logger.debug('settings window initialized!')

	def show(self):
		self.Show(wx.GetTopLevelWindows()[0])


class GeneralPage(wx.PreferencesPage):
	name: str = loc('settings.tab.general.name')
	BUWC: wx.CheckBox
	VGFC: wx.CheckBox
	SUCC: wx.CheckBox
	SSC: wx.CheckBox
	LDST: wx.StaticText
	LDDL: wx.Choice
	RLFB: wx.Button

	def GetName(self):
		return self.name

	def CreateWindow(self, parent):
		panel = wx.Panel(parent)
		panel.SetMinSize( (600, 300) )

		# BEE Uninstall Warning | checkbox
		self.BUWC = wx.CheckBox(
			parent=panel,
			name='BUWC',
			label=loc('settings.tab.general.buwc.text'),
			pos=wx.Point(0, -60)
		)
		self.BUWC.SetToolTip( wx.ToolTip( loc('settings.tab.general.buwc.tooltip') ) )
		self.BUWC.SetValue( config.load('showUninstallDialog', default=True) )

		# Verify Game Cache warning | checkbox
		self.VGFC = wx.CheckBox(
			parent=panel,
			name='VGFC',
			label=loc('settings.tab.general.vgfc.text'),
			pos=wx.Point(0, -40)
		)
		self.VGFC.SetToolTip(wx.ToolTip(loc('settings.tab.general.vgfc.tooltip')))
		self.VGFC.SetValue( config.load('showVerifyDialog', default=True) )

		# Startup Update Check | checkbox
		self.SUCC = wx.CheckBox(
			parent=panel,
			name='SUCC',
			label=loc('settings.tab.general.succ.text'),
			pos=wx.Point(0, -20)
		)
		self.SUCC.SetToolTip(wx.ToolTip(loc('settings.tab.general.succ.tooltip')))
		self.SUCC.SetValue( config.load('startupUpdateCheck', default=True) )

		# splash screen | checkbox
		self.SSC = wx.CheckBox(
			parent=panel,
			name='SSC',
			label=loc('settings.tab.general.ssc.text'),
			pos=wx.Point(0, 0)
		)
		self.SSC.SetToolTip(wx.ToolTip(loc('settings.tab.general.ssc.tooltip')))
		self.SSC.SetValue( config.load('showSplashScreen', default=True) )

		# language | static text | dropdown list
		self.LDST = wx.StaticText(
			parent=panel,
			label=loc('settings.tab.general.lddl.text'),
			pos=wx.Point(300, -60)
		)
		self.LDDL = wx.Choice(
			parent=panel,
			name='LDDL',
			choices=list(localizeObj.localizations.keys()),
			pos=wx.Point(300, -40)
		)
		self.LDDL.SetToolTip(wx.ToolTip(loc('settings.tab.general.lddl.tooltip')))
		self.LDDL.SetSelection(self.LDDL.FindString(localizeObj.lang))

		# reload lang files | button
		self.RLFB = wx.Button(
			parent=panel,
			label=loc('settings.tab.general.rlfb.text'),
			pos=wx.Point(299, -10)
		)
		self.RLFB.SetToolTip( wx.ToolTip( loc('settings.tab.general.rlfb.tooltip') ) )

		# bind everything
		self.BUWC.Bind(wx.EVT_CHECKBOX, self.save)
		self.VGFC.Bind(wx.EVT_CHECKBOX, self.save)
		self.SUCC.Bind(wx.EVT_CHECKBOX, self.save)
		self.SSC.Bind(wx.EVT_CHECKBOX, self.save)
		self.LDDL.Bind(wx.EVT_CHOICE, self.save)
		self.RLFB.Bind(wx.EVT_BUTTON, self.reloadLangFiles)

		return panel

	def save(self, evt: wx.CommandEvent):
		if evt.GetEventObject().GetName() == 'BUWC':
			config.save(not evt.IsChecked(), 'showUninstallDialog')
		elif evt.GetEventObject().GetName() == 'VGFC':
			config.save(not evt.IsChecked(), 'showVerifyDialog')
		elif evt.GetEventObject().GetName() == 'SUCC':
			config.save(not evt.IsChecked(), 'startupUpdateCheck')
		elif evt.GetEventObject().GetName() == 'SSC':
			config.save(not evt.IsChecked(), 'showSplashScreen')
		elif evt.GetEventObject().GetName() == 'LDDL':
			config.save(self.LDDL.GetString( evt.GetSelection() ), 'lang')

	@staticmethod
	def reloadLangFiles(evt: wx.CommandEvent):
		asyncio.run( localizeObj.loadLocFiles() )


class PathsPage(wx.PreferencesPage):
	name: str = loc('settings.tab.paths.name')
	P2PST: wx.StaticText  # p2 path
	P2PDP: wx.DirPickerCtrl
	P1PST: wx.StaticText  # p1 path
	P1PDP: wx.DirPickerCtrl
	BPST: wx.StaticText  # bee path
	BPDP: wx.DirPickerCtrl
	LDBPST: wx.StaticText  # local database path
	LDBPDP: wx.DirPickerCtrl
	PPST: wx.StaticText  # plugins path
	PPDP: wx.DirPickerCtrl

	def GetName(self):
		return self.name

	def CreateWindow(self, parent):
		panel = wx.Panel(parent)
		panel.SetMinSize( (600, 300) )

		# P2 Path | static text | DirPickerCtrl
		self.P2PST = wx.StaticText(
			parent=panel,
			label=loc('settings.tab.paths.p2pdp.text'),
			pos=wx.Point(0, -60)
		)
		self.P2PDP = wx.DirPickerCtrl(
			parent=panel,
			name='P2PDP',
			path=config.portalDir(),
			size=wx.Size(500, 20),
			pos=wx.Point(0, -45)
		)
		self.P2PDP.SetToolTip(wx.ToolTip(loc('settings.tab.paths.p2pdp.tooltip')))
		self.P2PDP.GetTextCtrl().SetMinSize( wx.Size( 400, self.P2PDP.GetTextCtrl().GetSize()[1] ) )

		# P1 Path | static text | DirPickerCtrl
		self.P1PST = wx.StaticText(
			parent=panel,
			label=loc('settings.tab.paths.p1pdp.text'),
			pos=wx.Point(0, -20)
		)
		self.P1PDP = wx.DirPickerCtrl(
			parent=panel,
			name='P1PDP',
			path='',
			size=wx.Size(500, 20),
			pos=wx.Point(0, -4)
		)
		self.P1PDP.Enable(False)
		self.P1PDP.SetPath('Not available')
		self.P1PDP.SetToolTip(wx.ToolTip(loc('settings.tab.paths.p1pdp.tooltip')))
		self.P1PDP.GetTextCtrl().SetMinSize(wx.Size(400, self.P1PDP.GetTextCtrl().GetSize()[1]))

		# BEE Path | static text | DirPickerCtrl
		self.BPST = wx.StaticText(
			parent=panel,
			label=loc('settings.tab.paths.bpdp.text'),
			pos=wx.Point(0, 20)
		)
		bp = config.load('beePath')
		self.BPDP = wx.DirPickerCtrl(
			parent=panel,
			name='BPDP',
			path=bp if bp is not None else '',
			size=wx.Size(500, 20),
			pos=wx.Point(0, 37)
		)
		if bp is None:
			self.BPDP.SetPath('Not installed')
			self.BPDP.Enable(False)
		self.BPDP.SetToolTip(wx.ToolTip(loc('settings.tab.paths.bpdp.tooltip')))
		self.BPDP.GetTextCtrl().SetMinSize( wx.Size( 400, self.BPDP.GetTextCtrl().GetSize()[1] ) )

		# Local Database Path | static text | DirPickerCtrl
		self.LDBPST = wx.StaticText(
			parent=panel,
			label=loc('settings.tab.paths.ldbpdp.text'),
			pos=wx.Point(0, 60)
		)
		self.LDBPDP = wx.DirPickerCtrl(
			parent=panel,
			name='LDBPDP',
			path=config.load('databasePath'),
			size=wx.Size(500, 20),
			pos=wx.Point(0, 78)
		)
		self.LDBPDP.SetToolTip(wx.ToolTip(loc('settings.tab.paths.ldbpdp.tooltip')))
		self.LDBPDP.GetTextCtrl().SetMinSize( wx.Size( 400, self.LDBPDP.GetTextCtrl().GetSize()[1] ) )

		# Plugins Path | static text | DirPickerCtrl
		self.PPST = wx.StaticText(
			parent=panel,
			label=loc('settings.tab.paths.ppdp.text'),
			pos=wx.Point(0, 100)
		)
		self.PPDP = wx.DirPickerCtrl(
			parent=panel,
			name='PPDP',
			path=config.load('pluginsPath'),
			size=wx.Size(500, 20),
			pos=wx.Point(0, 119)
		)
		self.PPDP.SetToolTip(wx.ToolTip(loc('settings.tab.paths.ppdp.tooltip')))
		self.PPDP.GetTextCtrl().SetMinSize( wx.Size( 400, self.PPDP.GetTextCtrl().GetSize()[1] ) )

		# bind everything
		self.P2PDP.Bind(wx.EVT_DIRPICKER_CHANGED, self.save)
		self.P1PDP.Bind(wx.EVT_DIRPICKER_CHANGED, self.save)
		self.BPDP.Bind(wx.EVT_DIRPICKER_CHANGED, self.save)
		self.LDBPDP.Bind(wx.EVT_DIRPICKER_CHANGED, self.save)
		self.PPDP.Bind(wx.EVT_DIRPICKER_CHANGED, self.save)

		return panel

	def save(self, evt: wx.FileDirPickerEvent):
		if not ( Path( evt.GetPath() ).exists() and Path( evt.GetPath() ).is_dir() ):
			return
		if evt.GetEventObject().GetName() == 'P2PDP':
			config.save(evt.GetPath(), 'portal2Dir')
		elif evt.GetEventObject().GetName() == 'P1PDP' and self.p1:
			config.save(evt.GetPath(), 'portal2Dir')
		elif evt.GetEventObject().GetName() == 'BPDP':
			config.save(evt.GetPath(), 'beePath')
		elif evt.GetEventObject().GetName() == 'LDBPDP':
			config.save(evt.GetPath(), 'databasePath')
		elif evt.GetEventObject().GetName() == 'PPDP':
			config.save(evt.GetPath(), 'pluginsPath')
		# TODO: add onlineDatabaseUrl and a check to see if the url is valid


class DevelopmentPage(wx.PreferencesPage):
	name: str = loc('settings.tab.development.name')

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
