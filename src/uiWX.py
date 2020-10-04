import asyncio
import os
import webbrowser as wb
from pathlib import Path

import wx
import wx.adv
import wx.py.dispatcher as dispatcher

import aboutWindow
import beeManager
import browser
import config
import logWindow
import pluginSystem
import settingsUI
import utilities
from pluginSystem import Events
from srctools.logger import get_logger, init_logging

# init important things
LOGGER = get_logger()

if utilities.env == 'dev':
	import importlib


wx.InitAllImageHandlers()


class root(wx.Frame):
	settingsWindowInstance: settingsUI.window = None

	def __init__(self):
		# load plugins
		super().__init__( None, title="BEE Manipulator " + str(config.version) )
		# sets the app icon
		self.SetIcon(utilities.icon)
		# init the logging window
		asyncio.run( logWindow.init() )
		asyncio.run( appDateCheck() )
		# set the utilities.root pointer to the object of this class
		utilities.root = self
		try:
			self.SetPosition(wx.Point(config.load('mainWindowPos')))
		except config.ConfigError:
			self.CenterOnScreen()
		self.SetSize(width=600, height=500)
		self.SetMinSize( wx.Size(width=600, height=500) )
		LOGGER.info(f'internet connected: {utilities.isonline()}')
		pluginSystem.systemObj.startSync()
		"""
		A menu bar is composed of menus, which are composed of menu items.
		This section builds the menu bar and binds actions to them
		"""
		# file menu bar
		self.fileMenu = wx.Menu()
		openPortalDirItem = self.fileMenu.Append(0, loc('menu.file.openportaldir.name')+'\tCtrl-P', loc('menu.file.openportaldir.description') )
		openBeeDirItem = self.fileMenu.Append(1, loc('menu.file.openbeedir.name')+"\tCtrl-B", loc('menu.file.openbeedir.description') )
		syncGamesItem = self.fileMenu.Append(2, loc('menu.file.syncgames.name'), loc('menu.file.syncgames.description') )
		exitItem = self.fileMenu.Append(3, loc('menu.file.exit.name'), loc('menu.file.exit.description') )

		# options menu bar
		self.optionsMenu = wx.Menu()
		settingsItem = self.optionsMenu.Append(4, loc('menu.options.settings.name')+'\tCtrl-S', loc('menu.options.settings.description') )
		toggleLogWindowItem = self.optionsMenu.Append(5, loc('menu.options.logtoggle.name')+'\tCtrl-L', loc('menu.options.logtoggle.description') )
		reloadPluginsItem = self.optionsMenu.Append(6, loc('menu.options.reloadplugins.name'), loc('menu.options.reloadplugins.description') )
		reloadPackagesItem = self.optionsMenu.Append(7, loc('menu.options.reloadpackages.name'), loc('menu.options.reloadpackages.description') )

		# portal 2 menu bar
		self.portalMenu = wx.Menu()
		verifyGameFilesItem = self.portalMenu.Append(8, loc('menu.portal.vgf.name'), loc('menu.portal.vgf.description') )
		uninstallBeeItem = self.portalMenu.Append(9, loc('menu.portal.uninstallbee.name'), loc('menu.portal.uninstallbee.description'))
		installBeeItem = self.portalMenu.Append(10, loc('menu.portal.installbee.name'), loc('menu.portal.installbee.description') )

		# help menu bar
		self.helpMenu = wx.Menu()
		aboutItem = self.helpMenu.Append(11, loc('menu.help.about.name'), loc('menu.help.about.description') )
		checkUpdatesItem = self.helpMenu.Append(12, loc('menu.help.cupdates.name'), loc('menu.help.cupdates.description') )
		wikiItem = self.helpMenu.Append(13, loc('menu.help.wiki.name'), loc('menu.help.wiki.description') )
		githubItem = self.helpMenu.Append(14, loc('menu.help.github.name'), loc('menu.help.github.description') )
		discordItem = self.helpMenu.Append(15, loc('menu.help.discord.name'), loc('menu.help.discord.description') )

		# set menu item icons
		self.helpMenu.FindItemById(11).SetBitmap( wx.Bitmap(f'{config.assetsPath}icons/menu_bm.png') )
		self.helpMenu.FindItemById(13).SetBitmap( wx.Bitmap(f'{config.assetsPath}icons/menu_github.png') )
		self.helpMenu.FindItemById(14).SetBitmap( wx.Bitmap(f'{config.assetsPath}icons/menu_github.png') )
		self.helpMenu.FindItemById(15).SetBitmap( wx.Bitmap(f'{config.assetsPath}icons/menu_discord.png') )

		# makes the menu bar
		self.menuBar = wx.MenuBar()
		self.menuBar.Append(self.fileMenu, loc('menu.file.name') )
		self.menuBar.Append(self.optionsMenu, loc('menu.options.name') )
		self.menuBar.Append(self.portalMenu, loc('menu.portal.name') )
		self.menuBar.Append(self.helpMenu, loc('menu.help.name') )

		# Give the menu bar to the frame
		self.SetMenuBar(self.menuBar)
		self.CreateStatusBar()
		self.SetStatusText( loc('statusbar.text').replace('{username}', config.steamUsername() ) )

		# file menu
		self.Bind(wx.EVT_MENU, self.openp2dir, openPortalDirItem)
		self.Bind(wx.EVT_MENU, self.openBEEdir, openBeeDirItem)
		self.Bind(wx.EVT_MENU, self.syncGames, syncGamesItem)
		self.Bind(wx.EVT_MENU, self.exit, exitItem)
		# options menu
		self.Bind(wx.EVT_MENU, self.openSettingsWindow, settingsItem)
		self.Bind(wx.EVT_MENU, logWindow.toggleVisibility, toggleLogWindowItem)
		self.Bind(wx.EVT_MENU, self.reloadPlugins, reloadPluginsItem)
		self.Bind(wx.EVT_MENU, self.reloadPackages, reloadPackagesItem)
		# portal 2 menu
		self.Bind(wx.EVT_MENU, self.verifyGameFiles, verifyGameFilesItem)
		self.Bind(wx.EVT_MENU, self.uninstallBee, uninstallBeeItem)
		self.Bind(wx.EVT_MENU, self.installBee, installBeeItem)
		# help menu
		self.Bind(wx.EVT_MENU, self.openAboutWindow, aboutItem)
		self.Bind(wx.EVT_MENU, self.checkUpdates, checkUpdatesItem)
		self.Bind(wx.EVT_MENU, self.openWiki, wikiItem)
		self.Bind(wx.EVT_MENU, self.openGithub, githubItem)
		self.Bind(wx.EVT_MENU, self.openDiscord, discordItem)
		# other events
		self.Bind(wx.EVT_CLOSE, self.OnClose, self)
		if config.load('beePath') is None:
			self.portalMenu.Enable(9, False)
			self.fileMenu.Enable(1, False)
		else:
			self.portalMenu.Enable(10, False)
		# register event handlers
		dispatcher.connect(self.UnregisterMenu, Events.UnregisterMenu)
		# trigger the registerMenu event
		dispatcher.send(Events.RegisterMenus, MenuBar=self.menuBar)
		"""
		A notebook is a controller which manages multiple windows with associated tabs.
		This section makes the notebook
		"""
		self.book = wx.Notebook(self, name="Main Menu")
		self.browserTab = PackageBrowserPage(self.book)
		self.book.AddPage(self.browserTab, "Package Browser")

	def OnClose(self, event: wx.CloseEvent):
		# stop all plugins
		asyncio.run(pluginSystem.systemObj.unloadAndStop())
		# get the window position as wx.Point and convert it to list
		try:
			pos = list(self.GetPosition().Get())
			LOGGER.debug(f'saved main window position: {pos}')
			config.save(pos, 'mainWindowPos')
		except:
			pass
		self.Destroy()

	def AddMenu(self, menu: wx.Menu, title: str):
		menu = self.GetMenuBar()
		menu.Append(menu, title)
		menu.Refresh()

	# file menu items actions
	@staticmethod
	def openp2dir(event):
		os.startfile( config.portalDir() )

	@staticmethod
	def openBEEdir(event):
		os.startfile( Path( config.load("beePath") ).parent )

	@staticmethod
	def syncGames(event):
		utilities.notimplementedyet()

	def exit(self, event):
		self.OnClose( wx.CloseEvent() )  # there's already an handler, so use that

	# options menu items actions
	def openSettingsWindow(self, event=None):
		"""
		this function opens the settings window.
		when this is called for the first time create an instance of the window, so when
		called again it will be faster, because it don't have to create everything again
		:param event: wx.EVT_something
		"""

		if utilities.env == 'dev':
			try:
				importlib.reload( settingsUI )
				settingsUI.window().Show(self)
			except:
				pass
		else:
			if self.settingsWindowInstance is None:  # if the window was opened once, this isn't None
				self.settingsWindowInstance = settingsUI.window()  # set it to the settings window instance
			self.settingsWindowInstance.show()  # show the window

	@staticmethod
	def reloadPlugins(event=None):
		"""
		reloads the plugins
		:param event: placeholder
		:return: nothing
		"""
		asyncio.run( pluginSystem.systemObj.hardReload('all') )

	def reloadPackages(self, event=None):
		"""
		reloads the package view
		:param event: placeholder
		:return:
		"""
		self.browserTab.reload()
		self.book.Refresh()
		self.Update()
		self.Refresh()

	# portal 2 items actions
	def verifyGameFiles(self, event):
		"""
		triggers the verify game cache dialog + event
		:param event:
		:return:
		"""
		if not config.load("noVerifyDialog"):
			dialog = wx.RichMessageDialog(
				self,
				'''This will remove EVERYTHING beemod-related from portal 2!
				click yes ONLY if you are sure!''',
				'WARNING!',
				wx.YES_NO | wx.ICON_WARNING | wx.STAY_ON_TOP | wx.NO_DEFAULT
			)
			dialog.ShowDetailedText(
				"if you don't want this dialog to show check this checkbox, but be aware, this is here to protect you"
			)
			dialog.ShowCheckBox("Don't show again")
			choice = dialog.ShowModal()
			if dialog.IsCheckBoxChecked():
				config.save(True, 'noVerifyDialog')
			if choice == wx.ID_YES:
				print('yes')
			else:
				print('no')

	def uninstallBee(self, event):
		"""
		called when the uninstall bee button is pressed
		:param event: placeholder
		:return:
		"""
		diag = wx.MessageDialog(
			parent=self,
			message="You're sure to want to uninstall BEE?",
			caption='Warning!',
			style=wx.YES_NO | wx.STAY_ON_TOP | wx.CENTRE | wx.ICON_WARNING
		)
		if diag.ShowModal() == wx.ID_NO:
			return
		beeManager.uninstall()
		self.portalMenu.Enable(10, True)
		self.portalMenu.Enable(9, False)
		self.fileMenu.Enable(1, False)

	def installBee(self, event):
		"""
		called when the install bee button is pressed
		:param event: placeholder
		:return:
		"""
		# check if is installed
		if beeManager.beeIsPresent():
			wx.GenericMessageDialog(
				self,
				message='BEE2.4 has been found on default install path!\nNo need to install again :D',
				caption='Notice!',
				style=wx.OK | wx.STAY_ON_TOP | wx.CENTRE
			).ShowModal()
			config.save(f'{utilities.defBeePath}/BEE2/', 'beePath')
		else:  # not installed
			dial = wx.DirDialog(
				self,
				message='Select where to install BEE (a BEE2 folder will be created)',
				# this gets the APPDATA path, go from Roaming to Local and then return the Programs folder full path
				defaultPath=utilities.defBeePath
			)
			# show the dialog and wait
			if dial.ShowModal() == wx.ID_CANCEL:
				return  # don't want to install anymore
			path = Path(dial.GetPath() + '/BEE2/')
			# create the missing folders
			if not path.exists():
				path.mkdir()
			# save the BEE path
			config.save(str(path.resolve()).replace(r'\\', '/'), 'beePath')
			# install BEE without messages
			beeManager.checkAndInstallUpdate(True)
		self.portalMenu.Enable(9, True)
		self.portalMenu.Enable(10, False)
		self.fileMenu.Enable(1, True)

	# help menu items actions
	def openAboutWindow(self, event):
		aboutWindow.init(self)

	@staticmethod
	def checkUpdates(event):
		asyncio.run(appDateCheck())

	@staticmethod
	def openWiki(event):
		openUrl('https://github.com/ENDERZOMBI102/BEE-manipulator/wiki')

	@staticmethod
	def openGithub(event):
		openUrl('https://github.com/ENDERZOMBI102/BEE-manipulator')

	@staticmethod
	def openDiscord(event):
		openUrl('https://discord.gg/hnGFJrz')

	def UnregisterMenu(self, menu: str):
		self.menuBar.FindMenu(menu)


