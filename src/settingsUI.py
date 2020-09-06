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
		panel.SetMinSize((600, 300))

		rightsizer = wx.BoxSizer(wx.VERTICAL)
		leftsizer = wx.BoxSizer(wx.VERTICAL)

		# BEE Uninstall Warning | checkbox
		self.BUWC = wx.CheckBox(
			parent=panel,
			name='BUWC',
			label=loc('settings.tab.general.buwc.text')
		)
		self.BUWC.SetToolTip(wx.ToolTip(loc('settings.tab.general.buwc.tooltip')))
		if not config.load('noUninstallDialog'):
			self.BUWC.SetValue(True)
		leftsizer.Add(
			self.BUWC,
			wx.SizerFlags(1).Left()
		)

		# Verify Game Cache warning | checkbox
		self.VGFC = wx.CheckBox(
			parent=panel,
			name='VGFC',
			label=loc('settings.tab.general.vgfc.text')
		)
		self.VGFC.SetToolTip(wx.ToolTip(loc('settings.tab.general.vgfc.tooltip')))
		if not config.load('noVerifyDialog'):
			self.VGFC.SetValue(True)
		leftsizer.Add(
			self.VGFC,
			wx.SizerFlags(1).Left()
		)

		# Startup Update Check | checkbox
		self.SUCC = wx.CheckBox(
			parent=panel,
			name='SUCC',
			label=loc('settings.tab.general.succ.text')
		)
		self.SUCC.SetToolTip(wx.ToolTip(loc('settings.tab.general.succ.tooltip')))
		if not config.load('noStartupUpdateCheck'):
			self.SUCC.SetValue(True)
		leftsizer.Add(
			self.SUCC,
			wx.SizerFlags(1).Left()
		)

		# splash screen | checkbox
		self.SSC = wx.CheckBox(
			parent=panel,
			name='SSC',
			label=loc('settings.tab.general.ssc.text')
		)
		self.SSC.SetToolTip(wx.ToolTip(loc('settings.tab.general.ssc.tooltip')))
		if not config.load('noSplashScreen'):
			self.SSC.SetValue(True)
		leftsizer.Add(
			self.SSC,
			wx.SizerFlags(1).Left()
		)

		# language | static text | dropdown list
		self.LDST = wx.StaticText(
			parent=panel,
			label=loc('settings.tab.general.lddl.text')
		)
		self.LDDL = wx.Choice(
			parent=panel,
			name='LDDL',
			choices=list(localizeObj.localizations.keys())
		)
		self.LDDL.SetToolTip(wx.ToolTip(loc('settings.tab.general.lddl.tooltip')))
		self.LDDL.SetSelection(self.LDDL.FindString(localizeObj.lang))
		rightsizer.AddMany([
			(
				self.LDST,
				wx.SizerFlags(1).Top()
			),
			(
				self.LDDL,
				wx.SizerFlags(1).Top()
			)
		])

		# reload lang files | button
		self.RLFB = wx.Button(
			parent=panel,
			label=loc('settings.tab.general.rlfb.text')
		)
		self.RLFB.SetToolTip( wx.ToolTip( loc('settings.tab.general.rlfb.tooltip') ) )
		rightsizer.Add(
			self.RLFB,
			wx.SizerFlags(1).Top()
		)

		# bind everything
		self.BUWC.Bind(wx.EVT_CHECKBOX, self.save)
		self.VGFC.Bind(wx.EVT_CHECKBOX, self.save)
		self.SUCC.Bind(wx.EVT_CHECKBOX, self.save)
		self.SSC.Bind(wx.EVT_CHECKBOX, self.save)
		self.LDDL.Bind(wx.EVT_CHOICE, self.save)
		self.RLFB.Bind(wx.EVT_BUTTON, self.reloadLangFiles)

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
		# return final panel
		return panel

	def save(self, evt: wx.CommandEvent):
		if evt.EventObject.GetName() == 'BUWC':
			config.save(not evt.IsChecked(), 'noUninstallDialog')
		elif evt.EventObject.GetName() == 'VGFC':
			config.save(not evt.IsChecked(), 'noVerifyDialog')
		elif evt.EventObject.GetName() == 'SUCC':
			config.save(not evt.IsChecked(), 'noStartupUpdateCheck')
		elif evt.EventObject.GetName() == 'SSC':
			config.save(not evt.IsChecked(), 'noSplashScreen')
		elif evt.EventObject.GetName() == 'LDDL':
			config.save(self.LDDL.GetString(evt.Selection), 'lang')

	@staticmethod
	def reloadLangFiles(evt: wx.CommandEvent):
		asyncio.run( localizeObj.loadLocFiles() )