def openUrl(url: str):
	LOGGER.info(f'opening "{url}" with default browser')
	wb.open(url)


async def appDateCheck():
	"""
	check app updates
	:return:
	"""
	if not utilities.isonline():  # if we're not online return false
		return False
	data = utilities.checkUpdate( 'https://github.com/ENDERZOMBI102/BEE-manipulator', config.version )
	if data.url is None:
		return
	data = wx.GenericMessageDialog(
		parent=wx.GetTopLevelWindows()[0],
		message=f'An update for the app is available, do you want to update now?\n\n{data.description}',
		caption=f'Update Available - new version: {data.version}',
		style=wx.YES_NO | wx.ICON_WARNING | wx.STAY_ON_TOP | wx.NO_DEFAULT
	)
	if data.ShowModal() == wx.ID_NO:
		return  # user don't want to update
	utilities.update()


class PackageBrowserPage(wx.Window):

	loadingGif: wx.adv.AnimationCtrl
	browserObj: browser.Browser

	def __init__(self, master: wx.Notebook):
		super().__init__(
			parent=master
		)
		self.browserObj = browser.Browser(self)

	def reload(self):
		if utilities.env == 'dev':
			try:
				importlib.reload(browser)
			except:
				pass
		self.browserObj = browser.Browser


if __name__ == "__main__":
	init_logging("./logs/latest.log")
	LOGGER = get_logger('BEE Manipulator')
	app = wx.App()
	root = root()
	root.Show()
	app.MainLoop()