class PathsPage(wx.PreferencesPage):
	p1 = False
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
		panel.SetMinSize((600, 300))

		# rightsizer = wx.BoxSizer(wx.VERTICAL)
		leftsizer = wx.BoxSizer(wx.VERTICAL)

		# P2 Path | static text | DirPickerCtrl
		self.P2PST = wx.StaticText(
			parent=panel,
			label=loc('settings.tab.paths.p2pdp.text')
		)
		self.P2PDP = wx.DirPickerCtrl(
			parent=panel,
			name='P2PDP',
			path=config.portalDir()
		)
		self.P2PDP.SetToolTip(wx.ToolTip(loc('settings.tab.paths.p2pdp.tooltip')))
		self.P2PDP.TextCtrl: wx.TextCtrl
		self.P2PDP.TextCtrl.SetMinSize( wx.Size( 400, self.P2PDP.TextCtrl.GetSize()[1] ) )
		leftsizer.AddMany([
			(
				self.P2PST,
				wx.SizerFlags(1).Left()
			),
			(
				self.P2PDP,
				wx.SizerFlags(1).Left()
			)
		])

		if self.p1:
			# P1 Path | static text | DirPickerCtrl
			self.P1PST = wx.StaticText(
				parent=panel,
				label=loc('settings.tab.paths.p1pdp.text')
			)
			self.P1PDP = wx.DirPickerCtrl(
				parent=panel,
				name='P1PDP',
				path=''
			)
			self.P1PDP.SetToolTip(wx.ToolTip(loc('settings.tab.paths.p1pdp.tooltip')))
			self.P1PDP.TextCtrl.SetMinSize(wx.Size(400, self.P1PDP.TextCtrl.GetSize()[1]))
			leftsizer.AddMany([
				(
					self.P1PST,
					wx.SizerFlags(1).Left()
				),
				(
					self.P1PDP,
					wx.SizerFlags(1).Left()
				)
			])

		# BEE Path | static text | DirPickerCtrl
		self.BPST = wx.StaticText(
			parent=panel,
			label=loc('settings.tab.paths.bpdp.text')
		)
		bp = config.load('beePath')
		self.BPDP = wx.DirPickerCtrl(
			parent=panel,
			name='BPDP',
			path=bp if bp is not None else ''
		)
		if bp is None:
			self.BPDP.SetPath('not installed')
			self.BPDP.Enable(False)
		self.BPDP.SetToolTip(wx.ToolTip(loc('settings.tab.paths.bpdp.tooltip')))
		self.BPDP.TextCtrl.SetMinSize( wx.Size( 400, self.BPDP.TextCtrl.GetSize()[1] ) )
		leftsizer.AddMany([
			(
				self.BPST,
				wx.SizerFlags(1).Left()
			),
			(
				self.BPDP,
				wx.SizerFlags(1).Left()
			)
		])

		# Local Database Path | static text | DirPickerCtrl
		self.LDBPST = wx.StaticText(
			parent=panel,
			label=loc('settings.tab.paths.ldbpdp.text')
		)
		self.LDBPDP = wx.DirPickerCtrl(
			parent=panel,
			name='LDBPDP',
			path=config.load('databasePath')
		)
		self.LDBPDP.SetToolTip(wx.ToolTip(loc('settings.tab.paths.ldbpdp.tooltip')))
		self.LDBPDP.TextCtrl.SetMinSize( wx.Size( 400, self.LDBPDP.TextCtrl.GetSize()[1] ) )
		leftsizer.AddMany([
			(
				self.LDBPST,
				wx.SizerFlags(1).Left()
			),
			(
				self.LDBPDP,
				wx.SizerFlags(1).Left()
			)
		])

		# Plugins Path | static text | DirPickerCtrl
		self.PPST = wx.StaticText(
			parent=panel,
			label=loc('settings.tab.paths.ppdp.text')
		)
		self.PPDP = wx.DirPickerCtrl(
			parent=panel,
			name='PPDP',
			path=config.load('pluginsPath')
		)
		self.PPDP.SetToolTip(wx.ToolTip(loc('settings.tab.paths.ppdp.tooltip')))
		self.PPDP.TextCtrl.SetMinSize( wx.Size( 400, self.PPDP.TextCtrl.GetSize()[1] ) )
		leftsizer.AddMany([
			(
				self.PPST,
				wx.SizerFlags(1).Left()
			),
			(
				self.PPDP,
				wx.SizerFlags(1).Left()
			)
		])

		# bind everything
		self.P2PDP.Bind(wx.EVT_DIRPICKER_CHANGED, self.save)
		if self.p1:
			self.P1PDP.Bind(wx.EVT_DIRPICKER_CHANGED, self.save)
		self.BPDP.Bind(wx.EVT_DIRPICKER_CHANGED, self.save)
		self.LDBPDP.Bind(wx.EVT_DIRPICKER_CHANGED, self.save)
		self.PPDP.Bind(wx.EVT_DIRPICKER_CHANGED, self.save)

		# add the sizers
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(
			leftsizer,
			wx.SizerFlags(1).Left()
		)
		# sizer.Add(
		#	rightsizer,
		#	wx.SizerFlags(1).Top()
		# )
		panel.SetSizer(sizer)
		# return final panel
		return panel

	def save(self, evt: wx.FileDirPickerEvent):
		if not ( Path( evt.GetPath() ).exists() and Path( evt.GetPath() ).is_dir() ):
			return
		if evt.EventObject.GetName() == 'P2PDP':
			config.save(evt.GetPath(), 'portal2Dir')
		elif evt.EventObject.GetName() == 'P1PDP' and self.p1:
			config.save(evt.GetPath(), 'portal2Dir')
		elif evt.EventObject.GetName() == 'BPDP':
			config.save(evt.GetPath(), 'beePath')
		elif evt.EventObject.GetName() == 'LDBPDP':
			config.save(evt.GetPath(), 'databasePath')
		elif evt.EventObject.GetName() == 'PPDP':
			config.save(evt.GetPath(), 'pluginsPath')


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
